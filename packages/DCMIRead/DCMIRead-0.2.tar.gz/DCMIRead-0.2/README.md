
# DCMIRead

DCMIRead is a Python package designed to facilitate the reading and normalization of DICOM images. It provides two primary functions that return a normalized image array, making it an invaluable tool for those working with DICOM images.

## Primary Functions

* `Read_Dicom_From_File(path: str, size: int=224, rescale: bool=True)`: This function reads a DICOM image from a file. The `path` parameter specifies the file path of the DICOM image. The `size` parameter sets the size of the output image, and defaults to 224. The `rescale` parameter determines whether the image should be rescaled, and defaults to True.
* `Read_Dicom_From_Buffer(buffer: str, size: int=224, rescale: bool=True)`: This function reads a DICOM image from a buffer. The `buffer` parameter specifies the buffer containing the DICOM image data. The `size` and `rescale` parameters function as described above.

## Usage

Whether you’re reading from a file or a buffer, DCMIRead makes it easy to obtain a normalized image array from your DICOM data. This can be particularly useful in medical imaging applications where DICOM is commonly used.

Please note that both functions return a normalized image array, ensuring consistency in your image data.

With DCMIRead, handling DICOM images has never been easier!
