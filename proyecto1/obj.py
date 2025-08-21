import os

def load_obj(filename):
    vertices = []
    texcoords = []
    normals = []
    faces = []

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
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
                    texcoords.append([u, v])

            elif line.startswith("vn "):
                parts = line.split()
                if len(parts) >= 4:
                    nx, ny, nz = map(float, parts[1:4])
                    normals.append([nx, ny, nz])

            elif line.startswith("f "):
                parts = line.split()[1:]
                face = []
                for part in parts:
                    values = part.split("/")
                    v_idx = int(values[0]) - 1
                    vt_idx = int(values[1]) - 1 if len(values) > 1 and values[1] else -1
                    vn_idx = int(values[2]) - 1 if len(values) > 2 and values[2] else -1
                    face.append((v_idx, vt_idx, vn_idx))

                # triangulación fan (convierte n-gons en triángulos)
                for i in range(1, len(face) - 1):
                    faces.append([face[0], face[i], face[i + 1]])

    return vertices, texcoords, normals, faces


# --------------------------
# Helpers para materiales .mtl
# --------------------------

def find_mtllib_in_obj(obj_path):
    """Busca el mtllib en el archivo .obj y devuelve la ruta absoluta al .mtl (o None)."""
    base_dir = os.path.dirname(obj_path)
    with open(obj_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("mtllib"):
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    return os.path.join(base_dir, parts[1])
    return None


def parse_mtl(mtl_path):
    """Parsea un archivo .mtl y devuelve un dict {material: {propiedades}}."""
    materials = {}
    current = None
    if not os.path.isfile(mtl_path):
        return materials

    with open(mtl_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if parts[0] == "newmtl" and len(parts) >= 2:
                current = parts[1]
                materials[current] = {}
            elif current is not None:
                if parts[0] == "map_Kd" and len(parts) >= 2:
                    materials[current]["map_Kd"] = " ".join(parts[1:])
                elif parts[0] == "Kd" and len(parts) >= 4:
                    materials[current]["Kd"] = tuple(map(float, parts[1:4]))

    return materials


def first_map_kd_from_obj(obj_path):
    """
    Devuelve la ruta absoluta a la primera textura difusa (map_Kd) encontrada
    en el .mtl asociado al .obj. Si no hay, devuelve None.
    """
    mtl_path = find_mtllib_in_obj(obj_path)
    if not mtl_path:
        return None

    materials = parse_mtl(mtl_path)
    for mat in materials.values():
        if "map_Kd" in mat:
            tex_path = mat["map_Kd"]
            # resolver relativo al archivo .mtl
            if not os.path.isabs(tex_path):
                tex_path = os.path.join(os.path.dirname(mtl_path), tex_path)
            return tex_path
    return None