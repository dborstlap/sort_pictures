# TODO make seperate get_timetaken function
# TODO check if samsung change time function changes exif, or something else

# TODO create 'make_sure' function that for all files in folder, writes the guessed datetime based on os.path into the exif data.
# TODO getexif instead of _getexif()??? For normal image can getexif produce exif when there is no _getexif?

# TODO make utils file. Put all functions like 'get_exif_datetime' and 'datetime_to_string' in this file, instead of spread out between all files

# TODO include dir_target input variable to indiciate where the sorted imgs should go to


import os
from datetime import datetime
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from PIL import Image
from pillow_heif import register_heif_opener
register_heif_opener()

# define in which directories it will be sorted
FOLDER_SORTED = 'sorted'
FOLDER_IMAGES = 'images'
FOLDER_VIDEOS = 'videos'
FOLDER_OTHER = 'other files'
FOLDER_NOT_SURE = 'not sure'


def get_file_type(file_path):
    # check if file is an image
    try:
        with Image.open(file_path) as img:
            img.verify()
            return 'image'
    except:
        pass

    # check if file is an video    
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']
    if file_path.lower().endswith(tuple(video_extensions)):
        return 'video'

    # if not image or video, it is other file
    return 'other'


def parse_exif_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except (TypeError, ValueError):
        return None

# TODO should not return none I think
def get_datetime_from_exif(exif):
    exif_DateTime = parse_exif_date(exif.get(306))  # datetime picture made (or file changed)
    exif_DateTimeOriginal = parse_exif_date(exif.get(36867))  # datetime original (=datetime taken)
    exif_OffsetTime_str = exif.get(36880)  # offset datetime (=time zone)

    if exif_DateTime and exif_DateTimeOriginal:
        local_dateTime = min(exif_DateTime, exif_DateTimeOriginal)
    elif exif_DateTime:
        local_dateTime = exif_DateTime
    elif exif_DateTimeOriginal:
        local_dateTime = exif_DateTimeOriginal

    # add timezone if available, else assume and add local timezone
    if exif_OffsetTime_str:
        local_dateTime_str = local_dateTime.isoformat()
        global_dateTime_str = local_dateTime_str + exif_OffsetTime_str
        img_dateTime = datetime.fromisoformat(global_dateTime_str)
    else:
        img_dateTime = local_dateTime.astimezone()
        print(img_dateTime)
        print('check if datetime is unchanged and local timezone is added.')
    return img_dateTime


def get_datetime_from_path(file_path):
    time_stamp_modify = os.path.getmtime(file_path)
    time_stamp_create = os.path.getctime(file_path)
    time_stamp_access = os.path.getatime(file_path)

    # earliest time stamp (most often getmtime()) is good guess for image/video taken date
    earliest_time_stamp = min(time_stamp_modify, time_stamp_create, time_stamp_access)
    datetime_obj = datetime.fromtimestamp(earliest_time_stamp)
    return datetime_obj.astimezone()

def get_image_datetime(image_path):
    # first try getting datetime using exif
    try:
        # if heif image
        if image_path.lower().endswith('.heic') or image_path.lower().endswith('.heif'):

            with Image.open(image_path) as img:
                exif = img.getexif()

            # Handle HEIF/HEIC format
            # heif_file = pyheif.read(image_path)
            # for metadata in heif_file.metadata or []:
            #     if metadata['type'] == 'Exif':
            #         # The Exif data is in bytes, need to convert it to an Image object
            #         exif = Image._getexif(Image.open(io.BytesIO(metadata['data'])))

        # if normal image type
        else:
            with Image.open(image_path) as img:
                exif = img._getexif()

        # transform exif data into datetime object with timezone info
        img_dateTime = get_datetime_from_exif(exif)
        sure = True

    # try getting datetime using file manager 
    except:
        img_dateTime = get_datetime_from_path(image_path)
        sure = False
    return img_dateTime, sure
    

