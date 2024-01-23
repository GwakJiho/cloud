from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
  name = models.CharField(max_length=64, blank=True)
  email = models.EmailField(unique=True, null=True)
  password = models.CharField(null=True, max_length=128 ,default=None)
  
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=True)
  is_active = models.BooleanField(default=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []  

  objects = UserManager()
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


