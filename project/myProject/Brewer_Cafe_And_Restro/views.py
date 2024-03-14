from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from .models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.db.models import Q
from datetime import date,datetime
from django.core.paginator import Paginator
import uuid
import re
import random

from .process import html_to_pdf
from django.template.loader import render_to_string
from django.views.generic import View

# Create your custom function here.

orderPlacedMinutes = None

def isFirstThreeCharacterLetter(subUname):
    count = 0

    firstThreeCh = subUname[0:3]

    for i in firstThreeCh:
        if((i >= "A" and i <= "Z") or (i >= "a" and i <= "z")):
            count += 1
        else:
            break
    
    return count


def isStringContainsNumberOrNot(puserFirstName):
    flag = 1

    for i in puserFirstName:
        if((i >= "A" and i <= "Z") or (i >= "a" and i <= "z") or (i == " ")):
            flag = 0
        else:
            flag = 1
            break
    
    if(flag == 1):
        return True
    else:
        pass

def isContainSpace(uName,character):
    res = None
    for i in range(0, len(uName)):
        if uName[i] == character:
            res = i + 1
            break
    
    if res == None:
        pass
    else:
        return True


def userNameValidation(uName):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_name == uName):
            error_message = "Username already taken!"
            break

    return error_message

def userEmailValidation(uEmail):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_email == uEmail):
            error_message = "Email ID already taken!"
            break

    return error_message

def userMobileValidation(uMobile):
    error_message = None
    u4 = User.objects.all()
    for i in u4:
        if(i.user_mobile == uMobile):
            error_message = "Mobileno already taken!"
            break

    return error_message

def userImageValidation(puserImage):
    error_message = None
    userImage = str(puserImage)

    if(not(userImage.lower().endswith(('.png','.jpg','.jpeg')))):
        error_message = "Choose only image!"

    return error_message

def validationForgotPassword(userEmail,myUserEmail):
    error_message = None
    if(not userEmail):
        error_message = "Please enter email!"
    elif userEmail:
        if(userEmail != myUserEmail):
            error_message = "Please enter valid email"
    
    return error_message

def validationChangePassword(userNewPassword,userNewSamePassword):
    error_message = None
    
    if(not userNewPassword):
        error_message = "Please enter new password.!"
    elif(userNewPassword):
        if(len(userNewPassword) < 6 or len(userNewPassword) > 15):
            error_message = "Your new password at least 6 character long and not greater than 15 character!"
        elif(userNewPassword != userNewSamePassword):
            error_message = "Your new password and new same password didn't match!"            
    
    return error_message

def validationChangePasswordDirectly(userCurPassword,userNewPassword,userNewSamePassword,flag):
    error_message = None
    if(not userCurPassword):
        error_message = "Please enter current password!"
    elif userCurPassword:
        if not flag:
            error_message = "Your current password is invalid.!"
        elif(not userNewPassword):
            error_message = "Please enter your new password!"
        elif userNewPassword:
            if(len(userNewPassword) < 6 or len(userNewPassword) > 15):
                error_message = "Your new password at least 6 character long and not greater than 15 character!"
            elif(userNewPassword != userNewSamePassword):
                error_message = "Your new password and new same password didn't match!"            
    
    return error_message


def validationUserProfile(puserName,puserEmail,puserMobile,puserFirstName,puserLastName,count):
    regxEmail = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    regxMobile = re.compile("(0|91)?[-\s]?[6-9][0-9]{9}")
    error_message = None
    mycharacter = " "

    if(not puserName):
        error_message = "Username is must!"
    elif(puserName):
        if (len(puserName) < 6 or len(puserName) > 15):
            error_message = "Username atleast 6 character long and maximum 15 character!"
        elif (isContainSpace(puserName,mycharacter)):
            error_message = "Username does not contain space!"
        elif (count < 3):
            error_message = "First three character of username must be in letter!"
        elif (not puserEmail):
            error_message = "Email is required!"
        elif puserEmail:
            if(not(re.fullmatch(regxEmail,puserEmail))):
                error_message = "Invalid email!"
            elif(not puserFirstName):
                pass
            elif puserFirstName:
                if(isStringContainsNumberOrNot(puserFirstName)):
                    error_message = "First name not contains number or special character!"
                elif(not puserMobile):
                    error_message = "Mobile no required!"
                elif(puserMobile):
                    if(len(puserMobile) > 10):
                        error_message = "Enter valid mobile no!"
                    elif(not(re.fullmatch(regxMobile,puserMobile))):
                        error_message = "Enter valid mobile"
                    elif(not puserLastName):
                        pass
                    elif(puserLastName):
                        if(isStringContainsNumberOrNot(puserLastName)):
                            error_message = "Last name not contains number or special character!"
    
    return error_message


def validationLogin(username,password,username1,flag):
    error_message = None
    if(not username):
        error_message = "Please enter username!"
    elif username:
            if not password:
                error_message = "Please enter password!"
            elif(username != username1):
                error_message = "Invalid username or password!"
            elif not flag:
                error_message = "Invalid username or password!"

    return error_message


# Create your views here.

def home(request):
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        object_list = Item.objects.all()
        
        param = {'current_user':current_user,'object_list':object_list}
        return render(request,'home.html',param)
    elif 'admin' in request.session:
        current_user = request.session['admin']
        param = {'current_admin':current_user}
        return render(request,'home.html',param)
    object_list = Item.objects.all()
    
    return render(request, 'home.html')

def error_404_view(request,exception):
    return render(request,'404.html')

def loginAction(request):
    if 'user_name' in request.session:
        messages.error(request,'You are already logged in!')
        return redirect('home')
    elif 'admin' in request.session:
        messages.error(request,'You are already logged in!')
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username1')
            password = request.POST.get('password1')
            error_message = None
            flag = None
            is_admin = 0
            username1 = None
            c1 = User.objects.all()
            for item in c1:
                if(username == item.user_name):
                    username1 = item.user_name
                    is_admin = 0
                    flag = check_password(password,item.user_password)
                    if(item.is_admin == 1):
                        is_admin = 1
            value={
                'uname':username
            }
        
            error_message = validationLogin(username,password,username1,flag)

            if not error_message:
                if(is_admin == 1):
                    request.session['admin'] = username
                    messages.success(request,'Login successfully!')
                    return redirect('home')
                else:
                    request.session['user_name'] = username
                    messages.success(request,'Login successfully!')
                    return redirect('home')

            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }
                return render(request, 'login.html',data)

        return render(request, 'login.html')


def goHomePage(request):
    return render(request, 'home.html')

def validation(userName,userPassword,userConfirmPassword,userEmail,userMobile,user,count,myCharacter):
    regxEmail = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    regxMobile = re.compile("(0|91)?[-\s]?[6-9][0-9]{9}")
    error_message = None
    if(not userName):
        error_message = "Username is required!"
    elif userName:
        isUserNameExistOrNot = user.isUserExists()
        if (len(userName) < 6 or len(userName) > 15):
            error_message = "Username atleast 6 character long and maximum 15 character!"
        elif (isContainSpace(userName,myCharacter)):
            error_message = "Username does not contain space!"
        elif (count < 3):
            error_message = "First three character of username must be in letter!"
        elif (isUserNameExistOrNot):
            error_message = "Username already taken.!"
        elif (not userEmail):
            error_message = "Email is required!"
        elif userEmail:
            isEmailExistOrNot = user.isEmailExists()
            if(isEmailExistOrNot):
                error_message = "Email already taken!"
            elif(not(re.fullmatch(regxEmail,userEmail))):
                error_message = "Invalid email!"
            elif (not userPassword):
                error_message = "Password is required.!"
            elif userPassword:
                if (len(userPassword) < 6 or len(userPassword) > 15):
                        error_message = "Password atleast 6 character long and maximum 15 character!"
                elif (userPassword != userConfirmPassword):
                        error_message = "Password and confirm password must be same!"
                elif(not userMobile):
                    error_message = "Mobile no is required!"
                elif userMobile:
                    isMobileExistOrNot = user.isMobileNoExists()
                    if(isMobileExistOrNot):
                        error_message = "Mobile no already taken!"
                    elif(len(userMobile) > 10):
                        error_message = "Enter valid mobile no!" 
                    elif(not(re.fullmatch(regxMobile,userMobile))):
                        error_message = "Enter valid mobile no"
    
    return error_message
        


def goSignUpPage(request):
    if 'user_name' in request.session:
        messages.error(request,'You are already registered!')
        return redirect('home')
        
    else: 
        if request.method == 'POST':
            postData = request.POST
            userName = postData.get('userName')
            userPassword = postData.get('userPassword')
            userConfirmPassword = postData.get('userConfirmPassword')
            userEmail = postData.get('userEmail')
            userMobile = postData.get('userMobileNo')
            userSecQue = postData.get('userSecQue')
            userSecAns = postData.get('userSecAns')
            firstArea = Area.objects.first()
            myCharacter = " "

            count = isFirstThreeCharacterLetter(userName)

            #validation

            error_message = None

            value = {
                'uName':userName,
                'uEmail':userEmail,
                'uMobile':userMobile
            }

            user = User(user_name=userName,
                            user_password=userPassword,
                            user_email=userEmail,
                            user_mobile=userMobile,
                            user_sec_question=userSecQue,
                            user_sec_answer=userSecAns,
                            is_admin=0,
                            # pincode=Area.objects.get(pincode=firstArea.pincode),
                            # idrestaurant=Restaurant.objects.get(idrestaurant=1)
                            )
        
            error_message = validation(userName,userPassword,userConfirmPassword,userEmail,userMobile,user,count,myCharacter)

            if not error_message: 
                user.user_password = make_password(user.user_password)
                user.register()
                request.session['user_name'] = userName
                messages.success(request,'Registration done successfully!')
                return redirect('home')
        
            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }
                return render(request, 'signup.html',data)

        return render(request, 'signup.html')


def logout(request):
    if 'user_name' in request.session:
        del request.session['user_name']
        messages.success(request,'Logout successfully!')
    else:
        messages.error(request,'You are not logged in!')
    return redirect('home')

def AdminLogout(request):
    if 'admin' in request.session:
        del request.session['admin']
        messages.success(request,'Logout successfully!')
    else:
        messages.error(request,'You are not logged in!')
    return redirect('home')

