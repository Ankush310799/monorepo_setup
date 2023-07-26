from django.db import models
from users.models import User

Report_Types = (
    ('Misguide','Misguide'),
    ('Fake','Fake'),
    ('Misbehave','Misbehave'),
    ('other','other')
)

class Feed(models.Model):
    """ This contain feed details """
    title = models.CharField(max_length=320,null=False,blank=False)
    content	=models.TextField(max_length=500,null=False,blank=False)
    image = models.ImageField(upload_to ='downloads/',)
    created_by = models.ForeignKey(User,on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)


class ReportOnFeed(models.Model):
    """ Report of existed feed """
    feed = models.ForeignKey(Feed,on_delete=models.CASCADE)
    report = models.BooleanField(default=False)
    type = models.CharField(max_length=100,choices=Report_Types,default='other')
