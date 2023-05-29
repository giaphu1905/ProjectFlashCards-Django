from .models import LearnerUser, FlashCard, Card
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Tên người dùng'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Xác nhận mật khẩu'}))

    class Meta:
        model = LearnerUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].validators = []    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and LearnerUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được sử dụng!!!')
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if LearnerUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được sử dụng!!!')
        return cleaned_data

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['word', 'meaning', 'flash_card']
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': 'Từ vựng'}),
            'meaning': forms.TextInput(attrs={'placeholder': 'Định nghĩa'}),
            'flash_card': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        flash_card = kwargs.pop('flash_card', None)
        super(CardForm, self).__init__(*args, **kwargs)
        if flash_card:
            self.fields['flash_card'].initial = flash_card
            self.fields['flash_card'].queryset = FlashCard.objects.filter(id=flash_card.id)

CardFormSet = forms.inlineformset_factory(FlashCard, Card, form=CardForm, extra=2, can_delete=False)

class FlashCardForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Đặt tên cho bộ FlashCard của bạn', 'class': 'form-control mr-3'})
    )
    user = forms.ModelChoiceField(
        queryset=LearnerUser.objects.all(),
        widget=forms.HiddenInput(),
        empty_label=None
    )

    class Meta:
        model = FlashCard
        fields = ['title', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(FlashCardForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].queryset = LearnerUser.objects.filter(id=user.id)

class FlashCardFormUpdate(forms.ModelForm):
    class Meta:
        model = FlashCard
        fields = ['title']  # Chỉ cho phép cập nhật tiêu đề

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "New Title"  # Đặt nhãn cho trường tiêu đề

class CardUpdateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['word', 'meaning']  # Chỉ cho phép cập nhật từ và nghĩa
        widgets = {
            'word': forms.TextInput(attrs={'placeholder': 'Từ vựng',
                                           'name': "card_data['word']",}),
            'meaning': forms.TextInput(attrs={'placeholder': 'Định nghĩa',
                                              'name': "card_data['meaning']",}),
        }


