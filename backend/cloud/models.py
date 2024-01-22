from django.db import models

# Create your models here.

class User(models.Model):
  name = models.CharField(max_length=64)

  def __str__(self):
    return self.name

# 파일 경로 : 문서와 또 다른 경로를 포함
class Path(models.Model):
  parent_path = models.ForeignKey('self',
                                on_delete=models.CASCADE, 
                                null=True, blank=True, 
                                related_name='parent_paths') 
  current_path = models.CharField(max_length=256)

  def __str__(self):
    return self.current_path
  
class Document(models.Model):
  title = models.CharField(max_length=256)
  abstract = models.TextField(null=True)
  publication_date = models.DateField()
  research_fund = models.IntegerField(null=True)
  writer = models.ForeignKey(User, on_delete=models.CASCADE)
  #파일의 경로 추가
  path = models.ForeignKey(Path, on_delete=models.CASCADE, 
                          related_name='documents',
                          null=True, blank=True)

  def __str__(self):
    return self.title


class DocumentFile(models.Model):
  document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='files')
  #path = models.ForeignKey(Path,on_delete=models.CASCADE, related_name="path")
  file = models.FileField(upload_to='upload', null=True, blank=True)


