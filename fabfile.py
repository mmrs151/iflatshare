from fabric.api import local, put, cd, run, env
from fabric.operations import prompt
import datetime

release_date = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
env.django = '/usr/local/lib/python2.6/dist-packages/django/'
env.hosts = ['root@allsimple']
app = 'iflatshare'

def qa():
    """Use QA environment settings on remote host"""
    env.path = '/sites/%s_qa' %app
    env.environment = 'qa'

def production():
    """Use Production environment settings on remote host"""
    env.path = '/sites/%s' %app
    env.environment = 'production'

def _release_dir():
    return '%s/releases/%s' % (env.path, release_date)

def prepare_server():
    print "Preaparing Server"
    run('mkdir -p %s/releases/%s' % (env.path, release_date))
    with cd(env.path):
        run('rm -Rf current')

def upload(tag_version):
    """Put code on remote host"""
    local('git archive --format=tar %s |gzip > /tmp/%s.tar.gz' \
            % (tag_version, app))
    put('/tmp/%s.tar.gz'  %app, '/tmp/')

def configure_server():
    with cd(_release_dir()):
        run('tar -xzf /tmp/%s.tar.gz' %app)
        run('cp %s/settings_%s.py %s/settings.py' \
                % (app, env.environment, app))
        run('cp django_%s.wsgi django.wsgi' % env.environment)
        run('rm django_*.wsgi')
        run('rm %s/settings_*.py' %app)
    with cd(env.path):
        run('ln -s %s current' % _release_dir())
        run('chmod -R 757 current/%s' %app)

def update_dependencies():
    """Update external dependencies on remote host"""
    with cd(env.path):
        run('source bin/activate')
        run('sudo pip install -E %(path)s --requirement %(path)s/current/requirements.txt' % env)

def bootstrap():
    """Prepare remote host"""
    run('mkdir -p %(path)s' % env)
    run('virtualenv %(path)s' % env)

def syncdb():
    """Run ./manage.py syncdb"""
    with cd(env.path):
        run('bash -c "source bin/activate && ./current/%s/manage.py syncdb --all"' %app)
        run('./current/%s/manage.py migrate core --fake"' %app)

def test():
    """Run tests (in virtual environment) on remote host"""
    with cd(env.path):
        run('source bin/activate')
        run('./current/%s/manage.py test core' %app)
        run('deactivate')
        
def reload():
    """touch the wsgi script, causing the app to reload"""
    with cd(env.path):
        run('touch current/django.wsgi')
        
def deploy(tag_version):
    if not tag_version:
        tag_version = prompt("No Tag version given, please specify one:")
    if 'environment' not in env:
        env.environment = prompt("No environment given, please specify one:")
    prepare_server()
    upload(tag_version)
    configure_server()
    reload()
