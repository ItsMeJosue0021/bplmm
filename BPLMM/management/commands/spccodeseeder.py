from django.core.management.base import BaseCommand # type: ignore
from BPLMM.models import SPC_CODE_MOCK

class Command(BaseCommand):
    help = 'Seed SPC code'

    def handle(self, *args, **kwargs):
        codes = ['C19T4', 'C19T5', 'C19T6', 'C19T7', 'C19T8',
         'C19T9', 'C19T10', 'C19T11', 'C19T12', 'C19T13',
         'C19T14', 'C19T15', 'C19T16', 'C19T17', 'C19T18',
         'PRC20', 'PRC21', 'PRC22', 'PRC23', 'PRC24']
        
        for code in codes:
            SPC_CODE_MOCK.objects.create(CODE=code)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
    