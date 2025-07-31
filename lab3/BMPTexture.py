import struct

class BMPTexture:
    def __init__(self, filename):
        with open(filename, "rb") as image:
            image.seek(10)
            header_offset = struct.unpack('<I', image.read(4))[0]

            image.seek(18)
            self.width = struct.unpack('<I', image.read(4))[0]
            self.height = struct.unpack('<I', image.read(4))[0]

            image.seek(header_offset)

            self.pixels = []

            # Cada fila debe estar alineada a 4 bytes
            row_padding = (4 - (self.width * 3) % 4) % 4

            for y in range(self.height):
                row = []
                for x in range(self.width):
                    b = int.from_bytes(image.read(1), 'little') / 255
                    g = int.from_bytes(image.read(1), 'little') / 255
                    r = int.from_bytes(image.read(1), 'little') / 255
                    row.append([r, g, b])
                image.read(row_padding)  # Saltar padding
                self.pixels.insert(0, row)  # Insertar al principio (imagen va de abajo hacia arriba)

    def get_color(self, u, v):
        # Repetir textura (wrap) si u o v están fuera de [0, 1]
        u = u % 1
        v = v % 1

        x = min(int(u * self.width), self.width - 1)
        y = min(int(v * self.height), self.height - 1)
        return self.pixels[y][x]