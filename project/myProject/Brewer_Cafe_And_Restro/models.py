from django.db import models
import os
from django.forms import ValidationError
from myProject.utils import unique_slug_generator,unique_slug_generator1
from django.db.models.signals import pre_save
from django.utils import timezone
import datetime

# Create your models here.

def filepath(request,filename):
    old_filename = filename
    return os.path.join('myImages/',old_filename)

def filepathItemCategory(request,filename):
    old_filename = filename
    return os.path.join('Item_Category/',old_filename)
    
def filepathItem(request,filename):
    old_filename = filename
    return os.path.join('Item_images/',old_filename)

def custome_validator(value):
    valid_formats = ['png','jpeg','jpg']
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image formate!')

class City(models.Model):
    idcity = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'city'
    
    def __str__(self):
        return self.city_name


class Area(models.Model):
    pincode = models.DecimalField(primary_key=True,max_digits=6, decimal_places=0)
    area_name = models.CharField(max_length=100)
    area_delivery_charges = models.IntegerField()
    city_idcity = models.ForeignKey(City,on_delete=models.SET_NULL,null=True, db_column='city_idcity')

    class Meta:
        managed = True
        db_table = 'area'
    
    def __str__(self):
        return self.area_name
    

class Restaurant(models.Model):
    idrestaurant = models.AutoField(primary_key=True)
    restaurant_name = models.CharField(max_length=45)
    restaurant_email = models.CharField(max_length=45)
    restaurant_phone = models.DecimalField(max_digits=10, decimal_places=0,null=True)
    restaurant_description = models.CharField(max_length=200)
    restaurant_image = models.ImageField(upload_to=filepath,null=True,blank=True)
    restaurant_address = models.CharField(max_length=500,null=True)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True, db_column='area_pincode')

    class Meta:
        managed = True
        db_table = 'restaurant'
    
    def __str__(self):
        return self.restaurant_name
    


class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    user_first_name = models.CharField(max_length=25,null=True)
    user_last_name = models.CharField(max_length=25,null=True)
    user_name = models.CharField(max_length=15,unique=True)
    user_password = models.CharField(max_length=300)
    user_email = models.CharField(max_length=245,unique=True)
    user_mobile = models.CharField(max_length=10,unique=True)
    user_address = models.TextField(max_length=200,null=True)
    user_sec_question = models.CharField(max_length=60,null=True)
    user_sec_answer = models.CharField(max_length=60,null=True)
    user_image = models.ImageField(upload_to=filepath,null=True,blank=True)
    is_admin = models.IntegerField()
    forgot_password_token = models.CharField(max_length=100,default="")
    pincode = models.ForeignKey(Area,null=True,on_delete=models.SET_NULL, db_column='area_pincode',default="")
    idrestaurant = models.ForeignKey(Restaurant,null=True,on_delete=models.SET_NULL, db_column='restaurant_idrestaurant')

    class Meta:
        managed = True
        db_table = 'user'
    
    def __str__(self):
        return self.user_name

    def register(self):
        self.save()

    def isEmailExists(self):
        if User.objects.filter(user_email=self.user_email):
            return True
        return False

    def isUserExists(self):
        if User.objects.filter(user_name=self.user_name):
            return True
        return False

    def isMobileNoExists(self):
        if User.objects.filter(user_mobile=self.user_mobile):
            return True
        return False
    
    @staticmethod
    def get_user_by_username(user_name):
        return User.objects.get(user_name=user_name)


class ItemCategory(models.Model):
    iditem_category = models.AutoField(primary_key=True)
    item_category_name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=250,null=True,blank=True)
    item_category_description = models.CharField(max_length=1000)
    item_category_image = models.ImageField(upload_to=filepathItemCategory,null=True,blank=True)
    restaurant_idrestaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, db_column='restaurant_idrestaurant')

    class Meta:
        managed = True
        db_table = 'item_category'
    
    def __str__(self):
        return self.item_category_name


