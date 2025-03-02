# Bandwidth Ninja (bwninja)

A modern replacement for `iftop`

Why?
- Colors!
- More easily readable UI
- Can track all interfaces
- Less overhead (uses eBPF to collect metrics, and does not need to copy and process packets in userspace)


## Install

```sh
pip install bwninja
```

### bcc

`bwninja` requires `python3-bpfcc` which does not seem to have a correct package in pip/pypi.

See the official install documentation here: https://github.com/iovisor/bcc/blob/master/INSTALL.md




## Run

`bwninja` requires root access to the network interfaces.

```sh
bwninja # bwninja will try to escalate itself.

python -m bwninja.tui # same. if bin script was not installed

sudo bwninja # will work only if bwninja was installed as a system package
```
