import subprocess
import time

def before_all(context):
    """
    Set up the mock OMDb provider before all tests.
    """
    subprocess.run(["docker-compose", "up", "-d", "db", "app", "nginx"], check=True)
    time.sleep(5)
    context.api_base = "http://localhost"

def after_all(context):
    subprocess.run(["docker-compose", "down"], check=True)