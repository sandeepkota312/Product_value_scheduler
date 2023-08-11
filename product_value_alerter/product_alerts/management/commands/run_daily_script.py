from django.core.management.base import BaseCommand
import schedule
import time
import sys
sys.path.append("../../")

def my_daily_task():
    # Your script logic here
    print("Running the daily script!")

class Command(BaseCommand):
    help = 'Runs a daily script'

    def handle(self, *args, **options):
        schedule.every().day.at("02:00").do(my_daily_task)  # Adjust the time as needed

        while True:
            schedule.run_pending()
            time.sleep(1)
