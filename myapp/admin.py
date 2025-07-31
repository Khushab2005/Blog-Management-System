from django.contrib import admin
from myapp.models import *
# Register your models here.
class CustomAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'created_at','author','updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
    


admin.site.register(User)
admin.site.register(Blog)
admin.site.register(Comment)