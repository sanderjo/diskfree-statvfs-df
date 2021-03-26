# diskfree-statvfs-df
diskfree statvfs df

On MacOS, with disks > 4TB, the output of statvfs() at C and OS level and thus with python's os.statvfs() are incorrect: overflow at each 4TB.

This python program finds a solution to report the correct Disk and Free space via call to statfs() (without v), directly in the C library.



For fun, also for Linux

