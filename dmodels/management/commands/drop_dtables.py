from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from dmodels.models import Modelsname

class Command(BaseCommand):
    
    help = 'Drop tables created for dynamic models.'

    def handle(self, *args, **options):     
        cursor = connection.cursor()
        for m in Modelsname.objects.all():
            cursor.execute('DROP TABLE IF EXISTS dmodels_%s' % m.name)
        Modelsname.objects.all().delete()
