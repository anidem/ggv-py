# pretests/management/reporter.py
import os
import csv
from datetime import datetime

from openpyxl import Workbook

from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.utils.text import slugify
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from pretests.models import PretestUser, PretestAccount


class Command(BaseCommand):
    """If running from crontab, then:
            VIRTUALENVPATH/python PROJECTPATH/manage.py report-pretest-scores <account_id> <to_email>
    """
    help = 'Writes an Excel file containing pretest scores for a given account id.'

    def add_arguments(self, parser):
        parser.add_argument('account_id', type=int)
        parser.add_argument('to_email')

    def handle(self, *args, **options):        
        try:
            account = PretestAccount.objects.get(pk=options['account_id'])
        except PretestAccount.DoesNotExist:
            raise CommandError('Pretest account "%s" does not exist' % account_id)
    
        file_path = self.compile_pretest_scores_excel(account=account)
        self.send_pretest_scores(account=account, recipients=[options['to_email']], attachment=file_path)

           
    def compile_pretest_scores_excel(self, account=None):
        root_dir = settings.ARCHIVE_DATA_DIR
        filename = slugify(account.name) + '-' + datetime.strftime(datetime.now(), '%Y-%m-%d') + '-report.xlsx'
        path = root_dir + '/' + filename
        
        # Openpyxl writer
        writer = Workbook()
        ws = writer.get_active_sheet()
        ws.title = slugify(account.name)
        for i in account.tokens.filter(email__isnull=False).order_by('email'):
            for j in i.pretest_user_completions.all():
                datarow = [i.program_id, i.email, i.first_name, i.last_name, j.completed_pretest.title, j.get_score()[0]]
                ws.append(datarow)
        writer.save(path)
        self.stdout.write(self.style.SUCCESS('Successfully wrote report "%s"' % filename))
        return path

    def compile_pretest_scores_csv(self, account=None):
        root_dir = settings.ARCHIVE_DATA_DIR
        filename = slugify(account.name) + '-' + datetime.strftime(datetime.now(), '%Y-%m-%d') + '-report.csv'
        path = root_dir + '/' + filename
        
        with open(path, 'wb') as csvfile:
            scores = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for i in account.tokens.filter(email__isnull=False).order_by('email'):
                for j in i.pretest_user_completions.all():
                    datarow = [i.program_id, i.email, i.first_name, i.last_name, j.completed_pretest.title.encode("utf-8"), j.get_score()[0]]
                    
                    scores.writerow(datarow)
        return path

    def send_pretest_scores(self, account=None, recipients=[], attachment=None):
        html_message = "<h3>{0}</h3><h4>See attached file for updated pretest scores.</h4>".format(account.name)

        email = EmailMultiAlternatives(
            subject='GGV Pretest Scores - {0}'.format(account.name),
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=recipients,        
            )
        email.attach_file(attachment)
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)
        self.stdout.write(self.style.SUCCESS('Successfully sent "%s"' % attachment))

