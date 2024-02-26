
from PIL import Image


# path = '/Users/dborstlap/Downloads/trying backup to try again/2023_10_21_qualy_BWSC_HPV1572 (1).jpg' # (wrong timezone)
# path = '/Users/dborstlap/Downloads/trying backup to try again/20231215_124345.jpg' # photo from phone (yes timezone)
# path = '/Users/dborstlap/Downloads/trying backup to try again/IMG_2222_SBN-zonder logo.JPG' # foto van onk surivalrun (no timezone)
# path = '/Users/dborstlap/Downloads/trying backup to try again/Australië (2)/DSCF4779.jpg' # ausi tour strand original no exif (no timezone)
# path = '/Users/dborstlap/Downloads/trying backup to try again/DSCF4779.jpg' # australie tour strand, modified time with samsung (yes timezone)
# path = '/Users/dborstlap/Downloads/trying backup to try again/IMG_6674.JPEG' # iphone image verdon (yes timezone)
# path = '/Users/dborstlap/Downloads/trying backup to try again/20231215_154823.jpg' # photo taken in AU at sunrise, to check time and time zone
# path = '/Users/dborstlap/Downloads/trying backup to try again/20221129_044609.heic' # .heic try
# path = '/Users/dborstlap/Downloads/trying backup to try again/20231215_170947.jpg' # peru time zone
# path = '/Users/dborstlap/Pictures/project mama/finished/1/1/00021127-2353-04.JPG' # picture previously sorted as '1-1-1' datetime
# path = '/Users/dborstlap/Pictures/project mama/finished/1/1/Z032-B33.jpg'


# with Image.open(path) as img:
#     exif1 = img._getexif()
#     exif2 = img.getexif()

#     print('exif1' , exif1.get(306), exif1.get(36867))
#     print('exif2' , exif2.get(306), exif2.get(36867))


local_dateTime_str = None.isoformat()
print(local_dateTime_str)



