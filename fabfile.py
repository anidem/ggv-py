from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

def push_changes(message='fabfile committed this, not me.'):
    local("git add -A && git commit -m '%s'" % message)
    local("git push origin master")

def deploy():
    code_dir = '/Users/rmedina/test-deploy'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone https://github.com/anidem/ggv-py.git %s" % code_dir)
    with cd(code_dir):
        run('git pull')
        run('touch ggvproject/wsgi.py')


