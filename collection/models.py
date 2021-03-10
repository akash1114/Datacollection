from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django import forms


# Create your models here.

class IpoDetails(models.Model):
    content = models.TextField()
    name = models.CharField(max_length=50)
    open = models.DateField(null=True)
    close = models.DateField(null=True)
    type = models.CharField(max_length=50, null=True)
    face_value = models.CharField(max_length=50, null=True)
    ipo_price = models.CharField(max_length=50, null=True)
    market_lot = models.CharField(max_length=50, null=True)
    listing_at = models.CharField(max_length=50, null=True)
    issue_size = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=10, null=True, default='mainboard')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-open"]


class Asset(models.Model):
    asset_id = models.ForeignKey(IpoDetails, on_delete=models.CASCADE, related_name='asset_id')
    date = models.CharField(max_length=20)
    total_asset = models.CharField(max_length=20)
    total_revenue = models.CharField(max_length=20)
    profit = models.CharField(max_length=20)

    def __str__(self):
        return self.asset_id.name


class TentativeDate(models.Model):
    tentative_id = models.ForeignKey(IpoDetails, on_delete=models.CASCADE)
    basic_of_allotment = models.DateField(null=True)
    initiation_date = models.DateField(null=True)
    credit_date = models.DateField(null=True)
    listing_date = models.DateField(null=True)

    def __str__(self):
        return self.tentative_id.name


class IpoSubscription(models.Model):
    sub_id = models.ForeignKey(IpoDetails, on_delete=models.CASCADE)
    qib_sub = models.CharField(max_length=20, null=True)
    nii_sub = models.CharField(max_length=20, null=True)
    retail_sub = models.CharField(max_length=20, null=True)
    employee = models.CharField(max_length=20, null=True)
    other = models.CharField(max_length=20, null=True)
    total_sub = models.CharField(max_length=20)

    def __str__(self):
        return self.sub_id.name


class ShareOffered(models.Model):
    share_id = models.ForeignKey(IpoDetails, on_delete=models.CASCADE)
    qib_share = models.CharField(max_length=20, null=True)
    nii_share = models.CharField(max_length=20, null=True)
    retail_share = models.CharField(max_length=20, null=True)
    total_share = models.CharField(max_length=20)

    def __str__(self):
        return self.share_id.name


class Allotment(models.Model):
    allotment_id = models.ForeignKey(IpoDetails, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='available')
    link = models.CharField(max_length=200, null=True)


class Comment(models.Model):
    ipo = models.ForeignKey(IpoDetails, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # manually deactivate inappropriate comments from admin site
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        # sort comments in chronological order by default
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {}'.format(self.user)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class DividendData(models.Model):
    company_name = models.CharField(max_length=20, unique=True)
    dividend_type = models.CharField(max_length=20, null=True)
    rate = models.CharField(max_length=10, null=True)
    announcement = models.CharField(max_length=20, null=True)
    record = models.CharField(max_length=20, null=True)
    ex_dividend = models.CharField(max_length=20, null=True)
    dividend_fv = models.CharField(max_length=10,null=True)
    dividend_mp = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.company_name