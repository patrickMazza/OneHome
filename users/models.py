from django.db import models
from django.utils import timezone  # Import timezone for DateTimeField
from django.contrib.auth.models import User  # Import User model
from PIL import Image
from datetime import datetime
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import datetime
from django.urls import reverse
from .validators import validate_file_extension
from django.core.files.storage import default_storage

from django.core.validators import MaxValueValidator, MinValueValidator


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    # If a user created the post is deleted, posts are deleted as well.ß
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # __str__() method returns how the Post is printed
    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Override the save method of the model
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize image
            # Save it again and override the larger image
            img.save(self.image.path)


class ClientProfile(models.Model):
    first_Name = models.CharField(max_length=30)
    last_Name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, null=True, max_length=250)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client_Intake_Date = models.DateField()
    image = models.ImageField(default='default.jpg', upload_to='client_pics')
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_Name} {self.last_Name}\'s Client Profile'

    # Override the save method of the model
    def get_absolute_url(self):
        return reverse("client_page", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        super(ClientProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image

        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  # Resize image
            # Save it again and override the larger image
            img.save(self.image.path)


def get_now():
    return datetime.now().strftime("%-m/%-d/%Y %-I:%M:%S %p")


class Application2010e_part1(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)
    application_Name = models.CharField(max_length=100, null=True)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    housing_Program = models.CharField(blank=True, max_length=100, null=True)
    applicant_Name = models.CharField(blank=True, max_length=100, null=True)
    application_ID = models.IntegerField(blank=True, null=True)
    referring_Agency = models.CharField(blank=True, max_length=100, null=True)
    referring_Site = models.CharField(blank=True, max_length=100, null=True)
    date_time = models.DateTimeField(blank=True, null=True)
    consent = models.BooleanField(verbose_name="I verify the applicant has signed the \"New York City Human Resources Administration HIPAA Compliant Authorization for Disclosure of Individual Health Information and Medicaid Records for the Coordinated Assessment Survey and/or Supportive Housing Application\” and the \“New York City Human Resources Administration Authorization for the Coordinated Assessment Survey (CAS) and/or Supportive Housing Application\" consents. I also verify that these two consents have been signed within the last 180 days authorizing the release of the applicant\’s health information, including his or her medical, mental health, HIV related, alcohol and substance use treatment, Cash Assistance, Supplemental Nutritional Assistance Program and prior supportive housing/coordinated assessment records and that my agency has on file the original form signed by the applicant.")
    consent_Date = models.DateField(blank=True, null=True)
    verified_By = models.CharField(max_length=100, blank=True, null=True)
    location_Kept = models.CharField(max_length=100, blank=True, null=True)
    supportive_type = models.CharField(blank=True, max_length=300, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Application2010e_part2(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)

    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    updated_at = models.DateTimeField(auto_now=True)


class Application2010e_part3(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)

    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    updated_at = models.DateTimeField(auto_now=True)


class Application2010e_part4(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)

    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    updated_at = models.DateTimeField(auto_now=True)


class Application2010e_part5(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)

    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    updated_at = models.DateTimeField(auto_now=True)


class Application2010e_part6(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)

    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    slug = models.SlugField(unique=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class Application2010e_part7(models.Model):
    done = models.BooleanField()
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)

    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    slug = models.SlugField(unique=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClientApplication(models.Model):
    caseworker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)
    application_Name = models.CharField(max_length=100)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])

    slug = models.SlugField(unique=True, null=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    part1_id = models.ForeignKey(Application2010e_part1,
                                 on_delete=models.CASCADE)
    part2_id = models.ForeignKey(Application2010e_part2,
                                 on_delete=models.CASCADE)
    part3_id = models.ForeignKey(Application2010e_part3,
                                 on_delete=models.CASCADE)
    part4_id = models.ForeignKey(Application2010e_part4,
                                 on_delete=models.CASCADE)
    part5_id = models.ForeignKey(Application2010e_part5,
                                 on_delete=models.CASCADE)
    part6_id = models.ForeignKey(Application2010e_part6,
                                 on_delete=models.CASCADE)
    part7_id = models.ForeignKey(Application2010e_part7,
                                 on_delete=models.CASCADE)


class Docs(models.Model):
    application = models.CharField(max_length=500)
    client = models.ForeignKey(ClientProfile,
                               on_delete=models.CASCADE)
    document_Name = models.CharField(max_length=500)
    file_field = models.FileField(upload_to='client_docs', validators=[
                                  validate_file_extension])
