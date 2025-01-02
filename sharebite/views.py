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
        """ POST METHOD """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View   
class LoginView(ObtainAuthToken):
    """ METHOD TO LOGIN """
    def post(self, request, *args, **kwargs):
        """ POST METHOD """
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id })

# Donation Views
class DonationListView(APIView):
    """ Donations APIVIEWs"""
    def get(self):
        """ Get all donations"""
        donations = Donation.objects.all()
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)   
    def post(self, request):
        """ Save a new donation by particular user """
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(donor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Donation Detail View
class DonationDetailView(APIView):
    """ Retrieve donations detail """
    def get(self, request, pk):
        """  get a particular donation """
        try:
            donation = Donation.objects.get(pk=pk)
        except Donation.DoesNotExist:
            return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DonationSerializer(donation)
        return Response(serializer.data)
    
# Admin Drop-Off Sites View
class DropOffSiteView(APIView):
    """ DropOff sites """

    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """ Addd a new site """
        serializer = DropOffSiteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        sites = DropOffsite.objects.all()
        serialzer = DropOffSiteSerializer(sites, many=True)
        return Response(serialzer.data)
