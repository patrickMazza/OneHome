from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.utils.timezone import now
from .validators import validate_file_extension


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # Configuration
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Create a UserUpdateForm to update a username and email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Create a ProfileUpdateForm to update image.


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class PastDateInput(forms.DateInput):
    input_type = 'date'

    def get_context(self, name, value, attrs):
        attrs.setdefault('max', now().strftime('%Y-%m-%d'))
        return super().get_context(name, value, attrs)


class ClientRegisterForm(forms.ModelForm):

    class Meta:
        model = ClientProfile
        fields = ["first_Name", "last_Name",
                  "birthdate", "client_Intake_Date", "image"]
        widgets = {
            'birthdate': PastDateInput(),
            'client_Intake_Date': PastDateInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ClientRegisterForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False


SORT_CHOICES = (
    ("1", "Highest Priority"),
    ("2", "Most Progress"),
    ("3", "Oldest to Newest"),
)


class Sort(forms.Form):
    field = forms.ChoiceField(choices=SORT_CHOICES, required=False,
                              widget=forms.Select(attrs={'onchange': 'submit();'}))


FORM_CHOICES = (
    ("",
     ""),
    ("2010e Supportive Housing Application",
     "2010e Supportive Housing Application"),
)


class DocsForm(forms.ModelForm):
    application_type = forms.ChoiceField(choices=FORM_CHOICES,
                                         )

    class Meta:
        model = Docs
        fields = ["document_Name", "file_field", "application_type"]


class DeleteForm(forms.ModelForm):
    application_type = forms.ChoiceField(choices=FORM_CHOICES,
                                         )

    class Meta:
        model = Docs
        fields = ["document_Name", "file_field", "application_type"]


class AddForm(forms.Form):
    application_type = forms.ChoiceField(choices=FORM_CHOICES, widget=forms.Select(attrs={'onchange': 'submit();'})
                                         )


HOUSING_CHOICES = (
    ("1",
     "Housing for Individuals with Serious Mental Illnesses including those with Co-Occurring Substance Use"),
    ("2",
     "Housing for Homeless Individuals with Substance Use Disorders"),
    ("3", "Housing for Individuals who have Successfully Completed/Participated in a Course of Substance Use Treatment"),
    ("4", "Housing for Individuals Living with HIV/AIDS with co-occurring Serious Mental Illness and/or Substance Use Disorder"),
    ("5", "Housing for low-income single adults with a disabling clinical condition currently residing in a Department of Homeless Services (DHS) shelter"),
)


class Application2010e_P1(forms.ModelForm):
    supportive_type = forms.ChoiceField(
        label="Type of Supportive Housing Applicant Applying for: Individual", choices=HOUSING_CHOICES)

    date_time = forms.DateTimeField(label="Date and Time Entered", required=False, widget=forms.DateTimeInput(
        format=('%-m/%-d/%Y %-I:%M:%S %p'), attrs={'type': 'datetime-local'}))
    done = forms.BooleanField(label="Finished With Section", required=False)
    # consent = forms.CharField(label="Selected_services *",
    #                           widget=forms.Textarea())

    class Meta:
        model = Application2010e_part1
        fields = ["application_ID", "referring_Agency",
                  "referring_Site", "date_time", "housing_Program", "applicant_Name", "consent", "date_time", "consent_Date",
                  "verified_By", "location_Kept", "supportive_type", "done"]
        widgets = {
            'consent_Date': PastDateInput(),
        }
