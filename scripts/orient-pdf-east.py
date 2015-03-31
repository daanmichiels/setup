import sys
import os.path
from subprocess import call

if len(sys.argv) < 2:
    print("No files given.")
    print("Usage: rotate-pdf-right.py <file1> [<file2> ...]")
    sys.exit(0)

files = sys.argv[1:]

for f in files:
    if not os.path.isfile(f):
        print(f + " is not a file.")
        break
    f = os.path.abspath(f)
    root, ext = os.path.splitext(f)
    t = root + "-east" + ext
    print("Rotating " + f)
    command = ["pdftk", f, "cat", "1-endeast", "output", t]
    returncode = call(command)
    if returncode:
        print(" -- pdftk gave non-zero return value")
        break
    oldsize = os.path.getsize(f)
    newsize = os.path.getsize(t)
    if abs(oldsize - newsize) < 100 or (3*oldsize > 2*newsize and 3*newsize > 2*oldsize):
        os.remove(f)
        os.rename(t, f)
    else:
        print(" -- Warning: file size has changed significantly. Not overwriting original.")

