from PIL import Image
import os, os.path, sys, time
import imageAffects

"""Settings"""

THUMBNAIL_SIZE = 1000
MIN_RESIZE = 0.8
CURSOR = "# "
WATERMARK_COLS = 16
WATERMARK_STYLE = "Corner"

#Directories
# - Path contains original photos
# - Watermarked contains original sized watermarked images
# - Thumbnails contains resized images
# TODO Add error handling for folder DNE
# TODO Add argumnet parsing
currentDir = os.getcwd()
path = currentDir + "/images"
watermarked = currentDir + "/fulls"
thumbnails = currentDir + "/thumbs"
mark = Image.open(currentDir + "/watermark.png")

imgs = [] #Count modified images
valid_images = [".jpg",".gif",".png",".tga"] #Valid format types

"""Methods"""

def loading(percent):
    """ Print Loading Screen

    Keyword arguments:
    percent -- completed / total (Converts to proper percent)
    """
    percent = str(int(percent*100))
    sys.stdout.write('\r' +f'{CURSOR}Processing... {percent}%')
    sys.stdout.flush()

"""Main loop"""

print(f"{CURSOR}Watermarking and resizing {len(os.listdir(path))} images")
print(f"{CURSOR}Thumbnail size average = {THUMBNAIL_SIZE}")

for i,f in enumerate(os.listdir(path)):
    #Print loading message
    loading(i/len(os.listdir(path)))

    #Check Extension
    ext = os.path.splitext(f)[1]
    if ext.lower() not in valid_images:
        continue

    #Open Image
    image = Image.open(os.path.join(path,f))

    #Add to array
    imgs.append(image)

    #Create Watermarked Copy
    imageAffects.watermark(image, mark, WATERMARK_STYLE, WATERMARK_COLS).save(watermarked + "/" + f)

    #Create Resized Thumbnail
    imageAffects.resize(image, THUMBNAIL_SIZE).save(thumbnails + "/" + f)

print()
print(f"{CURSOR}{len(imgs)} Images watermarked and resized")
print(f"{CURSOR}Done")
