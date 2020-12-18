from django.contrib import admin

from .models import Story, Page, Action, ActionCondition


admin.site.register(Story)
admin.site.register(Page)
admin.site.register(Action)
admin.site.register(ActionCondition)
