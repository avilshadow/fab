from fabric.api import *
from  gdn.helpers import *
import teamcity


@task
@roles('mongo')
def migrate():
    build_number = ask_for_build_number()

    artifact_folder = '/tmp/gdn_migration'
    ensure_empty_folder(artifact_folder, run)

    artifact_name = env.migration_artifact_template.format(version=build_number)

    download_file(teamcity.get_artifact_link(env.build_id, build_number, artifact_name), artifact_folder)

    with cd(artifact_folder):
    	run('unzip -q {0}'.format(artifact_name))
    	run('java -cp "lib/*" com.adstream.utils.mongodb.Migration {0} 27017 {1}'.format(env.mongo_host, env.mongo_db_name))
    	# apply akka settings
    	run('''echo '{0}' > postmigrate.js'''.format(get_postmigrate()))
    	run('mongo localhost/{0} postmigrate.js'.format(env.mongo_db_name))


def get_postmigrate():
	return config_pattern % {
	'activemq_host_port': env.activemq_host_port,
	'transcoding_db': env.transcoding_db,
	'akka': ','.join(['"akka.tcp://gdn@{0}:2552"'.format(x) for x in env.gdn_hosts]),
	'elastic_engine': env.elastic_engine,
	'elastic_url': env.elastic_url
	}

config_pattern = '''
db.setProfilingLevel(1);

var cursor = db.settings.find({_id: "gdn"});
if (cursor.hasNext()) {
	var gdnConfig = cursor.next();
	
	mq = gdnConfig.mqconfig;
	if (mq){
		var host_port = new RegExp(":\\\\\\(nio://([^)]*)\\\\\\)\\\\\\?","gm").exec(mq)[1];
		mq = mq.replace(host_port, "%(activemq_host_port)s");
		db.settings.update({_id: "gdn"}, {$set: {"mqconfig": mq}});
	}

	var url = gdnConfig.gdn.transcodingdb.url;
	if (url){
		db.settings.update({_id: "gdn"}, {$set: {"gdn.transcodingdb.url": "http://%(transcoding_db)s:5984/transcoding/_design/api/_rewrite/search/{SourceSpecDBDocID}/{System}/{Country}/{AgencyID}"}});
	}

	var newMq = gdnConfig.gdn.mq.serverURI;
	if (newMq){
		db.settings.update({_id: "gdn"}, {$set: {"gdn.mq.serverURI": "nio://%(activemq_host_port)s"}})
	}

}

db.settings.update({_id: "gdn"},
	{$set: {
		"gdn.rest.bindHost": "0.0.0.0",
		"gdn.fileUrlCdn.cName": "http://uakyivopt02:20282",
		"gdn.mq.inQueue": "adstream.yadn",
		"gdn.elastic.engine": "%(elastic_engine)s",
		"gdn.elastic.external.url": "%(elastic_url)s"
	}});

db.settings.update({_id: "akka"},
	{$set:{
		"akka.remote.netty.tcp.port": NumberInt(2552),
		"akka.cluster.seed-nodes" : [ %(akka)s ]
	}});
'''