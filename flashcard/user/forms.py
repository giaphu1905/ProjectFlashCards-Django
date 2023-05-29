from django import forms
from .models import LearnerUser

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = LearnerUser
        fields = ['avatar', 'fullname', 'date_of_birth', 'gender', 'phone_number', 'address']

    avatar = forms.ImageField(required=False)
    date_of_birth = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'), input_formats=['%d/%m/%Y'])
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['fullname'].widget.attrs['placeholder'] = 'Họ và tên'
        self.fields['date_of_birth'].widget.attrs['placeholder'] = 'dd/mm/yyyy'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Số điện thoại'
        self.fields['address'].widget.attrs['placeholder'] = 'Địa chỉ'

