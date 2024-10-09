from django.db import models

class Trip(models.Model):
    place_name = models.CharField(max_length=250)
    weather = models.CharField(max_length=200)
    
    # Location fields
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    
    google_map_link = models.URLField(max_length=200, blank=True, null=True)
    Trip_img = models.ImageField(upload_to='trip_images/')  # Changed to 'image' for clarity
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.place_name
