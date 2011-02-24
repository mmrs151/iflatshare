from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['sewinzco@sewinz.com']

def qa():
    """Use QA environment settings on remote host"""
    env.path = '/home2/sewinzco/www/iflatshare/qa/iflatshare/'
    env.environment = 'qa'

def production():
    """Use Production environment settings on remote host"""
    env.path = '/home2/sewinzco/www/iflatshare/'
    env.environment = 'production'

def test():
    with settings(warn_only=True):
        result = local('./manage.py test core', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request")

def pack():
    local('tar czf /tmp/iflatshare.tgz .', capture=False)

def prepare_deploy():
    test()
    pack()

def upload(tag_version):
    """Put latest tag on remote host"""
    local('git archive --format=tar %s |gzip > /tmp/%s.gz' % (tag_version,\
            tag_version))
    put('/tmp/%s.gz' % tag_version, '/tmp/')

def reload():
    """touch the fcgi script, causing the app to reload"""
    with cd(env.path):
        run('touch iflatshare.fcgi')

def syncdb():
    """Run ./manage.py syncdb"""
    with cd(env.path):
        run('./manage.py syncdb"')

def prepare_server():
    run('cp settings_qa.py settings.py')
    run('cp iflatshare_qa.fcgi iflatshare.fcgi')
    run('rm media/admin')
    run('ln -s /home2/sewinzco/.local/lib/python2.6/site-packages/django/contrib/admin/media/ media/admin')

def deploy(tag_version):
    prepare_deploy()
    upload(tag_version)
    with cd(env.path):
        run('tar -xzf /tmp/%s.gz' % tag_version)
        prepare_server()
        reload()
