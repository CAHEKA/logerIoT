from app import app, scheduler


def scheduleTask():
    print("This test runs every 30 seconds")


scheduler.add_job(id='Scheduled Task', func=scheduleTask, trigger="interval", seconds=30)
scheduler.start()
