""" Serailizers """
from rest_framework import serializers
from .models import User, Donation, Proof, DropOffsite, Receipt

class UserSerializer(serializers.ModelSerializer):
    """ User serialize"""
    class Meta:
        """ meta """
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_donor', 'is_receiver']

class DonationSerializer(serializers.ModelSerializer):
    """ Donation serialize """
    class Meta:
        """ meta """
        model = Donation
        fields = ['id','donor', 'title', 'description',\
                   'location', 'is_reserved', 'is_delivered', 'created_at', 'reserved_by']

class ProofSerializer(serializers.ModelSerializer):
    """ Proof Serializer """
    class Meta:
        """ meta """
        model = Proof
        fields = ['id', 'donation', 'proof_image', 'uploaded_by']

class DropOffSiteSerializer(serializers.ModelSerializer):
    """ Drop Serializer """
    class Meta:
        """ meta """
        model = DropOffsite
        fields = ['id', 'location', 'added_by', 'created_at']

class ReceiptSerializer(serializers.ModelSerializer):
    """ Receipt seerialize """
    class Meta:
        """ meta """
        model = Receipt
        fields = ['id', 'user', 'donation', 'pickup_date', 'created_at']
