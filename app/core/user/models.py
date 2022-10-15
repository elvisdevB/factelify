from tokenize import group
from django.contrib.auth.models import AbstractUser
from django.forms import model_to_dict
from django.db import models
from factelify.settings.development import MEDIA_URL
from factelify.settings.base import STATIC_URL
from datetime import datetime
from crum import get_current_request


# Create your models here.
class User(AbstractUser):
    img = models.ImageField(upload_to='user/%Y/%m/%d', null=True, blank=True)
    token = models.UUIDField(primary_key=False, editable=False, null=True, blank=True)

    def get_img(self):
        if self.img:
            return '{}{}'.format(MEDIA_URL,self.img)
        return '{}{}'.format(STATIC_URL,'img/empty.png')
    
    def toJSON(self):
        self.last_login = datetime.now()
        item = model_to_dict(self, exclude=['password','user_permissions','last_login'])
        if self.last_login:
            item['last_login'] = self.last_login
        item['date_joined'] = self.last_login
        item['img'] = self.get_img()
        item['full_name'] = self.get_full_name()
        item['groups'] = [{'id': g.id, 'nombre':g.name} for g in self.groups.all()]
        return item 
    
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
