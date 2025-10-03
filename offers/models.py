from django.db import models

class Offer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    outlet = models.CharField(max_length=200, default="All Outlet")
    image = models.ImageField(upload_to="Offers/")
    button_text = models.CharField(max_length=50, default="View Details")
    button_link = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.title
