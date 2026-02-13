from django.db import models

# Create your models here.
class VisitorActivity(models.Model):
    # IP address ko unique kiya taaki duplicate na rahe
    ip_address = models.GenericIPAddressField(unique=True) 
    
    # Session key ab unique nahi hogi kyunki hum IP ko overwrite kar rahe hain
    session_key = models.CharField(max_length=100, null=True, blank=True)
    
    pages_visited = models.PositiveIntegerField(default=1)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)

    def duration(self):
        return self.last_seen - self.first_seen

    def __str__(self):
        return f"{self.ip_address} - Pages: {self.pages_visited}"