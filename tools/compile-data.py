import sys

scale_factor = 1.0

with open(sys.argv[1], "rb") as f:
    f.seek(0, 2)  # Move to end of file
    file_size = f.tell()
    if file_size == 0:
        print("File is empty", file=sys.stderr)
        sys.exit(1)

    # Read last 1024 bytes or the whole file if smaller
    read_size = min(1024, file_size)
    f.seek(-read_size, 2)
    tail = f.read().decode("utf-8", errors="ignore")
    lines = tail.splitlines()
    cells = lines[-1].split()
    scale_factor = float(cells[2])  # Cum probability from last line

f = open(sys.argv[1], "r")
for line in f:
    (name, prob, cum, rank) = line.split()
    print(f"{name} {float(cum) / scale_factor:.8f}")
