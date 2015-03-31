import glob
import re
from pyPdf import PdfFileReader, PdfFileWriter
import sys
import os
import shutil
import subprocess

source_dir = "C:\\Users\\daan\\Dropbox\\boogie-board-pdfs\\"

if len(sys.argv) < 2:
    print("No argument given. Please specify tex file you're editing.")
    sys.exit(0)

texfile = sys.argv[1]
target_folder = os.path.dirname(os.path.realpath(texfile))

# the index argument is optional
# index=0 means "insert the most recent boogie pdf"
# index=n means "insert the (n+1)'th most recent boogie pdf"
index = 0
if len(sys.argv) > 2:
    index = int(sys.argv[2])

pdfs = glob.glob(os.path.join(source_dir, "*.[Pp][Dd][Ff]"))
if len(pdfs) < (index+1):
    print("Not enough pdfs found (" + str(len(pdfs)) + " found, but index=" + str(index) + ").")
    sys.exit(0)

# find the correct pdf
pdfs = sorted(pdfs, key=os.path.getctime, reverse=True)
source_full = pdfs[index]
source_base = os.path.basename(source_full)

# determine source and target file
target_base = source_base
target_base = target_base.replace(' ', '-')
target_full = os.path.join(target_folder, target_base)
number = 0
while os.path.exists(target_full):
    number += 1
    target_base = str(number) + "-" + source_base.replace(' ', '-')
    target_full = os.path.join(target_folder, target_base)

# we don't check whether this file exists
# but who cares; deleting it should be ok,
# and if it isn't, it's the file's own fault
# for being named something.tmp
target_full_temp = target_full + ".tmp"

# find bounding box of source file for cropping
boundingbox = subprocess.check_output(["gs", "-dSAFER", "-dNOPAUSE", "-dBATCH", "-sDEVICE=bbox", source_full], stderr=subprocess.STDOUT)
# math something that looks like '%%BoundingBox:' followed by four integers
# store the integers in groups, so that we can extract them after matching
boundingbox = re.search(r"%%BoundingBox:\s*(\d+)\s*(\d+)\s*(\d+)\s*(\d+)\s*", boundingbox)
if not boundingbox:
    print("Could not determine bounding box.")
    sys.exit(0)
left, top, right, bottom = boundingbox.groups()

input_pdf = PdfFileReader(file(source_full, "rb"))
output_pdf = PdfFileWriter()

nr_pages = input_pdf.getNumPages()
for i in range(nr_pages):
    page = input_pdf.getPage(i)
    page.trimBox.lowerLeft = (left, bottom)
    page.trimBox.upperRight = (right, top)
    page.cropBox.lowerLeft = (left, bottom)
    page.cropBox.upperRight = (right, top)
    output_pdf.addPage(page)

outputStream = file(target_full_temp, "wb")
output_pdf.write(outputStream)
outputStream.close()

# finally rotate the file 90 degrees clockwise
subprocess.call(["pdftk", target_full_temp, "cat", "1-endeast", "output", target_full])
os.remove(target_full_temp)

print("\\begin{center}")
print("    \\includegraphics[scale=0.7]{" + target_base + "}")
print("\\end{center}")
print("")

