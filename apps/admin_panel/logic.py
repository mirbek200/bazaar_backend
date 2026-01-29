from collections import Counter
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractWeekDay, ExtractDay
from django.utils import timezone

from apps.announcement.models import Announcement, BannedAnnouncement
from apps.complaint_system.models import Complaint


def get_announcement_stats():
    now = timezone.now()

    today_data = (
        Announcement.objects
            .filter(created_at__date=now.date())
            .annotate(hour=ExtractHour('created_at'))
            .values('hour')
            .annotate(count=Count('id'))
    )

    today_labels = [f"{hour}:00" for hour in range(24)]
    today_counts = {data['hour']: data['count'] for data in today_data}
    today_data_formatted = [today_counts.get(i, 0) for i in range(24)]

    current_hour = now.hour
    previous_hour = (current_hour - 1) % 24
    percent_change = 0
    if today_counts.get(previous_hour, 0) != 0:
        percent_change = ((today_counts[current_hour] - today_counts[previous_hour]) / today_counts[
            previous_hour]) * 100

    week_data = (
        Announcement.objects
            .filter(created_at__week=now.isocalendar()[1], created_at__year=now.year)
            .annotate(day_of_week=ExtractWeekDay('created_at'))
            .values('day_of_week')
            .annotate(count=Count('id'))
    )

    start_of_week = now - timedelta(days=now.weekday())
    week_labels = [(start_of_week + timedelta(days=i)).strftime("%d.%m") for i in range(7)]
    week_counts = {data['day_of_week']: data['count'] for data in week_data}
    week_data_formatted = [week_counts.get(i + 2, 0) for i in range(7)]

    month_data = (
        Announcement.objects
            .filter(created_at__month=now.month, created_at__year=now.year)
            .annotate(day_of_month=ExtractDay('created_at'))
            .values('day_of_month')
            .annotate(count=Count('id'))
    )

    month_labels = [f"{i} {now.strftime('%b')}" for i in range(1, 31)]
    month_counts = {data['day_of_month']: data['count'] for data in month_data}
    month_data_formatted = [month_counts.get(i, 0) for i in range(1, 31)]

    return {
        "today": {
            "labels": today_labels,
            "data":  today_data_formatted,
        },
        "week": {
            "labels": week_labels,
            "data": week_data_formatted,
        },
        "month": {
            "labels": month_labels,
            "data": month_data_formatted,
        },
    }


def get_banned_announcements_stats():
    banned_announcements = BannedAnnouncement.objects.values('cause')

    # Use Counter to count occurrences of each cause
    cause_counts = Counter(complaint['cause'] for complaint in banned_announcements)

    # Calculate total number of complaints
    total_complaints = len(banned_announcements)

    # Display statistics
    context = {
        'cause_statistic': [
            {
                'cause': cause,
                'count': count,
                'percentage': round((count / total_complaints) * 100, 2),
            }
            for cause, count in cause_counts.items()
        ]
    }

    return context
