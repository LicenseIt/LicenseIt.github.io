from django.db import models


# Create your models here.
class ContactData(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.full_name, self.email, self.text)
