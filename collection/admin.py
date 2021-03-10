from django.contrib import admin
from collection.models import *


# Register your models here.


class DetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'open', 'close', 'market_lot')
    list_filter = ('open', 'category')
    search_fields = ['company', 'open']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_asset', 'total_revenue', 'profit')
    list_filter = ('asset_id',)
    search_fields = ['asset_id', ]


class TentativeDateAdmin(admin.ModelAdmin):
    list_display = ('basic_of_allotment', 'initiation_date', 'credit_date', 'listing_date')
    list_filter = ('tentative_id',)
    search_fields = ['tentative_id', ]


class IpoSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('qib_sub', 'nii_sub', 'retail_sub', 'total_sub')
    list_filter = ('sub_id',)
    search_fields = ['sub_id', ]


class ShareAdmin(admin.ModelAdmin):
    list_display = ('qib_share', 'nii_share', 'retail_share', 'total_share')
    list_filter = ('share_id',)
    search_fields = ['share_id', ]


class AllotmentAdmin(admin.ModelAdmin):
    list_display = ('link',)
    list_filter = ('allotment_id',)
    search_fields = ['allotment_id', ]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','body', 'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ['name', 'email']

class DividendAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'dividend_type', 'rate', 'announcement')
    list_filter = ('company_name', 'rate')
    search_fields = ['company_name',]


admin.site.register(IpoDetails, DetailsAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(TentativeDate, TentativeDateAdmin)
admin.site.register(IpoSubscription, IpoSubscriptionAdmin)
admin.site.register(ShareOffered, ShareAdmin)
admin.site.register(Allotment, AllotmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(DividendData, DividendAdmin)