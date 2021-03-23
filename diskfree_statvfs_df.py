#!/usr/bin/env python3
import os, sys



from ctypes import * # CDLL, Structure, c_uint32, c_int64, c_uint64, c_char, create_string_buffer, byref, c_ubyte, c_int16, c_int64, c_int32

# when _DARWIN_FEATURE_64_BIT_INODE is not defined
class statfs32(Structure):
    _fields_ = [
                ("f_otype",       c_int16),
                ("f_oflags",      c_int16),
                ("f_bsize",       c_int64),
                ("f_iosize",      c_int64),
                ("f_blocks",      c_int64),
                ("f_bfree",       c_int64),
                ("f_bavail",      c_int64),
                ("f_files",       c_int64),
                ("f_ffree",       c_int64),
                ("f_fsid",        c_uint64),
                ("f_owner",       c_uint32),
                ("f_reserved1",   c_int16),
                ("f_type",        c_int16),
                ("f_flags",       c_int64),
                ("f_reserved2",   c_int64*2),
                ("f_fstypename",  c_char*15),
                ("f_mntonname",   c_char*90),
                ("f_mntfromname", c_char*90),
                ("f_reserved3",   c_char),
                ("f_reserved4",   c_int64*4),
               ]

# when _DARWIN_FEATURE_64_BIT_INODE is defined
class statfs64(Structure):
    _fields_ = [
                ("f_bsize",       c_uint32),
                ("f_iosize",      c_int32),
                ("f_blocks",      c_uint64),
                ("f_bfree",       c_uint64),
                ("f_bavail",      c_uint64),
                ("f_files",       c_uint64),
                ("f_ffree",       c_uint64),
                ("f_fsid",        c_uint64),
                ("f_owner",       c_uint32),
                ("f_type",        c_uint32),
                ("f_flags",       c_uint32),
                ("f_fssubtype",   c_uint32),
                ("f_fstypename",  c_char*16),
                ("f_mntonname",   c_char*1024),
                ("f_mntfromname", c_char*1024),
                ("f_reserved",    c_uint32*8),
               ]

'''
kern = CDLL('/usr/lib/system/libsystem_kernel.dylib')
fs_info = statfs32()
# put the path to any file on the mounted file system here
root_volume = create_string_buffer('/')
result = kern.statfs(root_volume, byref(fs_info))
'''







# MAIN:


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




# direct system call to statfs(), not statvfs()


print("\nsystem calls to statfs()")

from ctypes import util


kern = CDLL(util.find_library('c'), use_errno=True)
root_volume = create_string_buffer(str.encode(dir))

print("\nstatfs32")
fs_info = statfs32()
result = kern.statfs(root_volume, byref(fs_info))
print("f_blocks", fs_info.f_blocks)
print("f_bsize", fs_info.f_bsize)
print("f_bavail", fs_info.f_bavail)
print("Total Space MB", fs_info.f_blocks * fs_info.f_bsize / 1024**2)
print("Total Free Space MB", fs_info.f_bfree * fs_info.f_bsize / 1024**2)


print("\nstatfs64")
fs_info = statfs64()
result = kern.statfs(root_volume, byref(fs_info))
print("f_blocks", fs_info.f_blocks)
print("f_bsize", fs_info.f_bsize)
print("f_bavail", fs_info.f_bavail)
print("Total Space MB", fs_info.f_blocks * fs_info.f_bsize / 1024**2)
print("Total Free Space MB", fs_info.f_bfree * fs_info.f_bsize / 1024**2)



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

