from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(City)
admin.site.register(Area)
admin.site.register(Restaurant)
admin.site.register(User)
admin.site.register(ItemCategory)
admin.site.register(Offer)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderedItem)
admin.site.register(Review)
admin.site.register(Notification)
admin.site.register(Table)
admin.site.register(TableReservation)
admin.site.register(TableReservationDetails)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(RawMaterial)
admin.site.register(PurchaseRawMaterial)
admin.site.register(PurchaseReturn)
admin.site.register(PurchaseReturnOfRawMaterial)
admin.site.register(TotalGuest)