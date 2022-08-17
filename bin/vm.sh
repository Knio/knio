set -eoux

# https://www.kernel.org/doc/Documentation/sysctl/vm.txt

# don't agressively swap
echo 20 | sudo tee /proc/sys/vm/swappiness

# prefer caching fs metadata
echo 1 | sudo tee /proc/sys/vm/vfs_cache_pressure

# 50% of available memory to write cache
echo 50 | sudo tee /proc/sys/vm/dirty_ratio

# start flushing dirty cache at 5%
echo 5 | sudo tee /proc/sys/vm/dirty_background_ratio

# 20s max dirty page time
echo 20000 | sudo tee /proc/sys/vm/dirty_writeback_centisecs

# don't kill shit at random
echo 1 | sudo tee /proc/sys/vm/oom_kill_allocating_task

# limit overcommit
echo 2 | sudo tee /proc/sys/vm/overcommit_memory

# to swap + (X% of RAM)
echo 200 | sudo tee /proc/sys/vm/overcommit_ratio
