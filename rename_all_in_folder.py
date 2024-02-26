import os

dir = 'T:/Pictures/DISKS/Group030/Disc34/ZIM-MOZ/Deel6'
from PIL import Image, ExifTags
from sort_pictures import get_image_datetime, get_video_datetime


# Iterate directory
for rel_path in os.listdir(dir):

    path = os.path.join(dir, rel_path)

    # check if current path is a file
    if os.path.isfile(path):

        file_name, file_extension = os.path.splitext(rel_path)

        # check if file is image
        try:
            is_image = True
            img = Image.open(path)
        except:
            is_image = False
        
        is_video = file_extension in ('.MP4', '.mp4', '.AVI', '.avi')
        img.close()

        if is_image or is_video:

            if is_image:
                datetime = get_image_datetime(path)
            elif is_video:
                datetime = get_video_datetime(path)
            
            date = datetime.strftime('%Y_%m_%d')

            # new_file_name = file_name + '111'
            new_file_name = date
            new_file_path = new_file_name + file_extension

            # print(path, 'replaced by', os.path.join(dir, new_file_path))
            os.replace(path, os.path.join(dir, new_file_path))
            print(rel_path, 'renamed as', new_file_path)