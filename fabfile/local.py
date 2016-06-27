from datetime import datetime

from fabric.api import task, lcd, local, get

@task
def getBackup():
    filename = datetime.now().strftime("%Y-%m-%d")
    with lcd("data"):
        get('/opt/django-projects/.virtualenvs/survey/data/%s.dbdump' % filename)