from .models import *
from django import forms
from django.forms import ModelForm
from django.forms.widgets import DateInput, TextInput, DateTimeInput



class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
           # self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
            self.fields['password'].required = False
            self.fields['profile_pic'].required = False
            if kwargs.get('instance'):
                instance = kwargs.get('instance').__dict__
                self.fields['password'].required = False
                for field in CustomUserForm.Meta.fields:
                    self.fields[field].initial = instance.get(field)
                if self.instance.pk is not None:
                    self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

            
    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]

#forms for adding story or post
class StoryForm(FormSettings):
    class Meta:
        model = Story
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].widget = forms.HiddenInput() #hide the author field and auto add the current user in view
        
        
class CommentForm(FormSettings):
    class Meta:
        model = Comment
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["author"].widget = forms.HiddenInput() #hide the author field and auto add the current user in view
        self.fields["story"].widget = forms.HiddenInput() #hide the story field and auto add the actual story in view
        
