from django import forms


class GetUserPhone(forms.Form):
	phone_number = forms.IntegerField(required=True)


class GetUserCode(forms.Form):
	code = forms.IntegerField(required=True)
	jwt_code = forms.CharField(widget=forms.HiddenInput())