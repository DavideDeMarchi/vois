import importlib.util
import sys
import warnings
import os

from argparse import ArgumentParser

absolute_path_to_vois = '/absolute/path/to/vois/init/file/__init__.py'


def main(warning_set: bool, path_vois: str):
    # Check if __init__ file exists
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
