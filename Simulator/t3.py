from models.tasks import test_task
result = test_task.delay()
print(result)