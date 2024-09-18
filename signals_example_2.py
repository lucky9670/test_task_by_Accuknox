import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Signal receiver function that prints the current thread
@receiver(post_save, sender=User)
def signal_receiver(sender, instance, **kwargs):
    print(f"Signal triggered in thread: {threading.current_thread().name}")

# Function that creates a user and prints the thread where it's running
def create_user():
    print(f"User creation running in thread: {threading.current_thread().name}")
    user = User.objects.create(username="testuser")

# Call the function to create a user
create_user()
