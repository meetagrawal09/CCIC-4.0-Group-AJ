# main.py
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


from tasks.tasks import add, multiply
from celery import group

# Create a group of tasks to execute in parallel
tasks = group([add.s(2, 2), multiply.s(3, 3)])

# Execute the group of tasks
result = tasks.apply_async()

# Wait for the tasks to complete
result.join()

# Get the result of each task
print(result.get())
