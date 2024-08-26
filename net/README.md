# Bandwidth Ninja (bwninja)

A modern replacement for `iftop`

Why?
- Colors!
- More easily readable UI
- Can track all interfaces
- Less overhead (uses eBPF to collect metrics, and does not need to copy and process packets in userspace)


## Install

```sh
sudo pip install bwninja --break-system-packages
```

Yup, as root ¯\_(ツ)_/¯.  Just like `iftop`

LMK if you have a better way to package a python tool that requires running
as root.


## Run

```sh
sudo bwninja
```
