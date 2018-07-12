"""
Script to preload DICOM series info. Run this script overnight, then
loading a folder of DICOMs should take milliseconds instead of minutes
on a spinning disk hard drive.
"""

import argparse
import os
import pickle

from libs.dicom_io import DICOMReader

META_FILENAME = 'dicom_metadata.pkl'


def main(args):
    for base_path, _, file_names in os.walk(args.input_dir):
        dicom_names = [f for f in file_names if f.endswith(DICOMReader.suffix)]
        dicom_metadata = os.path.join(base_path, META_FILENAME)
        if len(dicom_names) > 0 and not os.path.exists(dicom_metadata):
            print('Collecting DICOMs in folder: {}'.format(base_path))
            series_infos = DICOMReader.scanAllDICOMs(base_path, check_preloaded=not args.do_overwrite)
            with open(dicom_metadata, 'wb') as pkl_fh:
                pickle.dump(series_infos, pkl_fh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_dir', type=str, required=True, help='Base directory to preload.')
    parser.add_argument('--do_overwrite', action='store_true', help='Overwrite previous metadata.')

    main(parser.parse_args())
