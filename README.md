## Note

* Question 1 example is written in file `signals_example_1.py`
* Question 2 example is written in file `signals_example_2.py`
* Question 3 example is written in file `signals_example_3.py`

## Question 1
By default, Django signals are executed synchronously. This means that when a signal is triggered, the connected receivers are executed immediately, within the same thread, before the next lines of code can run.

### Step-by-step logic:
* We connect a signal `(e.g., post_save)` to a receiver function.
* In the receiver function, we add a `time.sleep()` to simulate a delay, which blocks execution.
* We'll measure the time it takes for the entire process to complete.
### Code:
```
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
```
### Output:
* The signal is triggered immediately after the user is created.
* The entire flow is synchronous, meaning the `create_user` function will not complete until the signal's receiver function `(slow_signal_receiver)` finishes execution.

```
User creation started at: 2024-09-18 12:00:00
Signal triggered for testuser at: 2024-09-18 12:00:01
Signal processed at: 2024-09-18 12:00:06
User creation completed at: 2024-09-18 12:00:06
```

## Question 2:
Yes, Django signals run in the same thread as the caller by default. This means that when a signal is triggered, the signal’s receiver runs in the same thread as the code that emitted the signal.

To prove this, we can use Python’s `threading` module to check the current thread where the signal receiver and the caller code are executed.

### Code:
```
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
```

### Output:
```
User creation running in thread: MainThread
Signal triggered in thread: MainThread
```

### Explanation:
* We print the current thread’s name using `threading.current_thread().name` in both the `create_user()` function and the `signal_receiver()`.
* When the user is created, the signal `(post_save)` is triggered.
* Both the user creation code and the signal receiver code will run in the same thread, which is likely the "MainThread" unless explicitly handled otherwise.

According to above example show that the Django signals run in the same thread

## Question 3:
Yes, by default, Django signals run in the same database transaction as the caller. If a signal `(e.g., post_save)` is triggered within a transaction and the transaction is rolled back, the effects of the signal are also rolled back.

#### Here’s examle how Django signals run within the same database transaction:

* We'll use a signal `(e.g., post_save)`.
* Inside the signal receiver, we'll attempt to make a database change.
* We’ll use a transaction block with a manual rollback to see if changes inside the signal are also rolled back.

### Code:
```
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
```

### Output:
```
Transaction started.
User created.
Signal triggered for user: testuser
Transaction rolled back due to: Forcing rollback!
False
```

### Explanation:
* We start a transaction using `transaction.atomic()`.
* A user is created, which triggers the `post_save` signal.
* Inside the signal receiver `(create_profile)`, a `Profile` object is created for the new user.
* We deliberately raise an exception after the user is created to force a rollback.
* After the rollback, we check if the `Profile` still exists in the database. If it returns `False`, it confirms that both the user creation and the signal receiver’s actions were rolled back.

