from django.contrib import admin
from .models import Newstopic, Comment
# Register your models here.
admin.site.register(Newstopic)
admin.site.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.save()