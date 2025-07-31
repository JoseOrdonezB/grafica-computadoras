def load_obj(filename):
    vertices = []
    texcoords = []
    faces = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue  # ignorar comentarios y líneas vacías

            if line.startswith("v "):
                parts = line.split()
                if len(parts) >= 4:
                    x, y, z = map(float, parts[1:4])
                    vertices.append([x, y, z])

            elif line.startswith("vt "):
                parts = line.split()
                if len(parts) >= 3:
                    u = float(parts[1])
                    v = float(parts[2])
                    texcoords.append([u, v])  # ignoramos w si existe

            elif line.startswith("f "):
                parts = line.split()[1:]
                face = []
                for part in parts:
                    values = part.split("/")
                    v_idx = int(values[0]) - 1
                    vt_idx = int(values[1]) - 1 if len(values) > 1 and values[1] else 0
                    face.append((v_idx, vt_idx))

                # triangulación tipo fan si la cara tiene más de 3 vértices
                for i in range(1, len(face) - 1):
                    faces.append([face[0], face[i], face[i + 1]])

    return vertices, texcoords, faces