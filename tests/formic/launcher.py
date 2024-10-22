# Simple example driver w/ numerical tests of output
import mdi
import sys

# Initiate MDI 
mdi.MDI_Init("-mdi")

# Open plugin
mdi.MDI_Launch_plugin("mopac", "formic_acid3 -mdi \"-role ENGINE -name mopac -method LINK -plugin_path /repo/build/mopac/build\"", None, None, None)
