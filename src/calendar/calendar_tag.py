# TODO ensure image.close() is used everywhere properly

# TODO document: Some pictures are stored in local time (samsung images) without timezone info. Others are stored in UTC (I think), nuna quali Australia images taken on 02:33h for example. When edit Datetime with samsung: exif[36867] (=datetimeorinal) is edited. Other exif not edited. Iphone pictures do have exif.
# TODO document: pictures datetime original = local time , timezone = offset time
# TODO document: iso string format = localtime + offset (but local time+offset!=utc time, local time-offset=utctime)

# TODO make function to be able to easily change/add exif time to pictures

import os
import piexif
from PIL import Image
from datetime import datetime
from get_calendar_events import load_events
from src.date_taken.sort_pictures import get_image_datetime


def get_events_at_datetime(events, specific_datetime):
    events_at_time = []
    for event_id, event_details in events.items():

        start_date_iso = event_details.get('start')
        end_date_iso = event_details.get('end')
        start_dateTime = datetime.fromisoformat(start_date_iso)
        end_dateTime = datetime.fromisoformat(end_date_iso)

        if start_dateTime <= specific_datetime <= end_dateTime:
            events_at_time.append(event_details.get('summary', 'No Title'))
    return events_at_time

# TODO check if picture tag is persistent between windows and mac
# TODO write description exif?, or keywords exif? which exif key best to use?
def tag_photo_with_event(photo_path, event_name):
    try:
        image = Image.open(photo_path)
        exif_dict = piexif.load(image.info['exif'])

        # Add or update the image description tag in the EXIF data
        exif_dict['0th'][piexif.ImageIFD.ImageDescription] = event_name.encode('utf-8')

        exif_bytes = piexif.dump(exif_dict)
        image.save(photo_path, exif=exif_bytes)
    except Exception as e:
        print(f"Error tagging photo {photo_path}: {e}")


def main():
    events = load_events()
    for photo_path in os.listdir('.'):  # Assuming photos are in the current directory
        if photo_path.lower().endswith(('.jpg', '.jpeg')):
            photo_taken_time = get_photo_taken_time(photo_path)
            if photo_taken_time:
                for event in events:
                    if event['start'] <= photo_taken_time <= event['end']:
                        tag_photo_with_event(photo_path, event['name'])
                        print(f"Tagged {photo_path} with event: {event['name']}")
                        break

if __name__ == "__main__":

    # update_calendar_events()

    # path = '/Users/dborstlap/Downloads/trying backup to try again/2023_10_21_qualy_BWSC_HPV1572 (1).jpg' # (wrong timezone)
    # path = '/Users/dborstlap/Downloads/trying backup to try again/20231215_124345.jpg' # photo from phone (yes timezone)
    # path = '/Users/dborstlap/Downloads/trying backup to try again/IMG_2222_SBN-zonder logo.JPG' # foto van onk surivalrun (no timezone)
    # path = '/Users/dborstlap/Downloads/trying backup to try again/Australië (2)/DSCF4779.jpg' # ausi tour strand original no exif (no timezone)
    # path = '/Users/dborstlap/Downloads/trying backup to try again/DSCF4779.jpg' # australie tour strand, modified time with samsung (yes timezone)
    path = '/Users/dborstlap/Downloads/trying backup to try again/IMG_6674.JPEG' # iphone image verdon (yes timezone)
    # path = '/Users/dborstlap/Downloads/trying backup to try again/20231215_154823.jpg' # photo taken in AU at sunrise, to check time and time zone
    # path = '/Users/dborstlap/Downloads/trying backup to try again/20221129_044609.heic' # .heic try
    # path = '/Users/dborstlap/Downloads/trying backup to try again/20231215_170947.jpg' # peru time zone
    # path = '/Users/dborstlap/Pictures/project mama/finished/1/1/00021127-2353-04.JPG' # picture previously sorted as '1-1-1' datetime
    # path = '/Users/dborstlap/Pictures/project mama/finished/1/1/Z032-B33.jpg'



    events = load_events()
    img_dateTime, sure = get_image_datetime(path)
    events_at_time = get_events_at_datetime(events, img_dateTime)
    print(events_at_time)
    print('DONE')



