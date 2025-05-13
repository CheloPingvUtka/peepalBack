from django.db import models
from django.db import models as django_models


class City(models.Model):
    city_name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.city_name

    class Meta:
        db_table = 'city'


class LocationCategory(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'location_category'


class Location(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ForeignKey relationships
    city = models.ForeignKey(City, on_delete=django_models.deletion.CASCADE)
    category = models.ForeignKey(LocationCategory, on_delete=django_models.deletion.CASCADE)
    user = models.ForeignKey('user.User', on_delete=django_models.deletion.CASCADE)

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'location'


class LocationChange(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    location = models.ForeignKey(Location, on_delete=django_models.deletion.CASCADE)
    user = models.ForeignKey('user.User', on_delete=django_models.deletion.CASCADE)
    field_name = models.CharField(max_length=50)
    old_value = models.JSONField()
    new_value = models.JSONField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    moderator_comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'location_change'


class Filter(models.Model):
    filter_name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(LocationCategory, on_delete=django_models.deletion.CASCADE)

    def __str__(self):
        return self.filter_name

    class Meta:
        db_table = 'filter'


class LocationFilter(models.Model):
    location = models.ForeignKey(Location, on_delete=django_models.deletion.CASCADE)
    filter = models.ForeignKey(Filter, on_delete=django_models.deletion.CASCADE)

    class Meta:
        db_table = 'location_filter'
