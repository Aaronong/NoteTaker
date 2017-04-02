from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(NoteUser)
admin.site.register(Note)
admin.site.register(Notebook)
admin.site.register(Document)
admin.site.register(Tagging)
admin.site.register(Tags)
admin.site.register(Authorization)
admin.site.register(TextComment)
admin.site.register(InsertComment)
admin.site.register(DeleteComment)
admin.site.register(NoteAuthorization)