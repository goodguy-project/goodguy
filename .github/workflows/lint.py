import os


def lint():
    root = os.getcwd()
    for path, _, files in os.walk(root):
        for file in files:
            if file.split('.')[-1] == 'py':
                args = (
                    '--max-line-length=120',
                    '--disable=C0114,C0115,C0116,R1722',
                    '--variable-rgx=[a-z_][a-z0-9_]*$',
                )
                c = os.system(f'pylint {os.path.join(path, file)} ' + ' '.join(args))
                if c != 0:
                    exit(c)


if __name__ == '__main__':
    lint()
