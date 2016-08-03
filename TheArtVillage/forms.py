from models import Art, Agent, Image, MyDecimalField, generate_filename_art, generate_filename_picture, Artist, UserProfile
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django_countries.widgets import CountrySelectWidget



def generate_filename_picture(self, filename):
    url = "Art/%s/%s" % (self.art, filename)
    return url


class Image(forms.ModelForm):
    art = models.ForeignKey(Art)
    additional_image = models.ImageField(upload_to=generate_filename_picture)

    class Meta:
        model = Image
        fields = ('id', 'art',)


class AgentForm(forms.ModelForm):
    surname = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    phone = models.CharField(max_length=16)
    postcode = models.CharField(max_length=8)
    fullname = models.CharField(max_length=256, blank=True, editable=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Agent

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        # exclude = ('category',)
        # or specify the fields to include (i.e. not include the category field)
        fields = ('surname', 'firstname', 'phone', 'postcode')


class ArtForm(forms.ModelForm):
    name = models.CharField(max_length=128, help_text="Enter the name of the piece of art")
    category = models.CharField(max_length=128)
    sub_category = models.CharField(max_length=128)
    artist_id = models.ForeignKey(Artist, help_text="Click magnifying glass to find correct artist")
    price = MyDecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    picture = models.ImageField(upload_to=generate_filename_art, blank=True)  # !!!!
    agent_id = models.ForeignKey(Agent, help_text="Click magnifying glass to find correct agent")
    weight = models.CharField(max_length=16, help_text="weight in kg")
    size = models.CharField(max_length=16, help_text="dimensions in cm")
    description = models.TextField(blank=True)


    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Art
        fields = ('name', 'sub_category', 'category', 'artist_id', 'price', 'quantity', 'picture')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')



class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    surname = forms.CharField(widget=forms.HiddenInput(), required=False)
    country = forms.CharField(required=False, widget=CountrySelectWidget())
    city = forms.CharField(widget=forms.HiddenInput(), required=False)
    postcode = forms.CharField(widget=forms.HiddenInput(), required=False)
    address1 = forms.CharField(widget=forms.HiddenInput(), required=False)
    address2 = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'surname', 'country', 'city', 'address1', 'address2', 'postcode']
        widgets = {'country': CountrySelectWidget()}



class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ShippingDetailsForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    surname = forms.CharField(required=False)
    country = forms.CharField(required=False, widget=CountrySelectWidget())
    city = forms.CharField(required=False)
    postcode = forms.CharField(required=False)
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['first_name', 'surname', 'country', 'city', 'address1', 'address2', 'postcode']
        widgets = {'country': CountrySelectWidget()}


class PasswordReset(forms.Form):
    oldpassword = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordReset, self).__init__(*args, **kwargs)

    def clean_oldpassword(self):
        if self.clean_data.get('oldpassword') and not self.user.check_password(self.clean_data['oldpassword']):
            raise forms.ValidationError('Please type your current password.')
        return self.clean_data['oldpassword']

    def clean_password2(self):
        if self.clean_data.get('password1') and self.clean_data.get('password2') and self.clean_data['password1'] != \
                self.clean_data['password2']:
            raise forms.ValidationError('The new passwords are not the same')
        return self.clean_data['password2']


class CartAddProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        current_quantity = kwargs.pop('current_quantity')
        update = kwargs.pop('update')
        total_quantity = kwargs.pop('total_quantity')
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        self.fields['quantity'] = forms.TypedChoiceField(
            choices=[(i, str(i)) for i in range(1, total_quantity + 1)],
            coerce=int,
            initial=current_quantity
        )
        self.fields['update'] = forms.BooleanField(required=False, initial=update, widget=forms.HiddenInput)
