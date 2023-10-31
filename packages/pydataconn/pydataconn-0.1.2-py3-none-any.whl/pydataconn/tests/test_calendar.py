import os
import pytz
import pandas as pd
from datetime import datetime
from pydataconn import Calendar


if __name__ == '__main__':

    start_date = datetime.now(pytz.utc).isoformat()
    
    calendar = Calendar(os.getenv("GOOGLE_CALENDAR_ID"))
    events = calendar.list_events(start_date=start_date)

    # Extract the event date and name from the list of dicts
    event_name = [event['summary'] for event in events]
    event_date = [event['start']['date'] for event in events]
    df = pd.DataFrame({
        'Date': event_date,
        'Event Name': event_name
    })
    print(df)