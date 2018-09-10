from apscheduler.schedulers.blocking import BlockingScheduler
import script

twische = BlockingScheduler()


@twische.scheduled_job('interval', minutes=60)
def timed_job():
    script.tweet()


if __name__ == "__main__":
    twische.start()