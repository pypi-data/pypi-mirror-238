from pydicom import dcmread
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2

"""
    DCMIRead normalize a DICOM Image readed by a path or a binary file.
    * This module make you work easy when dealing with Dicom Images 
"""

def Read_Dicom_From_File(path : str, size : int =224, rescale : bool = True):
    """
    Read a Dicom Image from a path

    Args: 
        path: str
        size: int
        rescale: bool (True for rescale image array to 0-1 False for keep image array in range 0-255)
    
    Return: Image pixel array in range 0-1 or 0-255 in RGB format
    """


    dicom = dcmread(path, force=True)
    img = dicom.pixel_array

    # img is pixel_array.

    # Convert pixel_array (img) to -> gray image (img_2d_scaled)
    ## Step 1. Convert to float to avoid overflow or underflow losses.
    img_2d = img.astype(float)

    ## Step 2. Rescaling grey scale between 0-255
    img_2d_scaled = (np.maximum(img_2d,0) / img_2d.max()) * 255.0

    ## Step 3. Convert to uint
    img_2d_scaled = np.uint8(img_2d_scaled)

    ## Step 4. Convert to RGB
    im = Image.fromarray(img_2d_scaled)
    im = im.convert('RGB')

    ## Step 6. Image to Array
    im_array = np.array(im)
    im_array.shape

    ## Step 7. ReSize
    item = cv2.resize(im_array,dsize=(size,size), interpolation=cv2.INTER_CUBIC)

    ## Step 8. ReScale Values
    if rescale:
        item = item / 255

    return item

def Read_Dicom_From_Buffer(buffer : bytes, size : int =224, rescale : bool = True):
    
    """
    Read a Dicom Image from a buffer

    Args: 
        buffer: bytes
        size: int
        rescale: bool (True for rescale image array to 0-1 False for keep image array in range 0-255)
    
    Return: Image pixel array in range 0-1 or 0-255 in RGB format
    """
    
    dicom = dcmread(buffer, force=True)
    img = dicom.pixel_array

    # img is pixel_array.

    # Convert pixel_array (img) to -> gray image (img_2d_scaled)
    ## Step 1. Convert to float to avoid overflow or underflow losses.
    img_2d = img.astype(float)

    ## Step 2. Rescaling grey scale between 0-255
    img_2d_scaled = (np.maximum(img_2d,0) / img_2d.max()) * 255.0

    ## Step 3. Convert to uint
    img_2d_scaled = np.uint8(img_2d_scaled)

    ## Step 4. Convert to RGB
    im = Image.fromarray(img_2d_scaled)
    im = im.convert('RGB')

    ## Step 6. Image to Array
    im_array = np.array(im)
    im_array.shape

    ## Step 7. ReSize
    item = cv2.resize(im_array,dsize=(size, size), interpolation=cv2.INTER_CUBIC)

    ## Step 8. ReScale Values
    if rescale:
        item = item / 255

    return item

