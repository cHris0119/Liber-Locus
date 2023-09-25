from rest_framework import serializers
from .models import *


class userSerializer(serializers.ModelSerializer):
    class Meta:
        Model = User
        fields = '__all__'
        
class roleSerializer(serializers.ModelSerializer):
    
    class Meta:
        Model: Role
        fields = '__all__'
        
class userRoleSerializer(serializers.ModelSerializer):
    
    class Meta:
        Model: UserRole
        fields = '__all__'
        

