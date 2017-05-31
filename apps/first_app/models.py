from __future__ import unicode_literals
from django.db import models
import bcrypt


# Create your models here.
class UserManager(models.Manager):
    def reg(self,postData):
        if len(postData['name']) < 3 or any(char.isdigit() for char in postData['name']):
            return {'error' : 'No fewer than 3 characters in Name; letters only'}
        elif len(postData['username']) < 3 or not any(char.isalpha() for char in postData['username']):
            return {'error' : 'No fewer than 3 characters in Username; at least one character'}
        elif len(postData['pwd']) < 8 or not any(char.isalpha() for char in postData['pwd']):
            return {'error': 'No fewer than 8 characters in password; at least one character'}
        elif len(postData['confirm_pwd']) < 8:
            return {'error': 'No fewer than 8 characters in confirm password'}
        elif postData['confirm_pwd'] != postData['pwd']:
            return {'error': 'No match password'}

        else:
            hashed_pw = bcrypt.hashpw(postData['pwd'].encode('utf-8'), bcrypt.gensalt())
            if User.objects.all().count() < 1:
                user_level = 9
            else:
                user_level = 1
            
            return {'theUser' : User.objects.create(name = postData['name'], username = postData['username'], password = hashed_pw) }

    def login(self, postData):
        if len(postData['username']) < 3 or not any(char.isalpha() for char in postData['username']):
            return {'error' : 'No fewer than 3 characters in Username; at least letters'}
        elif len(postData['pwd']) < 8 or not any(char.isalpha() for char in postData['pwd']):
            return {'error': 'No fewer than 8 characters in password; at least one character'}
        else:
            if User.objects.filter(username=postData['username']):
                stored_hash = User.objects.get(username=postData['username']).password
                input_hash = bcrypt.hashpw(postData['pwd'].encode(), stored_hash.encode())
                if not input_hash == stored_hash:
                    return {'error' : 'Wrong password'}
                else:
                    print "Success"
                    return { 'theUser' : User.objects.get(username=postData['username']) }  


class ItemManager(models.Manager):
    def add(self, postData):
        if len(postData['name']) < 3:
            return {'error' : 'No fewer than 3 characters in item'}
        else:
            return { 'Item' : Item.objects.create(name = postData['name'], user = postData['user'])}



class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name="items")
    items_to_user = models.ManyToManyField(User, related_name="user_wishlist")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ItemManager()
