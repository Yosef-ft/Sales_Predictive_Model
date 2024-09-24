from django.db import models


# Create your models here.
class SalesData(models.Model):
    Zero_one_choice = (
        (0, 'zero: 0'),
        (1, 'One: 1')
    )
    ABC_choice = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    )
    ABC_Zero_choice = (
        ('0', 'Zero: 0'),
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    )
    ABCD_choice = (
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('d', 'D'),
    )
    Promo_choice = (
        ('Jan,Apr,Jul,Oct', 'Jan,Apr,Jul,Oct'),
        ('Feb,May,Aug,Nov', 'Feb,May,Aug,Nov'),
        ('Mar,Jun,Sept,Dec', 'Mar,Jun,Sept,Dec')    
    )
    

    Store = models.IntegerField(default=1)
    DayOfWeek = models.IntegerField(default=1)
    Date = models.DateField()
    Open = models.IntegerField(default=1)
    Promo = models.IntegerField(choices=Zero_one_choice) # 0, 1
    StateHoliday = models.CharField(max_length=1, choices=ABC_Zero_choice) # a,b,c
    SchoolHoliday = models.IntegerField(choices=Zero_one_choice) # 0, 1
    StoreType = models.CharField(max_length=1, choices=ABCD_choice) # a, b, c ,d
    Assortment = models.CharField(max_length=1, choices=ABC_choice) # a, b, c 
    CompetitionDistance = models.FloatField(default=0)
    CompetitionOpenSinceMonth = models.IntegerField(default=0)
    CompetitionOpenSinceYear = models.IntegerField(default=0)
    Promo2 = models.IntegerField(choices=Zero_one_choice) # 0, 1
    Promo2SinceWeek = models.IntegerField(default=0)
    Promo2SinceYear = models.IntegerField(default=0)
    PromoInterval = models.CharField(max_length=100, choices=Promo_choice)


    def __str__(self):
        return self.Store