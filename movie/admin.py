from django.contrib import admin
from .models import StreamPlatform, WatchList, Caterogy, SubCaterogy

# Register your models here.
admin.site.register(StreamPlatform)
admin.site.register(WatchList)
admin.site.register(Caterogy)
admin.site.register(SubCaterogy)
