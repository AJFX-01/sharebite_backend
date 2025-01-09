""" views """

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from .models import Receipt, Donation, DropOffsite
from .serializers import (
    ReceiptSerializer, UserSerializer, DonationSerializer, ProofSerializer, DropOffSiteSerializer)


# Register View
class RegisterView(APIView):
    """ METHOD CALL FOR REGISTER """

    permission_classes = [AllowAny]
    def post(self, request):
        """ POST METHOD """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(ObtainAuthToken):
    """Method to login"""

    def post(self, request, *args, **kwargs):
        """POST method with error handling"""
        try:
            response = super().post(request, *args, **kwargs)
            token_key = response.data.get('token')
            
            if not token_key:
                raise AuthenticationFailed('Token generation failed. Please check your credentials.')
            try:
                token = Token.objects.get(key=token_key)  # pylint: disable=no-member
                user = token.user  
            except Token.DoesNotExist: # pylint: disable=no-member
                return Response({'error': 'Invalid token. Authentication failed.'}, \
                                 status=status.HTTP_401_UNAUTHORIZED)
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_donor': getattr(user, 'is_donor', False),
                'is_receiver': getattr(user, 'is_receiver', False),
            }
            
            return Response({
                'token': token.key,
                'user_id': user_data,
            }, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as e:
            return Response(f"error: invalid email or passwword, {e}",\
                             status=status.HTTP_400_BAD_REQUEST)

# Donation Views
class DonationListView(APIView):
    """ Donations APIVIEWs"""
    def get(self):
        """ Get all donations"""
        donations = Donation.objects.all() # pylint: disable=no-member
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
    def get(self, pk):
        """  get a particular donation """
        donation = get_object_or_404(Donation, pk=pk)
        serializer = DonationSerializer(donation)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    def get(self):
        """ retrieve all site """
        sites = DropOffsite.objects.all() # pylint: disable=no-member
        serialzer = DropOffSiteSerializer(sites, many=True)
        return Response(serialzer.data, status=status.HTTP_200_OK)

# Reserve Donation View
class ReserveDonationView(APIView):
    """ Reservation APis """
    def post(self, request, donation_id):
        """ reserve a particular donation """
        try:
            donation = Donation.objects.get(pk=donation_id, is_reserved=False) # pylint: disable=no-member
        except Donation.DoesNotExist: # pylint: disable=no-member
            return Response({"error": "Donation not available for reservation."},
            status=status.HTTP_404_NOT_FOUND)

        donation.is_reserved = True
        donation.reserved_by = request.user
        donation.save()
        return Response({"message": "Donation reserved successfully."}, status=status.HTTP_200_OK)

# View Receipt History
class ReceiptHistoryView(APIView):
    """ Reciepts  Apis"""
    def get(self, request):
        """ retrieve a particular receipt """
        receipts = Receipt.objects.filter(user=request.user) # pylint: disable=no-member
        serializer = ReceiptSerializer(receipts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Cancel Pickup
class CancelPickupView(APIView):
    """ Cancel Pickup """
    def post(self, request, donation_id):
        """ poat donation data """

        try:
            donation = Donation.objects.get(pk=donation_id, reserved_by=request.user, is_reserved=True) # pylint: disable=no-member
        except Donation.DoesNotExist: # pylint: disable=no-member
            return Response({"error": "You cannot cancel this reservation."},
            status=status.HTTP_404_NOT_FOUND)

        donation.cancel_reservation()
        return Response({"message": "Reservation canceled successfully."},
        status=status.HTTP_200_OK)
# Proof Upload View
class ProofUploadView(APIView):
    """ PRoof Upload api """
    def post(self, request, donation_id):
        """ proof for a particular donation """
        try:
            donation = Donation.objects.get(pk=donation_id) # pylint: disable=no-member
        except Donation.DoesNotExist: # pylint: disable=no-member
            return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProofSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(donation=donation, uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)