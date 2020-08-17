from django.db import models
from django.urls import reverse

# Create your models here.
# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager,
#                     self).get_queryset()  #\
                    # .filter(id=1) ##
                    # .filter(status='published') ## Not in this version of Django
                    # .filter(body='My first Blog') ##
                    # .filter(id='My first Blog') ##
                    # .filter(image='My first Blog') ##
                    # .filter(title='My first Blog') ##

class Blog(models.Model):
    # objects = models.Manager() # The default manager.
    # published = PublishedManager() # Our custom manager.

    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:250]   #[:100]

    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

    def get_absolute_url(self):
        return reverse('blog:detail', args=[blog_id])
    # From a "Django2 By Examples" Book
    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                                     args=[self.publish.year,
    #                                     self.publish.month,
    #                                     self.publish.day,
    #                                     self.slug])
