# post_install.py
import os
import subprocess


def install_wheel():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    wheel_path = os.path.join(dir_path, 'bundled_wheels', 'neoapi-1.2.0-cp39-cp39-win_amd64.whl')
    subprocess.check_call(['pip', 'install', wheel_path])


if __name__ == "__main__":
    install_wheel()
