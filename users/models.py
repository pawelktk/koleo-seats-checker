from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class SpecialCompartmentType(models.Model):
    """Model reprezentujący typy przedziałów specjalnych z KOLEO."""
    name = models.CharField(max_length=100)
    koleo_id = models.IntegerField(unique=True, help_text="ID używane w API KOLEO")

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Profil użytkownika z dodatkowymi ustawieniami."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_start_station = models.CharField(max_length=100, blank=True)
    default_end_station = models.CharField(max_length=100, blank=True)
    allowed_compartments = models.ManyToManyField(
        SpecialCompartmentType, blank=True
    )

    def __str__(self):
        return f"Profil użytkownika {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()