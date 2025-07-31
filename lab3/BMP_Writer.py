import struct

def GenerateBMP(filename: str, width: int, height: int, byteDepth: int, colorBuffer: list[list[list[int]]]) -> None:
    def char(c: str) -> bytes:
        return struct.pack("<c", c.encode("ascii"))

    def word(w: int) -> bytes:
        return struct.pack("<H", w)

    def dword(d: int) -> bytes:
        return struct.pack("<L", d)

    # Alineación por fila a múltiplos de 4 bytes (BMP lo requiere)
    row_padding = (4 - (width * byteDepth) % 4) % 4
    row_size = width * byteDepth + row_padding
    pixel_data_size = row_size * height
    file_size = 14 + 40 + pixel_data_size

    with open(filename, "wb") as f:
        # Header
        f.write(char("B"))
        f.write(char("M"))
        f.write(dword(file_size))
        f.write(dword(0))              # Reserved
        f.write(dword(14 + 40))        # Pixel data offset

        # DIB Header (BITMAPINFOHEADER)
        f.write(dword(40))             # Header size
        f.write(dword(width))
        f.write(dword(height))
        f.write(word(1))               # Planes
        f.write(word(byteDepth * 8))   # Bits per pixel
        f.write(dword(0))              # Compression (none)
        f.write(dword(pixel_data_size))
        f.write(dword(0))              # Horizontal resolution
        f.write(dword(0))              # Vertical resolution
        f.write(dword(0))              # Colors in palette
        f.write(dword(0))              # Important colors

        # Pixel data (bottom-up BMP)
        for y in range(height):
            for x in range(width):
                color = colorBuffer[x][y]
                bgr = [int(c) for c in reversed(color[:3])]  # RGB to BGR
                f.write(bytes(bgr))
            f.write(b'\x00' * row_padding)  # padding por fila