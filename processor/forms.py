from django import forms

from .models import Preset


class UploadForm(forms.Form):
    image = forms.ImageField()


class PresetForm(forms.ModelForm):
    dot_spacing = forms.IntegerField(initial=10)
    style = forms.ChoiceField(choices=[("classic", "Classic"), ("diamond", "Diamond"), ("line", "Line")])

    class Meta:
        model = Preset
        fields = ["name", "is_default"]


class PresetImportForm(forms.Form):
    json_data = forms.CharField(widget=forms.Textarea)


class BatchUploadForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    make_public = forms.BooleanField(required=False, label="Make all images public")
