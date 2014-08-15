from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm
from fabric.operations import prompt
import time

def push_changes(message='fabfile committed with this message, not me.'):
    local("git add -A && git commit -m '%s'" % message)
    local("git push origin master")

def deploy(remote_dir):
    with settings(warn_only=True):        
        if run("cd %s" % remote_dir).failed:
            run("git clone https://github.com/anidem/ggv-py.git %s" % remote_dir)

    with cd(remote_dir):
        ts = time.strftime('%Y%m%d%H%M%S')
        run('cd ..')
        run('sudo tar cvf ggv-py-%s.tar %s' % (ts, remote_dir))
        run('sudo git pull origin master')
        run('sudo touch ggvproject/wsgi.py')
        run('sudo ls -l')
        run('sudo python manage.py collectstatic --settings=ggvproject.settings.prod')

def start_deploy():
    if not confirm("You are about to push changes to the repository to a production environment. Are you sure you want to do this?"):
        abort("Aborting at user request.")
    rd = prompt('Please specify remote directory: ')
    deploy(remote_dir=rd)




