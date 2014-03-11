from fabric.api import *
import gdn
import mongo
import json

cfg = json.load(open('env.js'))

# colorize errors
env.colorize_errors = True

env.build_id = cfg['build_id']
env.gdn_hosts = cfg['gdn_hosts']
env.mongo_host = cfg['mongo_host']
env.mongo_db_name = cfg['mongo_db_name']
env.activemq_host_port = cfg['activemq_host_port']
env.transcoding_db = cfg['transcoding_db']
env.fortress_artifact_template = cfg['fortress_artifact_template']
env.migration_artifact_template = cfg['migration_artifact_template']

env.roledefs['gdn'] = env.gdn_hosts
env.roledefs['mongo'] = [env.mongo_host]
env.roledefs['elastic'] = []

env.user = 'qauser'
env.password = 'qwerty'