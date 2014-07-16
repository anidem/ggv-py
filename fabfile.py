from fabric.api import local

def hello(name="world"):
    print("Hello %s!" % name)

def push_changes(message='fabfile committed this, not me.'):
    local("git add -A && git commit -m '%s'" % message)
    local("git push origin master")


