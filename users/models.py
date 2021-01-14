from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
import string
from django.utils.text import slugify
import random
from Securities.models import Stock

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    company = models.CharField(max_length = 500, blank = True, default = "")
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    cover_image = models.ImageField(upload_to='profile_pics', default='default.jpg')

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Portfolio(models.Model):
    portfolio_name = models.CharField(max_length = 50, blank = False, default = "")
    portfolio_author = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    portfolio_symbols = models.ManyToManyField(Stock)

    class Meta:
        verbose_name_plural = "Portfolio"

    def __str__(self):
        return self.portfolio_name

    def get_absolute_url(self):
        return reverse('portfolio-detail', kwargs={'slug': self.slug})

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.portfolio_name)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug = slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug, randstr = random_string_generator(size = 4))

        return unique_slug_generator(instance, new_slug = new_slug)
    return slug

def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender = Portfolio)
