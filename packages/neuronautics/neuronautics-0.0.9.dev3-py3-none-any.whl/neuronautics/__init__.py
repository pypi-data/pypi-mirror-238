import subprocess
___version___="0.0.9.1.3"

branch = (subprocess
          .run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
               stdout=subprocess.PIPE, text=True)
          .stdout.strip())

major, minor, patch, rc, dev = ___version___.split('.')
if branch in ('master', 'main'):
    __version__ = f'{major}.{minor}.{patch}'
elif branch in ('staging', ):
    __version__ = f'{major}.{minor}.{patch}rc{rc}'
else:
    __version__ = f'{major}.{minor}.{patch}dev{dev}'