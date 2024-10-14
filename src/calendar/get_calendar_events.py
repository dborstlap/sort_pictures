# TODO when other google account is open, it gives error: Token has been expired or revoked
# TODO make sure/test if timezones are taken into account
# TODO with tan iphone cam take a .heic and .jpg at certain time and check if exif is utc time or local time?

# where was I: try get timezone from google calendar api
# trying to save events including timezone in the events.json file 
# trying ot check if camera images time is stored in utc or local timezone
# work on the if start <= picture <= end function!!



import datetime
import os.path
import json
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

CALENDAR_FOLDER = 'calendar_files/'
CREDENTIALS_FILE = CALENDAR_FOLDER + 'credentials.json'
TOKEN_FILE = CALENDAR_FOLDER + 'token.json'
EVENTS_FILE = CALENDAR_FOLDER + 'google_calender_events.json'


# transform timezone naive datetime to timezone aware datetime in iso format
def make_aware(datetime_naive_str, user_timezone):
    datetime_obj = datetime.datetime.fromisoformat(datetime_naive_str)
    if datetime_obj.tzinfo is None:
        datetime_obj_tz = user_timezone.localize(datetime_obj)
    else:
        datetime_obj_tz = datetime_obj
    return datetime.datetime.isoformat(datetime_obj_tz)


# Get all events in period from google calendar API
def get_events(start_date_obj, end_date_obj):

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # google calendar service
    service = build("calendar", "v3", credentials=creds)

    # get timezone
    calendar = service.calendars().get(calendarId='primary').execute()
    user_timezone = pytz.timezone(calendar['timeZone'])

    iso_datetime_str = "2023-06-01"
    datetime_obj = datetime.datetime.fromisoformat(iso_datetime_str)
    datetime_obj_mytz = user_timezone.localize(datetime_obj)

    # get events
    all_events = []

    start_date = start_date_obj.isoformat() + 'Z'
    end_date = end_date_obj.isoformat() + 'Z'

    page_token = None
    while True:
        events_result = service.events().list(calendarId='primary', 
                                                timeMin=start_date,
                                                timeMax=end_date, 
                                                pageToken=page_token,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
        events = events_result.get('items', [])
        all_events.extend(events)

        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    if not all_events:
        print('No events found.')
        return
    
    for event in all_events:
        if event['start'].get('date'):
            event['start']['dateTime'] = make_aware(event['start']['date'], user_timezone)
            event['end']['dateTime'] = make_aware(event['end']['date'], user_timezone)
        else:
            event['start']['dateTime'] = make_aware(event['start']['dateTime'], user_timezone)
            event['end']['dateTime'] = make_aware(event['end']['dateTime'], user_timezone)
            

    # Events retrieved
    print('All events retrieved in period', start_date_obj.date(), 'until', end_date_obj.date())
    return all_events


# Save all events to events.json file
def save_events(events):
    events_dict = {}
    for event in events:
        event_id = event['id']
        events_dict[event_id] = {
            'summary': event.get('summary', 'No Title'),
            'start': event['start'].get('dateTime'),
            'end': event['end'].get('dateTime'),
            'description': event.get('description', '')
        }

    # Writing the events to a JSON file
    with open(EVENTS_FILE, 'w') as file:
        json.dump(events_dict, file, indent=4)

    # events saved
    print('Events saved to', EVENTS_FILE)


# Load events from events.json into dict
def load_events(filename=EVENTS_FILE):
    try:
        with open(filename, 'r') as file:
            events = json.load(file)
        print('Loaded all events from file')
        return events
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {filename}.")
        return {}
    

# print all events in dict chronologically
def print_events(events):
    for event_id, event_details in events.items():
        start_date = event_details.get('start', '')
        end_date = event_details.get('end', '')
        event_name = event_details.get('summary', 'No Title')
        print(f"Start Date: {start_date}, End Date: {end_date}, Event: {event_name}")
    print('Done printing events')


# update the events.json file with new events
def update_calendar_events(start_date_input="1999-02-24", end_date_input=None):
    # define start and end date
    start_date_obj = datetime.datetime.strptime(start_date_input, '%Y-%m-%d')
    end_date_obj = datetime.datetime.strptime(end_date_input, '%Y-%m-%d') if end_date_input else datetime.datetime.utcnow()
    # retrieve events
    events = get_events(start_date_obj, end_date_obj)
    # save events
    save_events(events)
    print('calendar events updated')
    


if __name__ == "__main__":
    # Converting user input to datetime and formatting it for the API call
    start_date_obj = datetime.datetime.strptime("1999-02-24", '%Y-%m-%d')
    # end_date_obj = datetime.datetime.strptime("2015-02-24", '%Y-%m-%d')
    end_date_obj = datetime.datetime.utcnow()

    events = get_events(start_date_obj, end_date_obj)
    save_events(events)
    # events_dict = load_events()
    # print_events(events_dict)



