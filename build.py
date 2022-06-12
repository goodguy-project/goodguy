import os
import platform

def get_source_env():
    return {
        "CGO_ENABLED": 1,
        "GOARCH": platform.machine().lower(),
        "GOOS": platform.system().lower(),
    }

ROOT = os.path.dirname(os.path.abspath(__file__))

def build_cmd():
    source_env = get_source_env()
    for goos in ('darwin', 'freebsd', 'linux', 'windows'):
        for goarch in ('386', 'amd64', 'arm'):
            print(f'GOOS: {goos}, GOARCH: {goarch}')
            os.system(f'go env -w CGO_ENABLED=0 GOOS={goos} GOARCH={goarch}')
            os.system(f'cd {os.path.join(ROOT, "cmd")} && go build -o dist/goodguy.cmd.{goarch}.{goos}')
    os.system('go env -w ' + ' '.join([f"{k}={v}" for k, v in source_env.items()]))

build_cmd()
