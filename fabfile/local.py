from datetime import datetime

from fabric.api import task, lcd, local, get


@task
def dbBackup(append=None):
    filename = datetime.now().strftime("%Y-%m-%d")
    if (append):
        filename += "-" + append
    with lcd("data"):
        local(
            "pg_dump -h 54.211.200.87 -U newproducts -W -F c -f %s.dbdump survey" % filename
        )

@task
def getBackup():
    filename = datetime.now().strftime("%Y-%m-%d")
    with lcd("data"):
        get('/opt/django-projects/.virtualenvs/survey/data/%s.dbdump' % filename)