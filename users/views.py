from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import UserCreateSerializer, UserAuthSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import UserConfirmCode


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, password=password, is_active=False)

    confirmation = UserConfirmCode.objects.create(user=user)
    confirmation.generate_code()

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id,
                          'confirmation_code': confirmation.confirmation_code})


@api_view(['POST'])
def confirm_user_api_view(request):
    user_id = request.data.get('user_id')
    confirmation_code = request.data.get('confirmation_code')

    try:
        user = User.objects.get(id=user_id)
        confirmation = UserConfirmCode.objects.get(user=user)

        if confirmation.confirmation_code == confirmation_code:
            user.is_active = True
            user.save()
            return Response({'message': 'User confirmed successfully!'})
        else:
            return Response({'error': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except UserConfirmCode.DoesNotExist:
        return Response({'error': 'Confirmation code not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User credentials are wrong!'})
