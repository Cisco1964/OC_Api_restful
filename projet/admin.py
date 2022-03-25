from django.contrib import admin
from .models import Projects, Issues, Comments, Contributors

admin.site.register(Contributors)
admin.site.register(Projects)
admin.site.register(Issues)
admin.site.register(Comments)
