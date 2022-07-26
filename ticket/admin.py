from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from .models import Ticket, Replie

# Register your models here.
class ProjectAdmin(GuardedModelAdmin):
	pass

admin.site.register(Ticket, ProjectAdmin)
admin.site.register(Replie, ProjectAdmin)