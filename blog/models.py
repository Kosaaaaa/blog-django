from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title)

        has_slug = Post.objects.filter(slug=slug).exists()
        count = 1

        while has_slug:
            count += 1
            slug = slugify(instance.title) + '-' + str(count)
            has_slug = Post.objects.filter(slug=slug).exists()

        instance.slug = slug


pre_save.connect(pre_save_post_receiver, sender=Post)
