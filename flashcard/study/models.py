from django.db import models
from user.models import LearnerUser
from django.core.exceptions import ValidationError
# Create your models here.
class FlashCard(models.Model):
    user = models.ForeignKey(LearnerUser, on_delete=models.CASCADE, related_name='user_flashcard')
    title = models.CharField(max_length=100)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id) + ' - ' + self.title
    
    def clean(self):
        if not self.user_id:
            raise ValidationError('Please select a user before creating a new flash card.')
    
    def word_count(self):
        return self.card_set.count()
    
class Card(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.CharField(max_length=200)
    flash_card = models.ForeignKey(FlashCard, on_delete=models.CASCADE)

    def clean(self):
        if not self.flash_card_id:
            raise ValidationError('Bạn phải lưu hoặc chọn một bộ thẻ trước khi tạo các từ vựng mới.')
        