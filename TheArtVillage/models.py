from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from decimal import Decimal
from django_countries.fields import CountryField


def generate_filename_art(self, filename):
    url = "Art/%s/Profile/%s" % (self.identification, filename)
    return url


def generate_filename_picture(self, filename):
    url = "Art/%s/%s" % (self.art, filename)
    return url


class MyDecimalField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        places = kwargs.get('decimal_places', 2)
        self.q = Decimal(10) ** -places

    def to_python(self, value):
        value = super(self.__class__, self).to_python(value)

        if isinstance(value, Decimal):
            return value.quantize(self.q)
        else:
            return value

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        places = kwargs.get('decimal_places', 2)
        self.q = Decimal(10) ** -places

    def to_python(self, value):
        value = super(self.__class__, self).to_python(value)

        if isinstance(value, Decimal):
            return value.quantize(self.q)

        else:
            return value


class Agent(models.Model):
    surname = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    phone = models.CharField(max_length=16)
    postcode = models.CharField(max_length=8, blank=True)
    email = models.CharField(max_length=128)
    fullname = models.CharField(max_length=256, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.fullname = self.firstname + " " + self.surname
        super(Agent, self).save(*args, **kwargs)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.fullname


class Artist(models.Model):
    surname = models.CharField(max_length=128)
    firstname = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    fullname = models.CharField(max_length=256, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.fullname = self.firstname + " " + self.surname
        super(Artist, self).save(*args, **kwargs)

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return self.fullname


class Art(models.Model):
    name = models.CharField(max_length=128, help_text="Enter the name of the piece of art")
    category = models.CharField(max_length=128)
    sub_category = models.CharField(max_length=128)
    artist_id = models.ForeignKey(Artist, help_text="Click magnifying glass to find correct artist")
    price = MyDecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    picture = models.ImageField(upload_to=generate_filename_art, blank=True)  # !!!!
    slug = models.SlugField(max_length=160, blank=True, editable=False)
    agent_id = models.ForeignKey(Agent, help_text="Click magnifying glass to find correct agent")
    identification = models.CharField(max_length=10, blank=True, editable=False)
    authenticate = models.CharField(max_length=64, blank=True, editable=False)
    weight = models.CharField(max_length=16, help_text="weight in kg")
    size = models.CharField(max_length=16, help_text="dimensions in cm")
    description = models.TextField(blank=True)
    artist = models.CharField(max_length=256, blank=True, editable=False)
    agent = models.CharField(max_length=256, blank=True, editable=False)
    special_delivery = models.BooleanField(default=False,
                                           help_text="check box if piece of art requires courier services (i.e. cannot be sent through mail)")
    postage_price = MyDecimalField(max_digits=10, decimal_places=2, default=0.00,
                                   help_text="Enter the price for postage in the UK, enter 0 if special delivery is required")

    def save(self, *args, **kwargs):
        self.authenticate = "pending"
        artist_name = self.artist_id.firstname + " " + self.artist_id.surname
        self.artist = artist_name

        agent_name = self.agent_id.firstname + " " + self.agent_id.surname
        self.agent = agent_name

        # Uncomment if you don't want the slug to change every time the name changes
        # if self.id is None:
        # self.slug = slugify(self.name)

        self.slug = slugify(self.name)
        super(Art, self).save(*args, **kwargs)

        self.price = Decimal(self.price).quantize(Decimal(10) ** -2)
        super(Art, self).save(update_fields=["price"])

        artid = str(self.id)
        agid = str(self.agent_id.id)

        if len(artid) < 6:
            for x in range(0, 6 - len(artid)):
                artid = "0" + artid

        if len(agid) < 4:
            for x in range(0, 4 - len(agid)):
                agid = "0" + agid

        self.identification = "ID" + agid + artid
        super(Art, self).save(update_fields=["identification"])

    def __unicode__(self):  # For Python 2, use __str__ on Python 3
        return str(self.identification) + " " + str(self.name)


class Image(models.Model):
    name = models.CharField(max_length=128, blank=True, editable=False)
    art = models.ForeignKey(Art, help_text="Click magnifying glass to find correct piece of art")
    additional_image = models.ImageField(upload_to=generate_filename_picture)

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
        self.name = str(self.art.identification)
        super(Image, self).save(update_fields=["name"])

    class Meta:
        ordering = ["additional_image"]

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(blank=True, max_length=100)
    surname = models.CharField(blank=True, max_length=100)
    country = CountryField(blank=True)
    city = models.CharField(blank=True, max_length=100)
    postcode = models.CharField(blank=True, max_length=32)
    address1 = models.CharField(blank=True, max_length=100)
    address2 = models.CharField(blank=True, max_length=100)

    def __unicode__(self):
        return self.user.username


class Orders(models.Model):
    payer_email = models.CharField(max_length=128)
    time = models.CharField(max_length=128)
    payment_date = models.DateField(max_length=128)
    buyer = models.OneToOneField(User)
    payment_gross = models.FloatField(max_length=128)
    payment_fee = models.FloatField(max_length=128)
    payment_net = models.FloatField(max_length=128)
    payment_status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Order"
