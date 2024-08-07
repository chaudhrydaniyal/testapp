from django.db import models
import uuid
import markdown
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from tinymce.models import HTMLField


class Source(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    detail_mode = models.BooleanField(default=False)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, serialize=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.user.source_set.count() >= self.user.num_of_sources:
    #         raise ValidationError(
    #             f"User '{self.user.username}' has reached the maximum number of sources.")
    #     super().save(*args, **kwargs)

    def count_topics(self):
        return self.topics.count()


class Topic(models.Model):
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=255, null=True, blank=True)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, serialize=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Document(models.Model):
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, related_name='documents', blank=True)
    raw_title = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(
        max_length=255, blank=True, null=True, default='')
    image_alt = models.CharField(
        max_length=255, blank=True, null=True, default='')
    meta_description = models.CharField(
        max_length=255, blank=True, null=True, default='')
    image = models.ImageField(
        upload_to='document_images/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, serialize=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        # self._set_order()
        # self._clean_fields()
        super().save(*args, **kwargs)

    def _create_passage(self):
        if not self.id:
            return

        if not Passage.objects.filter(document=self).exists():
            Passage.objects.create(document=self, header='default')


class SharedLink(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    link = models.CharField(max_length=150, null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    count_visits = models.PositiveIntegerField(default=0)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, serialize=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # fixing name in admin panel because it named in plural

    class Meta:
        verbose_name = 'Shared Link'
        verbose_name_plural = 'Shared Links'

    def __str__(self):
        return self.link

    def save(self, *args, **kwargs):
        if self.is_active and self.count_visits < 0:
            # Perform some additional logic before saving
            # For example, set count_visits to 0 if it is negative
            self.count_visits = 0
        super().save(*args, **kwargs)

    @classmethod
    def get(cls, link_id):
        shared_link = cls.objects.get(id=link_id)
        if shared_link.is_active:
            # Increment the visit count
            shared_link.count_visits += 1
            shared_link.save()
        return shared_link


class Passage(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, null=True, blank=True)
    header = models.CharField(
        max_length=255, blank=True, null=True, default="")
    header_level_choices = [
        ('H1', 'H1'),
        ('H2', 'H2'),
        ('H3', 'H3'),
        ('H4', 'H4'),
        ('H5', 'H5'),
        ('H6', 'H6'),
    ]
    header_level = models.CharField(
        max_length=2, choices=header_level_choices, null=True, blank=True, default="H1")
    anchor_text = models.CharField(max_length=255, blank=True, null=True)
    anchor_url = models.CharField(max_length=255, blank=True, null=True)
    context = HTMLField(null=True, blank=True, default="")
    summer_note = HTMLField(null=True, blank=True, default="")
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, serialize=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def summer_To_markdown(self):
        return markdown.markdown(self.summer_note, extensions=["markdown.extensions.fenced_code"])

    def get_doc(self):
        return self.document


class Accessability(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True)
    term = models.CharField(max_length=150, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True, default=101)
    volume = models.IntegerField(null=True, blank=True, default=0)
    traffic = models.IntegerField(default="0")
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    id = models.UUIDField(default=uuid.uuid4, primary_key=True,
                          editable=False, serialize=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.term

    def save(self, *args, **kwargs):
        if not self.id:
            self.order = Accessability.objects.filter(
                document=self.document).count() + 1

        super().save(*args, **kwargs)
