from django.contrib import admin
from .models import ContactInfo
from .models import RegisterEventInfo

admin.site.register(ContactInfo)
admin.site.register(RegisterEventInfo)