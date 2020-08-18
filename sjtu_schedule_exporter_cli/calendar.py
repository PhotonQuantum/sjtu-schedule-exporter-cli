import datetime
from typing import List

import arrow
from ics import Calendar, Event

from pysjtu.models import ScheduleCourse
from pysjtu.utils import flatten
from .utils import get_lesson_time


def schedule_to_ics(schedule, term_start_date: datetime.date) -> str:
    def lesson_to_events(lesson: ScheduleCourse) -> List[Event]:
        def lesson_week_to_event(week: int):
            lesson_day = term_start_date + datetime.timedelta(days=lesson.day + (week - 1) * 7 - 1)
            begin_time, end_time = get_lesson_time(list(lesson.time))
            e = Event()
            e.name = lesson.name
            e.begin = arrow.get(datetime.datetime.combine(lesson_day, begin_time, local_tz))
            e.end = arrow.get(datetime.datetime.combine(lesson_day, end_time, local_tz))
            e.location = lesson.location
            e.description = lesson.remark
            return e

        return [lesson_week_to_event(week) for week in list(flatten(lesson.week))]

    c = Calendar()
    local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    events = set(flatten(lesson_to_events(lesson) for lesson in schedule))
    c.events.update(events)
    return str(c)
