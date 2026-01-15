from django import forms
from django.contrib.auth.models import User
from shop.models import Product
from events.models import Event
from weather.models import SearchHistory
from blog.models import Post

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'image', 'stock']


class EventForm(forms.ModelForm):
    """
    🔥 FULL EVENT FORM - All editable fields including category selection for discounts
    """
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "event_type",
            "event_date",
            "end_date",
            "discount_percentage",
            "categories",  # Added for category-based discounts
            "banner_image",
            "is_active",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Event name",
                "class": "form-control"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Short description about the event",
                "rows": 4,
                "class": "form-control"
            }),
            "event_type": forms.Select(attrs={
                "class": "form-control"
            }),
            "event_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control"
                },
                format="%Y-%m-%dT%H:%M"
            ),
            "end_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control"
                },
                format="%Y-%m-%dT%H:%M"
            ),
            "discount_percentage": forms.NumberInput(attrs={
                "min": 0,
                "max": 100,
                "placeholder": "0 - 100",
                "class": "form-control"
            }),
            "categories": forms.CheckboxSelectMultiple(attrs={
                "class": "form-check-input"
            }),
            "banner_image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "status": forms.Select(attrs={
                "class": "form-control"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 FORCE UNLOCK ALL FIELDS
        for name, field in self.fields.items():
            field.disabled = False
            field.required = name in ["name", "event_date"]
            
            # Remove any readonly or disabled attributes
            if hasattr(field.widget, "attrs"):
                field.widget.attrs.pop("readonly", None)
                field.widget.attrs.pop("disabled", None)

        # 🔥 Format datetime fields for editing
        if self.instance and self.instance.pk:
            if self.instance.event_date:
                self.initial["event_date"] = self.instance.event_date.strftime("%Y-%m-%dT%H:%M")
            if self.instance.end_date:
                self.initial["end_date"] = self.instance.end_date.strftime("%Y-%m-%dT%H:%M")


class WeatherForm(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields = '__all__'


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=False),
        required=False,
        help_text='Set or change the user password. Leave empty to keep current password.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        pwd = self.cleaned_data.get('password')
        if pwd:
            user.set_password(pwd)
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

