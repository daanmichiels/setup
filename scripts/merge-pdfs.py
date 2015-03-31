import sys
import os.path
from subprocess import call

if len(sys.argv) < 3:
    print("Not enough files given.")
    print("Usage: merge-pdfs <file1> <file2> [<file3> ...]")
    sys.exit()

filenames = sys.argv[1:]
correct_filenames = []
for f in filenames:
    if os.path.isfile(f):
        correct_filenames.append(os.path.abspath(f))
    else:
        print("Invalid file: " + f)
filenames = correct_filenames

print("Files:")
for f in filenames:
    print("    " + f)

if len(filenames) < 2:
    print("Not enough valid files.")
    sys.exit(0)

folder = os.path.dirname(filenames[0])
target = os.path.join(folder, "merged.pdf")
i = 0
while os.path.exists(target):
    i = i + 1
    target = os.path.join(folder, "merged-" + str(i) + ".pdf")

call(["pdftk"] + filenames + ["cat", "output", target])


