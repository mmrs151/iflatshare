from django.core.management.base import NoArgsCommand, CommandError
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from datetime import date
from calendar import month_name

from iflatshare.core.models import *

class Command(NoArgsCommand):
    help = "help help"

    def handle_noargs(self, **options):
        when = date.today()
        year = when.strftime("%Y")
        month = when.strftime("%m")
        month = int(month) - 1 #last month
        if month == 0: 
            month = 12
        month_str = month_name[month]

        users = User.objects.all()
        for user in users:
            if not user.is_superuser:
                if user.profile.status == 'present':
                    avg = user.profile.address.monthly_avg(year, month)
                    monthly_total = user.profile.address.monthly_total(year, \
                                                                        month)
                     
                    expenditure = user.profile.monthly_total(year,month)
                    balance = expenditure - avg
                    context = {
                                'user': user,
                                'address': user.profile.address.house_number + ', ' +
                                        user.profile.address.post_code,
                                'flat_admin': user.profile.get_admin(),
                                'flat_admin_email': \
                                        user.profile.get_admin().email,
                                'avg': avg,
                                'balance': balance,
                                'expenditure' : expenditure,
                                'monthly_total': monthly_total,
                                'action' : 'pay',
                                'adverb': 'less than',     
                                'month': month_str,
                                'year': year,
                                'url': 'https://www.iflatshare.co.uk/avg_diff/',
                               }
                    if balance > 0:
                        context.update({
                                'action' : 'collect',
                                'adverb': 'more than',
                            })
                    if not user.profile.is_admin:
                        mailbody = render_to_string( \
                                'emails/monthly_report.txt', context)
                    else:
                        mailbody = render_to_string( \
                                'emails/monthly_admin_report.txt', context)

                    send_mail('iFlatshare Monthly Report for '+month_str+' '+str(year), \
                      mailbody, \
                      settings.DEFAULT_FROM_EMAIL, [user.email,], \
                      fail_silently=False)