def get_video_datetime(video_path):
    try:
        parser = createParser(video_path)
        metadata = extractMetadata(parser)
        local_dateTime = metadata.get('creation_date')
        vid_dateTime = local_dateTime.astimezone() # add timezone info
        sure = True
    except:
        vid_dateTime = get_datetime_from_path(video_path)
        sure = False
    return vid_dateTime, sure


def get_sort_path(file_dateTime, dir_sorted, dir_not_sure, sure, sort_by):
    if sort_by == 'year':
        sort_dir = str(file_dateTime.year)
    elif sort_by == 'month':
        sort_dir = str(file_dateTime.year) + '/' + str(file_dateTime.month)
    elif sort_by == 'day':
        sort_dir = str(file_dateTime.year) + '/' + str(file_dateTime.month) + '/' + str(file_dateTime.day)

    # if unsure of datetime sort in 'not sure' folder based on guessed dateTime. Otherwise sort in 'sorted' folder 
    sort_path = (dir_sorted if sure else dir_not_sure) + sort_dir

    if not os.path.exists(sort_path):
        os.makedirs(sort_path)

    return sort_path


# where the real magic happens
def sort_by_date(dir_to_sort, orig=True, dir_orig=None, sort_by='month'):

    if sort_by not in ['year', 'month', 'day']:
        raise ValueError("sort_by must be 'year', 'month', or 'day'")

    if orig == True:
        dir_orig = dir_to_sort
    dir_sorted = dir_orig + '/' + FOLDER_SORTED + '/'
    dir_sorted_ims = dir_sorted + FOLDER_IMAGES + '/'
    dir_sorted_vids = dir_sorted + FOLDER_VIDEOS + '/'
    dir_other_files = dir_sorted + FOLDER_OTHER + '/'
    dir_not_sure_ims = dir_sorted_ims + FOLDER_NOT_SURE + '/'
    dir_not_sure_vids = dir_sorted_vids + FOLDER_NOT_SURE + '/'


    # lists to store files and folders
    files = []
    folders = []

    # Iterate directory
    for path in os.listdir(dir_to_sort):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_to_sort, path)):
            files.append(path)
        elif os.path.isdir(os.path.join(dir_to_sort, path)):
            if not (orig and os.path.normpath(os.path.join(dir_to_sort, path)) == os.path.normpath(dir_sorted)):
                folders.append(path)
        else:
            print('wtf happened here this is not right, this is not a file nor a folder how tf is that possible:' + str(os.path.join(dir_to_sort, path)))


    for file in files:
        path = os.path.join(dir_to_sort, file)
        file_type = get_file_type(path)
        
        # sort images
        if file_type == 'image':
            img_dateTime, img_sure = get_image_datetime(path)
            print(path)
            sort_path = get_sort_path(img_dateTime, dir_sorted_ims, dir_not_sure_ims, img_sure, sort_by)
            os.replace(path, os.path.join(sort_path, file))
            print('image', file, 'sorted in folder', sort_path)

        # sort video files by date
        elif file_type == 'video':
            vid_dateTime, vid_sure = get_video_datetime(path)
            sort_path = get_sort_path(vid_dateTime, dir_sorted_vids, dir_not_sure_vids, vid_sure, sort_by)
            os.replace(path, os.path.join(sort_path, file))
            print('video', file, 'sorted in folder', sort_path)

        # put all other files together in folder
        else:
            if not os.path.exists(dir_other_files):
                os.makedirs(dir_other_files)
            os.replace(path, os.path.join(dir_other_files, file))
            print('other file', file, 'sorted in folder', dir_other_files)

    for folder in folders:
        sort_by_date(os.path.join(dir_to_sort, folder), orig=False, dir_orig=dir_orig)

    print('directory ', dir_to_sort, ' is sorted')
    return


if __name__ == "__main__":
    dir_to_sort = '/Users/dborstlap/tmp/DISKS best of'
    sort_by_date(dir_to_sort, sort_by='month')
    print('DONE')








