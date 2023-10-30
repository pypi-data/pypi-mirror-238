from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, fields
from .models import User


class UserForm(ModelForm):

    language_code = fields.ChoiceField(
        label=_('Language'),
        choices=settings.LANGUAGES,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
        ]

    def save(self, commit=True):
        super().save(commit=False)
        self.instance.language_code = self.cleaned_data['language_code']
        if commit:
            self.instance.save()
            self.save_m2m()
