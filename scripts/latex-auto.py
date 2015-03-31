import glob
import sys
from subprocess import Popen, call

print(len(sys.argv))

if len(sys.argv) < 2:
    texfiles = glob.glob("*.tex")
    if len(texfiles) < 1:
        print("No .tex files found.")
        sys.exit()
    if len(texfiles) > 1:
        print("Too many .tex files found. Picking between them has not been implemented.")
        sys.exit()
    texfile = texfiles[0]
else:
    texfile = sys.argv[1]

print(texfile)

latexmk = Popen(["latexmk","-pvc","-pdf",texfile])
call(["C:\\Program Files (x86)\\Vim\\vim74\\gvim.exe", texfile])
Popen("TASKKILL /F /PID {pid} /T".format(pid=latexmk.pid))

