import argparse
import subprocess


def config(key):
    return subprocess.check_output(['git', 'config', '--get', key]).decode().strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repository')
    args = parser.parse_args()
    user = config('user.name')
    email = config('user.email')
    username = config('user.githubusername')
    repository = f'git@github.com:{username}/{args.repository}.git'
    print(f'{user = }')
    print(f'{email = }')
    print(f'{repository = }')
    subprocess.check_call(['git', 'clone', repository])


if __name__ == '__main__':
    main()