class Offer(models.Model):
    idoffer = models.AutoField(primary_key=True)
    offer_value = models.DecimalField(max_digits=2, decimal_places=0)
    offer_start_date = models.DateField()
    offer_end_date = models.DateField()
    offer_description = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'offer'
    
    def __str__(self):
        return self.offer_description

class Item(models.Model):
    iditem = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=60)
    slug = models.SlugField(max_length=250,null=True,blank=True)
    item_price = models.IntegerField()
    offer_price = models.FloatField(default=0)
    item_description = models.CharField(max_length=200)
    item_image = models.ImageField(upload_to=filepathItem,null=True,blank=True)
    offer_idoffer = models.ForeignKey(Offer,on_delete=models.SET_NULL,null=True, db_column='offer_idoffer')
    item_category_iditem_category = models.ForeignKey(ItemCategory,on_delete=models.SET_NULL,null=True, db_column='item_category_iditem_category')

    class Meta:
        managed = True
        db_table = 'item'
    
    def __str__(self):
        return self.item_name

class Cart(models.Model):
    user_iduser = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, db_column='user_iduser')
    item_iditem = models.ForeignKey(Item, on_delete=models.SET_NULL,null=True, db_column='item_iditem')
    offer_record = models.IntegerField(default=1)
    item_qty = models.IntegerField(null=False,blank=False)

    class Meta:
        managed = True
        db_table = 'cart'
    
    def __str__(self):
        return f'Cart of {self.user_iduser}'
    

class Order(models.Model):
    idorder = models.AutoField(primary_key=True)
    orderfname = models.CharField(max_length=150,null=True)
    orderlname = models.CharField(max_length=150,null=True)
    orderemail = models.CharField(max_length=150,null=True)
    ordermobile = models.CharField(max_length=150,null=True)
    order_date = models.DateField(auto_now_add=True)
    cancel_order_date = models.DateTimeField(null=True)
    order_delivery_date = models.DateTimeField(auto_now_add=True)
    order_delivery_address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    total_amount = models.FloatField(null=False)
    order_payment_method = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,null=True)
    status = (
        ('Pending','Pending'),
        ('Out for shipping','Out for shipping'),
        ('Completed','Completed'),
    )
    order_status = models.CharField(max_length=150,choices=status,default='Pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    is_cancel_order = models.IntegerField(default=0)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True, db_column='area_pincode')
    user_iduser = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, db_column='user_iduser')
    created_at = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'order'
    
    def __str__(self):
        return '{} - {}'.format(self.idorder,self.tracking_no)

class OrderedItem(models.Model):
    order_idorder = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True, db_column='order_idorder')
    item_iditem = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True, db_column='item_iditem')
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'ordered_item'
    
    # def __str__(self):
    #     return '{} - {}'.format(self.order_idorder,self.order_idorder.tracking_no)

class Review(models.Model):
    idreview = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100,blank=True)
    review_description = models.TextField(max_length=500,blank=True)
    rating_value = models.FloatField(null=True)
    status = models.BooleanField(default=True)
    reviewDate = models.DateField(datetime.date.today,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_iduser = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,db_column='user_iduser')
    item_iditem = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True,db_column='item_iditem')

    class Meta:
        managed = True
        db_table = 'review'
    
    def __str__(self):
        return '{} - review'.format(self.user_iduser.user_name)