def forgot_password(request):
    if 'user_name' in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        if request.method == "POST":
            userEmail = request.POST.get('uEmail')
            myUserEmail = userEmail
            error_message = None
            success_message = None
            token = str(uuid.uuid4())

            c1 = User.objects.all()

            for item in c1:
                if(item.user_email == userEmail):
                    myUserEmail = item.user_email
                    User.objects.filter(user_email = userEmail).update(forgot_password_token = token)
                    break
        
            value = {
                'email':userEmail
            }
            error_message = validationForgotPassword(userEmail,myUserEmail)

            if not error_message:
                success_message = "Your password reset link is sent to your email ID successfully!"
                subject = 'Welcome to brewer cafe & restro'
                myMessage = f'Hello user, your password reset link is http://127.0.0.1:8000/change_password/{token}/:, thank you for visiting our site!'
                email_from = 'milanthesiya53@gmail.com'
                recipient_list = [myUserEmail,]
                data = {
                    'success' : success_message
                }
                send_mail(subject, myMessage, email_from, recipient_list)
                return render(request,'forgot_password.html',data)
        
            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }

                return render(request, 'forgot_password.html',data)


        return render(request,'forgot_password.html')

def change_password(request,token):
    if 'user_name' in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:  
        if request.method == "POST":
            userNewPassword = request.POST.get('userNewPassword')
            userSameNewPassword = request.POST.get('userSameNewPassword')
            error_message = None

            u1 = User.objects.get(forgot_password_token = token)

            error_message = validationChangePassword(userNewPassword,userSameNewPassword)

            if not error_message:
                u1.user_password = make_password(userNewPassword)
                u1.register()
                messages.success(request,'Password has been changed!')
                return redirect('home')
        
            else:
                data = {
                    'error' : error_message
                }

                return render(request,'change_password.html',data)

        return render(request,'change_password.html')

def directly_change_pass(request):
    if 'user_name' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        if request.method == "POST":
            userCurrentPassword = request.POST.get('userCurrentPassword')
            userNewPassword = request.POST.get('userNewPassword')
            userNewSamePassword = request.POST.get('userSameNewPassword')
            error_message = None
            flag = None

            current_user = request.session['user_name']

            u1 = User.objects.all()
            u2 = User.objects.get(user_name=current_user)

            for item in u1:
                if(item.user_name == current_user):
                    flag = check_password(userCurrentPassword,item.user_password)
                    break
        
            value = {
                'uCurPass':userCurrentPassword
            }

            error_message = validationChangePasswordDirectly(userCurrentPassword,userNewPassword,userNewSamePassword,flag)

            if not error_message:
                u2.user_password = make_password(userNewPassword)
                u2.register()
                messages.success(request,'Password has been changed!')
                return redirect('home')
        
            else:
                data = {
                    'error' : error_message,
                    'values' : value
                }

                return render(request,'directly_change_password.html',data)


        return render(request,'directly_change_password.html')

def user_profile(request):
    if 'user_name' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        u1 = User.objects.filter(user_name=request.session['user_name'])
        u3 = User.objects.get(user_name=request.session['user_name'])
        data = {
            'user1':u1
        }

        if request.method == "POST":
            puserName = request.POST.get('update_username')
            puserEmail = request.POST.get('update_email')
            puserMobile = request.POST.get('update_mobile')
            puserFirstName = request.POST.get('update_First_Name')
            puserLastName = request.POST.get('update_Last_Name')
            error_message = None
            error_message1 = None
            success_message = None
            count = isFirstThreeCharacterLetter(puserName)

            error_message = validationUserProfile(puserName,puserEmail,puserMobile,puserFirstName,puserLastName,count)

            if not error_message:
                success_message = "Profile updated successfully!"

                for i in u1:
                    if(i.user_name != puserName):
                        error_message1 = userNameValidation(puserName)
                        break
                    elif(i.user_email != puserEmail):
                        error_message1 = userEmailValidation(puserEmail)
                        break
                    elif(i.user_mobile != puserMobile):
                        error_message1 = userMobileValidation(puserMobile)
                        break
                    elif(len(request.FILES) != 0):
                        puserImage = request.FILES['update_image']
                        error_message1 = userImageValidation(puserImage)
                        break

                if not error_message1:
                    u3.user_name = puserName
                    u3.user_email = puserEmail
                    u3.user_first_name = puserFirstName
                    u3.user_mobile = puserMobile
                    u3.user_last_name = puserLastName
                    if(len(request.FILES) != 0):
                        u3.user_image = request.FILES['update_image']
                
                    u3.save()
                    request.session['user_name'] = puserName
                    u1 = User.objects.filter(user_name = request.session['user_name'])
                    data = {
                        'user1':u1,
                        'success':success_message
                    }

                    return render(request,'user_profile.html',data)

                else:
                    data = {
                        'user1':u1,
                        'error1':error_message1
                    }
                    return render(request,'user_profile.html',data)
            else:
                data = {
                    'user1':u1,
                    'error':error_message
                }

                return render(request,'user_profile.html',data) 

        return render(request,'user_profile.html',data)

class CategoryListView(ListView):
    model = ItemCategory
    template_name = 'itemcategory_list.html'
    queryset = ItemCategory.objects.all()

    def get_queryset(self):
        q = self.request.GET.get('q')
        if q:
            object_list = self.model.objects.filter(Q(item_category_name__icontains=q) | Q(item_category_description__icontains=q))
        else:
            object_list = self.model.objects.all()
        return object_list

class ItemListView(ListView):
    model = Item
    template_name = 'item.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getCategory = ItemCategory.objects.get(slug=self.kwargs['slug_text'])
        if self.kwargs.get('slug_text'):
            object_list = Item.objects.filter(item_category_iditem_category=getCategory.iditem_category)
            if q:
                object_list = self.model.objects.filter((Q(item_name__icontains=q) | Q(item_description__icontains=q)),item_category_iditem_category=getCategory.iditem_category)
            else:
                object_list = Item.objects.filter(item_category_iditem_category=getCategory.iditem_category)

        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = ItemCategory.objects.get(slug=self.kwargs['slug_text'])
        return context

def ItemDetails(request,cat_slug,prod_slug):
    if 'user_name' in request.session:
        current_user = request.session['user_name']
        u1 = User.objects.get(user_name=request.session['user_name'])
        i1 = Item.objects.get(slug=prod_slug)
        itemId = i1.iditem
        r1 = Review.objects.filter(item_iditem=itemId)
        try:
            r2 = Review.objects.get(item_iditem=itemId,user_iduser=u1.iduser)
        except:
            r2 = None
            print("error!")
        param = {'current_user':current_user,'itemName':i1,'currentUserDetails':u1,'usersReview':r1,'currentUserReview':r2}
        return render(request,'itemDetails.html',param)
    else:
        if 'admin' in request.session:
            admin = request.session['admin']  
        else:
            admin = None
        try:
            current_user = request.session['user_name']
            u1 = User.objects.get(user_name=request.session['user_name'])
        except:
            current_user = None
            u1 = None
        i1 = Item.objects.get(slug=prod_slug)
        itemId = i1.iditem
        r1 = Review.objects.filter(item_iditem=itemId)
        try:
            r2 = Review.objects.get(item_iditem=itemId,user_iduser=u1.iduser)
        except:
            r2 = None
            print("error!")
        param = {'current_user':current_user,'itemName':i1,'currentUserDetails':u1,'usersReview':r1,'currentUserReview':r2,'admin':admin}
        return render(request,'itemDetails.html',param)

def addtocart(request):
    if request.method == "POST":
        if 'user_name' in request.session:
            u1 = User.objects.get(user_name=request.session['user_name'])
            userId = u1.iduser
            item_id = int(request.POST.get('item_id'))
            itemCheck = Item.objects.get(iditem=item_id)
            if(itemCheck.offer_idoffer):
                if(Cart.objects.filter(user_iduser=u1.iduser,item_iditem=item_id)):
                    item_qty = int(request.POST.get('item_qty'))
                    cartQty = Cart.objects.get(user_iduser=u1.iduser,item_iditem=item_id)
                    cartQty.item_qty = cartQty.item_qty + item_qty
                    cartQty.save()
                    return JsonResponse({'status':"Quantity updated!"})
                else:
                    item_qty = int(request.POST.get('item_qty'))
                    userCart = Cart.objects.create(user_iduser=User.objects.get(iduser=userId),item_iditem=Item.objects.get(iditem=item_id),offer_record=0,item_qty=item_qty)
                    userCart.save()
                    return JsonResponse({'status':"Item added successfully with offer!"})
            elif(not itemCheck.offer_idoffer):
                if(Cart.objects.filter(user_iduser=u1.iduser,item_iditem=item_id)):
                    item_qty = int(request.POST.get('item_qty'))
                    cartQty = Cart.objects.get(user_iduser=u1.iduser,item_iditem=item_id)
                    cartQty.item_qty = cartQty.item_qty + item_qty
                    cartQty.save()
                    return JsonResponse({'status':"Quantity updated!"})
                else:
                    item_qty = int(request.POST.get('item_qty'))
                    userCart = Cart.objects.create(user_iduser=User.objects.get(iduser=userId),item_iditem=Item.objects.get(iditem=item_id),item_qty=item_qty)
                    userCart.save()
                    return JsonResponse({'status':"Item added successfully"})
            else:
                return JsonResponse({'data':"No such item found!"})
        elif 'admin' in request.session:
            return JsonResponse({'data':"Can't Add to Cart!"})
        else:
            return JsonResponse({'data':"Login to continue!"})
    return redirect('home')

def userCart(request): 
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    cart1 = Cart.objects.filter(user_iduser=userId)
    data = {
        'userCart':cart1
    }
    if 'user_name' not in request.session:
        messages.error(request,'Login to continue!')
        return redirect('home')
    return render(request,'cart.html',data)

