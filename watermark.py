from PIL import Image
import os, os.path, sys, time

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

def getCorner(image, mark):
    x = image.size[0]-mark.size[0]
    y = image.size[1]-mark.size[1]
    return [x, y]


def watermark(image):
    """ Add Watermark to Image

    Keyword arguments:
    image -- PIL image
    """
    # Make temp copies
    temp_image = image.copy()
    temp_mark = mark.copy()

    # Apply the watermark

    if(WATERMARK_STYLE == "Checker"):
        temp_mark = resize(temp_mark, temp_image.size[0]/WATERMARK_COLS, 1)

        for i in range(0, temp_image.size[0], temp_mark.size[0]):
            for j in range(0, temp_image.size[1], temp_mark.size[1]):
                temp_image.paste(temp_mark, (i, j), temp_mark)
    else: # No style implies "Corner" style
        temp_image.paste(temp_mark, getCorner(temp_image, temp_mark),temp_mark)

    return temp_image

def resize(image, size, minResize = MIN_RESIZE):
    """ Resize Image

    Keyword arguments:
    image -- PIL image
    size -- Average size for height and width
    minResize -- The minimum percent that the image with be resized by (Default is MIN_RESIZE)
    """
    width,height = image.size

    #Reduce amount bring height and width down to an average of size
    reduce_amount = size / ((width + height) / 2 )
    #Ensure all images are resized to at least min resize
    if reduce_amount > minResize:
        reduce_amount = minResize

    #Resized dimensions
    new_width = int(width * reduce_amount)
    new_height = int(height * reduce_amount)

    #Returned resized image
    return image.resize(( new_width, new_height ))

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
    watermark(image).save(watermarked + "/" + f)

    #Create Resized Thumbnail
    resize(image, THUMBNAIL_SIZE).save(thumbnails + "/" + f)

print()
print(f"{CURSOR}{len(imgs)} Images watermarked and resized")
print(f"{CURSOR}Done")
