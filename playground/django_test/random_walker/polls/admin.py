from django.contrib import admin

# Register your models here.

from .models import Question
from .models import Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    # list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']



admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)

