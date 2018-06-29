# https://www.kernel.org/doc/Documentation/sysctl/vm.txt

# don't agressively swap
echo 1 | sudo tee /proc/sys/vm/swappiness

# prefer caching fs metadata
echo 1 | sudo tee /proc/sys/vm/vfs_cache_pressure

# 50% of available memory to write cache
echo 50 | sudo tee /proc/sys/vm/dirty_ratio

# 30% of vailable memory to kernel write cache
echo 30 | sudo tee /proc/sys/vm/dirty_background_ratio

# don't kill shit at random
echo 1 | sudo tee /proc/sys/vm/oom_kill_allocating_task
