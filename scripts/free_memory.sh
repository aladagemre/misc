#free && sync && echo 3 > /proc/sys/vm/drop_caches && free
free && sync && echo 3 | sudo tee /proc/sys/vm/drop_caches && free
