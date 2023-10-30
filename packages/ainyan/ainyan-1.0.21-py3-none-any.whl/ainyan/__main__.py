
import argparse
import os

import datasets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare and upload dataset to s3')
    parser.add_argument('--source', metavar='path', required=True,
                        help='the path to workspace')
    parser.add_argument('--dspath', required=True,
                        help='the path to save the dataset (either local or s3://)')
    # only required when
    parser.add_argument('--profile', required=False,
                        help='aws profile to use for upload')
    args = parser.parse_args()
    os.environ['AWS_PROFILE'] = args.profile
    lib.dataset_preprocess(args.source, args.dspath)