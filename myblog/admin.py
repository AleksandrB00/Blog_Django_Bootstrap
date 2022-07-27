from django.contrib import admin
from .models import Post


class AdminPanel(admin.ModelAdmin):
   prepopulated_fields = {'slug': ('h1',)}

admin.site.register(Post, AdminPanel)