
with open("Bugle7T_littleEndian", "rb") as f:
    byte = f.read(1)
    while byte != "":
        # Do stuff with byte.
        byte = f.read(1)
        print byte
        raw_input()