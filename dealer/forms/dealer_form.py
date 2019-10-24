from django import forms
from django.contrib.auth.models import User
from dealer.models import Dealer


class DealerForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    repeat_password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super(DealerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=False):
        if self.cleaned_data['password'] == self.cleaned_data['repeat_password']:
            user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password'])
            user.first_name = self.cleaned_data['first_name']
            user.save()

            dealer = Dealer.objects.create(user_id=user.id)
            dealer.save()
            return dealer
