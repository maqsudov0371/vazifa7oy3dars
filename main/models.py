from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=13, blank=True, null=True, db_index=True)
    auth_code = models.CharField(max_length=6, blank=True)

    def __str__(self) -> str:
        return f"{self.username}"

class Category(models.Model):
    title = models.CharField(max_length=25)
    
    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField(max_length=25)
    
    def __str__(self):
        return self.title

class Course(models.Model):
    LANGUAGES = (
        ('EN', 'English'),
        ('RU', 'Russian'),
        ('UZ', 'Uzbek'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    duration = models.DurationField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    language = models.CharField(max_length=100, blank=True, choices=LANGUAGES)
    rating = models.PositiveBigIntegerField(default=0)
    image = models.ImageField(upload_to='images/', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.subject}'
