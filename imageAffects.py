from PIL import Image


def getCorner(image, mark):
    x = image.size[0]-mark.size[0]
    y = image.size[1]-mark.size[1]
    return [x, y]


def watermark(image, mark, style = "Corner", cols = 12):
    """ Add Watermark to Image

    Keyword arguments:
    image -- PIL image
    """
    # Make temp copies
    temp_image = image.copy()
    temp_mark = mark.copy()

    # Apply the watermark

    if(style == "Checker"):
        temp_mark = resize(temp_mark, temp_image.size[0]/cols, 1)

        for i in range(0, temp_image.size[0], temp_mark.size[0]):
            for j in range(0, temp_image.size[1], temp_mark.size[1]):
                temp_image.paste(temp_mark, (i, j), temp_mark) #TODO Add correct PNG usage with customizable opacity
    else: # No style implies "Corner" style
        temp_image.paste(temp_mark, getCorner(temp_image, temp_mark),temp_mark)

    return temp_image

def resize(image, size, minResize = 0.8):
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