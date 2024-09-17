from django.db import models

# Create your models here.

class Video(models.Model):
    video_title= models.CharField(max_length=255)
    video_file= models.FileField(upload_to='videos/')
    uploaded_at= models.DateTimeField(auto_now_add=True)
    processed_flag= models.BooleanField(default=False)

class Subtitle(models.Model):
    video= models.ForeignKey(Video, on_delete= models.CASCADE)
    language= models.CharField(max_length=10, default='en')
    text= models.TextField()
    timestamp= models.TimeField() #this timestamp stores the time value for pharase ocurrence time