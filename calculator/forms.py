from django import forms

class Calc(forms.ModelForm):
    class Meta:
        model = Calc
        fields = ('num1','num2')