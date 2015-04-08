import getpass
import os.path
import sys
import string
import re
from subprocess import call

# Server configuration
user = "michiel2"
server = "ssh.math.uiuc.edu"
printer = "ih220"

# Default printing options
pages_per_page = 1                # 2, 4, 6, 9, 16
two_sided = True                  # False
page_ranges = ""                  # e.g. "1-7,9,10-11"
output_order = "normal"           # "reverse"
landscape = False                 # True

# Get the filename
if len(sys.argv) < 2:
    print "No filename given."
    print "Usage: print-illini <filename>"
    sys.exit(0)
filename = sys.argv[1]
if not os.path.isfile(filename):
    print "\"" + filename + "\" is not a valid file."
    sys.exit(0)
filename = os.path.abspath(filename)
print("Printing file " + filename + " on printer " + printer + ".")

# Configure the printing
while True:
    sys.stdout.write("Pages per sheet (" + str(pages_per_page) + "): ")
    choice = raw_input()
    if choice == "":
        break
    if choice in ["1", "2", "4", "6","9", "16"]:
        pages_per_page = int(choice)
        break
    print("Options are 1, 2, 4, 6, 9, 16.")
while True:
    sys.stdout.write("Two-sided (" + ("yes" if two_sided else "no") + "): ")
    choice = raw_input().lower()
    if choice == "":
        break
    if choice in ["y", "ye", "yes", "t", "true"]:
        two_sided = True
        break
    if choice in ["n", "no", "f", "false"]:
        two_sided = False
        break
    print("Options are yes, no.")
while True:
    sys.stdout.write("Page ranges (all): ")
    choice = raw_input()
    if choice == "":
        page_ranges = ""
        break
    if re.match("^((\d+-\d+|\d+),)*(\d+-\d+|\d+)$", choice):
        page_ranges = choice
        break
    print("Enter something like \"1-7,9,12-14\".")
while True:
    sys.stdout.write("Landscape (" + ("yes" if landscape else "no") + "): ")
    choice = raw_input().lower()
    if choice == "":
        break
    if choice in ["y", "ye", "yes", "t", "true"]:
        landscape = True
        break
    if choice in ["n", "no", "f", "false"]:
        landscape = False
        break
    print("Options are yes, no.")
print("")

# These interact in an annoying way. Check the CUPS documentation. Blame CUPS.
if pages_per_page != 1 and page_ranges != "":
    print("Warning: multiple pages per sheet and page ranges used. This will give counterintuitive results.")
    print("")

# Ask for the password
pwd = getpass.getpass("Password for " + user + "@" + server + ": ")

# Copy the file to the server
remote_filename = os.path.basename(filename)
remote_filename = "".join(ch for ch in remote_filename if ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-") # filter out everything that's not nice
if remote_filename == '':
    remote_filename = 'temp'
remote_filename = "printing-temp/" + remote_filename
call(["pscp", "-pw", pwd, filename, user + "@" + server + ":" + remote_filename])

# Now print it
command = ["plink", "-pw", pwd, user + "@" + server, "lpr", "-P", printer]
command.extend(["-o", "number-up=" + str(pages_per_page)])
if landscape:
    command.extend(["-o", "landscape"])
if two_sided:
    if landscape:
        command.extend(["-o", "sides=two-sided-short-edge"])
    else:
        command.extend(["-o", "sides=two-sided-long-edge"])
else:
    command.extend(["-o", "sides=one-sided"])
if page_ranges != "":
    command.extend(["-o", "page-ranges=" + page_ranges])
command.append(remote_filename)
call(command)

print("Done.")
raw_input()

# Now set a timer to remove the file from the server in an hour
# This is not working yet
# call(["plink", "-pw", pwd, user + "@" + server, "echo \"rm ~/" + remote_filename + "\" | at now + 1 hour"])


