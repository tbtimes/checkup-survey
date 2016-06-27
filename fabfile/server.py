from datetime import datetime

from fabric.api import task, env, prefix, run, sudo, cd, get

env.hosts = ["bhiggins@54.211.200.87"]


@task
def backup():
    filename = datetime.now().strftime("%Y-%m-%d")
    with cd('/opt/django-projects/.virtualenvs/survey/data'):
        run('pg_dump -U newproducts -W -F c -f %s.dbdump survey' % filename)
        location = '/opt/django-projects/.virtualenvs/survey/data/%s.dbdump' % filename