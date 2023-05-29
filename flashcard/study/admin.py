from django.contrib import admin
from .models import FlashCard, Card
# Register your models here.
class FlashCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'word_count')

    def word_count(self, obj):
        return obj.card_set.count()
admin.site.register(FlashCard, FlashCardAdmin)
admin.site.register(Card)