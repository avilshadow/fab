from fabric.api import *
import teamcity
from helpers import *

#
#
# TASKS
#
#

@task
@roles('gdn')
def clear_logs():
    clean_folder('/var/log/gdn', sudo)

@task
@roles('gdn')
def status():
    fortress('status')
    
@task
@roles('gdn')
def stop():
    fortress('stop')
    
@task
@roles('gdn')
def start():
    fortress('start')

@task
@roles('gdn')
def restart():
    fortress('restart')

@task
@roles('gdn')
def clear_kaha():
    clean_folder('/opt/gdn/kahadb', sudo)

@task
@roles('gdn')
def install(build_number):
    tmp_gdn_artifact_folder = '/tmp/gdn-artifacts'
    
    artifact_name = env.fortress_artifact_template.format(version=build_number)

    ensure_empty_folder(tmp_gdn_artifact_folder, run)
    download_file(teamcity.get_artifact_link(env.build_id, build_number, artifact_name), tmp_gdn_artifact_folder)

    sudo('rpm -Uvh --force {0}/{1}'.format(tmp_gdn_artifact_folder, artifact_name))

    set_fortress_db(env.mongo_host, env.mongo_db_name)


@task
def update():
    build_number = ask_for_build_number()    
    execute(install, build_number=build_number)

@task
@roles('gdn')
def kaha_size():
    run('du -h /opt/gdn/kahadb')
    
@task
@roles('gdn')
def version():
    run('rpm -qi gdn-fortress')

@task
@roles('gdn')
def config_head():
    run('head /opt/gdn/config/default.properties')
