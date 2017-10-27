from django.db import models


# Create your models here.
def file_path(instance, filename):
    '''
    file will be uploaded to MEDIA_ROOT/user_id/file_name
    :param instance: an instance of this class
    :param filename: the original file name
    :return: the path to the file
    '''
    return 'files/{0}'.format(filename)


class SiteFiles(models.Model):
    '''
    files to be saved and used on the site
    '''
    file_name = models.CharField(max_length=200)
    file = models.FileField(upload_to=file_path)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