def updatecart(request):
    if request.method == "POST":
        item_id = int(request.POST.get('item_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(Cart.objects.filter(user_iduser=userId, item_iditem=item_id)):
            item_qty = int(request.POST.get('item_qty'))
            cart = Cart.objects.get(item_iditem=item_id,user_iduser=userId)
            cart.item_qty = item_qty
            cart.save()
            return JsonResponse({'status':"Cart updated successfully"})
    return redirect('home')

def deletecartitem(request):
    if request.method == "POST":
        item_id = int(request.POST.get('item_id'))
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        if(Cart.objects.filter(user_iduser=userId, item_iditem=item_id)):
            cartitem = Cart.objects.get(item_iditem=item_id,user_iduser=userId)
            cartitem.delete()
        return JsonResponse({'status':"Item removed from cart!"})
    return redirect('home')

def checkout(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    c1 = City.objects.all()
    a1 = Area.objects.all()
    a2 = Area.objects.get(pincode=u1.pincode.pincode)
    delcharges = a2.area_delivery_charges
    userId = u1.iduser
    cartitems = Cart.objects.filter(user_iduser=userId)
    cartOfferItem = Cart.objects.filter(user_iduser=userId,offer_record=0)
    grand_total = 0
    total_offer_price = 0
    total_price = 0
    for i in cartOfferItem:
        total_offer_price = total_offer_price + i.item_iditem.offer_price * i.item_qty
    
    for item in cartitems:
        total_price = total_price + (item.item_iditem.item_price * item.item_qty)

    grand_total = (total_price) - total_offer_price  
    context = {'cartitems':cartitems,'total_price':total_price, 'city':c1, 'area':a1,'current_user':u1,'delArea':delcharges,'offerPrice':total_offer_price,'grandTotal':grand_total}
    return render(request,'checkout.html',context)

def changecharges(request):
    if request.method == "POST":
        areaname = request.POST.get('areaname')
        a1 = Area.objects.get(area_name=areaname)
        return JsonResponse({'status':a1.area_delivery_charges})
    return redirect('home')

def placeorder(request):
    if request.method == "POST":
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        neworder = Order()
        neworder.user_iduser = User.objects.get(iduser=userId)
        neworder.orderfname = request.POST.get('fname')
        neworder.orderlname = request.POST.get('lname')
        neworder.orderemail = request.POST.get('email')
        neworder.ordermobile = request.POST.get('mobile')
        neworder.order_delivery_address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        a1 = Area.objects.get(area_name=request.POST['area1'])
        neworder.area_pincode = Area.objects.get(pincode=a1.pincode)
        neworder.order_payment_method = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        userpincode = request.POST.get('pincode')

        cart = Cart.objects.filter(user_iduser=userId)
        cartOfferItem = Cart.objects.filter(user_iduser=userId,offer_record=0)
        total_offer_price = 0
        for i in cartOfferItem:
            total_offer_price = total_offer_price + i.item_iditem.offer_price * i.item_qty
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + (item.item_iditem.item_price * item.item_qty)

        cart_total_price = (cart_total_price - total_offer_price)
        neworder.total_amount = cart_total_price + a1.area_delivery_charges
        trackno = 'brewer'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'brewer'+str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno

        currentDateTime2 = datetime.now()
        neworder.created_at = datetime(currentDateTime2.year,currentDateTime2.month,currentDateTime2.day,currentDateTime2.hour,currentDateTime2.minute,currentDateTime2.second)
        neworder.save()

        neworderitem = Cart.objects.filter(user_iduser=userId)
        for item in neworderitem:
            OrderedItem.objects.create(
                order_idorder = neworder,
                item_iditem = item.item_iditem,
                price = item.item_iditem.item_price,
                quantity = item.item_qty
            )

        Cart.objects.filter(user_iduser=userId).delete()
        u1.user_address = neworder.order_delivery_address
        u1.pincode = neworder.area_pincode
        u1.save()

        payMode = request.POST.get('payment_mode')
        if(payMode == "Paid by Razorpay" or payMode == "paid by paypal"):
            return JsonResponse({'status':"Your order has been placed successfully!"})
        else:
            messages.success(request,"Your order has been placed successfully!")
    
    return redirect('home')

def razorPayProcess(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    cart = Cart.objects.filter(user_iduser=userId)
    total_price = 0
    for item in cart:
        total_price = total_price + item.item_iditem.item_price * item.item_qty
    
    return JsonResponse({
        'total_price':total_price
    })

def orderpage(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    orders = Order.objects.filter(user_iduser=userId)
    context = {'userOrderData':orders}
    return render(request,'user_order.html',context)

def orderdetailspage(request,t_no):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    order = Order.objects.filter(tracking_no=t_no).filter(user_iduser=userId).first()
    orderitems = OrderedItem.objects.filter(order_idorder=order)
    context = {'userOrderData':order,'userOrderDetails':orderitems}
    return render(request,'userOrderDetails.html',context)


#-------------
def cancelOrder1(request,t_no):
    u1 = User.objects.get(user_name=request.session['user_name'])
    userId = u1.iduser
    order = Order.objects.filter(tracking_no=t_no).filter(user_iduser=userId).first()
    order.order_status = "Cancelled by Customer"
    order.save()
    orderitems = OrderedItem.objects.filter(order_idorder=order)
    context = {'userOrderData':order,'userOrderDetails':orderitems}
    return render(request,'userOrderDetails.html',context)


def reviewsubmit(request,item_id):
    url = request.META.get('HTTP_REFERER')
    if 'user_name' in request.session:
        u1 = User.objects.get(user_name=request.session['user_name'])
        userId = u1.iduser
        try:
            if(Review.objects.get(user_iduser=userId,item_iditem=item_id)):
                r1 = Review.objects.get(user_iduser=userId,item_iditem=item_id)
                ratingValue = request.POST.get('rating')
                if(not ratingValue):
                    r1.rating_value = 0
                else:
                    r1.rating_value = request.POST.get('rating')
                r1.subject = request.POST.get('subject')
                r1.review_description = request.POST.get('review')
                r1.reviewDate = date.today()
                r1.save()
                messages.success(request,'Review updated successfully!')
                return redirect(url)
        except:
            if request.method == "POST":
                userReview = Review()
                ratingValue = request.POST.get('rating')
                if(not ratingValue):
                    userReview.rating_value = 0
                else:
                    userReview.rating_value = request.POST.get('rating')
                userReview.subject = request.POST.get('subject')
                userReview.review_description = request.POST.get('review')

                userReview.user_iduser = User.objects.get(iduser=u1.iduser)
                userReview.item_iditem = Item.objects.get(iditem=item_id)
                userReview.reviewDate = date.today()
                userReview.save()
                messages.success(request,'Review added successfully!')
            return redirect(url)
    else:
        messages.error(request,'Login to continue!')
        return redirect(url)

def offer(request):
    current_user = request.session['user_name']
    current_date = date.today()
    allItems = Item.objects.filter(offer_idoffer__isnull=False)
    for i in allItems:
        i.offer_price = (i.item_price * i.offer_idoffer.offer_value) / 100
        i.save()
        
        if(i.offer_idoffer.offer_end_date < date.today()):
            getOffer = Offer.objects.get(idoffer=i.offer_idoffer.idoffer)
            getOffer.delete()
    
    print(current_date)
    
    param = {'current_user':current_user,'allItem':allItems,'currentDate':current_date}
    return render(request,'offer.html',param)

def orderCancel(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        userOrder = Order.objects.get(tracking_no=order_id)
        currentDateTime1 = datetime.now()
        a = datetime(currentDateTime1.year,currentDateTime1.month,currentDateTime1.day,currentDateTime1.hour,currentDateTime1.minute,currentDateTime1.second)
        b = datetime(userOrder.created_at.year,userOrder.created_at.month,userOrder.created_at.day,userOrder.created_at.hour,userOrder.created_at.minute,userOrder.created_at.second)
        c = a - b
        totalMinutes = int(c.total_seconds() / 60)
        if(totalMinutes > 5):
            return JsonResponse({'data':"You Can't Cancel Order After 5 Minutes of Placing Order!"})
        else:
            if(userOrder.order_payment_method == "COD"):
                userOrder.is_cancel_order = 1
                userOrder.cancel_order_date = datetime.now()
                orderedItemDelete = OrderedItem.objects.get(order_idorder=userOrder.idorder)
                orderedItemDelete.delete()
                userOrder.save()
                return JsonResponse({'status':"Order Cancel successfully!"})
    return redirect('home')

def userNotifications(request):
    try:
        currentUser = User.objects.get(user_name=request.session['user_name'])
    except:
        print("error!")
    notificationsOfCurrentUser = Notification.objects.all()
    data = {'userNotifications':notificationsOfCurrentUser,'current_user':currentUser}
    return render(request,'userNotification.html',data)    

def bookTable(request):
    if 'user_name' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        u1 = User.objects.get(user_name=request.session['user_name'])
        totalGuestNum = TotalGuest.objects.all()
        data = {'current_user':u1,'totalGuestNum':totalGuestNum}
        return render(request,'book-table.html',data)   

def load_tables(request):
    guestId = request.GET.get('guestId')
    totalCapacity = 0
    tablesData = Table.objects.all()
    for i in tablesData:
        totalCapacity = totalCapacity + i.table_capacity
    if(totalCapacity < int(guestId)):
        tablesData = Table.objects.none()
    elif(totalCapacity >= int(guestId)):
        tablesData = Table.objects.all()
    totalTable = Table.objects.filter(table_capacity=guestId).count()
    return render(request,'tables_dropdown_list.html',{'tables':tablesData,'totalTable':totalTable})

def findTotalCost(usertotaltable,usertotalguest):
    totalCost = None
    if((int(usertotaltable) * 4) != int(usertotalguest)):
        if((int(usertotaltable) * 4) > int(usertotalguest)):
            totalNonePayable = (int(usertotaltable) * 4) - int(usertotalguest);
            tmp = (int(usertotaltable) * 4) - totalNonePayable;
            totalCost = tmp * 100;
        elif((int(usertotaltable) * 4) < int(usertotalguest)):
            totalNonePayable = int(usertotalguest) - (int(usertotaltable) * 4);
            tmp = int(usertotalguest) - totalNonePayable;
            totalCost = tmp * 100;
        elif((int(usertotaltable) * 4) == int(usertotalguest)):
            totalCost = int(usertotalguest) * 100
    
    return totalCost

def tableRes(request):
    if 'user_name' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        if request.method == "POST":
            u1 = User.objects.get(user_name=request.session['user_name'])
            tableDetailsSecond = Table.objects.first()
            currentDateTime1 = datetime.now()
            currentDateTime1str = currentDateTime1.strftime('%Y-%m-%d %I:%M')
            userfirstname = request.POST.get('fname')
            userlastname = request.POST.get('lname')
            useremail = request.POST.get('mobile')
            usermobile = request.POST.get('email')
            usertotalguest = request.POST.get('totalGuest')
            usertotaltable = request.POST.get('totalTable')
            tableResDate = request.POST.get('tableResDate')
            payment_mode = request.POST.get('payment_mode')
            totalCost = None
            # specialCharacter = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            if(int(usertotalguest) == 0 or int(usertotaltable) == 0):
                messages.error(request,"Total guest or table can not be zero!")
                return redirect('book-table')
            elif(tableResDate):
                tableResDate2 = datetime.strptime(tableResDate, '%Y-%m-%dT%H:%M')
                tableResDate3 = tableResDate2.strftime('%Y-%m-%d %I:%M')
                currentDateTime2 = datetime.strptime(currentDateTime1str, '%Y-%m-%d %I:%M')
                tableResDate1 = datetime.strptime(tableResDate3,'%Y-%m-%d %I:%M')
                currentDateTime3 = datetime(currentDateTime2.year,currentDateTime2.month,currentDateTime2.day,currentDateTime2.hour,currentDateTime2.minute,currentDateTime2.second)
                tableResDate4 = datetime(tableResDate1.year,tableResDate1.month,tableResDate1.day,tableResDate1.hour,tableResDate1.minute,tableResDate1.second)

                if(currentDateTime3 > tableResDate4):
                    messages.error(request,"Invalid date!")
                    return redirect('book-table')
            else:
                pass
        
            totalCost = findTotalCost(usertotaltable,usertotalguest)
        
            newTableRes = TableReservation()
            newTableRes.user_iduser = User.objects.get(iduser=u1.iduser)
            newTableRes.tableResfname = userfirstname
            newTableRes.tableReslname = userlastname
            newTableRes.tableResemail = useremail
            newTableRes.tableResmobile = usermobile
            newTableRes.table_reservation_no_guest = usertotalguest
            newTableRes.table_reservation_total_table_reserved = usertotaltable
            newTableRes.total_amount = totalCost
            newTableRes.tableRes_payment_method = payment_mode
            newTableRes.table_reservation_date_time = tableResDate4
            tableEmpty1 = tableEmpty1 - int(usertotaltable)
            tableDetailsSecond.table_total_empty_table = int(tableEmpty1)
            tableDetailsSecond.total_table_reserved = int(usertotaltable)
            tableDetailsSecond.save()
            newTableRes.save()

            TableReservationDetails.objects.create(
                    table_reservation_idtable_reservation = newTableRes,
                    table_idtable = Table.objects.get(idtable=tableDetailsSecond.idtable)
            )
        
            if(payment_mode == "Paid by Razorpay" or payment_mode == "paid by paypal"):
                return JsonResponse({'status':"Your order has been placed successfully!"})
            else:
                messages.success(request,"Your table booked successfully!")

        return redirect('home') 

def userTabReser(request):
    u1 = User.objects.get(user_name=request.session['user_name'])
    tableReservations = TableReservation.objects.filter(user_iduser=u1.iduser)
    context = {'tableReservations':tableReservations}
    return render(request,'userTableReservation.html',context)

def userTableReservationDetail(request,tab_id):
    u1 = User.objects.get(user_name=request.session['user_name'])
    tableReservationUserDeails = TableReservation.objects.filter(idtable_reservation=tab_id).filter(user_iduser=u1.iduser).first()
    context = {'tableReservationUserDeails':tableReservationUserDeails}
    return render(request,'userTableReservationDetails.html',context)

def cancelTableReservation(request):
    if request.method == "POST":
        tableDetails = Table.objects.first()
        table_reservation_id = request.POST.get('table_reservation_id')
        userTableReservation = TableReservation.objects.get(idtable_reservation=table_reservation_id)
        currentDateTime1 = datetime.now()
        currentTableResercationDate = userTableReservation.table_reservation_date_time
        tableResDate3 = currentTableResercationDate.strftime('%Y-%m-%d %I:%M')
        currentDateTime1str = currentDateTime1.strftime('%Y-%m-%d %I:%M')
        tableResDate1 = datetime.strptime(tableResDate3,'%Y-%m-%d %I:%M')
        currentDateTime2 = datetime.strptime(currentDateTime1str, '%Y-%m-%d %I:%M')
        currentDateTimeTableRes = datetime(currentDateTime2.year,currentDateTime2.month,currentDateTime2.day,currentDateTime2.hour,currentDateTime2.minute,currentDateTime2.second)
        tableReservationDate = datetime(tableResDate1.year,tableResDate1.month,tableResDate1.day,tableResDate1.hour,tableResDate1.minute,tableResDate1.second)
        
        if(currentDateTimeTableRes > tableReservationDate):
            return JsonResponse({'data':"You Can't Cancel Table Reservation!"})
        else:
            if(userTableReservation.tableRes_payment_method == "COD"):
                tableDetails.table_total_empty_table = int(tableDetails.table_total_empty_table) + int(userTableReservation.table_reservation_total_table_reserved)
                userTableReservation.is_table_reservation_cancel = 1
                tableDetails.save()
                userTableReservation.save()
                return JsonResponse({'status':"Table Reservation Cancel successfully!"})
    return redirect('home')

def ProjectadminPanel(request):
    if 'admin' not in request.session:
        messages.error(request,"Request denied!")
        return redirect('home')
    restrorant = Restaurant.objects.first()
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'restrorant':restrorant,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    return render(request,'adminPanel.html',data)



def AddAdmin(request):
    if request.method == 'POST':
        postData = request.POST
        userName = postData.get('userName')
        userPassword = postData.get('userPassword')
        userConfirmPassword = postData.get('userConfirmPassword')
        userEmail = postData.get('userEmail')
        userMobile = postData.get('userMobileNo')
        userSecQue = postData.get('userSecQue')
        userSecAns = postData.get('userSecAns')
        firstArea = Area.objects.first()
        myCharacter = " "

        count = isFirstThreeCharacterLetter(userName)

        #validation

        error_message = None

        value = {
                'uName':userName,
                'uEmail':userEmail,
                'uMobile':userMobile
        }

        user = User(user_name=userName,
                            user_password=userPassword,
                            user_email=userEmail,
                            user_mobile=userMobile,
                            user_sec_question=userSecQue,
                            user_sec_answer=userSecAns,
                            is_admin=1,
                            pincode=Area.objects.get(pincode=firstArea.pincode),
                            idrestaurant=Restaurant.objects.get(idrestaurant=1))
        
        error_message = validation(userName,userPassword,userConfirmPassword,userEmail,userMobile,user,count,myCharacter)

        if not error_message: 
            user.user_password = make_password(user.user_password)
            user.register()
            messages.success(request,'Registration done successfully!')
            return redirect('home')
        
        else:
            data = {
                'error' : error_message,
                'values' : value
            }
            return render(request, 'addAdmin.html',data)

    return render(request,'addAdmin.html')

def AdminProfile(request):
    if 'admin' not in request.session:
        messages.error(request,'You can not access the page!')
        return redirect('home')
    else:
        u1 = User.objects.filter(user_name=request.session['admin'])
        u3 = User.objects.get(user_name=request.session['admin'])
        data = {
            'user1':u1
        }

        if request.method == "POST":
            puserName = request.POST.get('update_username')
            puserEmail = request.POST.get('update_email')
            puserMobile = request.POST.get('update_mobile')
            puserFirstName = request.POST.get('update_First_Name')
            puserLastName = request.POST.get('update_Last_Name')
            error_message = None
            error_message1 = None
            success_message = None
            count = isFirstThreeCharacterLetter(puserName)

            error_message = validationUserProfile(puserName,puserEmail,puserMobile,puserFirstName,puserLastName,count)

            if not error_message:
                success_message = "Profile updated successfully!"

                for i in u1:
                    if(i.user_name != puserName):
                        error_message1 = userNameValidation(puserName)
                        break
                    elif(i.user_email != puserEmail):
                        error_message1 = userEmailValidation(puserEmail)
                        break
                    elif(i.user_mobile != puserMobile):
                        error_message1 = userMobileValidation(puserMobile)
                        break
                    elif(len(request.FILES) != 0):
                        puserImage = request.FILES['update_image']
                        error_message1 = userImageValidation(puserImage)
                        break

                if not error_message1:
                    u3.user_name = puserName
                    u3.user_email = puserEmail
                    u3.user_first_name = puserFirstName
                    u3.user_mobile = puserMobile
                    u3.user_last_name = puserLastName
                    if(len(request.FILES) != 0):
                        u3.user_image = request.FILES['update_image']
                
                    u3.save()
                    request.session['admin'] = puserName
                    u1 = User.objects.filter(user_name = request.session['admin'])
                    data = {
                        'user1':u1,
                        'success':success_message
                    }

                    return render(request,'adminProfile.html',data)

                else:
                    data = {
                        'user1':u1,
                        'error1':error_message1
                    }
                    return render(request,'adminProfile.html',data)
            else:
                data = {
                    'user1':u1,
                    'error':error_message
                }

                return render(request,'adminProfile.html',data) 

        return render(request,'adminProfile.html',data)

def EditCafeData(request):
    if request.method == "POST":
        cafeName = request.POST.get('cafeName')
        cafeEmail = request.POST.get('cafeEmail')
        cafeMobile = request.POST.get('cafeMobile')
        cafeDesc = request.POST.get('cafeDesc')
        cafeAddress = request.POST.get('cafeAddress')
        
        RestaurantData = Restaurant.objects.first()

        RestaurantData.restaurant_name = cafeName
        RestaurantData.restaurant_email = cafeEmail
        RestaurantData.restaurant_phone = cafeMobile
        RestaurantData.restaurant_description = cafeDesc
        RestaurantData.restaurant_address = cafeAddress

        if(len(request.FILES) != 0):
            cafeimage = request.FILES['cafeImage']
            cafeImage1 = str(cafeimage)
            if(not(cafeImage1.lower().endswith(('.png','.jpg','.jpeg')))):
                messages.error(request,'Choose only image!')
                return redirect('adminPanel')
            else:
                RestaurantData.restaurant_image = request.FILES['cafeImage']
            
        RestaurantData.save()
        messages.success(request,'Data updated!')
        return redirect('adminPanel')

    return render(request,'adminPanel.html')

def UserAdminPanell(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allUserDetails = User.objects.filter(is_admin=0).order_by('iduser')
    paginator = Paginator(allUserDetails,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allUserDetails':page_obj}
    return render(request,'userAdminPanel.html',data)

def allOrderedItemAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allOrderedItem = OrderedItem.objects.all().order_by('item_iditem')
    paginator = Paginator(allOrderedItem,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOrderedItem':page_obj}
    return render(request,'allOrderedItemAdmin.html',data)

def allAreaAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allAreaDetails = Area.objects.all().order_by('pincode')
    paginator = Paginator(allAreaDetails,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allAreaDetails':page_obj}
    return render(request,'allAreaAdminPanel.html',data)

def allAreaAdminPanelUpdate(request,pincode):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        areaPincode = request.POST.get('pincode')
        areaName = request.POST.get('areaName')
        areadek = request.POST.get('delCharges')
        
        if(Area.objects.filter(pincode = int(areaPincode)).exists()):
            areaDetails = Area.objects.get(pincode = int(areaPincode))
            areaDetails.pincode = areaPincode
            areaDetails.area_name = areaName
            areaDetails.area_delivery_charges = areadek
            areaDetails.save()
            messages.success(request,"Area Updated!")
            return redirect(url)
        else:
            messages.error(request,"Invalid Data")
            return redirect(url)

    return render(request,'allAreaAdminPanel.html')

def allAreaAdminPanelDelete(request,pincode):
    url = request.META.get('HTTP_REFERER')
    areaDelete = Area.objects.filter(pincode=pincode)
    areaDelete.delete()
    messages.success(request,"Area deleted!")
    return redirect(url)

def allOrderAdminPanelUpdate(request,idorder):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        orderstatus = request.POST.get('orderStatus')
        orderUpdate = Order.objects.get(idorder=idorder)
        orderUpdate.order_status = orderstatus
        orderUpdate.save()
        messages.success(request,"Order Updated!")
        return redirect(url)
    return render(request,'allOrderAdminPanel.html')

def allOrderAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allOrderDetails = Order.objects.filter(is_cancel_order=0).order_by('idorder')
    paginator = Paginator(allOrderDetails,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOrderDetails':page_obj}
    return render(request,'allOrderAdminPanel.html',data)

def allCancelOrderAdmin(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allCancelOrderDetails = Order.objects.filter(is_cancel_order=1).order_by('idorder')
    paginator = Paginator(allCancelOrderDetails,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allCancelOrderDetails':page_obj}
    return render(request,'allCancelOrderAdminPanel.html',data)

def allItemCategoryAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allItemCategory = ItemCategory.objects.all().order_by('iditem_category')
    paginator = Paginator(allItemCategory,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allItemCategory':page_obj}
    return render(request,'allItemCategoryAdminPanel.html',data)


def allItemCategoryAdminPanelUpdate(request,id_itemCat):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        catName = request.POST.get('catName')
        catDesc = request.POST.get('catDesc')

        itemCategoryData = ItemCategory.objects.get(iditem_category=id_itemCat)

        itemCategoryData.item_category_name = catName
        itemCategoryData.item_category_description = catDesc

        if(len(request.FILES) != 0):
            catimage = request.FILES['catImage']
            catImage1 = str(catimage)
            if(not(catImage1.lower().endswith(('.png','.jpg','.jpeg')))):
                messages.error(request,'Choose only image!')
                return redirect(url)
            itemCategoryData.item_category_image = request.FILES['catImage']
            
        itemCategoryData.save()
        messages.success(request,'Data updated!')
        return redirect(url)

    return render(request,'allItemCategoryAdminPanel.html')

def allItemCategoryAdminPanelDelete(request,id_itemCat):
    url = request.META.get('HTTP_REFERER')
    itemCatDelete = ItemCategory.objects.filter(iditem_category=id_itemCat)
    itemCatDelete.delete()
    messages.success(request,"Item category deleted!")
    return redirect(url)

def allItemAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allItem = Item.objects.all().order_by('iditem')
    allItemCategory = ItemCategory.objects.all()
    paginator = Paginator(allItem,8,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allItem':page_obj,'allItemCategory':allItemCategory}
    return render(request,'allItemAdminPanel.html',data)

def allItemAdminPanelUpdate(request,id_item):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        itemName = request.POST.get('itemName')
        itemPrice = request.POST.get('itemPrice')
        itemCat = request.POST.get('Catitem')
        itemDesc = request.POST.get('itemDesc')

        itemData = Item.objects.get(iditem=id_item)
        getCat = ItemCategory.objects.get(item_category_name=itemCat)
        getCatId = getCat.iditem_category

        itemData.item_name = itemName
        itemData.item_price = itemPrice
        itemData.item_category_iditem_category = ItemCategory.objects.get(iditem_category=getCatId)
        itemData.item_description = itemDesc

        if(len(request.FILES) != 0):
            itemimage = request.FILES['itemImage']
            itemImage1 = str(itemimage)
            if(not(itemImage1.lower().endswith(('.png','.jpg','.jpeg')))):
                messages.error(request,'Choose only image!')
                return redirect(url)
            itemData.item_image = request.FILES['itemImage']
            
        itemData.save()
        messages.success(request,'Data updated!')
        return redirect(url)

    return render(request,'allItemAdminPanel.html')

def allItemAdminPanelDelete(request,id_item):
    url = request.META.get('HTTP_REFERER')
    itemDelete = Item.objects.filter(iditem=id_item)
    itemDelete.delete()
    messages.success(request,"Item deleted!")
    return redirect(url)

def allOfferAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allItems = Item.objects.all()
    allOfferItems = Item.objects.filter(offer_idoffer__isnull=False).order_by('iditem')
    paginator = Paginator(allOfferItems,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOfferItems':page_obj,'allItems':allItems}
    return render(request,'offerAdminPanel.html',data)

def allOfferAdminPanelUpdate(request,id_itemOfferId):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        offerItemName = request.POST.get('Offeritem')
        offerStartDate = request.POST.get('offerstartDate')
        offerEndDate = request.POST.get('offerendDate')
        offerValue = request.POST.get('offerValue')
        offerDesc = request.POST.get('offerDesc')

        rmofferItemData = Item.objects.get(iditem=id_itemOfferId)
        offerId = Offer.objects.get(idoffer=rmofferItemData.offer_idoffer.idoffer)
        getNewItem = Item.objects.get(item_name=offerItemName)
        getNewItem.offer_idoffer = Offer.objects.get(idoffer=rmofferItemData.offer_idoffer.idoffer)
        rmofferItemData.offer_idoffer = None

        offerId.offer_value = offerValue
        offerId.offer_description = offerDesc
        
        offerStart = datetime.strptime(offerStartDate,'%Y-%m-%d')
        offerEnd = datetime.strptime(offerEndDate,'%Y-%m-%d')

        if(offerStart.date() < date.today()):
            messages.error(request,"Invalid Data!")
            return redirect(url)
        if(offerStart.date() > offerEnd.date()):
            messages.error(request,"Invalid Data!")
            return redirect(url)

        offerId.offer_start_date = offerStart.date()
        offerId.offer_end_date = offerEnd.date()

        getNewItem.save()
        offerId.save()
        rmofferItemData.save()

        messages.success(request,'Data updated!')
        return redirect(url)

    return render(request,'offerAdminPanel.html')

def allOfferAdminPanelDelete(request,id_itemOfferId):
    url = request.META.get('HTTP_REFERER')
    itemOfferDelete = Item.objects.get(iditem=id_itemOfferId)
    OfferDeleteData = Offer.objects.filter(idoffer=itemOfferDelete.offer_idoffer.idoffer)
    itemOfferDelete.offer_idoffer = None
    OfferDeleteData.delete()
    itemOfferDelete.save()
    messages.success(request,"Offer deleted!")
    return redirect(url)

def allTableReservationAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allTableReservationDetails = TableReservation.objects.filter(is_table_reservation_cancel=0).order_by('idtable_reservation')
    paginator = Paginator(allTableReservationDetails,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allTableReservationDetails':page_obj}
    return render(request,'tableReservationAdminPanel.html',data)

def allCancelTableReservationAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allCancelTableReservationDetails = TableReservation.objects.filter(is_table_reservation_cancel=1).order_by('idtable_reservation')
    paginator = Paginator(allCancelTableReservationDetails,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allCancelTableReservationDetails':page_obj}
    return render(request,'cancelTableReservationAdminPanel.html',data)

def tableDetailsAdminPanell(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    tableDetails = Table.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'tableDetails':tableDetails}
    return render(request,'tableAdminPanel.html',data)

def tableDetailsAdminPanellUpdate(request,id_table):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        totalTable = request.POST.get('totalTableData')
        tableData = Table.objects.first()
        tableData.total_table = int(totalTable)
        tableData.save()
        messages.success(request,"Table Data Updated!")
        return redirect(url)
    return render(request,'offerAdminPanel.html')

def allSupplierAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    supplier = Supplier.objects.all().order_by('idsupplier')
    paginator = Paginator(supplier,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'supplier':page_obj}
    return render(request,'allSupplierAdminPanel.html',data)

def supplierAdminPanelUpdate1(request,id_supplier):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        sName = request.POST.get('supplierName')
        sMobile = request.POST.get('supplierMobile')
        sAddress = request.POST.get('sAddress')
        sAreaName = request.POST.get('supplierAreaName')
        sPincode = request.POST.get('spincode')

        currentSupplierData = Supplier.objects.get(idsupplier=id_supplier)
        currentSupplierData.supplier_name = sName
        currentSupplierData.supplier_mobile_no = sMobile
        currentSupplierData.supplier_address = sAddress
        currentSupplierData.area_name = sAreaName
        currentSupplierData.pincode = sPincode
        currentSupplierData.save()
        messages.success(request,"Supplier Data Updated!")
        return redirect(url)
    return render(request,'allSupplierAdminPanel.html')

def supplierAdminPanelDelete1(request,id_supplier):
    url = request.META.get('HTTP_REFERER')
    supplierData = Supplier.objects.filter(idsupplier=id_supplier)
    supplierData.delete()
    messages.success(request,"Supplier deleted!")
    return redirect(url)

def addSupplierAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    areaData = Area.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'areaData':areaData}
    return render(request,'addSupplierAdminPanel.html',data)

def addSupplierAdminData1(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        sName = request.POST.get('supplierName')
        sMobile = request.POST.get('supplierMobile')
        sAddress = request.POST.get('sAddress')
        sAreaName = request.POST.get('sArea')
        restaurantData = Restaurant.objects.first()
        getArea = Area.objects.get(pincode=sAreaName) 

        supplierData = Supplier.objects.create(
            supplier_name = sName,
            supplier_mobile_no = sMobile,
            supplier_address = sAddress,
            area_name = getArea.area_name,
            pincode = getArea.pincode,
            restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=restaurantData.idrestaurant)
        )

        supplierData.save()

        messages.success(request,"Supplier Added Successfully!")
        return redirect(url)
    
    return render(request,'addSupplierAdminPanel.html')

def addPurchaseRawMaterialAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allSupplierData = Supplier.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allSupplierData':allSupplierData}
    return render(request,'addPurchaseRawMaterial.html',data)

def addPurchaseRawMaterialAdminData1(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        rName = request.POST.getlist('rName')
        rqty = request.POST.getlist('rawMatQ')
        rPrice = request.POST.getlist('rawMatPrice')
        rSupplier = request.POST.get('selectSupplier')
        totalPrice = 0
        restaurantData = Restaurant.objects.first()
        supplierData = Supplier.objects.get(idsupplier=rSupplier)
        rawMaterialIds = list()
        
        totalrName = len(rName)
        totalrMobile = len(rqty)
        totalr = len(rPrice)

        if(totalrName == 1):
            if(totalrMobile > 1 or totalr > 1):
                messages.success(request,"Invalid Data!")
                return redirect(url)
            else:
                rName = request.POST.get('rName')
                rqty = request.POST.get('rawMatQ')
                rPrice = request.POST.get('rawMatPrice')
                rawMaterialData = RawMaterial.objects.create(
                    raw_material_name = rName,
                    raw_materialtotal_quantity = rqty,
                    raw_material_price = rPrice,
                    restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=restaurantData.idrestaurant)
                )

                totalPrice = int(rawMaterialData.raw_materialtotal_quantity) * int(rawMaterialData.raw_material_price)

                purchaseData = Purchase.objects.create(
                    purchase_total_amount = totalPrice,
                    purchase_date = date.today(),
                    supplier_idsupplier = Supplier.objects.get(idsupplier=supplierData.idsupplier)
                )

                PurchaseRawMaterial.objects.create(
                    raw_material_idraw_material = rawMaterialData,
                    purchase_idpurchase = purchaseData,
                    quantity = rawMaterialData.raw_materialtotal_quantity,
                    price = rawMaterialData.raw_material_price
                )

                purchaseData.save()
                rawMaterialData.save()

        elif(totalrName > 1):
            if(totalrMobile == 1 and totalr == 1):
                rqty = request.POST.get('rawMatQ')
                rPrice = request.POST.get('rawMatPrice')
                for i in range(0,totalrName):
                    rawMaterialData = RawMaterial.objects.create(
                        raw_material_name = rName[i],
                        raw_materialtotal_quantity = rqty,
                        raw_material_price = rPrice,
                        restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=restaurantData.idrestaurant)
                    )

                    rawMaterialIds.append(rawMaterialData.idraw_material)

                    totalPrice = totalPrice + (int(rawMaterialData.raw_materialtotal_quantity) * int(rawMaterialData.raw_material_price))

                    rawMaterialData.save()

                purchaseData = Purchase.objects.create(
                    purchase_total_amount = totalPrice,
                    purchase_date = date.today(),
                    supplier_idsupplier = Supplier.objects.get(idsupplier=supplierData.idsupplier)
                )

                for i in range(0,len(rawMaterialIds)):
                    PurchaseRawMaterial.objects.create(
                        raw_material_idraw_material = RawMaterial.objects.get(idraw_material=rawMaterialIds[i]),
                        purchase_idpurchase = purchaseData,
                        quantity = rqty,
                        price = rPrice
                    )

                purchaseData.save()                

            elif(totalrMobile > 1 and totalr == 1):
                if(totalrMobile != totalrName):
                    messages.success(request,"Invalid Data!")
                    return redirect(url)
                else:
                    rPrice = request.POST.get('rawMatPrice')
                    for i in range(0,totalrName):
                        rawMaterialData = RawMaterial.objects.create(
                            raw_material_name = rName[i],
                            raw_materialtotal_quantity = rqty[i],
                            raw_material_price = rPrice,
                            restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=restaurantData.idrestaurant)
                        )

                        rawMaterialIds.append(rawMaterialData.idraw_material)

                        totalPrice = totalPrice + (int(rawMaterialData.raw_materialtotal_quantity) * int(rawMaterialData.raw_material_price))

                        rawMaterialData.save()

                    purchaseData = Purchase.objects.create(
                        purchase_total_amount = totalPrice,
                        purchase_date = date.today(),
                        supplier_idsupplier = Supplier.objects.get(idsupplier=supplierData.idsupplier)
                    )

                    for i in range(0,len(rawMaterialIds)):
                        PurchaseRawMaterial.objects.create(
                            raw_material_idraw_material = RawMaterial.objects.get(idraw_material=rawMaterialIds[i]),
                            purchase_idpurchase = purchaseData,
                            quantity = rqty[i],
                            price = rPrice
                        )

                    purchaseData.save() 

            elif(totalr > 1 and totalrMobile == 1):
                if(totalr != totalrName):
                    messages.success(request,"Invalid Data!")
                    return redirect(url)
                else:
                    rqty = request.POST.get('rawMatQ')
                    for i in range(0,totalrName):
                        rawMaterialData = RawMaterial.objects.create(
                            raw_material_name = rName[i],
                            raw_materialtotal_quantity = rqty,
                            raw_material_price = rPrice[i],
                            restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=restaurantData.idrestaurant)
                        )

                        rawMaterialIds.append(rawMaterialData.idraw_material)
                    
                        totalPrice = totalPrice + (int(rawMaterialData.raw_materialtotal_quantity) * int(rawMaterialData.raw_material_price))

                        rawMaterialData.save()

                    purchaseData = Purchase.objects.create(
                        purchase_total_amount = int(totalPrice),
                        purchase_date = date.today(),
                        supplier_idsupplier = Supplier.objects.get(idsupplier=supplierData.idsupplier)
                    )

                    for i in range(0,len(rawMaterialIds)):
                        PurchaseRawMaterial.objects.create(
                            raw_material_idraw_material = RawMaterial.objects.get(idraw_material=rawMaterialIds[i]),
                            purchase_idpurchase = purchaseData,
                            quantity = rqty,
                            price = rPrice[i]
                        )

                    purchaseData.save()
            else:
                if(totalr != totalrName or totalrMobile != totalrName):
                    messages.success(request,"Invalid Data!")
                    return redirect(url)
                else:
                    for i in range(0,totalrName):
                        rawMaterialData = RawMaterial.objects.create(
                            raw_material_name = rName[i],
                            raw_materialtotal_quantity = rqty[i],
                            raw_material_price = rPrice[i],
                            restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=restaurantData.idrestaurant)
                        )

                        rawMaterialIds.append(rawMaterialData.idraw_material)
                    
                        totalPrice = totalPrice + (int(rawMaterialData.raw_materialtotal_quantity) * int(rawMaterialData.raw_material_price))

                        rawMaterialData.save()

                    purchaseData = Purchase.objects.create(
                        purchase_total_amount = int(totalPrice),
                        purchase_date = date.today(),
                        supplier_idsupplier = Supplier.objects.get(idsupplier=supplierData.idsupplier)
                    )

                    for i in range(0,len(rawMaterialIds)):
                        PurchaseRawMaterial.objects.create(
                            raw_material_idraw_material = RawMaterial.objects.get(idraw_material=rawMaterialIds[i]),
                            purchase_idpurchase = purchaseData,
                            quantity = rqty[i],
                            price = rPrice[i]
                        )

                    purchaseData.save()


        messages.success(request,"Purchase Raw Material Record Added Successfully!")
        return redirect(url)

    return render(request,'addPurchaseRawMaterial.html')

def allPurchaseRawMaterialAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allSupplierData = Supplier.objects.all()
    purchaseRawMaterialData = PurchaseRawMaterial.objects.all().order_by('raw_material_idraw_material')
    paginator = Paginator(purchaseRawMaterialData,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'purchaseRawMaterialData':page_obj,'allSupplierData':allSupplierData}
    return render(request,'allPurchaseRawMaterial.html',data)

def purchaseRawMaterialDataUpdateAdminPanel(request,id_rawmaterial):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        rName = request.POST.get('rName')
        rQty = request.POST.get('rQty')
        rPrice = request.POST.get('rPrice')
        sChange = request.POST.get('supplierChange')
        totalPriceofOldRawMaterial = 0
        totalPriceofNewRawMaterial = 0

        getCurrentRawMaterialData = RawMaterial.objects.get(idraw_material=id_rawmaterial)
        totalPriceofOldRawMaterial = int(getCurrentRawMaterialData.raw_materialtotal_quantity) * int(getCurrentRawMaterialData.raw_material_price)
        getCurrentRawMaterialData.raw_material_name = rName
        getCurrentRawMaterialData.raw_materialtotal_quantity = rQty
        getCurrentRawMaterialData.raw_material_price = rPrice
        getCurrentRawMaterialData.save()
        totalPriceofNewRawMaterial = int(getCurrentRawMaterialData.raw_materialtotal_quantity) * int(getCurrentRawMaterialData.raw_material_price)

        getCurrentPurchaseRawMaterialData = PurchaseRawMaterial.objects.get(raw_material_idraw_material=id_rawmaterial)
        getCurrentPurchaseRawMaterialData.quantity = rQty
        getCurrentPurchaseRawMaterialData.price = rPrice
        getSupplierData = Purchase.objects.get(supplier_idsupplier=getCurrentPurchaseRawMaterialData.purchase_idpurchase.supplier_idsupplier)
        getSupplierData.supplier_idsupplier = Supplier.objects.get(idsupplier=sChange)
        getSupplierData.purchase_total_amount = (int(getSupplierData.purchase_total_amount) - int(totalPriceofOldRawMaterial)) + int(totalPriceofNewRawMaterial)

        getCurrentPurchaseRawMaterialData.save()
        getSupplierData.save()

        messages.success(request,"Purchase Raw Material Data Updated!")
        return redirect(url)
    return render(request,'allPurchaseRawMaterial.html')


def purchaseRawMaterialDataReturnAdminPanel(request,id_rawmaterial):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        totalPriceofOldRawMaterial = 0
        totalPriceofNewRawMaterial = 0
        totalPurchaseReturnAmount = 0
        purchaseReturnExist = None
        purchaseReturnData = None
        purchaseReturnDataRawMaterial = None
        rQty = request.POST.get('rQty')
        getCurrentPurchaseRawMaterialData = PurchaseRawMaterial.objects.get(raw_material_idraw_material=id_rawmaterial)
        if(int(rQty) > getCurrentPurchaseRawMaterialData.quantity or int(rQty) <= 0):
            messages.success(request,"Invalid Quantity!")
            return redirect(url)

        elif(int(rQty) < getCurrentPurchaseRawMaterialData.quantity):
            getCurrentRawMaterialData = RawMaterial.objects.get(idraw_material=id_rawmaterial)
            getCurrentPurchaseRawMaterialData = PurchaseRawMaterial.objects.get(raw_material_idraw_material=id_rawmaterial)
            totalPriceofOldRawMaterial = getCurrentPurchaseRawMaterialData.quantity * getCurrentPurchaseRawMaterialData.price
            getCurrentPurchaseRawMaterialData.quantity = getCurrentPurchaseRawMaterialData.quantity - int(rQty)
            getCurrentPurchaseRawMaterialData.save()
            totalPriceofNewRawMaterial = int(getCurrentPurchaseRawMaterialData.quantity) * int(getCurrentPurchaseRawMaterialData.price)
            getSupplierData = Purchase.objects.get(supplier_idsupplier=getCurrentPurchaseRawMaterialData.purchase_idpurchase.supplier_idsupplier)
            getSupplierData.purchase_total_amount = (int(getSupplierData.purchase_total_amount) - int(totalPriceofOldRawMaterial)) + int(totalPriceofNewRawMaterial)

            getSupplierData.save()

            totalPurchaseReturnAmount = int(getCurrentPurchaseRawMaterialData.price) * int(rQty)

            try:
                purchaseReturnExist = PurchaseReturn.objects.get(purchase_idpurchase=Purchase.objects.get(idpurchase=getCurrentPurchaseRawMaterialData.purchase_idpurchase.idpurchase))
            except:
                purchaseReturnExist = None
                print("error")

            if(purchaseReturnExist):
                purchaseReturnExist = PurchaseReturn.objects.get(purchase_idpurchase=Purchase.objects.get(idpurchase=getCurrentPurchaseRawMaterialData.purchase_idpurchase.idpurchase))
                purchaseReturnExist.purchase_return_total_amount = purchaseReturnExist.purchase_return_total_amount + totalPurchaseReturnAmount
                purchaseReturnExist.purchase_return_date = date.today()
                purchaseReturnExist.save()

                purchaseReturnDataRawMaterial = PurchaseReturnOfRawMaterial(
                    raw_material_idraw_material = RawMaterial.objects.get(idraw_material=id_rawmaterial),
                    purchase_return_idpurchase_return = PurchaseReturn.objects.get(idpurchase_return=purchaseReturnExist.idpurchase_return),
                    quantity = int(rQty),
                    price = getCurrentRawMaterialData.raw_material_price
                )

                purchaseReturnDataRawMaterial.save()

            else:
                purchaseReturnData = PurchaseReturn.objects.create(
                    purchase_return_total_amount = totalPurchaseReturnAmount,
                    purchase_return_date = date.today(),
                    purchase_idpurchase = Purchase.objects.get(idpurchase=getCurrentPurchaseRawMaterialData.purchase_idpurchase.idpurchase)
                )

                purchaseReturnData.save()

                purchaseReturnDataRawMaterial = PurchaseReturnOfRawMaterial(
                    raw_material_idraw_material = RawMaterial.objects.get(idraw_material=id_rawmaterial),
                    purchase_return_idpurchase_return = PurchaseReturn.objects.get(idpurchase_return=purchaseReturnData.idpurchase_return),
                    quantity = int(rQty),
                    price = getCurrentRawMaterialData.raw_material_price
                )

                purchaseReturnDataRawMaterial.save()

            messages.success(request,"Raw Material Retured!")
            return redirect(url)
        
        else:
            getCurrentRawMaterialData = RawMaterial.objects.get(idraw_material=id_rawmaterial)
            totalPriceofNewRawMaterial = int(getCurrentRawMaterialData.raw_materialtotal_quantity) * int(getCurrentRawMaterialData.raw_material_price)
            getSupplierData = Purchase.objects.get(supplier_idsupplier=getCurrentPurchaseRawMaterialData.purchase_idpurchase.supplier_idsupplier)
            getSupplierData.purchase_total_amount = getSupplierData.purchase_total_amount - totalPriceofNewRawMaterial
            getCurrentPurchaseRawMaterialData1 = PurchaseRawMaterial.objects.get(raw_material_idraw_material=id_rawmaterial)
            getCurrentRawMaterialData.delete()
            getCurrentPurchaseRawMaterialData1.delete()
            getSupplierData.save()

            messages.success(request,"All Quantity of Raw Material Retured!")
            return redirect(url)

    return render(request,'allPurchaseRawMaterial.html')

def allRawMaterialAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allRawMaterialData = RawMaterial.objects.all().order_by('idraw_material')
    paginator = Paginator(allRawMaterialData,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allRawMaterialData':page_obj}
    return render(request,'allRawMaterialAdmin.html',data)

def allRawMaterialAdminPanelUpdate(request,id_rawmat):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        rQty = request.POST.get('rQty')
        purchaseData = PurchaseRawMaterial.objects.get(raw_material_idraw_material=id_rawmat)
        if(int(rQty) <= 0 or int(rQty) > purchaseData.quantity):
            messages.success(request,"Invalid Quantity!")
            return redirect(url)
        
        rawMaterialData = RawMaterial.objects.get(idraw_material=id_rawmat)
        rawMaterialData.raw_materialtotal_quantity = int(rQty)
        rawMaterialData.save()

        messages.success(request,"Quantity Updated!")
        return redirect(url)
    
    return render(request,'allRawMaterialAdmin.html')

def allPurchaseAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseData = Purchase.objects.all().order_by('idpurchase')
    paginator = Paginator(allPurchaseData,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseData':page_obj}
    return render(request,'allPurchaseAdmin.html',data)

def allPurchaseReturnAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseReturnData = PurchaseReturn.objects.all().order_by('idpurchase_return')
    paginator = Paginator(allPurchaseReturnData,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseReturnData':page_obj}
    return render(request,'allPurchaseReturnAdmin.html',data)

def allPurchaseRawMaterialReturnAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseReturnRawMaterialData = PurchaseReturnOfRawMaterial.objects.all().order_by('raw_material_idraw_material')
    paginator = Paginator(allPurchaseReturnRawMaterialData,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseReturnRawMaterialData':page_obj}
    return render(request,'allPurchaseReturnRawMaterial.html',data)

def notificationAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    notification = Notification.objects.all().order_by('idnotification')
    paginator = Paginator(notification,7,orphans=1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'notification':page_obj}
    return render(request,'notificationAdmin.html',data)

def notificationAdminPanelUpdate(request,id_notification):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        notificationDesc = request.POST.get('notificationDesc')
        notificationData = Notification.objects.get(idnotification=id_notification)
        notificationData.notification_description = notificationDesc
        notificationData.save()
        messages.success(request,"Notification Data Updated!")
        return redirect(url)
    return render(request,'notificationAdmin.html')

def notificationAdminPanelDelete(request,id_notification):
    url = request.META.get('HTTP_REFERER')
    notificationDeleteData = Notification.objects.filter(idnotification=id_notification)
    notificationDeleteData.delete()
    messages.success(request,"Notification deleted!")
    return redirect(url)

def addAreaAdminPanel(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    return render(request,'addAreaAdminPanel.html',data)

def addAreaAdminPanelData1(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        cityData = City.objects.first()
        allAreaData = Area.objects.all()
        pincode = request.POST.get('pincode')
        areaName = request.POST.get('areaName')
        delCharges = request.POST.get('delCharges')

        for i in allAreaData:
            if(i.pincode == int(pincode)):
                messages.error(request,"Pincode already exist!")
                return redirect(url)

        areaData = Area.objects.create(
            pincode = pincode,
            area_name=areaName,
            area_delivery_charges=delCharges,
            city_idcity=City.objects.get(idcity=cityData.idcity)
        )

        areaData.save()
        messages.success(request,"Area Added Successfully!")
        return redirect(url)
    
    return render(request,'addAreaAdminPanel.html')
        
def addItemCatAdminPanell(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    return render(request,'addItemCategory.html',data)

def addItemCatAdminPanellData(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        RestaurantData = Restaurant.objects.first()
        catName = request.POST.get('catName')
        catDesc = request.POST.get('catDesc')
        allCatData = ItemCategory.objects.all()

        if(ItemCategory.objects.filter(item_category_name__icontains=catName)):
            messages.error(request,'Category already exist!')
            return redirect(url)
        
        uniqueString = str(uuid.uuid4())
        catSlug = catName + uniqueString

        catData = ItemCategory()

        catData.item_category_name = catName
        catData.item_category_description = catDesc
        for i in allCatData:
            if(i.slug == catSlug):
                uniqueString = str(uuid.uuid4())
                break
        catSlug = catName + uniqueString
        catData.slug = catSlug
        # catData.restaurant_idrestaurant = Restaurant.objects.get(idrestaurant=RestaurantData.idrestaurant)

        if(len(request.FILES) != 0):
            catImage = request.FILES['catImage']
            catImage1 = str(catImage)
            if(not(catImage1.lower().endswith(('.png','.jpg','.jpeg')))):
                messages.error(request,'Choose only image!')
                return redirect(url)
            catData.item_category_image = request.FILES['catImage']
            
        catData.save()
        messages.success(request,'Item Category Added!')
        return redirect(url)

    return render(request,'addItemCategory.html')

def addItemAdminPanell(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allItemCategory = ItemCategory.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allItemCategory':allItemCategory}
    return render(request,'addItemAdminPanel.html',data)

def addItemAdminPanellData(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        itemName = request.POST.get('itemName')
        itemPrice = request.POST.get('itemPrice')
        catItem = request.POST.get('Catitem')
        itemDesc = request.POST.get('itemDesc')
        allItemData = Item.objects.all()
        getCategory = ItemCategory.objects.get(item_category_name=catItem)
        
        uniqueString = str(uuid.uuid4())
        itemSlug = itemName + uniqueString

        itemData = Item()

        itemData.item_name = itemName
        itemData.item_price = itemPrice
        itemData.item_description = itemDesc
        for i in allItemData:
            if(i.slug == itemSlug):
                uniqueString = str(uuid.uuid4())
                break
        itemSlug = itemName + uniqueString
        itemData.slug = itemSlug
        itemData.item_category_iditem_category = ItemCategory.objects.get(iditem_category=getCategory.iditem_category)
        itemData.offer_price = 0

        if(len(request.FILES) != 0):
            itemImage = request.FILES['itemImage']
            itemImage1 = str(itemImage)
            if(not(itemImage1.lower().endswith(('.png','.jpg','.jpeg')))):
                messages.error(request,'Choose only image!')
                return redirect(url)
            itemData.item_image = request.FILES['itemImage']
            
        itemData.save()
        messages.success(request,'Item Added!')
        return redirect(url)
    
    return render(request,'addItemAdminPanel.html')

def addOfferAdminPanell(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allItems = Item.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allItems':allItems}
    return render(request,'addOfferAdminPanel.html',data)

def addOfferAdminPanellData(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        offerValue = request.POST.get('offerValue')
        offerStartDate = request.POST.get('offerstartDate')
        offerEndDate = request.POST.get('offerendDate')
        offerItem = request.POST.get('item')
        offerDescription = request.POST.get('offerDesc')

        getItem = Item.objects.get(item_name=offerItem)

        offerData = Offer()

        offerStart = datetime.strptime(offerStartDate,'%Y-%m-%d')
        offerEnd = datetime.strptime(offerEndDate,'%Y-%m-%d')

        if(offerStart.date() < date.today()):
            messages.error(request,"Invalid Data!")
            return redirect(url)

        if(offerStart.date() > offerEnd.date()):
            messages.error(request,"Invalid Data!")
            return redirect(url)
        
        offerData.offer_value = offerValue
        offerData.offer_start_date = offerStart.date()
        offerData.offer_end_date = offerEnd.date()
        offerData.offer_description = offerDescription

        offerData.save()

        getItem.offer_idoffer = Offer.objects.get(idoffer=offerData.idoffer)

        getItem.save()

        messages.success(request,'Offer Added!')
        return redirect(url)

    return render(request,'addOfferAdminPanel.html')

def addNotificationAdminPanell(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    return render(request,'addNotificationAdminPanel.html',data)

def addNotificationAdminPanellData(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        notificationDesc = request.POST.get('notificationDesc')

        notificationData = Notification()

        notificationData.notification_description = notificationDesc

        notificationData.save()

        messages.success(request,'Notification Added!')
        return redirect(url)
    
    return render(request,'addNotificationAdminPanel.html')

class orderInvoicePdf(View):
    def get(self, request, *args, **kwargs):
        totalOfferPrice = 0
        totalPrice = 0
        current_user = request.session['user_name']
        cusername = User.objects.get(user_name=current_user)
        u1 = cusername.iduser
        o1 = Order.objects.get(tracking_no=self.kwargs['t_no'])
        od1 = OrderedItem.objects.filter(order_idorder=o1.idorder)
        for i in od1:
            totalOfferPrice = totalOfferPrice + i.item_iditem.offer_price

        for i in od1:
            totalPrice = totalPrice + i.item_iditem.item_price

        data = {
            'order':o1,
            'orderDetails':od1,
            'totalOfferPrice':totalOfferPrice,
            'totalPrice':totalPrice
        }
        open('templates/temp.html',"w").write(render_to_string("Invoice.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')
    
def reportBrewerOrderAdmin(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allOrderData = Order.objects.filter(is_cancel_order=0)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOrderData':allOrderData}
    return render(request,'report.html',data)

sdate = None
edate = None
def orderReport(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    if request.method == "POST":
        global sdate
        global edate
        sdate = request.POST.get('start_date')
        edate = request.POST.get('end_date')
        allOrderData = Order.objects.filter(order_date__range=(sdate,edate),is_cancel_order=0)
        data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOrderData':allOrderData}
        return render(request,'orderOutputreport.html',data)
    return render(request,'orderOutputreport.html',data)

class orderReportGenerateAdmin(View):
    def get(self, request, *args, **kwargs):
        if(sdate and edate):
            o = Order.objects.filter(order_date__range=(sdate,edate),is_cancel_order=0)
        else:
            o = Order.objects.filter(is_cancel_order=0)
        
        data = {
            'order':o
        }
        
        open('templates/temp.html',"w").write(render_to_string("orderReportPdf.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')

def brewerCancelOrder(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allCancelOrderData = Order.objects.filter(is_cancel_order=1)
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allCancelOrderData':allCancelOrderData}
    return render(request,'cancelOrderReport.html',data)

csdate = None
cedate = None
def orderCancelReportAdmin(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    if request.method == "POST":
        global csdate
        global cedate
        csdate = request.POST.get('start_date')
        cedate = request.POST.get('end_date')
        allCancelOrderData = Order.objects.filter(cancel_order_date__date__range=(csdate,cedate),is_cancel_order=1)
        data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allCancelOrderData':allCancelOrderData}
        return render(request,'cancelOrderOutput.html',data)
    return render(request,'cancelOrderOutput.html',data)

class cancelOrderReportGenerateAdmin(View):
    def get(self, request, *args, **kwargs):
        if(csdate and cedate):
            o = Order.objects.filter(cancel_order_date__date__range=(csdate,cedate),is_cancel_order=1)
        else:
            o = Order.objects.filter(is_cancel_order=1)
        
        data = {
            'cancelOrder':o
        }
        
        open('templates/temp.html',"w").write(render_to_string("cancelOrderReportPdf.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')


def brewerOffer(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allOfferItems = Offer.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOfferItems':allOfferItems}
    return render(request,'offerReport.html',data)

Offersdate = None
Offeredate = None
def offerReportAdmin(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer}
    if request.method == "POST":
        global Offersdate
        global Offeredate
        Offersdate = request.POST.get('start_date')
        Offeredate = request.POST.get('end_date')
        allOfferItems = Offer.objects.filter(offer_start_date__range=(Offersdate,Offeredate), offer_end_date__range=(Offersdate,Offeredate))
        data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allOfferItems':allOfferItems}
        return render(request,'offerOutput.html',data)
    return render(request,'offerOutput.html',data)

class offerReportGenerateAdmin(View):
    def get(self, request, *args, **kwargs):
        if(Offersdate and Offeredate):
            o = Offer.objects.filter(offer_start_date__range=(Offersdate,Offeredate), offer_end_date__range=(Offersdate,Offeredate))
        else:
            o = Offer.objects.all()
        
        data = {
            'offer':o
        }
        
        open('templates/temp.html',"w").write(render_to_string("offerReportPdf.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')


def brewerPurchase(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseData = Purchase.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseData':allPurchaseData}
    return render(request,'purchaseReport.html',data)

Purchasesdate = None
Purchaseedate = None
def purchaseReportAdmin(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseData = Purchase.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseData':allPurchaseData}
    if request.method == "POST":
        global Purchasesdate
        global Purchaseedate
        Purchasesdate = request.POST.get('start_date')
        Purchaseedate = request.POST.get('end_date')
        allPurchaseData = Purchase.objects.filter(purchase_date__range=(Purchasesdate,Purchaseedate))
        data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseData':allPurchaseData}
        return render(request,'purchaseOutput.html',data)
    return render(request,'purchaseOutput.html',data)

class purchaseReportGenerateAdmin(View):
    def get(self, request, *args, **kwargs):
        if(Offersdate and Offeredate):
            o = Purchase.objects.filter(purchase_date__range=(Purchasesdate,Purchaseedate))
        else:
            o = Purchase.objects.all()
        
        data = {
            'purchase':o
        }
        
        open('templates/temp.html',"w").write(render_to_string("purchaseReportPdf.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')

def brewerPurchaseReturn(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseReturnData = PurchaseReturn.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseReturnData':allPurchaseReturnData}
    return render(request,'purchaseReturnReport.html',data)

PurchaseReturnsdate = None
PurchaseReturnedate = None
def purchaseReturnReportAdmin(request):
    u3 = User.objects.get(user_name=request.session['admin'])
    totalAdmin = User.objects.filter(is_admin=1).count()
    totalUser = User.objects.filter(is_admin=0).count()
    totalItems = Item.objects.all().count()
    totalOffer = Offer.objects.all().count()
    allPurchaseReturnData = PurchaseReturn.objects.all()
    data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseReturnData':allPurchaseReturnData}
    if request.method == "POST":
        global PurchaseReturnsdate
        global PurchaseReturnedate
        PurchaseReturnsdate = request.POST.get('start_date')
        PurchaseReturnedate = request.POST.get('end_date')
        allPurchaseReturnData = PurchaseReturn.objects.filter(purchase_return_date__range=(PurchaseReturnsdate,PurchaseReturnedate))
        data = {'currentAdmin':u3,'totalAdmin':totalAdmin,'totalUser':totalUser,'totalItem':totalItems,'totalOffer':totalOffer,'allPurchaseReturnData':allPurchaseReturnData}
        return render(request,'purchaseReturnOutput.html',data)
    return render(request,'purchaseReturnOutput.html',data)

class purchaseReturnReportGenerateAdmin(View):
    def get(self, request, *args, **kwargs):
        if(PurchaseReturnsdate and PurchaseReturnedate):
            o = PurchaseReturn.objects.filter(purchase_return_date__range=(PurchaseReturnsdate,PurchaseReturnedate))
        else:
            o = PurchaseReturn.objects.all()
        
        data = {
            'purchaseReturn':o
        }
        
        open('templates/temp.html',"w").write(render_to_string("purchaseReturnReportPdf.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')