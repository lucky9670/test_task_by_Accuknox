from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models

# Example model for proving transaction handling
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="")

# Signal receiver that creates a Profile when a User is saved
@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    print(f"Signal triggered for user: {instance.username}")
    Profile.objects.create(user=instance)  # This will be rolled back if the transaction fails

# Simulate user creation inside a transaction
def create_user_with_rollback():
    try:
        with transaction.atomic():  # Start a transaction
            print("Transaction started.")
            user = User.objects.create(username="testuser")
            print("User created.")
            raise Exception("Forcing rollback!")  # Force a rollback to simulate an error
    except Exception as e:
        print(f"Transaction rolled back due to: {e}")

# Call the function to simulate user creation with a forced rollback
create_user_with_rollback()

# Check if the Profile was created in the database
print(Profile.objects.filter(user__username="testuser").exists())  # Should print False if rollback worked
