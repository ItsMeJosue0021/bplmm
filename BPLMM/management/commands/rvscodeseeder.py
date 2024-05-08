from django.core.management.base import BaseCommand # type: ignore
from BPLMM.models import RVS_CODE_MOCK

class Command(BaseCommand):
    help = 'Seed RVS code'

    def handle(self, *args, **kwargs):
        base_code = 4550
        prefix = 'CR'
        
        for i in range(40):
            RVS_CODE_MOCK.objects.create(CODE=f'{prefix}{base_code + i}')

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
