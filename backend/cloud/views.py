import logging

from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

#rest
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

#직렬화
from .serializers import DocumentSerializers, UserSerializers, DocumentFileSerializer, PathSerializers, MyTokenObtainPairSerializer
from .models import Document, User, DocumentFile, Path

#페이지네이션
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

#날짜
from .utils import convert_to_date

from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(['GET'])
def hello_world(request):
  return Response("Hello. World!")


class DocumentView(viewsets.ViewSet):
  pagination_class = PageNumberPagination  #페이지네이션 활성화
  filter_backends = [SearchFilter, OrderingFilter]
  search_fields = ['title', 'writer']
  ordering_fields = ['publication_date', 'research_fund']  #페이지 네이션 검색, 정렬 설정
  queryset = Document.objects.all()
  serializers_class = DocumentSerializers

  def get_queryset(self):
      queryset = self.queryset

      title = self.request.query_params.get('title', None)
      writer = self.request.query_params.get('writer', None)

      if title:
        queryset = queryset.filter(title__icontains=title)
      if writer:
        queryset = queryset.filter(writer__icontains=writer)
    

      ordering = self.request.query_params.get('ordering', None)
      if ordering:
        queryset = queryset.order_by(ordering)

      return queryset

  def list(self, request, *args, **kwargs):
      queryset = self.get_queryset()
      paginator = PageNumberPagination()
      paginated_queryset = paginator.paginate_queryset(queryset, request)
      serializer = self.serializers_class(paginated_queryset, many=True)

      return paginator.get_paginated_response(serializer.data)

  def retrieve(self, request, pk=None):
    document = get_object_or_404(self.queryset.all(), pk=pk)
    serializer = self.serializers_class(document)
    return Response(serializer.data)
  
  def create(self, request, *args, **kwargs):
    serializer = self.serializers_class(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

  def update(self, request, pk=None):
    documnet = get_object_or_404(self.queryset, pk=pk)
    serializer = self.serializers_class(documnet, data=request)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=400)
  
  def destroy(self, request, pk=None):
    documnet = get_object_or_404(self.queryset, pk=pk)
    documnet.delete()
    return Response(status=204)
  


class UserView(viewsets.ViewSet):
  queryset = User.objects.all()
  serializers_class = UserSerializers
  
  def list(self, request):
    serializer = self.serializers_class(self.queryset.all(), many=True)
    return Response(serializer.data, status= 201)
  def retrieve(self, request):
    return 0
  
  def create(self, request):
    serializer = self.serializers_class(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
  
  def update(self, request):
    return 0
  
  def destroy(self, request, pk=None):
    documnet = get_object_or_404(self.queryset, pk=pk)
    documnet.delete()
    return Response(status=204)



class DocumentFileViewSet(viewsets.ModelViewSet):
    queryset = DocumentFile.objects.all()
    serializer_class = DocumentFileSerializer

    def create(self, request, *args, **kwargs):
        document_data = request.data.get('document')
        files_data = request.data.get('files')

        # Create Document instance
        document_serializer = DocumentSerializers(data=document_data)
        if document_serializer.is_valid():
            document = document_serializer.save()

            # Create DocumentFile instances associated with the document
            for file_data in files_data:
                file_data['document'] = document.id
                file_serializer = DocumentFileSerializer(data=file_data)
                if file_serializer.is_valid():
                    file_serializer.save()

            return Response(document_serializer.data, status=201)
        else:
            return Response(document_serializer.errors, status=404)
        

class PathViewSet(viewsets.ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializers

    def list(self, request):
      serializer = self.serializer_class(self.queryset.all(), many=True)
      return Response(serializer.data, status= 201)
    

    def create(self, request, *args, **kwargs):
      parent_id = request.data.get('parent_id')
      folder_name  = request.data.get('folder_name')
      
      parent_path = Path.objects.get(pk=parent_id) if parent_id else None

      path = Path(parent_path=parent_path, current_path=folder_name)  # 약간 헷갈리긴 하는데 
      # current_path 가 folder_name
      path.save()

      serializer = self.serializer_class(path)
      return Response(serializer.data, status=201)

@csrf_exempt
def document_upload_view(request):
  if request.method == 'POST':
    title = request.POST['title']
    publication_date = request.POST['workdate']
    path = request.POST['pathid']
    writer_id = request.POST['worker']
    abstract = request.POST['abstract']

    path_obj = get_object_or_404(Path, id=path)

    document = Document(
        title=title,
        publication_date=convert_to_date(publication_date),
        writer_id = writer_id,
        abstract = abstract,
        path = path_obj
    )
    document.save()

    for file in request.FILES.getlist('files'):
        DocumentFile.objects.create(document=document, file=file)

    return JsonResponse({'status': 'success', 'document_id': document.id})

  return JsonResponse({'status': 'error'}, status=400)


