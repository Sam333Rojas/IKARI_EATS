from django import forms
from restaurant.models import Tag, Item, Restaurant


class ItemForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.TextInput)
    price = forms.IntegerField(widget=forms.NumberInput)
    tag_label = forms.CharField(max_length=12)

    class Meta:
        model = Item
        fields = ['price', 'description', 'path', 'name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=False):
        restaurant = Restaurant.objects.get(pk=self.request.user.id)

        tag = Tag.objects.filter(label=self.cleaned_data['tag_label']).first()

        if tag is None:
            tag = Tag.objects.create(label=self.cleaned_data['tag_label'])
            tag.save()

        item = Item.objects.create(name=self.cleaned_data['name'], description=self.cleaned_data['description'],
                                   price=self.cleaned_data['price'], restaurant=restaurant, tag=tag
                                   )
        item.save()
        return item
