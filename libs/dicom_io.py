# Copyright (c) 2018 Christopher Chute
# Create by Christopher Chute <chutechristopher@gmail.com>

import numpy as np
import os
import pickle
import pydicom

from libs.constants import META_FILENAME
from tqdm import tqdm
try:
    from PyQt5.QtGui import QImage, qRgb
except ImportError:
    from PyQt4.QtGui import QImage, qRgb

DCM_EXT = 'dcm'


class DICOMReader(object):

    suffix = DCM_EXT

    def __init__(self):
        raise NotImplementedError('DICOMReader is a static class.')

    @classmethod
    def getQImage(cls, dicom_path, w_width=None, w_level=None):
        """Read a DICOM file from `file_path`.

        Args:
            dicom_path: Path to read DICOM file from.
            w_width: Width for window to apply. If None, don't apply window.
            w_level: Center for window to apply. If None, don't apply window.

        Returns:
            QImage image data for DICOM file, windowed if `w_center` and `w_width` are not None.

        Raises:
            RuntimeWarning: If cannot find DICOM file at the given `dicom_path`.
        """
        # Read DICOM from disk
        dcm = cls.readRawDICOM(dicom_path)

        # Convert to raw Hounsfield Units and apply window
        pixels = cls._dicomToRaw(dcm)
        if w_level is not None and w_width is not None:
            pixels = cls._applyWindow(pixels, w_level, w_width)

        # Convert to QImage
        q_image = cls._toQImage(pixels)

        return q_image

    @classmethod
    def isDICOMFile(cls, file_name):
        """Check if file is a DICOM file.

        Not robust: only checks that the file ends with '.dcm'.

        Args:
            file_name: Name of file to check.
        """
        return file_name.endswith('.%s' % cls.suffix)

    @staticmethod
    def readRawDICOM(dicom_path, stop_before_pixels=False):
        """Read a raw DICOM from disk.

        Args:
            dicom_path: Path to DICOM file to read.
            stop_before_pixels: If true, stop reading before pixel_data.
            Used for fast loading when you only need metadata.

        Returns:
            DICOM object.

        Raises:
            RuntimeWarning: If cannot find DICOM file at the given `dicom_path`.
        """
        try:
            with open(dicom_path, 'rb') as dicom_fh:
                dcm = pydicom.dcmread(dicom_fh, stop_before_pixels=stop_before_pixels)
        except IOError:
            raise RuntimeWarning('Could not load DICOM at path {}'.format(dicom_path))

        return dcm

    @staticmethod
    def scanAllDICOMs(folderPath, check_preloaded=True):
        """Scan a directory tree for DICOMs.

        Args:
            folderPath: Root of directory tree to scan for DICOMs.
            check_preloaded: If true, check for preloaded metadata files to speed loading.
            See scripts/preload_dicoms.py for more info.

        Returns:
            List of tuples each of format (series_number, description, num_images, height, width, path_list).
        """
        if check_preloaded:
            # Check for preloaded metadata to speed up loading.
            series_infos = []
            for base_path, _, file_names in os.walk(folderPath):
                if META_FILENAME in file_names:
                    with open(os.path.join(base_path, META_FILENAME), 'rb') as pkl_fh:
                        try:
                            preloaded_series_info = pickle.load(pkl_fh)
                        except ValueError:
                            # Unsupported pickle version. Load all info from scratch.
                            series_infos = []
                            break
                    series_infos += preloaded_series_info
            if len(series_infos) > 0:
                return series_infos

        # No preloaded info
        series2info = {}
        for base_path, _, file_names in os.walk(folderPath):
            dcm_names = set(f for f in file_names if f.endswith('.%s' % DICOMReader.suffix))
            for dcm_name in tqdm(dcm_names):
                # Check if DICOM matches a series already seen
                dcm = DICOMReader.readRawDICOM(os.path.join(base_path, dcm_name), stop_before_pixels=True)
                series_key = (int(dcm.SeriesNumber),
                              int(dcm.Rows) if 'Rows' in dcm else 0,
                              int(dcm.Columns) if 'Columns' in dcm else 0)
                if series_key not in series2info:
                    # Add new series
                    series_num, height, width = series_key
                    description = dcm.SeriesDescription if 'SeriesDescription' in dcm else 'None'
                    series2info[series_key] = DICOMSeriesInfo(series_num, height, width, description)

                # Add DICOM to series
                series_info = series2info[series_key]
                instance_num = dcm.InstanceNumber if 'InstanceNumber' in dcm else 0
                series_info.add_dicom(instance_num, os.path.abspath(os.path.join(base_path, dcm_name)))

        # Construct list of DICOMSeriesInfo objects
        series_infos = [series2info[k] for k in sorted(series2info.keys())]

        return series_infos

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


class DICOMSeriesInfo(object):
    def __init__(self, series_num, height, width, description):
        self.series_num = series_num
        self.height = height
        self.width = width
        self.description = description
        self.num_images = 0
        self.dicom_paths = []
        self.instance_nums = []
        self.is_sorted = True

    def __len__(self):
        return self.num_images

    def add_dicom(self, instance_num, dicom_path):
        """Add a DICOM to this series.

        Args:
            dicom_path: Absolute path to DICOM file.
        """
        if instance_num in self.instance_nums:
            print('Warning: Ignoring duplicate instance in series: {}'.format(dicom_path))
            return

        self.is_sorted = False
        self.num_images += 1
        self.instance_nums.append(instance_num)
        self.dicom_paths.append(dicom_path)

    def sorted_paths(self):
        """Get list of DICOM paths sorted by instance number."""
        if not self.is_sorted:
            self.instance_nums, self.dicom_paths = zip(*sorted(zip(self.instance_nums, self.dicom_paths),
                                                               key=lambda x: x[0]))
            self.is_sorted = True

        return self.dicom_paths

    def to_str(self):
        """Get a string that can be displayed in a QT dialog window."""
        s = '(Series %d) "%s" [%d x %d x %d]' % (self.series_num, self.description,
                                                 self.height, self.width, self.num_images)

        return s
