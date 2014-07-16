from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm
import time

def push_changes(message='fabfile committed this, not me.'):
    local("git add -A && git commit -m '%s'" % message)
    local("git push origin master")

def deploy():
    code_dir = '/Users/rmedina/test-deploy'
    with settings(warn_only=True):
        if run("cd %s" % code_dir).failed:
            run("git clone https://github.com/anidem/ggv-py.git %s" % code_dir)
    with cd(code_dir):
        ts = time.strftime('%Y%m%d')
        run('cd ..')
        run('tar cvf ggv-py-%s.tar %s' % (ts, code_dir))
        run('cd %s' % code_dir)
        run('git pull origin master')
        run('touch ggvproject/wsgi.py')

def prompt():
    if not confirm("You are about to push changes to the repository to a production environment. Are you sure you want to do this?"):
        abort("Aborting at user request.")
    ts = time.strftime('%Y%m%d')
    print(ts)




