from ctypes import * # CDLL, Structure, c_uint32, c_int64, c_uint64, c_char, create_string_buffer, byref, c_ubyte, c_int16, c_int64, c_int32
from ctypes import util

import sys, os

'''
from "man statfs" ... used as input for the class statfs(Structure):

           struct statfs {
               __fsword_t f_type;    /* Type of filesystem (see below) */
               __fsword_t f_bsize;   /* Optimal transfer block size */
               fsblkcnt_t f_blocks;  /* Total data blocks in filesystem */
               fsblkcnt_t f_bfree;   /* Free blocks in filesystem */
               fsblkcnt_t f_bavail;  /* Free blocks available to
                                        unprivileged user */
               fsfilcnt_t f_files;   /* Total file nodes in filesystem */
               fsfilcnt_t f_ffree;   /* Free file nodes in filesystem */
               fsid_t     f_fsid;    /* Filesystem ID */
               __fsword_t f_namelen; /* Maximum length of filenames */
               __fsword_t f_frsize;  /* Fragment size (since Linux 2.6) */
               __fsword_t f_flags;   /* Mount flags of filesystem
                                        (since Linux 2.6.36) */
               __fsword_t f_spare[xxx];
                               /* Padding bytes reserved for future use */
           };

'''


def linux_disk_free_clib_statfs(directory):
	class statfs(Structure):
	    _fields_ = [
                ("f_type",       c_int64),
                ("f_bsize",      c_int64),
                ("f_blocks",     c_ulong),
                ("f_bfree",      c_ulong),
                ("f_bavail",     c_ulong),
                ("f_files",      c_ulonglong),
                ("f_ffree",      c_ulonglong),
                ("f_fsid",       c_int64),
                ("f_namelen",       c_int64),
                ("f_frsize",       c_int64),
                ("f_flags",       c_int64),
                ("f_fspare",       c_int64),
              ]

	kern = CDLL(util.find_library('c'), use_errno=True)
	root_volume = create_string_buffer(str.encode(directory))
	fs_info = statfs()
	result = kern.statfs(root_volume, byref(fs_info)) # you have to call this to get fs_info filled out
	disk_size_MB = fs_info.f_blocks * fs_info.f_bsize / 1024**2
	free_size_MB = fs_info.f_bavail  * fs_info.f_bsize / 1024**2
	return round(disk_size_MB), round(free_size_MB)



try:
    dir = sys.argv[1]
except:
    dir = "."

if not os.path.isdir(dir):
	print("dir", dir, "does exist")
	sys.exit(1)

print("dir is", dir)



print(linux_disk_free_clib_statfs(dir))

