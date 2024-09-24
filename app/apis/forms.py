from django import forms
from . models import SalesData

class SalesForm(forms.Form):
    
    Store = forms.IntegerField()
    DayOfWeek = forms.IntegerField()
    Date = forms.DateField()
    Open = forms.IntegerField()
    Promo = forms.ChoiceField(choices=[(0, 'zero: 0'),(1, 'One: 1')]) # 0, 1
    StateHoliday = forms.ChoiceField(choices=[('0', 'Zero: 0'),('a', 'A'),('b', 'B'),('c', 'C'),]) # a,b,c
    SchoolHoliday = forms.ChoiceField(choices=[(0, 'zero: 0'),(1, 'One: 1')]) # 0, 1
    StoreType = forms.ChoiceField(choices=[('d', 'D'),('a', 'A'),('b', 'B'),('c', 'C'),]) # a, b, c ,d
    Assortment = forms.ChoiceField(choices=[('a', 'A'),('b', 'B'),('c', 'C'),]) # a, b, c 
    CompetitionDistance = forms.FloatField()
    CompetitionOpenSinceMonth = forms.IntegerField()
    CompetitionOpenSinceYear = forms.IntegerField()
    Promo2 = forms.ChoiceField(choices=[(0, 'zero: 0'),(1, 'One: 1')]) # 0, 1
    Promo2SinceWeek = forms.IntegerField()
    Promo2SinceYear = forms.IntegerField()
    PromoInterval = forms.ChoiceField(choices=[('Jan,Apr,Jul,Oct', 'Jan,Apr,Jul,Oct'),('Feb,May,Aug,Nov', 'Feb,May,Aug,Nov'),('Mar,Jun,Sept,Dec', 'Mar,Jun,Sept,Dec') ])	
