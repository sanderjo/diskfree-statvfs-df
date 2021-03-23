#!/usr/bin/env python3
import os, sys

try:
    dir = sys.argv[1]
except:
    dir = "."
print("dir is", dir)

# statvfs
s = os.statvfs(dir)
disk_size = float(s.f_blocks) * float(s.f_frsize)
available = float(s.f_bavail) * float(s.f_frsize)

statvfs_disk_size_MB = round(disk_size / 1024 ** 2)
statvfs_available_MB = round(available / 1024 ** 2)



print("statvfs results: Partition (MB):" , statvfs_disk_size_MB, "Available (MB):", statvfs_available_MB)


# df -m (space in MB)
cmd = "df -m " + dir  # show in MB
for thisline in os.popen(cmd).readlines():
    if thisline.startswith("/"):
        _, df_blocks_MB, _, df_available_MB = thisline.split()[:4]
        df_blocks_MB = int(df_blocks_MB)
        df_available_MB = int(df_available_MB)
        print("df -m results:   Partition (MB):", df_blocks_MB, "Available (MB):", df_available_MB)

# calculate diff
diff_disk_size_MB = df_blocks_MB - statvfs_disk_size_MB
diff_available_MB = df_available_MB - statvfs_available_MB



if diff_disk_size_MB > 10 or diff_available_MB > 10:
	print("Diff! in MB. Disk:", diff_disk_size_MB, "Available:", diff_available_MB)
	print("Diff! in TB. Disk:", diff_disk_size_MB / 1024**2 , "Available:", diff_available_MB / 1024**2)	
else:
	print("no diff")


'''

Linux:
$ df /media/zeegat/
Filesystem      1K-blocks       Used  Available Use% Mounted on
/dev/sda2      4883638268 3642537472 1241100796  75% /media/zeegat

$ python3 -c "import os; print(os.statvfs('/media/zeegat/')) "
os.statvfs_result(f_bsize=4096, f_frsize=4096, f_blocks=1220909567, f_bfree=310275199, f_bavail=310275199, f_files=1241166332, f_ffree=1241156854, f_favail=1241156854, f_flag=4096, f_namemax=255)


MacOS:
Filesystem   512-blocks      Used  Available Capacity iused      ifree %iused  Mounted on
/dev/disk0s2 1951845952 879061888 1072272064    46% 1754925 4293212354    0%   /
/dev/disk0s2  931Gi  418Gi  512Gi    45% 1754871 4293212408    0%   /

$ df -m .
Filesystem   1M-blocks   Used Available Capacity iused      ifree %iused  Mounted on
/dev/disk0s2    953049 428409    524390    45% 1754874 4293212405    0%   /


'''

