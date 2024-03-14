"""
myProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    

"""
from django.contrib import admin
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings
from Brewer_Cafe_And_Restro import views
from Brewer_Cafe_And_Restro.views import *

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login/',views.loginAction,name='login'),
    path('signup/',views.goSignUpPage,name='signup'),
    path('logout/',views.logout, name='logout'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('change_password/<token>/',views.change_password,name='change_password'),
    path('directly_change_password/',views.directly_change_pass,name='directly_change_password'),
    # Product related urls
    path('user_profile/',views.user_profile,name='user_profile'),
    path('item_category_list/',views.CategoryListView.as_view(),name='item_category_list'),
    path('item_category_list/<slug:slug_text>/',views.ItemListView.as_view(),name='item'),
    path('item_category_list/<slug:cat_slug>/<slug:prod_slug>/',views.ItemDetails,name='itemDetails'),
    path('add-to-cart',views.addtocart,name='add-to-cart'),
    path('cart',views.userCart,name='cart'),
    path('update-cart',views.updatecart,name='update-cart'),
    path('delete-cart-item',views.deletecartitem,name='delete-cart-item'),
    path('change-charges',views.changecharges,name='change-charges'),
    path('checkout',views.checkout,name='checkout'),
    path('place-order',views.placeorder,name='place-order'),
    path('proceed-to-pay',views.razorPayProcess,name='proceed-to-pay'),
    path('my-orders',views.orderpage,name='my-orders'),
    path('orderview/<str:t_no>',views.orderdetailspage,name='orderview'),

    #-----------
    path('cancelOrder1/<str:t_no>',views.cancelOrder1,name='orderview'),



    path('submit_review/<int:item_id>',views.reviewsubmit,name='submit_review'),
    path('offer',views.offer,name='offer'),
    path('cancelOrder',views.orderCancel,name='cancelOrder'),
    path('user-notifications',views.userNotifications,name='user-notifications'),
    path('book-table',views.bookTable,name='book-table'),
    path('bookTableRes',views.tableRes,name='bookTableRes'),
    path('userTabReservation',views.userTabReser,name='userTabReservation'),
    path('userTableReservationDetails/<int:tab_id>',views.userTableReservationDetail,name='userTableReservationDetails'),
    path('cancelTableReservation',views.cancelTableReservation,name='cancelTableReservation'),
    path('adminPanel/',views.ProjectadminPanel,name='adminPanel'),
    path('Adminlogout/',views.AdminLogout,name='Adminlogout'),
    path('AdminAdd/',views.AddAdmin,name='AdminAdd'),
    path('adminProfile/',views.AdminProfile,name='adminProfile'),
    path('editCafeData/',views.EditCafeData,name='editCafeData'),
    path('UserAdminPanel/',views.UserAdminPanell,name='UserAdminPanel'),
    path('allAreaAdmin/',views.allAreaAdminPanel,name='allAreaAdmin'),
    path('allAreaAdmin/<int:pincode>/',views.allAreaAdminPanelUpdate,name='allAreaAdminUpdate'),
    path('allAreaAdmin/<int:pincode>/delete/',views.allAreaAdminPanelDelete,name='allAreaAdminDelete'),
    path('allOrderAdmin/',views.allOrderAdminPanel,name='allOrderAdmin'),
    path('allOrderAdmin/<int:idorder>/',views.allOrderAdminPanelUpdate,name='allOrderAdminUpdate'),
    path('allCancelOrderAdmin/',views.allCancelOrderAdmin,name='allCancelOrderAdmin'),
    path('allItemCategoryAdmin/',views.allItemCategoryAdminPanel,name='allItemCategoryAdmin'),
    path('allItemCategoryAdminUpdate/<int:id_itemCat>/',views.allItemCategoryAdminPanelUpdate,name='allItemCategoryAdminUpdate'),
    path('allItemCategoryAdmin/<int:id_itemCat>/delete/',views.allItemCategoryAdminPanelDelete,name='allItemCategoryAdminDelete'),
    path('allItemAdmin/',views.allItemAdminPanel,name='allItemAdmin'),
    path('allItemAdminUpdate/<int:id_item>/',views.allItemAdminPanelUpdate,name='allItemAdminUpdate'),
    path('allItemAdmin/<int:id_item>/delete/',views.allItemAdminPanelDelete,name='allItemAdminDelete'),
    path('allOfferAdmin/',views.allOfferAdminPanel,name='allOfferAdmin'),
    path('allOfferAdminUpdate/<int:id_itemOfferId>/',views.allOfferAdminPanelUpdate,name='allOfferAdminUpdate'),
    path('allOfferAdmin/<int:id_itemOfferId>/delete/',views.allOfferAdminPanelDelete,name='allOfferAdminDelete'),
    path('allTableReservationAdmin/',views.allTableReservationAdminPanel,name='allTableReservationAdmin'),
    path('allCancelTableReservationAdmin/',views.allCancelTableReservationAdminPanel,name='allCancelTableReservationAdmin'),
    path('tableDetailsAdminPanel/',views.tableDetailsAdminPanell,name='tableDetailsAdminPanel'),
    path('tableDetailsAdminPanelUpdate/<int:id_table>/',views.tableDetailsAdminPanellUpdate,name='tableDetailsAdminPanelUpdate'),
    path('notificationAdmin/',views.notificationAdminPanel,name='notificationAdmin'),
    path('notificationAdminUpdate/<int:id_notification>/',views.notificationAdminPanelUpdate,name='notificationAdminUpdate'),
    path('notificationAdmin/<int:id_notification>/delete/',views.notificationAdminPanelDelete,name='notificationAdminDelete'),
    path('addAreaAdminPanel/',views.addAreaAdminPanel,name='addAreaAdminPanel'),
    path('addAreaAdminPanelData/',views.addAreaAdminPanelData1,name='addAreaAdminPanelData'),
    path('addItemCatAdminPanel/',views.addItemCatAdminPanell,name='addItemCatAdminPanel'),
    path('addItemCatAdminPanelData/',views.addItemCatAdminPanellData,name='addItemCatAdminPanelData'),
    path('addItemAdminPanel/',views.addItemAdminPanell,name='addItemAdminPanel'),
    path('addItemAdminPanelData/',views.addItemAdminPanellData,name='addItemAdminPanelData'),
    path('addOfferAdminPanel/',views.addOfferAdminPanell,name='addOfferAdminPanel'),
    path('addOfferAdminPanelData/',views.addOfferAdminPanellData,name='addOfferAdminPanelData'),
    path('addNotificationAdminPanel/',views.addNotificationAdminPanell,name='addNotificationAdminPanel'),
    path('addNotificationAdminPanelData/',views.addNotificationAdminPanellData,name='addNotificationAdminPanelData'),
    path('allOrderedItemAdmin/',views.allOrderedItemAdminPanel,name='allOrderedItemAdmin'),
    path('allSupplierAdmin/',views.allSupplierAdminPanel,name='allSupplierAdmin'),
    path('supplierAdminPanelUpdate/<int:id_supplier>/',views.supplierAdminPanelUpdate1,name='supplierAdminPanelUpdate'),
    path('allSupplierAdmin/<int:id_supplier>/delete/',views.supplierAdminPanelDelete1,name='supplierAdminDelete'),
    path('addSupplierAdmin/',views.addSupplierAdminPanel,name='addSupplierAdmin'),
    path('addSupplierAdminData/',views.addSupplierAdminData1,name='addSupplierAdminData'),
    path('addPurchaseRawMaterialAdmin/',views.addPurchaseRawMaterialAdminPanel,name='addPurchaseRawMaterialAdmin'),
    path('addPurchaseRawMaterialAdminData/',views.addPurchaseRawMaterialAdminData1,name='addPurchaseRawMaterialAdminData'),
    path('allPurchaseRawMaterialAdmin/',views.allPurchaseRawMaterialAdminPanel,name='allPurchaseRawMaterialAdmin'),
    path('purchaseRawMaterialDataUpdate/<int:id_rawmaterial>/',views.purchaseRawMaterialDataUpdateAdminPanel,name='purchaseRawMaterialDataUpdate'),
    path('purchaseRawMaterialDataReturn/<int:id_rawmaterial>/',views.purchaseRawMaterialDataReturnAdminPanel,name='purchaseRawMaterialDataReturn'),
    path('allRawMaterialAdmin/',views.allRawMaterialAdminPanel,name='allRawMaterialAdmin'),
    path('allRawMaterialAdmin/<int:id_rawmat>/',views.allRawMaterialAdminPanelUpdate,name='allRawMaterialAdmin'),
    path('allPurchaseAdmin/',views.allPurchaseAdminPanel,name='allPurchaseAdmin'),
    path('allPurchaseReturnAdmin/',views.allPurchaseReturnAdminPanel,name='allPurchaseReturnAdmin'),
    path('allPurchaseRawMaterialReturn/',views.allPurchaseRawMaterialReturnAdminPanel,name='allPurchaseRawMaterialReturn'),
    path('ajax/load_tables/',views.load_tables,name='ajax_load_tables'),
    path('orderInvoice/<str:t_no>/',orderInvoicePdf.as_view(),name='orderInvoice'),

    path('brewerReportOrder/',views.reportBrewerOrderAdmin,name='brewerReportOrder'),
    path('brewerReportOrder/orderResult/',views.orderReport,name='orderReport'),
    path('orderReportGenerate/report/',orderReportGenerateAdmin.as_view(),name='orderReportGenerate'),
    path('brewerReportOrderCancel/',views.brewerCancelOrder,name='brewerReportOrderCancel'),
    path('brewerReportOrderCancel/orderResult/',views.orderCancelReportAdmin,name='orderCancelReport'),
    path('cancelOrderReportGenerate/report/',cancelOrderReportGenerateAdmin.as_view(),name='cancelOrderReportGenerate'),
    path('brewerReportOffer/',views.brewerOffer,name='brewerReportOffer'),
    path('brewerReportOffer/orderResult/',views.offerReportAdmin,name='orderOfferReport'),
    path('offerReportGenerateAdminPanel/report/',offerReportGenerateAdmin.as_view(),name='offerReportGenerateAdminPanel'),
    path('brewerReportPurchase/',views.brewerPurchase,name='brewerReportPurchase'),
    path('brewerReportPurchase/orderResult/',views.purchaseReportAdmin,name='purchaseReport'),
    path('purchaseReportGenerateAdminPanel/report/',purchaseReportGenerateAdmin.as_view(),name='purchaseReportGenerateAdminPanel'),
    path('brewerReportPurchaseReturn/',views.brewerPurchaseReturn,name='brewerReportPurchaseReturn'),
    path('brewerReportPurchaseReturn/orderResult/',views.purchaseReturnReportAdmin,name='purchaseReturnReport'),
    path('purchaseReturnReportGenerateAdminPanel/report/',purchaseReturnReportGenerateAdmin.as_view(),name='purchaseReturnReportGenerateAdminPanel'),
]

handler404 = 'Brewer_Cafe_And_Restro.views.error_404_view'