# Simple example driver w/ numerical tests of output
import mdi
import sys

iarg = 1
while iarg < len(sys.argv):
    arg = sys.argv[iarg]

    if arg == "-mdi":
        # Initialize MDI
        if len(sys.argv) <= iarg+1:
            raise Exception("Argument to -mdi option not found")
        mdi.MDI_Init(sys.argv[iarg+1])
        iarg += 1
    else:
        raise Exception("Unrecognized argument")

    iarg += 1

# Open plugin
mdi.MDI_Launch_plugin("mopac", "formic_acid3 -mdi \"-role ENGINE -name mopac -method TCP -hostname localhost -port 8021\"", None, None, None)
