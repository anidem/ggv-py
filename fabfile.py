from __future__ import with_statement

import time, os, shutil

from fabric.api import local, settings, abort, run, cd, lcd
from fabric.contrib.console import confirm
from fabric.operations import prompt




def push_changes(m='fabfile committed with this message, not me.'):
    local("git add -A && git commit -m '%s'" % m)
    local("git push origin master")


def deploy(remote_dir, app_dir):
    with settings(warn_only=True):
        deploy_dir = '%s/%s' % (remote_dir, app_dir)
        if run('cd %s' % deploy_dir).failed:
            run("git clone https://github.com/anidem/ggv-py.git %s" %
                deploy_dir)

    with cd(remote_dir):
        ts = time.strftime('%Y%m%d%H')
        print ts
        run('pwd')
        run('tar cvf ggv-py-%s.tar %s' % (ts, app_dir))

    with cd(deploy_dir):
        run('git pull origin master')
        run('touch ggvproject/wsgi.py')
        run('ls -l')
        # settings file specified in env variable
        run('python manage.py collectstatic')
        run('pwd')


def start_deploy(rd, ad):
    if not confirm("You are about to push changes to the repository to a production environment. Are you sure you want to do this?"):
        abort("Aborting at user request.")
    deploy(remote_dir=rd, app_dir=ad)


def tester(args='default arguments'):
    print args


def readfiles(dirpath):
    files = []
    for fstr in os.listdir(dirpath):
        if fstr != '.DS_Store':
            files.append(fstr)

    with lcd(dirpath):
        local('pwd')

        for f in files:
            j = f.replace('.csv', '.json')
            local(
                'csvcut -c "WID","QUESTION DISPLAY ORDER","QUESTION","IMAGE","SELECT TYPE","CORRECT ANSWER","option 1","option 2","option 3","option 4" %s | csvjson -i 4 > jsondir/%s' % (f, j))

# Creates a slugified copy of files in the directory specified by path. IS NOT recursive.
def slug_names(path='.'):
    pdir = os.path.abspath(path) 
    if not confirm('Preparing to slug files in %s. Continue?' % pdir):
        return
    files = [fstr for fstr in os.listdir(pdir) if fstr != '.DS_Store']
    for f in files:
        f1 = os.path.join(pdir, f)
        f2 = os.path.join(pdir, slugify(unicode(f, errors='replace')))
        f2 = f2.replace('-web', '')
        f2 = os.path.join(pdir, f2)
        shutil.copytree(f1, f2)
        
        # print f, f2
        # local('cp %s %s'%(unicode(f), f2))

        # os.rename(
        #     os.path.join(pdir, f),
        #     os.path.join(pdir, slugify(unicode(f, errors='replace')))
        # )
    files = [fstr for fstr in os.listdir(pdir) if fstr != '.DS_Store']


