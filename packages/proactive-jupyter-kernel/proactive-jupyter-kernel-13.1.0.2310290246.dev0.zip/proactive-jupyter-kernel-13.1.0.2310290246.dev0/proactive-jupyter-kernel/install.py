import json
import os
import sys
import argparse

import urllib

from jupyter_client.kernelspec import KernelSpecManager
from IPython.utils.tempdir import TemporaryDirectory


kernel_json = {"argv": [sys.executable, "-m", "proactive-jupyter-kernel", "-f", "{connection_file}"],
               "display_name": "ProActive",
               "language": "python",
               "codemirror_mode": "python"
               }


def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
            git_url = "https://raw.githubusercontent.com/ow2-proactive/proactive-jupyter-kernel/" \
                      "master/proactive-jupyter-kernel/"
            urllib.request.urlretrieve(os.path.join(git_url, 'logo-32x32.png'), os.path.join(td, 'logo-32x32.png'))
            urllib.request.urlretrieve(os.path.join(git_url, 'logo-64x64.png'), os.path.join(td, 'logo-64x64.png'))
            urllib.request.urlretrieve(os.path.join(git_url, 'logo-128x128.png'), os.path.join(td, 'logo-128x128.png'))
        # TODO: Copy resources once they're specified

        print('Installing IPython kernel spec')
        try:
            KernelSpecManager().install_kernel_spec(td, 'ProActive', user=user, prefix=prefix)
            print('Successfully installed ProActive kernel!')
        except Exception as e:
            print(str(e))


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Install KernelSpec for ProActive Kernel'
    )
    prefix_locations = parser.add_mutually_exclusive_group()

    prefix_locations.add_argument(
        '--user',
        help='Install KernelSpec in user home directory',
        action='store_true'
    )
    prefix_locations.add_argument(
        '--sys-prefix',
        help='Install KernelSpec in sys.prefix. Useful in conda / virtualenv',
        action='store_true',
        dest='sys_prefix'
    )
    prefix_locations.add_argument(
        '--prefix',
        help='Install KernelSpec in this prefix',
        default=None
    )

    args = parser.parse_args(argv)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)


if __name__ == '__main__':
    main()
