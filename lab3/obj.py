def load_obj(filename):
    # Lista para almacenar vértices (x, y, z)
    vertices = []

    # Lista para almacenar caras (índices de los vértices que forman triángulos)
    faces = []

    # Abrimos el archivo .obj en modo lectura
    with open(filename, "r") as file:
        for line in file:
            # Eliminamos espacios en blanco al inicio y final de la línea
            line = line.strip()

            # Si la línea define un vértice (empieza con 'v ')
            if line.startswith("v "):
                # Separamos los valores y convertimos x, y, z a float
                _, x, y, z = line.split()
                vertices.append([float(x), float(y), float(z)])

            # Si la línea define una cara (empieza con 'f ')
            elif line.startswith("f "):
                # Obtenemos los índices de vértices (pueden venir como 'v/vt/vn')
                parts = line.split()[1:]

                # Nos quedamos solo con la parte del índice de vértice y restamos 1 (los .obj son 1-based)
                face = [int(p.split('/')[0]) - 1 for p in parts]

                # Triangulación de la cara (convierte polígonos con más de 3 lados en triángulos)
                for i in range(1, len(face) - 1):
                    # Forma triángulos usando el primer vértice como ancla
                    faces.append([face[0], face[i], face[i + 1]])

    # Devuelve la lista de vértices y la lista de triángulos
    return vertices, faces