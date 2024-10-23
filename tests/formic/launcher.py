# Simple example driver w/ numerical tests of output
import mdi
import sys


def driver_callback(mpi_comm, comm, class_object):

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
    coords2 = [coord*1.1 for coord in coords]
    mdi.MDI_Send_Command(">COORDS", comm)
    mdi.MDI_Send(coords2, 3 * natoms, mdi.MDI_DOUBLE, comm)

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
    
    return 0


if __name__ == "__main__":
    # Initiate MDI 
    mdi.MDI_Init("-role DRIVER -name driver -method LINK -plugin_path /repo/build/mopac/build")

    # Launch plugin
    mdi.MDI_Launch_plugin("mopac", "formic_acid2 -mdi \"-role ENGINE -name mopac -method LINK -plugin_path /repo/build/mopac/build\"", None, driver_callback, None)
