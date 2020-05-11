import bpy
from struct import unpack
from . import shared


def load(context, filepath):
    with open(filepath, 'rb') as f:
        (version,) = unpack('<i', f.read(4))
        assert version == 1, 'Unknown file version.'

        vertices = []
        faces = []
        vertex_uvs = []

        f.read(4 * 6)

        (node_count,) = unpack('<i', f.read(4))
        f.read(4 * 4 * node_count)

        (vertex_count,) = unpack('<i', f.read(4))
        for _ in range(vertex_count):
            vertices.append(unpack('<fff', f.read(4 * 3)))
            vertex_uvs.append(unpack('<ff', f.read(4 * 2)))

        (face_count,) = unpack('<i', f.read(4))
        for _ in range(face_count):
            (num_vertices,) = unpack('<i', f.read(4))
            vertex_indices = []

            for _ in range(num_vertices):
                (vertex_id,) = unpack('<i', f.read(4))
                vertex_indices.append(vertex_id)

            vertex_indices.reverse()
            faces.append(tuple(vertex_indices))

        name = bpy.path.display_name_from_filepath(filepath)
        shared.load_mesh(context, name, vertices, faces, vertex_uvs)

    return {'FINISHED'}
