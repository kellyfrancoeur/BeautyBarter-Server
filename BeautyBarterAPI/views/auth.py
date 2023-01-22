from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django import forms
from BeautyBarterAPI.forms import NewMemberRegistrationForm
from BeautyBarterAPI.models import Member, Admin, Profession, LicenseState

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    authenticated_user = authenticate(username=username, password=password)

    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'id': authenticated_user.id,
            'token': token.key,
            'staff': authenticated_user.is_staff
        }
        return Response(data)
    else:
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    account_type = request.data.get('account_type', None)
    username = request.data.get('username', None)
    password = request.data.get('password', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    email = request.data.get('email', None)

    if account_type is not None \
        and username is not None \
        and password is not None \
        and first_name is not None \
        and last_name is not None \
        and email is not None:

        if account_type == 'member':
            birthday = request.data.get('birthday', None)
            if birthday is None:
                return Response(
                    {'message': 'You must provide an birthday for a member'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif account_type == 'staff':
            bio = request.data.get('bio', None)
            if bio is None:
                return Response(
                    {'message': 'You must provide a bio for an staff'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {'message': 'Invalid account type. Valid values are \'member\' or \'staff\''},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            new_user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email= request.data['email']
            )

        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        account = None

        if account_type == 'member':
            account = BourbonUser.objects.create(
                birthday=request.data['birthday'],
                user=new_user
            )
        elif account_type == 'staff':
            new_user.is_staff = True
            new_user.save()

            account = BourbonStaff.objects.create(
                bio=request.data['bio'],
                user=new_user
            )

        token = Token.objects.create(user=account.user)
        data = { 'token': token.key, 'staff': new_user.is_staff }
        return Response(data)
    
    return Response({'message': 'You must provide a username, password, first_name, last_name, email and account_type'}, status=status.HTTP_400_BAD_REQUEST)