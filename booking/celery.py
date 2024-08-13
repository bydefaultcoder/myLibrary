from celery.schedules import crontab

app.conf.beat_schedule = {
    'update-booking-status-every-day': {
        'task': 'your_app_name.tasks.update_booking_status',
        'schedule': crontab(hour=0, minute=0),  # Runs every day at midnight
    },
}
