from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import User, Donation, Proof, DropOffsite
from .serializers import UserSerializer, DonationSerializer, ProofSerializer, DropOffSiteSerializer


# Register View
class RegisterView(APIView):
    """ METHOD CALL FOR REGISTER """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)