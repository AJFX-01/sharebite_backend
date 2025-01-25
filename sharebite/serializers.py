""" Serailizers """
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Donation, Proof, DropOffsite, Receipt

class UserSerializer(serializers.ModelSerializer):
    """ User serialize"""
    class Meta:
        """ meta """
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password', \
                  'email', 'is_donor', 'is_receiver']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """ Create user """
        # Hash the password before saving
        password = validated_data.pop('password', None)
        is_donor = validated_data.pop('is_donor', False)
        is_receiver = validated_data.pop('is_receiver', False)
        
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Properly hashes the password
        user.is_donor = is_donor
        user.is_receiver = is_receiver
        user.save()
        return user
class LimitedUserSerializer(serializers.ModelSerializer):
    """Custom serializer with conditional fields"""
    class Meta:
        """ Needed field """
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class ProofSerializer(serializers.ModelSerializer):
    """ Proof Serializer """
    class Meta:
        """ meta """
        model = Proof
        fields = ['id', 'donation', 'proof_image', 'uploaded_by']

class DonationSerializer(serializers.ModelSerializer):
    """ Donation serialize """
    proof = ProofSerializer(read_only=True)
    donor = LimitedUserSerializer(read_only=True)
    reserved_by = LimitedUserSerializer(read_only=True)
    class Meta:
        """ meta """
        model = Donation
        fields = ['id','donor', 'title', 'description',\
                   'location', 'is_reserved', 'is_delivered', 'created_at', \
                    'reserved_by', 'proof', 'status']

    def get_proof(self, obj):
        """ GET FULL URL """
        request = self.context.get('request')
        if obj.proof:
            return request.build_absolute_uri(obj.proof.url)
        return None
class DropOffSiteSerializer(serializers.ModelSerializer):
    """ Drop Serializer """
    added_by = UserSerializer(read_only=True)
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
