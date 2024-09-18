import time
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Signal receiver that adds a delay
@receiver(post_save, sender=User)
def slow_signal_receiver(sender, instance, **kwargs):
    print(f"Signal triggered for {instance.username} at: {datetime.datetime.now()}")
    time.sleep(5)  # Simulate a delay
    print(f"Signal processed at: {datetime.datetime.now()}")

# Simulating the creation of a user to trigger the signal
def create_user():
    print(f"User creation started at: {datetime.datetime.now()}")
    user = User.objects.create(username="testuser")
    print(f"User creation completed at: {datetime.datetime.now()}")

# Call the function to simulate user creation
create_user()
