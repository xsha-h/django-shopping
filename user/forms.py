from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    """
    类属性必须和表单的name值一样。
    原因：
        在视图函数中（或者类视图里函数）可以直接将获取的参数名及值传给form类
    """
    user = forms.CharField(required=True)
    pwd = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField()


class RegisterForm(forms.Form):
    """
    类属性必须和表单的name值一样。
    原因：
        在视图函数中（或者类视图里函数）可以直接将获取的参数名及值传给form类
    """
    user = forms.CharField(required=True)
    pwd = forms.CharField(required=True, min_length=6)
    repwd = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    # 验证码
    captcha = CaptchaField()

    # 自定义方法（局部钩子），密码必须包含字母和数字
    def clean_pwd(self):
        """
        校验函数名必须符合下列要求：clean_ 开头，属性名结尾
        校验不成功，则需要抛出异常，导入相关的类 ValidationError
        通过校验，我们可以对该属性的值做一点修改（注：这里暂时没有）
        :return:属性的值（通过该对象下的cleaned_data字典的键值对形式获取）
        """
        if self.cleaned_data.get("pwd").isdigit() or self.cleaned_data.get("pwd").isalpha():
            raise ValidationError("密码必须包括数字和字母")
        else:
            return self.cleaned_data["pwd"]

    # 自定义方法（全局钩子, 检验两个字段），检验两次密码一致;
    def clean(self):
        """
        校验函数名必须符合下列要求：clean_ 开头，属性名结尾
        校验不成功，则需要抛出异常，导入相关的类 ValidationError
        通过校验，我们可以对该属性的值做一点修改（注：这里暂时没有）
        :return:属性的值（通过该对象下的cleaned_data字典的键值对形式获取）
        """
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('repwd'):
            raise ValidationError('密码不一致')
        else:
            return self.cleaned_data
