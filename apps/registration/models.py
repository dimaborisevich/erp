from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)  

    # fields for all users
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    tg_nickname = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=150, blank=True, null=True) 
    
    # fields for students
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    instagram_nickname = models.CharField(max_length=255, blank=True, null=True)
    group_number = models.CharField(max_length=20, blank=True, null=True)
    points = models.IntegerField(default=0)
    student_status = models.CharField(
        max_length=50,
        choices=[
            ('studying', 'Учится'),
            ('academic_leave', 'В академ. отпуске'),
            ('returned', 'Возврат'),
            ('finished', 'Закончил обучение')
        ],
        blank=True, null=True
    )
    package = models.CharField(max_length=50, blank=True, null=True)
    internship_included = models.BooleanField(default=False)
    diploma_defended = models.BooleanField(default=False)
    
    # fields for teachers
    groups_teaching_now = models.CharField(max_length=255, blank=True, null=True)
    groups_taught_before = models.CharField(max_length=255, blank=True, null=True)
    teacher_comment = models.TextField(blank=True, null=True)
    teacher_status = models.CharField(
        max_length=50,
        choices=[
            ('working', 'Работает'),
            ('not_working', 'Не работает')
        ],
        blank=True, null=True
    )

    def __str__(self):
        return self.username

    

    