from __future__ import unicode_literals
from tasks.utils import *
from tasks.server import *
from tasks.project import *


# ~$ ENVIRONMENTS
# ---------------------------------------------------------------------

@task
def production():
    set_stage('production')


@task
def develop():
    set_stage('develop')


@task
def test():
    set_stage('test')


# ~$ COMMANDS
# ---------------------------------------------------------------------

@task
def upgrade():
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.upgrade, hosts=env.hosts)


@task
def install():
    """
    Install app in selected server(s)
    """
    set_user(superuser=True)

    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.deps, hosts=env.hosts)
        execute(Server.user, hosts=env.hosts)
        execute(Server.group, hosts=env.hosts)
        execute(Server.path, hosts=env.hosts)
        execute(Server.git, hosts=env.hosts)
        execute(Server.add_remote, hosts=env.hosts)
        execute(Server.nginx, hosts=env.hosts)
        execute(Server.letsencrypt, hosts=env.hosts)
        execute(Server.fix_permissions, hosts=env.hosts)


@task
def uninstall():
    """
    Uninstall app in selected server(s)
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.clean, hosts=env.hosts)


@task
def restart():
    """
    Restart all app services.
    """
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.restart_services, hosts=env.hosts)

@task
def deploy():
    """
    Deploy application in selected server(s)
    """
    set_user()
    with settings(hide('warnings'), warn_only=True, ):
        execute(Project.push, hosts=env.hosts)

@task
def add_remote():
    """
    Add project repo url to local git configuration.
    """
    with settings(hide('warnings'), warn_only=True, ):
        execute(Server.add_remote, hosts=env.hosts)

@task
def upload_key():
    """
    Upload SSH key to server.
    """
    set_user()
    with settings(hide('warnings'), warn_only=True, ):
        execute(Utils.upload_key, hosts=env.hosts)

@task
def profile():
    local("echo \"export LANG=C.UTF-8\" >> ~/.bash_profile")
    local("echo \"export LC_CTYPE=C.UTF-8\" >> ~/.bash_profile")
    local("echo \"export LC_ALL=C.UTF-8\" >> ~/.bash_profile")


@task
def add_certificate(domain=None):
    set_user(superuser=True)
    with settings(hide('warnings'), warn_only=True, ):
        if domain:
            execute(Server.letsencrypt, domain, hosts=env.hosts)
        else:
            raise Exception("The domain param is required!")


@task
def help():
    print ""
    print "~$ COMMANDS"
    print "-------------------------------------------------------------------------"
    print ""
    print "  - [server] install                 Install project into server."
    print "  - [server] uninstall               Remove project from server."
    print "  - [server] deploy                  Deploy project to server."
    print "  - [server] restart                 Restart project services."
    print "  - [server] upload_key              Upload SSH key to server."
    print "  - [server] add_remote              Add git remote from server to local git config."
    print "  - [server] profile                 Set language ENV Variables"
    print "  - [server] add_certificate:DOMAIN  add SSL Certificates via letsencrypt"
    print ""
    print "-------------------------------------------------------------------------"
