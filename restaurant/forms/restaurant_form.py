from django import forms
from django.contrib.auth.models import User, Group
from restaurant.models import Restaurant, Tag


class RestaurantForm(forms.ModelForm):
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    repeat_password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)

    description = forms.CharField(widget=forms.TextInput)
    latitude = forms.DecimalField(decimal_places=8 ,max_digits=12)
    longitude = forms.DecimalField(decimal_places=8 ,max_digits=12)
    address = forms.CharField(max_length=100)

    tag_label = forms.CharField(max_length=12)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'username']

    # 'rank', 'description', 'latitude', 'longitude', 'address' , 'tag'
    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=False):
        if self.cleaned_data['password'] == self.cleaned_data['repeat_password']:
            user = User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
                                            password=self.cleaned_data['password'])
            user.first_name = self.cleaned_data['first_name']
            user.groups.add( Group.objects.get(name='restaurant') )
            user.save()

            tag = Tag.objects.filter(label=self.cleaned_data['tag_label']).first()

            if tag is None:
                tag = Tag.objects.create(label=self.cleaned_data['tag_label'])
                tag.save()

            restaurant = Restaurant.objects.create(user_id=user.id, description=self.cleaned_data['description'],
                                                   latitude=self.cleaned_data['latitude'],
                                                   longitude=self.cleaned_data['longitude'],
                                                   address=self.cleaned_data['address'], rank=0, tag=tag)

            restaurant.save()
            return restaurant
