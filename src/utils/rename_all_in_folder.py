import os
from src.date_taken.sort_pictures import get_image_datetime, get_video_datetime, get_file_type

def rename_pictures_in_folder(dir_path):
    """
    Renames all pictures and videos in the given directory to a 'YYYY_MM_DD' format based on their metadata.
    """
    datetime_counts = {}
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            file_type = get_file_type(item_path)

            if file_type in ['image', 'video']:
                try:
                    if file_type == 'image':
                        file_datetime, _ = get_image_datetime(item_path)
                    else:  # video
                        file_datetime, _ = get_video_datetime(item_path)
                    
                    # date_str = file_datetime.strftime('%Y_%m_%d')
                    date_str = file_datetime.strftime('%Y%m%d-%H%M')

                    base_new_name = f"{date_str}{os.path.splitext(item)[1]}"

                    # Create a unique name by appending a counter if necessary
                    counter = datetime_counts.get(base_new_name, 0)
                    datetime_counts[base_new_name] = counter + 1


                    new_file_name = f"{date_str}_{counter}{os.path.splitext(item)[1]}"
                    new_path = os.path.join(dir_path, new_file_name)

                    
                    os.rename(item_path, new_path)
                    print(f"{item_path} renamed to {new_path}")
                except Exception as e:
                    print(f"Error processing {item_path}: {e}")



def rename_pictures_recursively(dir_path):
    """
    Recursively renames pictures in all directories and subdirectories starting from the given directory.
    """
    for root, dirs, files in os.walk(dir_path):
        rename_pictures_in_folder(root)

if __name__ == "__main__":
    dir_path = '/Users/dborstlap/Downloads/EXPEDITIE ABISKO 2024 foto en video'
    rename_pictures_recursively(dir_path)
    print('DONE')
