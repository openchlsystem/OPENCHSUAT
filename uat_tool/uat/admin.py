from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Organization)
admin.site.register(System)
admin.site.register(Functionality)
admin.site.register(TestCase)
admin.site.register(TestStep)
admin.site.register(TestExecution)
admin.site.register(Defect)
admin.site.register(User)
# admin.site.register(Roles)
# admin.site.register(DefectOptions)
# admin.site.register(StatusChoices)
# admin.site.register(DefectStatus)
# admin.site.register(TesterDashboard)
# admin.site.register(DefectStatusChoices)
# admin.site.register(TesterDashboard)