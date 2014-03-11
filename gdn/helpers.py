from fabric.api import *
import teamcity
from fabric.contrib.console import confirm
###########################################################
#
#
#   HELPERS
#
#

def ask_for_build_number():
    build_number = teamcity.get_last_build_number(env.build_id)

    if not confirm('Deploy build v{0}'.format(build_number)):
        while True:
            build_number = prompt('Enter build version: ')
            if teamcity.check_version(env.build_id, build_number):
                break

    return build_number

def clean_folder(folder, run_or_sudo):
    with warn_only():
        run_or_sudo('rm {0}/*'.format(folder))

def ensure_empty_folder(path, run_or_sudo):
    with warn_only():
        run_or_sudo('rm -fr {0}'.format(path))
        run_or_sudo('mkdir -p {0}'.format(path))

def download_file(url, out_path):
    run('wget -nv {0} -P {1}'.format(url, out_path))

def fortress(cm):
    with warn_only():
        sudo('service gdn_fortress {0}'.format(cm))

def download_all_artifacts_from_shadow(build_type, build_version, out_path):
    run('wget -nv http://shadow/guestAuth/repository/downloadAll/{0}/{1} -O {2}'.format(build_type, build_version, out_path))

def get_shadow_build_id():
    pass

def unzip_artifacts(archive, out_path):
    run('unzip -q {0} -d {1}'.format(archive, out_path))

def clear_artifacts_dir(artifacts_dir):
    run('rm -fr {0}'.format(artifacts_dir))
    run('mkdir {0}'.format(artifacts_dir))


def set_fortress_db(host, db):
    conffile = '/opt/gdn/config/default.properties'
    db_port = '27017'
    sudo('sed -i "s/\(^database.name=\).*/\\1{0}/" {1}'.format(db, conffile))
    sudo('sed -i "s/\(^database.host=\).*/\\1{}:{0}/" {1}'.format(host, db_port, conffile))

    