from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from BeautyBarterAPI.forms import NewMemberRegistrationForm
from BeautyBarterAPI.models import Member


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            member = Member.objects.get(user=user)
            if member.approved:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, ("Your account is not yet approved. Please wait for an administrator to approve your account."))
                return redirect('login')

def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = NewMemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            review = Member.objects.create(user=user, license_state=form.cleaned_data['license_state'], license_number=form.cleaned_data['license_number'])
            review.save()
            login(request, user)
            messages.success(request, ("You have been approved!"))
            return redirect('home')


# from django.contrib.auth import login, authenticate
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.db import IntegrityError
# from rest_framework.authtoken.models import Token
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from django import forms
# from BeautyBarterAPI.forms import NewMemberRegistrationForm, AdminRegistrationForm
# from BeautyBarterAPI.models import Member, Admin, Profession, LicenseState

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_user(request):
#     '''Handles the authentication of a user

#     Method arguments:
#       request -- The full HTTP request object
#     '''
#     username = request.data['username']
#     password = request.data['password']

#     authenticated_user = authenticate(username=username, password=password)

#     if authenticated_user is not None:
#         token = Token.objects.get(user=authenticated_user)
#         data = {
#             'valid': True,
#             'id': authenticated_user.id,
#             'token': token.key,
#             'staff': authenticated_user.is_staff
#         }
#         return Response(data)
#     else:
#         data = { 'valid': False }
#         return Response(data)

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register_user(request):
#     '''Handles the creation of a new user for authentication

#     Method arguments:
#       request -- The full HTTP request object
#     '''
#     account_type = request.data.get('account_type', None)
#     username = request.data.get('username', None)
#     password = request.data.get('password', None)
#     first_name = request.data.get('first_name', None)
#     last_name = request.data.get('last_name', None)
#     email = request.data.get('email', None)

#     if account_type is not None \
#         and username is not None \
#         and password is not None \
#         and first_name is not None \
#         and last_name is not None \
#         and email is not None:

#         if request.method == 'POST':
#             account_type = request.POST.get('account_type', None)
#             if account_type == 'member':
#                 form = NewMemberRegistrationForm(request.POST)
#                 if form.is_valid():
#                     user = form.save()
#                     review = LicenseCheck.objects.create(user=user, profession=form.cleaned_data['profession'], license_state=form.cleaned_data['license_state'], license_number=form.cleaned_data['license_number'])
#                     review.save()
#                     login(request, user)
#                     return redirect('success')
#             elif account_type == 'admin':
#                 form = AdminRegistrationForm(request.POST)
#                 if form.is_valid():
#                     user = form.save()
#                     user.is_staff = True
#                     user.save()
#                     login(request, user)
#                     return redirect('success')
#         else:
#             form = NewMemberRegistrationForm()
#             return Response(
#                 {'message': 'Invalid account type. Valid values are \'member\' or \'staff\''},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if account_type == 'member':
#             profession = request.data.get('profession', None)
#             if profession is None:
#                 return Response(
#                     {'message': 'You must provide an profession for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             license_state = request.data.get('license_state', None)
#             if license_state is None:
#                 return Response(
#                     {'message': 'You must provide an license_state for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             license_number = request.data.get('license_number', None)
#             if license_number is None:
#                 return Response(
#                     {'message': 'You must provide an license_number for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             link_to_site = request.data.get('link_to_site', None)
#             if link_to_site is None:
#                 return Response(
#                     {'message': 'You must provide an link_to_site for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             about = request.data.get('about', None)
#             if about is None:
#                 return Response(
#                     {'message': 'You must provide an about for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             interested_in = request.data.get('interested_in', None)
#             if interested_in is None:
#                 return Response(
#                     {'message': 'You must provide an interested_in for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             willing_to_trade = request.data.get('willing_to_trade', None)
#             if willing_to_trade is None:
#                 return Response(
#                     {'message': 'You must provide an willing_to_trade for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             img = request.data.get('img', None)
#             if img is None:
#                 return Response(
#                     {'message': 'You must provide an img for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             portfolio_img = request.data.get('portfolio_img', None)
#             if portfolio_img is None:
#                 return Response(
#                     {'message': 'You must provide an portfolio_img for a member'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         elif account_type == 'admin':
#             position = request.data.get('position', None)
#             if position is None:
#                 return Response(
#                     {'message': 'You must provide a position for an admin'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             img = request.data.get('img', None)
#             if img is None:
#                 return Response(
#                     {'message': 'You must provide a img for an admin'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         else:
#             return Response(
#                 {'message': 'Invalid account type. Valid values are \'member\' or \'staff\''},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         try:

#             new_user = User.objects.create_user(
#                 username=request.data['username'],
#                 password=request.data['password'],
#                 first_name=request.data['first_name'],
#                 last_name=request.data['last_name'],
#                 email= request.data['email']
#             )

#         except IntegrityError:
#             return Response(
#                 {'message': 'An account with that email address already exists'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         account = None

#         if account_type == 'member':
#             account = Member.objects.create(
#                 profession=Profession.objects.get(pk=request.data['profession']),
#                 license_state=LicenseState.objects.get(pk=request.data['license_state']),
#                 license_number=request.data['license_number'],
#                 link_to_site=request.data['link_to_site'],
#                 about=request.data['about'],
#                 interested_in=request.data['interested_in'],
#                 willing_to_trade=request.data['willing_to_trade'],
#                 img=request.data['img'],
#                 portfolio_img=request.data['portfolio_img'],
#                 user=new_user
#             )
#         elif account_type == 'admin':
#             new_user.is_staff = True
#             new_user.save()

#             account = Admin.objects.create(
#                 position=request.data['position'],
#                 img=request.data['img'],
#                 user=new_user
#             )

#         token = Token.objects.create(user=account.user)
#         data = { 'token': token.key, 'admin': new_user.is_staff }
#         return Response(data)
    
#     return Response({'message': 'You must provide a username, password, first_name, last_name, email and account_type'}, status=status.HTTP_400_BAD_REQUEST)