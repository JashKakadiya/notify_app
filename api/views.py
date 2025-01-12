from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .models import Request_approve
from rest_framework_simplejwt.tokens import RefreshToken

from .email_helper import send_email
from notify_app import settings
from django.views.decorators.csrf import csrf_exempt
import os 
from .models import *
from dotenv import load_dotenv
load_dotenv()

def check_authentication(request):
    if not request.headers.get('Authorization'):
        return False, None
    token = request.headers.get('Authorization')
    try:
        user = User_Table.objects.get(token=token)
    except:
        return False, None
    if not user:
        
        return False, None
    return user , True

@csrf_exempt
@api_view(['POST'])
def approve(request):
    data = request.data
    transaction_id = data.get('transaction_id')
    approve = data.get('approve')
    try:
        user, is_authenticated = check_authentication(request)
        if not is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        if approve == 'approved':
            Request_approve.objects.filter(transaction_id=transaction_id).update(is_approved='approved')
            
            return Response({"status":"approved"}, status=status.HTTP_200_OK)
        if approve == 'disapproved':
            Request_approve.objects.filter(transaction_id=transaction_id).update(is_approved='disapproved')
            return Response({"status":"disapproved"}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_request_approve(request):
    """
    Handle POST requests to create a new Request_approve object.
    """
    email = request.data.get('email')
    transaction_id = request.data.get('transaction_id')
    image = request.FILES.get('image')

    if not email or not transaction_id or not image:
        return Response(
            {"error": "email, transaction_id, and image are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create and save the object
    try:
        request_approve = Request_approve.objects.create(
            emal=email,
            transaction_id=transaction_id,
            image=image
        )
        image_url  = f"{request.build_absolute_uri(settings.MEDIA_URL)}{request_approve.image}"
        approve_url = f"{os.getenv('BASE_URL')}/api/approve/{request_approve.transaction_id}"
        print(request_approve.image)
        print(image_url)
        print(approve_url)
        send_email(email, image_url, request_approve.transaction_id,approve_url)
        return Response(
            {
                "message": "Request created successfully.",
                "id": request_approve.id
            },
            status=status.HTTP_201_CREATED
        )
        
    except Exception as e:
        return Response(
            {"error": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@csrf_exempt
@api_view(['GET'])
def get_requests(request):
    try:
        user, is_authenticated = check_authentication(request)
        if not is_authenticated:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
        req_data = Request_approve.objects.all()
        
        json_data = []
        for data in req_data:
            json_data.append({
                
                "email": data.emal,
                "transaction_id": data.transaction_id,
                "image": f"{request.build_absolute_uri(settings.MEDIA_URL)}{data.image}",
                "is_approved": data.is_approved,
                
                "created_at": data.created_at,
                "updated_at": data.updated_at
            })
        return Response({'data': json_data}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
@csrf_exempt
@api_view(['POST'])
def login(request):
        
    if request.method == 'POST':
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = User_Table.objects.filter(email=email, password=password).first()
        if user is None:
            return Response({'status': False,"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        token=refresh.access_token
        User_Table.objects.filter(email=user.email).update(token=token, refresh_token=refresh)
        if user.is_active:
            return Response({
                'status': True,
                'message': 'Login successful',
                'email': user.email,
                'access_token': str(token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'status': False,"message": "User_Table is not active"}, status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@api_view(['POST'])
def logout(request):
    user, is_authenticated = check_authentication(request)
    if not is_authenticated:
        return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    if user is None:
        return Response({'status': False,"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    User_Table.objects.filter(email=user.email).update(token=None, refresh_token=None)
    return Response({'status': True,"message": "Logout successful"}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def enter_text(request):
    data = request.data
    trasaction_id = data.get('transaction_id')
    text = data.get('text')
    try:
        Request_approve.objects.filter(transaction_id=trasaction_id).update(text=text)
        return HttpResponse("Text entered successfully.", status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def forget_password(request):
    # user, is_authenticated = check_authentication(request)
    # if not is_authenticated:
    #     return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    data = request.data
    email = data.get('email')
    password = data.get('password')
    user = User_Table.objects.filter(email=email).first()
    if user is None:
        return Response({'status': False,"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    User_Table.objects.filter(email=user.email).update(password=password)
    return Response({'status': True,"message": "Password changed successfully"}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        try:
            data = request.data
            email = data.get('email')
            password = data.get('password')
            User_Table.objects.create(email=email, password=password)
            return Response({'status': True,"message": "Registration successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)