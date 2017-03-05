from django import forms
from django.contrib.auth.models import User
from market.models import Category,Goods,UserProfile,Comment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username','email','password')


class UserProfieldForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar',)


class GoodsForm(forms.ModelForm):
    name = forms.CharField(max_length=32,help_text="商品名称",widget=forms.TextInput(attrs={'class':'name','placeholder':'最多二十五个字'}))
    description = forms.CharField(max_length=512,help_text="商品详情",widget=forms.Textarea(attrs={'id':'desc','placeholder':'建议填写物品用途、新旧程度、原价等信息，至少15个字'}))
    trade_location = forms.CharField(max_length=32,help_text="交易地点",widget=forms.TextInput(attrs={'id':'trade_place','placeholder':'宿舍、金三角、食堂等'}))
    price = forms.IntegerField(help_text="价格",widget=forms.TextInput(attrs={'id':'price'}))
    discount = forms.ChoiceField(choices=[('0','不可刀'),('1','可小刀')])
    goods_phone = forms.IntegerField(widget=forms.TextInput(attrs={'id':'tel'}))
    goods_qq = forms.IntegerField(widget=forms.TextInput(attrs={'id':'qq'}))

    class Meta:
        model = Goods
        exclude = ('seller','picture_url')


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=128,widget=forms.Textarea(attrs={'id':'comment_input','class':'comment-input',}))

    class Meta:
        model = Comment
        fields = ('content',)


