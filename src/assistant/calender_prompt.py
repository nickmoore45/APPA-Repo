import dateparser
import pytz
import re
from datetime import datetime, timedelta

# Define the Eastern Time Zone
eastern = pytz.timezone('America/New_York')

def resolve_next_this(date_str, base_date=datetime.now(eastern)):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_weekday = base_date.weekday()
    
    if 'next' in date_str:
        target_day = date_str.split()[-1].capitalize()
        if target_day in weekdays:
            days_ahead = (weekdays.index(target_day) - current_weekday) % 7
            days_ahead += 7  # Ensure it's next week
            next_date = base_date + timedelta(days=days_ahead)
            return next_date.strftime('%Y-%m-%d')
    
    if 'this' or 'on' in date_str:
        target_day = date_str.split()[-1].capitalize()
        if target_day in weekdays:
            days_ahead = (weekdays.index(target_day) - current_weekday) % 7
            this_date = base_date + timedelta(days=days_ahead)
            return this_date.strftime('%Y-%m-%d')
    
    return base_date.strftime('%Y-%m-%d')

def parse_calendar_prompt(prompt, base_date=datetime.now(eastern)):
    text = prompt.lower().replace('hey calendar', '')
    event_pattern = r'(?:add\s+)?(?:i\s+have\s+)?(.+?)(?:\s+at|\s+on|\s+to\s+my\s+schedule|$)'
    time_pattern = r'at\s+(\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?)'
    date_pattern = r'(next\s+\w+|\w+day|on\s+\w+day|this\s+\w+day|tomorrow|on\s+\w+\s+\d{1,2}(?:th|st|nd|rd)?(?:\s+at)?|march\s+\d{1,2}(?:th|st|nd|rd)?)'

    event_match = re.search(event_pattern, text)
    time_match = re.search(time_pattern, text)
    date_match = re.search(date_pattern, text)

    event = event_match.group(1) if event_match else 'Unknown Event'
    time_str = time_match.group(1) if time_match else '9:00 am'
    date_str = resolve_next_this(date_match.group(1) if date_match else base_date.strftime('%A'), base_date)

    datetime_str = f"{date_str} {time_str}"
    event_datetime = dateparser.parse(datetime_str, settings={'TIMEZONE': 'America/New_York', 'TO_TIMEZONE': 'America/New_York', 'RETURN_AS_TIMEZONE_AWARE': True})

    if event_datetime is None:
        print(f"Error parsing date and time from input: '{datetime_str}'")
        return None

    start_time = event_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    end_time = (event_datetime + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')

    event = event.replace(" add ", "").replace(" i have a ", "").replace(" i have ", "").capitalize()

    return {
        'summary': event,
        'start_time': start_time,
        'end_time': end_time
    }




