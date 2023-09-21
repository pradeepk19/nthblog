from django.contrib import admin

from .models import Post,Profile,Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug','author','status']
    list_filter = ['status']
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}
    list_editable = ['status']
    date_hierarchy = ('created')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','dob','phote']

admin.site.register(Profile,ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
