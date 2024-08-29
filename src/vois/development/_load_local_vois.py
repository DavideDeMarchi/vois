# Instructions:
# 1. Copy this file in this folder renaming it 'load_local_vois.py'
# 2. In the created 'load_local_vois.py' change the 'absolute_path_to_vois' accordingly
# Changes in the 'load_local_vois.py' will not be detected (thanks .gitignore) a.k.a. sensitive info in path are secured

import importlib.util
import sys
import warnings
import os
from argparse import ArgumentParser

absolute_path_to_vois = '/absolute/path/to/vois/init/file/__init__.py'


def main(warning_set: bool, path_vois: str):
    # Check if __init__ file exists
    if os.path.basename(path_vois) != '__init__.py':
        raise FileNotFoundError(f'You are not pointing to a __init__.py file {path_vois}')
    if not os.path.exists(path_vois):
        raise FileNotFoundError(f'Could not find {path_vois}')

    # Load local vois library as python package
    spec = importlib.util.spec_from_file_location("vois", path_vois)
    module = importlib.util.module_from_spec(spec)
    sys.modules['vois'] = module
    spec.loader.exec_module(module)

    # Disable warnings
    if warning_set:
        warnings.filterwarnings("ignore", category=DeprecationWarning)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-w", "--warning-off",
                        action='store_const',
                        dest="warning",
                        help="Disable warning messages",
                        required=False,
                        const=True,
                        default=False)
    parser.add_argument("-p", "--path-local-vois",
                        action='store',
                        dest='path_vois',
                        help="Absolute path to local vois library __init__.py file",
                        type=str,
                        required=False,
                        default=absolute_path_to_vois)

    args = parser.parse_args()
    main(warning_set=args.warning, path_vois=args.path_vois)
