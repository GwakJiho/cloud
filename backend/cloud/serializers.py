from rest_framework import serializers
from .models import Document, User, DocumentFile,Path


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