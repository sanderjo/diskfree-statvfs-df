#!/usr/bin/env python3
import os, sys, platform



from ctypes import * # CDLL, Structure, c_uint32, c_int64, c_uint64, c_char, create_string_buffer, byref, c_ubyte, c_int16, c_int64, c_int32
from ctypes import util
	

# Three different functions to get Disk size and Free size

def disk_free_os_df(directory):
	# On any any POSIX with any disksize, "df" is always right, but heavy as it needs a process
	directory = '"' + directory + '"'
	cmd = "df -m " + directory  # show in MB
	for thisline in os.popen(cmd).readlines():
		if thisline.startswith("/"):
			_, df_blocks_MB, _, df_available_MB = thisline.split()[:4]
			df_blocks_MB = int(df_blocks_MB) # blocks of 1MB, so blocks is MBs
			df_available_MB = int(df_available_MB)
			#print("df -m results:   Partition (MB):", df_blocks_MB, "Available (MB):", df_available_MB)
			break # line found, so we're done
	return df_blocks_MB, df_available_MB

def disk_free_python_statvfs(directory):
	# just plain python's os.statvfs
	# Works almost always, but not on MacOS with >4TB drives
	s = os.statvfs(directory)
	disk_size = float(s.f_blocks) * float(s.f_frsize)
	available = float(s.f_bavail) * float(s.f_frsize)

	statvfs_disk_size_MB = round(disk_size / 1024 ** 2)
	statvfs_available_MB = round(available / 1024 ** 2)
	#print("statvfs results: Partition (MB):" , statvfs_disk_size_MB, "Available (MB):", statvfs_available_MB)
	return statvfs_disk_size_MB, statvfs_available_MB


def disk_free_clib_statfs32(directory):
	# direct system call to c-lib's statfs(), not python's os.statvfs()
	# Only safe on MacOS!!! Probably because of the data structure used below; Linux other types / byte length?
	# Based on code of pudquick and blackntan
	
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
	

	kern = CDLL(util.find_library('c'), use_errno=True)
	root_volume = create_string_buffer(str.encode(directory))
	fs_info = statfs32()
	result = kern.statfs(root_volume, byref(fs_info)) # you have to call this to get fs_info filled out
	disk_size_MB = round(fs_info.f_blocks * fs_info.f_bsize / 1024**2)
	free_size_MB = round(fs_info.f_bavail * fs_info.f_bsize / 1024**2)
	return disk_size_MB, free_size_MB


def TEST_disk_free_clib_statfs32(directory, counter):
	# direct system call to c-lib's statfs(), not python's os.statvfs()
	# Only safe on MacOS!!! Probably because of the data structure used below; Linux other types / byte length?	
	
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
	

	kern = CDLL(util.find_library('c'), use_errno=True)
	root_volume = create_string_buffer(str.encode(dir))
	fs_info = statfs32()
	
	for i in range(counter):
		result = kern.statfs(root_volume, byref(fs_info)) # you have to call this to get fs_info filled out
		
	disk_size_MB = round(fs_info.f_blocks * fs_info.f_bsize / 1024**2)
	free_size_MB = round(fs_info.f_bavail * fs_info.f_bsize / 1024**2)
	return disk_size_MB, free_size_MB


# MAIN:


try:
    dir = sys.argv[1]
except:
    dir = "."

if not os.path.isdir(dir):
	print("dir", dir, "does exist")
	sys.exit(1)

print("dir is", dir)

print("df is always right, so: Disk size, and free (in MB):", disk_free_os_df(dir))
print("python's os.statvfs() says", disk_free_python_statvfs(dir))
print("clib statfs32 says", disk_free_clib_statfs32(dir))



counter = 0
if counter > 0:

	print("\nMeasure time it takes for X loops:", counter)
	import time
	
	start_time = time.time()
	for i in range(counter):
		disk_free_os_df(dir)
	print("disk_free_os_df() method: --- %s seconds ---" % (time.time() - start_time))

	start_time = time.time()
	for i in range(counter):
		disk_free_python_statvfs(dir)
	print("disk_free_python_statvfs() method: --- %s seconds ---" % (time.time() - start_time))
	
	start_time = time.time()
	for i in range(counter):
		disk_free_clib_statfs32(dir)
	print("disk_free_clib_statfs32() method: --- %s seconds ---" % (time.time() - start_time))


	start_time = time.time()
	TEST_disk_free_clib_statfs32(dir, counter)
	print("TEST_disk_free_clib_statfs32() method: --- %s seconds ---" % (time.time() - start_time))	

	
	print("Done with measurement\n")



print("Now the real determination")

use_statfs32 = False
if platform.system().lower() == "darwin" and disk_free_os_df(dir)[0] > 4 * 1024**2:
	# MacOS, and disk bigger than 4TB, so use statfs32()
	use_statfs32 = True

# We're done. Now use it

if not use_statfs32:
	print(disk_free_python_statvfs(dir))
else:
	print(disk_free_clib_statfs32(dir))


'''

Linux:
$ df -m .
Filesystem   1M-blocks   Used Available Capacity iused      ifree %iused  Mounted on
/dev/disk0s2    953049 428409    524390    45% 1754874 4293212405    0%   /


'''

