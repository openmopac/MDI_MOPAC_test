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
comm = mdi.MDI_Open_plugin("mopac", "formic_acid3 -mdi \"-role ENGINE -name mopac -method LINK\"", None)
print(f"Communicator: {comm}")

# Get the name of the engine, which will be checked and verified at the end
mdi.MDI_Send_Command("<NAME", comm)
engine_name = mdi.MDI_Recv(mdi.MDI_NAME_LENGTH, mdi.MDI_CHAR, comm)
print(f"Engine name: {engine_name}")

# Get the node name
mdi.MDI_Send_Command("<@", comm)
node_name = mdi.MDI_Recv(mdi.MDI_COMMAND_LENGTH, mdi.MDI_CHAR, comm)
print(f"Node name: {node_name}")

# Get data from the first geometry of the molecule
mdi.MDI_Send_Command("<NATOMS", comm)
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
print(f"NATOMS: {natoms}")

mdi.MDI_Send_Command("<COORDS", comm)
coords = mdi.MDI_Recv(3 * natoms, mdi.MDI_DOUBLE, comm)
print(f"COORDS: {coords}")

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print(f"ENERGY: {energy}")

# Adjust the geometry of the molecule
print("Sending new coordinates...")
for coord in coords:
    coord *= 1.1
mdi.MDI_Send_Command(">COORDS", comm)
mdi.MDI_Send(coords, 3 * natoms, mdi.MDI_DOUBLE, comm)

# Get data from the second geometry of the molecule
mdi.MDI_Send_Command("<NATOMS", comm)
natoms = mdi.MDI_Recv(1, mdi.MDI_INT, comm)
print(f"NATOMS: {natoms}")

mdi.MDI_Send_Command("<COORDS", comm)
coords = mdi.MDI_Recv(3 * natoms, mdi.MDI_DOUBLE, comm)
print(f"COORDS: {coords}")

mdi.MDI_Send_Command("<ENERGY", comm)
energy = mdi.MDI_Recv(1, mdi.MDI_DOUBLE, comm)
print(f"ENERGY: {energy}")

# Normal exit
mdi.MDI_Send_Command("EXIT", comm)

# Close plugin
mdi.MDI_Close_plugin(comm)

