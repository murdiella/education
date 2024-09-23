from django.contrib import admin

from .models import AbitUser, SignupToken


class AbitUserAdmin(admin.ModelAdmin):
    pass


class SignupTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(AbitUser, AbitUserAdmin)
admin.site.register(SignupToken, SignupTokenAdmin)