class Notification(models.Model):
    idnotification = models.AutoField(primary_key=True)
    notification_description = models.TextField(max_length=500,blank=True)
    notificationDate = models.DateField(datetime.date.today,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'notification'
    
    def __str__(self):
        return 'Notifications'


class Table(models.Model):
    idtable = models.AutoField(primary_key=True)
    table_capacity = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'table'
    
    def __str__(self):
        return f'Table details - {self.table_capacity}'
    
class TableReservation(models.Model):
    idtable_reservation = models.AutoField(primary_key=True)
    tableResfname = models.CharField(max_length=150,null=True)
    tableReslname = models.CharField(max_length=150,null=True)
    tableResemail = models.CharField(max_length=150,null=True)
    tableResmobile = models.CharField(max_length=150,null=True)
    table_reservation_date_time = models.DateTimeField(null=True)
    table_reservation_no_guest = models.IntegerField()
    table_reservation_total_table_reserved = models.CharField(max_length=45)
    total_amount = models.IntegerField(null=True)
    is_table_reservation_cancel = models.IntegerField(default=0)
    tableRes_payment_method = models.CharField(max_length=150,null=False)
    tableRes_payment_id = models.CharField(max_length=250,null=True)
    tableRes_status = models.CharField(max_length=150,default='Success')
    user_iduser = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, db_column='user_iduser')

    class Meta:
        managed = True
        db_table = 'table_reservation'

    def __str__(self):
        return "Table reservation of {}".format(self.user_iduser.user_name)

class TableReservationDetails(models.Model):
    table_reservation_idtable_reservation = models.ForeignKey(TableReservation,on_delete=models.SET_NULL,null=True, db_column='table_reservation_idtable_reservation')
    table_idtable = models.ForeignKey(Table, on_delete=models.SET_NULL,null=True, db_column='table_idtable')

    class Meta:
        managed = True
        db_table = 'table_reservation_details'

class Supplier(models.Model):
    idsupplier = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=60)
    supplier_mobile_no = models.DecimalField(max_digits=10, decimal_places=0)
    supplier_address = models.CharField(max_length=200)
    area_name = models.CharField(max_length=200)
    pincode = models.DecimalField(max_digits=6, decimal_places=0)
    restaurant_idrestaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True,db_column='restaurant_idrestaurant')

    class Meta:
        managed = True
        db_table = 'supplier'
    
    def __str__(self):
        return self.supplier_name

class RawMaterial(models.Model):
    idraw_material = models.AutoField(primary_key=True)
    raw_material_name = models.CharField(max_length=60)
    raw_materialtotal_quantity = models.IntegerField()
    raw_material_price = models.IntegerField()
    restaurant_idrestaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True,db_column='restaurant_idrestaurant')

    class Meta:
        managed = True
        db_table = 'raw_material'
    
    def __str__(self):
        return self.raw_material_name

class Purchase(models.Model):
    idpurchase = models.AutoField(primary_key=True)
    purchase_total_amount = models.IntegerField()
    purchase_date = models.DateField()
    gst = models.DecimalField(max_digits=3, decimal_places=1,null=True)
    supplier_idsupplier = models.ForeignKey(Supplier,on_delete=models.SET_NULL,null=True,db_column='supplier_idsupplier')

    class Meta:
        managed = True
        db_table = 'purchase'

class PurchaseRawMaterial(models.Model):
    raw_material_idraw_material = models.ForeignKey(RawMaterial,on_delete=models.SET_NULL,null=True, db_column='raw_material_idraw_material')
    purchase_idpurchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL,null=True, db_column='purchase_idpurchase')
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'purchase_raw_material'

class PurchaseReturn(models.Model):
    idpurchase_return = models.AutoField(primary_key=True)
    purchase_return_total_amount = models.IntegerField()
    purchase_return_date = models.DateField()
    purchase_idpurchase = models.ForeignKey(Purchase, on_delete=models.SET_NULL,null=True, db_column='purchase_idpurchase')

    class Meta:
        managed = True
        db_table = 'purchase_return'

class PurchaseReturnOfRawMaterial(models.Model):
    raw_material_idraw_material = models.ForeignKey(RawMaterial, on_delete=models.SET_NULL,null=True, db_column='raw_material_idraw_material')
    purchase_return_idpurchase_return = models.ForeignKey(PurchaseReturn,on_delete=models.SET_NULL,null=True, db_column='purchase_return_idpurchase_return')
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'purchase_return_of_raw_material'

class TotalGuest(models.Model):
    idguest = models.AutoField(primary_key=True)
    guestNumber = models.IntegerField()

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

def slug_generator1(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator1(instance)

pre_save.connect(slug_generator,sender=ItemCategory)
pre_save.connect(slug_generator1,sender=Item)