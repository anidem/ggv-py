from fabric.api import local

def push_changes():
    local("git add -A && git commit")
    local("git push")
