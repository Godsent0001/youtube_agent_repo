from datetime import datetime, timedelta
import time


# =========================
# CURRENT TIMESTAMP
# =========================
def now():
    return datetime.utcnow()


# =========================
# FORMAT TIME
# =========================
def format_datetime(dt: datetime):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


# =========================
# ADD MINUTES
# =========================
def add_minutes(minutes: int):
    return datetime.utcnow() + timedelta(minutes=minutes)


# =========================
# ADD HOURS
# =========================
def add_hours(hours: int):
    return datetime.utcnow() + timedelta(hours=hours)


# =========================
# CHECK IF PAST TIME
# =========================
def is_past(dt: datetime):
    return dt < datetime.utcnow()


# =========================
# SLEEP SAFE (WORKER FRIENDLY)
# =========================
def safe_sleep(seconds: float):
    time.sleep(seconds)


# =========================
# TIME DIFFERENCE
# =========================
def time_diff_seconds(start: datetime, end: datetime):
    return (end - start).total_seconds()


# =========================
# SCHEDULE NEXT RUN (DAILY POSTING)
# =========================
def next_daily_run(hour: int = 9):
    now_time = datetime.utcnow()
    next_run = now_time.replace(hour=hour, minute=0, second=0, microsecond=0)

    if next_run < now_time:
        next_run += timedelta(days=1)

    return next_run