from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helper import send_otp_to_phone
from .models import User
from django.core.cache import cache


@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Key 'phone_number' is required"
        })

    if data.get('password') is None:
        return Response({
            'status': 400,
            'message': "Key 'password' is required"
        })

    user = User.objects.create(
        phone_number=data.get('phone_number'),
        otp=send_otp_to_phone(data.get('phone_number'))
    )
    user.set_password = data.get('set_password')
    user.save()

    return Response({
        'status': 200,
        'message': 'Otp sent'
    })


@api_view(['POST'])
def verify_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Key 'phone_number' is required"
        })

    if data.get('otp') is None:
        return Response({
            'status': 400,
            'message': "Key 'otp' is required"
        })

    try:
        user_obj = User.objects.get(phone_number=data.get('phone_number'))

    except Exception as e:
        return Response({
            'status': 400,
            'message': 'Invalid phone'
        })

    if user_obj.otp == data.get('otp'):
        user_obj.is_phone_verify = True
        user_obj.save()
        return Response({
            'status': 200,
            'message': 'otp matched'
        })

    return Response({
        'status': 400,
        'message': 'Invalid otp'
    })


def resend_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Key 'phone_number' is required"
        })

    user_obj = User.objects.get(phone_number=data.get('phone_number'))

    if cache.get(user_obj.phone_number):
        return Response({
            'status': 400,
            'message': f'otp already sent try after {cache.get(user_obj.phone_number)}'
        })
    user_obj.otp = send_otp_to_phone(user_obj.phone_number)
    user_obj.save()
    cache.set(user_obj.phone_number, user_obj.otp, 60 * 2)

    return Response({
        'status': 200,
        'message': 'otp sent'
    })