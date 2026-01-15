from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "description",
            "event_type",
            "event_date",
            "end_date",
            "discount_percentage",
            "banner_image",
            "is_active",
            "status",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Event name"
            }),
            "description": forms.Textarea(attrs={
                "placeholder": "Short description about the event",
                "rows": 4
            }),
            "event_type": forms.Select(),
            "event_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "end_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M"
            ),
            "discount_percentage": forms.NumberInput(attrs={
                "min": 0,
                "max": 100,
                "placeholder": "0 - 100"
            }),
            "banner_image": forms.FileInput(),
            "is_active": forms.CheckboxInput(),
            "status": forms.Select(),
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
