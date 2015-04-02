"""Figure out the public ip of the computer and write it to a file.

The public ip of the machine is determined using the ipsetter module by
Fernando Giannasi (see https://github.com/phoemur/ipgetter).
It is then written to the specified file.
"""

import sys
import ipgetter

if len(sys.argv) < 2:
    print('No destination file given.')
    print('Usage: ' + __file__ + ' <file>')
    sys.exit()

fname = sys.argv[1]
if not os.path.isfile(fname):
    print('Invalid file ' + fname)
    sys.exit()

myip = ipgetter.myip()
f = open(fname, 'w')
f.write(myip)
f.close()

