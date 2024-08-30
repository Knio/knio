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


## Run

bwninja requires root to access the network interfaces.


```sh
bwninja # bwninja will try to escalate itself.

python -m bwninja.tui # same. if bin script was not installed

sudo bwninja # will work only if bwninja is installed as a system package
```
