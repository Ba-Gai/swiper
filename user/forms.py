from django import forms
from user.models import User, Profile


# User表单
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # 添加指定字段
        fields = ['nickname', 'sex', 'birthday', 'location']


# Profile表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # 将所有的字段都添加进去
        fields = '__all__'

    # 特殊字段的验证
    def clean_max_distance(self):
        cleaned = super().clean()
        if cleaned['max_distance'] < cleaned['min_distance']:
            raise forms.ValidationError('max_distance必须大于min_distance')
        else:
            # 在django自动处理这个max_distance的时候，如果不返回django就会认为没有写这个字段
            return cleaned['max_distance']

    def clean_max_dating_age(self):
        cleaned = super().clean()
        if cleaned['max_dating_age'] < cleaned['min_dating_age']:
            raise forms.ValidationError('max_distance必须大于min_dating_age')
        else:
            return cleaned['max_dating_age']