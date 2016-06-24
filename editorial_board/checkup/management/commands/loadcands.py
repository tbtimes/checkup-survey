from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from checkup.models import Reporter, Assignment, Survey, Group, Respondent, QuestionGroup
import csv, os

class Command(BaseCommand):
    help = 'Loads candidates from csv into database'

    def createReporter(self, fname, lname, email, password, phone):
        user = self.createUser(fname, lname, email, password)
        try:
            return Reporter.objects.get(user=user)
        except Reporter.DoesNotExist:
            r = Reporter(user=user, phone=phone, title=None)
            r.save()
            return r

    def createUser(self, fname, lname, email, password):
        try:
            return User.objects.get(username="{0}.{1}".format(fname, lname))
        except User.DoesNotExist:
            return User.objects.create_user(username="{0}.{1}".format(fname, lname),
                                            email=email, password=password,
                                            first_name=fname, last_name=lname)

    def add_arguments(self, parser):
        parser.add_argument('file', nargs=1)

    def getGroup(self, office):
        try:
            return Group.objects.get(name=office)
        except Group.DoesNotExist:
            g = Group(name=office)
            g.save()
            return g

    def handle(self, *args, **options):
        file = options['file'][0]
        path = ""
        if len(file.split('/')) < 3:
            path = "{0}/{1}".format(os.getcwd(), file)
        else:
            path = file

        john = self.createReporter('John', 'Hill', 'jhill@tampabay.com', 'secretpassword15', '(813) 226-3379')
        sharon = self.createReporter('Sharon', 'Otts', 'sotts@tampabay.com', 'secretpassword14', "(727) 893-8559")

        with open(path, 'rU') as importFile:
            reader = csv.DictReader(importFile)
            for row in reader:
                if row['Type of Race'] != '':
                    # Get respondent and group
                    group = self.getGroup(row['Office'])
                    respondent = Respondent(title=None, group=group, party=row['Party'], district=row['District'],
                                            gender=None, first_name=row['First'], last_name=row['Last'], email=row['Email'])
                    respondent.save()

                    # get questions
                    qgroup = ''
                    if row['Type of Race'] == 'Federal':
                        qgroup = 'congress'
                    elif row['Type of Race'] == 'State':
                        qgroup = 'florida legislature'
                    else:
                        if row['Office'] == 'School Board':
                            qgroup = 'school board'
                        else:
                            qgroup = 'personal'

                    # assign reporter
                    if row['County'] == 'Hillsborough':
                        reporter = john
                    else:
                        reporter = sharon

                    # assign survey here
                    survey = Survey.objects.get_or_create(name="Editorial Board Candidate Survey 2016", home_slug="edi2016")[0]

                    assignment = Assignment(survey=survey, respondent=respondent, reporter=reporter, questions=QuestionGroup.objects.get(name=qgroup))
                    assignment.save()
