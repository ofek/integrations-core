import os
import platform
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLATFORM = (
    'windows' if platform.system() == 'Windows'
    else 'macos' if platform.system() == 'Darwin'
    else 'linux'
)


def display_action(script_file):
    display_header = f'Running: {script_file}'
    print(f'\n{display_header}\n{"-" * len(display_header)}\n')


def main():
    if len(sys.argv) == 1:
        return

    checks = [c.strip() for c in sys.argv[1:]]
    print(f'Checks chosen: {repr(checks).strip("[]")}')

    if 'changed' in checks:
        print('Detecting changed checks...')
        result = subprocess.run(['ddev', 'test', '--list'], encoding='utf-8', capture_output=True, check=True)
        checks = sorted(c.strip('`') for c in re.findall('^`[^`]+`', result.stdout, re.M))
    else:
        checks = sorted(c for c in checks if c and not c.startswith('-'))

    for check in checks:
        check_path = os.path.join(HERE, check)
        if not os.path.isdir(check_path):
            continue

        contents = os.listdir(check_path)
        if 'run.py' in contents:
            script_file = os.path.join(check_path, 'run.py')
            display_action(script_file)
            subprocess.run([sys.executable, script_file], check=True)
        elif PLATFORM in contents:
            print(f'\nSetting up: {check}')
            scripts_path = os.path.join(check_path, PLATFORM)
            scripts = sorted(os.listdir(scripts_path))

            for script in scripts:
                script_file = os.path.join(scripts_path, script)
                display_action(script_file)
                subprocess.run([script_file], shell=True, check=True)


if __name__ == '__main__':
    main()
