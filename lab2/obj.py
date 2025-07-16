def load_obj(filename):
    vertices = []
    faces = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if line.startswith("v "):
                _, x, y, z = line.split()
                vertices.append([float(x), float(y), float(z)])

            elif line.startswith("f "):
                parts = line.split()[1:]

                face = [int(p.split('/')[0]) - 1 for p in parts]

                for i in range(1, len(face) - 1):
                    faces.append([face[0], face[i], face[i + 1]])

    return vertices, faces