# Copyright (c) 2018 Christopher Chute
# Create by Christopher Chute <chutechristopher@gmail.com>

import numpy as np
import pydicom

try:
    from PyQt5.QtGui import QImage, qRgb
except ImportError:
    from PyQt4.QtGui import QImage, qRgb


class DICOMReader(object):
    def __init__(self):
        raise NotImplementedError('DICOMReader is a static class.')

    @classmethod
    def read(cls, dicom_path, w_center=None, w_width=None):
        """Read a DICOM file from `file_path`.

        Args:
            dicom_path: Path to read DICOM file from.
            w_center: Center for window to apply. If None, don't apply window.
            w_width: Width for window to apply. If None, don't apply window.

        Returns:
            QImage image data for DICOM file, windowed if `w_center` and `w_width` are not None.

        Raises:
            RuntimeWarning: If cannot find DICOM file at the given `dicom_path`.
        """
        # Read DICOM from disk
        try:
            with open(dicom_path, 'rb') as dicom_fh:
                dcm = pydicom.dcmread(dicom_fh)
        except IOError:
            raise RuntimeWarning('Could not find DICOM at path {}'.format(dicom_path))

        # Convert to raw Hounsfield Units and apply window
        pixels = cls._dicomToRaw(dcm)
        if w_center is not None and w_width is not None:
            pixels = cls._applyWindow(pixels, w_center, w_width)

        # Convert to QImage
        image_data = cls._toQImage(pixels)

        return image_data

    @classmethod
    def isDICOMFile(cls, file_name):
        """Check if file is a DICOM file.

        Not robust: only checks that the file ends with '.dcm'.

        Args:
            file_name: Name of file to check.
        """
        return file_name.endswith('.dcm')

    @staticmethod
    def _dicomToRaw(dcm, dtype=np.int16):
        """Convert a DICOM object to a Numpy array of raw Hounsfield Units.
        Scale by the RescaleSlope, then add the RescaleIntercept (both DICOM header fields).
        Args:
            dcm: DICOM object.
            dtype: Type of elements in output array.
        Returns:
            ndarray of shape (height, width). Pixels are `int16` raw Hounsfield Units.
        See Also:
            https://www.kaggle.com/gzuidhof/full-preprocessing-tutorial
        """
        img_np = dcm.pixel_array.astype(dtype)

        # Set outside-of-scan pixels to 0
        img_np[img_np == -2000] = 0

        intercept = dcm.RescaleIntercept
        slope = dcm.RescaleSlope

        if slope != 1:
            img_np = slope * img_np.astype(np.float64)
            img_np = img_np.astype(dtype)

        img_np += int(intercept)
        img_np = img_np.astype(np.int16)

        return img_np

    @staticmethod
    def _applyWindow(img, w_center, w_width):
        """Apply a window to raw Hounsfield Units to get a PNG.

        Args:
            img: Raw Hounsfield Units for every pixel.
            w_center: Center of window to apply (e.g. 40 Hounsfield Units).
            w_width: Total width of window to apply (e.g. 400 Hounsfield Units).

        Returns:
            Single-byte pixel values for the Hounsfield Units image as a windowed greyscale image.
        """

        # Convert to float
        img = np.copy(img).astype(np.float64)

        # Clip to min and max values
        w_max = w_center + w_width / 2
        w_min = w_center - w_width / 2
        img = np.clip(img, w_min, w_max)

        # Normalize to uint8
        img -= w_min
        img /= w_width
        img *= np.iinfo(np.uint8).max
        img = img.astype(np.uint8)

        return img

    @staticmethod
    def _toQImage(arr, do_copy=False):
        """Convert NumPy ndarray to QImage format.
        
        Taken from:
            https://gist.github.com/smex/5287589
        
        Args:
            arr: NumPy array to convert.
            do_copy: If true, copy the QImage file before returning.

        Returns:
            QImage formatted image.
        """
        if arr is None:
            return QImage()

        gray_color_table = [qRgb(i, i, i) for i in range(256)]

        # TODO: Possibly add this line? `im = np.require(im, np.uint8, 'C')`
        if arr.dtype == np.uint8:
            if len(arr.shape) == 2:
                qim = QImage(arr.data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_Indexed8)
                qim.setColorTable(gray_color_table)
                return qim.copy() if do_copy else qim

            elif len(arr.shape) == 3:
                if arr.shape[2] == 3:
                    qim = QImage(arr.data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_RGB888)
                    return qim.copy() if do_copy else qim
                elif arr.shape[2] == 4:
                    qim = QImage(arr.data, arr.shape[1], arr.shape[0], arr.strides[0], QImage.Format_ARGB32)
                    return qim.copy() if do_copy else qim

        raise NotImplementedError('Unsupported image format.')
