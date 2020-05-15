import bpy
from struct import unpack
from . import shared


def load(context, filepath):
    with open(filepath, 'rb') as f:
        (version,) = unpack('<i', f.read(4))
        assert version == 2, 'Unknown file version.'

        # Texture file name
        f.read(64)

        vertices = []
        faces = []
        vertex_uvs = []

        (vertex_count,) = unpack('<i', f.read(4))
        for _ in range(vertex_count):
            vertices.append(unpack('<fff', f.read(4 * 3)))
            vertex_uvs.append(unpack('<ff', f.read(4 * 2)))

        (face_count,) = unpack('<i', f.read(4))
        for _ in range(face_count):
            vertex_indices = unpack('<iii', f.read(4 * 3))[::-1]
            faces.append(vertex_indices)

        name = bpy.path.display_name_from_filepath(filepath)
        shared.load_mesh(context, name, vertices, faces, vertex_uvs)

    return {'FINISHED'}
