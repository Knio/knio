set -eoux

sudo sysctl -w kernel.pid_max=9999

# https://www.kernel.org/doc/Documentation/sysctl/vm.txt

# don't agressively swap
echo 10 | sudo tee /proc/sys/vm/swappiness

# prefer caching fs metadata
echo 1 | sudo tee /proc/sys/vm/vfs_cache_pressure

# 50% of available memory to write cache
echo 50 | sudo tee /proc/sys/vm/dirty_ratio

# start flushing dirty cache at 10%
echo 10 | sudo tee /proc/sys/vm/dirty_background_ratio

# 60s max dirty inode time
echo 60000 | sudo tee /proc/sys/vm/dirtytime_expire_seconds

# 20s max dirty page time
echo 20000 | sudo tee /proc/sys/vm/dirty_writeback_centisecs

# don't kill shit at random
echo 1 | sudo tee /proc/sys/vm/oom_kill_allocating_task

# limit overcommit..
echo 2 | sudo tee /proc/sys/vm/overcommit_memory

# ..to swap + (X% of RAM)
echo 500 | sudo tee /proc/sys/vm/overcommit_ratio
