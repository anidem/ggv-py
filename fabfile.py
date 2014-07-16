from fabric.api import local

def push_changes():
    local("git add -A && git commit -m 'fabfile default' ")
    local("git push origin master")


