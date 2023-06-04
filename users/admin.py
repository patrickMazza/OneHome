from django.contrib import admin
from .models import Post
from .models import Profile
from .models import ClientProfile

# Register your models here.
admin.site.register(Profile)
admin.site.register(ClientProfile)
# Register your models here.
admin.site.register(Post)
