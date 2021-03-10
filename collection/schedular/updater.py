from apscheduler.schedulers.background import BackgroundScheduler
from collection import update_data,dividend_update


def start():
    scheduler = BackgroundScheduler()
    print("Starting....")
    scheduler.add_job(update_data.data_save, 'interval', minutes=3)
    scheduler.add_job(dividend_update.dividend, 'interval', minutes=3)
    scheduler.start()
    print(scheduler.print_jobs())
