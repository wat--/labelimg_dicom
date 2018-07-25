"""Get paths for calcium reports."""
import argparse
import os
import pickle
import re
import shutil

META_FILENAME = 'dicom_metadata.pkl'


def main(args):

    # Collect paths to all 3D lab reports
    acc2report = {}
    report_re = re.compile('3d\s?lab:\s+ca', flags=re.IGNORECASE)

    for base_path, _, _ in os.walk(args.input_dir):
        meta_path = os.path.join(base_path, META_FILENAME)
        if os.path.exists(meta_path):
            with open(meta_path, 'rb') as pkl_fh:
                series_infos = pickle.load(pkl_fh)
            for s in series_infos:
                m = report_re.search(s.description)
                if m is not None:
                    acc = int(base_path.split(os.path.sep)[5])
                    acc2report[acc] = s.dicom_paths

    for acc, report_dcms in acc2report.items():
        dst_dir = os.path.join(args.output_dir, str(acc))
        if os.path.exists(dst_dir):
            continue

        os.makedirs(dst_dir)
        for dcm in report_dcms:
            shutil.copy(dcm, dst_dir)
        print('Copied {} DICOMs from {}'.format(len(report_dcms), acc))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_dir', default='/Volumes/Pigeon/ccta/calcs')
    parser.add_argument('--output_dir', default='/Volumes/Pigeon/ccta/ca_reports')

    main(parser.parse_args())
