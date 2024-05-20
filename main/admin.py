from django.contrib import admin

# Register your models here.
from .models import Obuca, Odeca, Marka, Tip, VelicinaObuce, VelicinaOdece, Boja, SlikaObuce, SlikaOdece, NacinKupovine, Praćenje
admin.site.register(Obuca)
admin.site.register(Odeca)
admin.site.register(Marka)
admin.site.register(Tip)
admin.site.register(VelicinaObuce)
admin.site.register(VelicinaOdece)
admin.site.register(Boja)
admin.site.register(SlikaObuce)
admin.site.register(SlikaOdece)
admin.site.register(NacinKupovine)
admin.site.register(Praćenje)