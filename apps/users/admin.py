from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, _unicode_ci_compare, UserModel, PasswordResetForm, \
    AdminPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy

from users.models import UserProfile


# Register your models here.
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # 设置密码为只读
    # password = ReadOnlyPasswordHashField()

    # 重写密码
    password = ReadOnlyPasswordHashField(label=("密码Hash值"),
                                         help_text=("<a href=\"../password/\">点击修改密码</a>."))

    # 重设密码，原admin是邮件做帐号，需自己重写设置密码
    # password=AdminPasswordChangeForm()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'username', 'nickname', 'is_superuser', 'is_staff'
                  , 'mobile', 'gender', 'birthday')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = (
        'username', 'mobile', 'nickname', 'gender', 'birthday', 'email', 'create_time',
        'update_time')  # add more columns.
    list_filter = ['mobile']  # add filter function.
    fieldsets = (
        (None, {'fields': ('username', 'password', 'mobile', 'email')}),

        (gettext_lazy('用户信息'), {'fields': ('birthday', 'gender', 'nickname')}),

        (gettext_lazy('权限'), {'fields': ('is_staff', 'is_superuser',
                                         'groups')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'mobile', 'password1', 'password2')}
         ),
    )
    search_fields = ('username','mobile','email')
    ordering = ('username',)
    filter_horizontal = ()


# 注册用户model
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = 'xx 项目管理系统'
admin.site.site_title = '登录系统后台'
admin.site.index_title = '后台管理'
