from django.contrib import admin
from core import models


class SuplierAdmin(admin.ModelAdmin):
    search_fields = ['title', 'ca_license_bool']


class BonusAdmin(admin.ModelAdmin):
    list_display = ('bonus_digit', 'two_word_desc', 'bonus_desc', 'dep_bool', 'dep')

    list_filter = ('bonus_digit', 'suplier', 'dep_bool', 'dep')
    search_fields = ('bonus_digit', 'suplier', 'dep_bool', 'dep')


admin.site.register(models.Suplier, SuplierAdmin)
admin.site.register(models.Bonus, BonusAdmin)