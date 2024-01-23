from rest_framework import serializers
from .models import Document, User, DocumentFile,Path

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework import exceptions



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['name'] = user.name
    return token
  def validate(self, attrs):
    email = attrs.get('email', '')
    password = attrs.get('password', '')

    user = authenticate(request=self.context.get('request'), 
                        email=email, password=password)
    
    if user is None or not user.is_active:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')

    data = {}

    refresh = self.get_token(user)

    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)

    data['name'] = user.name
    
    return data
  

class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'



class DocumentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentFile
        fields = ['id', 'document', 'file']

    def validate_document(self, value):
        if not Document.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Invalid document ID.")
        return value



class DocumentSerializers(serializers.ModelSerializer):
  writer = UserSerializers()
  files = DocumentFileSerializer(many=True, read_only=True)

  class Meta:
    model = Document
    fields = '__all__'

class PathSerializers(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    documents = DocumentSerializers(many=True, read_only=True)

    def get_children(self, obj):
      children = obj.parent_paths.all()
      return PathSerializers(children, many=True).data
    
    class Meta:
      model = Path
      fields = ['id', 'current_path', 'children', 'documents']