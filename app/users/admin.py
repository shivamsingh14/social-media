from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from app.users.models import User, FriendStatus, PendingRequests


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new User usign the Django Admin
    """
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta(object):
        model = User
        fields = ('first_name', 'email')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserUpdationForm(forms.ModelForm):
    """
    A from for updating current user in Django Admin
    """

    password = ReadOnlyPasswordHashField()

    class Meta(object):
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):

    form = UserUpdationForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'first_name', 'is_staff')
    list_filter = ('is_staff', 'email', 'first_name', 'verification_status')
    search_fields = ('email', )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password',
                'gender', 'date_of_birth'
            )}),
    )
    ordering = ('email',)
    filter_horizontal = ()


class FriendAdmin(admin.ModelAdmin):
    raw_id_fields = ('user_1', 'user_2',)


class PendingRequestsAdmin(admin.ModelAdmin):
    raw_id_fields = ('request_from', 'request_to',)

admin.site.register(User, UserAdmin)
admin.site.register(FriendStatus, FriendAdmin)
admin.site.register(PendingRequests, PendingRequestsAdmin)
