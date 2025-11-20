import os
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from filelock import FileLock, Timeout
from apscheduler.triggers.cron import CronTrigger
from automate_functions.run_both_task import run_both_tasks
from app_logging import logger

SCHED_TZ = pytz.timezone("Asia/Kolkata")
scheduler = AsyncIOScheduler(timezone=SCHED_TZ)
SCHED_LOCK_PATH = "/tmp/scheduler.lock"


def start_scheduler_guarded(): 
    if os.getenv("RUN_SCHEDULER", "0") != "1":
        print("[SCHEDULER] Skipped (RUN_SCHEDULER not set)", flush=True)
        return

    lock = FileLock(SCHED_LOCK_PATH)
    try:
        
        print("scheduler running...................................................")
        with lock.acquire(timeout=0):  # only one worker wins
        #     scheduler.add_job(
        #     run_both_tasks,
        #     CronTrigger(
        #         # day_of_week='mon',  # Every Monday
        #         hour=23,             # 12:00 AM
        #         minute=6,
        #         timezone=SCHED_TZ   # Asia/Kolkata
        #     ),
        #     id="run_both_tasks_monday_midnight",
        #     replace_existing=True
        # )
        
        
            scheduler.add_job(
                run_both_tasks,
                CronTrigger(
                    hour=16,              # 5 PM (24-hour format)
                    minute=51,            # :10
                    timezone=SCHED_TZ     # Asia/Kolkata
                ),
                id="run_both_tasks_now",
                replace_existing=True
            )

            

            scheduler.start()

            job = scheduler.get_job("run_both_tasks_now")
            print("[SCHEDULER] APScheduler started", flush=True)
            if job is not None:
                print("[SCHEDULER] Next run time:", job.next_run_time, flush=True)
            else:
                print("[SCHEDULER] Job not found!", flush=True)
    except Timeout:
        print("[SCHEDULER] Skipped (another worker owns the scheduler)", flush=True)
