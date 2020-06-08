from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Role

class UserCreationForm(forms.ModelForm):
    """
    A form for registering new users with all required field
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    is_admin = forms.BooleanField(label='Is Admin', required=False, widget=forms.CheckboxInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'is_admin')

    def clean_password2(self):
        """
        Check to ensure passwords are the same
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords are n't the same")
        else:
            raise forms.ValidationError("Passwords can't be empty")

        return password2

    def save(self, commit=True):
        """
        Save password in hashed form
        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        admin = self.cleaned_data.get('is_admin')
        if admin:
            user.is_admin=True
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """
    A form for updating users with all fields while replacing password
    field with admin's password hash display field
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class RoleCreationForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ('name', 'description')

class EditRoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = ['name', 'description']
