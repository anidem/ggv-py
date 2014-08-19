from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm
from fabric.operations import prompt
import time

def push_changes(m='fabfile committed with this message, not me.'):
    local("git add -A && git commit -m '%s'" % m)
    local("git push origin master")

def deploy(remote_dir, app_dir):
    with settings(warn_only=True):
        deploy_dir = '%s/%s' % (remote_dir, app_dir)      
        if run('cd %s' % deploy_dir).failed:
            run("git clone https://github.com/anidem/ggv-py.git %s" % deploy_dir)

    with cd(remote_dir):
        ts = time.strftime('%Y%m%d%H')
        print ts
        run('pwd')
        run('tar cvf ggv-py-%s.tar %s' % (ts, app_dir))

    with cd(deploy_dir):
        run('git pull origin master')
        run('touch ggvproject/wsgi.py')
        run('ls -l')
        run('python manage.py collectstatic') # settings file specified in env variable
        run('pwd')

def start_deploy(rd, ad):
    if not confirm("You are about to push changes to the repository to a production environment. Are you sure you want to do this?"):
        abort("Aborting at user request.")
    deploy(remote_dir=rd, app_dir=ad )

def tester(args='default arguments'):
    print args




