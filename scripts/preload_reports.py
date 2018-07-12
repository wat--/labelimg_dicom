"""
Script to verify that a cohort is present and preloaded on disk.
"""

import argparse
import os
import pandas as pd

from libs.constants import META_FILENAME, REPORT_FILENAME
from libs.dicom_io import DICOMReader


def main(args):
    df = pd.read_csv(args.cohort_csv)
    cohort = [(int(row['AccessionID']), row['Report']) for _, row in df.iterrows()]

    # Verify there's a dir for every accession in the cohort
    num_missing = 0
    for acc, report in cohort:
        example_dir = os.path.join(args.input_dir, str(acc))
        if not os.path.exists(example_dir):
            num_missing += 1
            print('{}'.format(acc))
        else:
            for base_path, _, file_names in os.walk(example_dir):
                dicom_names = [f for f in file_names if f.endswith(DICOMReader.suffix)]
                if len(dicom_names) > 0:
                    with open(os.path.join(base_path, REPORT_FILENAME), 'w') as fh:
                        fh.write(report)

    print('Total missing: {}'.format(num_missing))

    # Verify every dir present in the cohort is preloaded
    num_unloaded = 0
    for base_path, _, file_names in os.walk(args.input_dir):
        dicom_names = [f for f in file_names if f.endswith(DICOMReader.suffix)]
        dicom_metadata = os.path.join(base_path, META_FILENAME)
        if len(dicom_names) > 0 and not os.path.exists(dicom_metadata):
            num_unloaded += 1
            print('Not preloaded: {}'.format(base_path))
    print('Total unloaded: {}'.format(num_unloaded))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_dir', type=str, required=True, help='Base directory to verify.')
    parser.add_argument('--cohort_csv', type=str, required=True, help='CSV file with cohort information.')

    main(parser.parse_args())
