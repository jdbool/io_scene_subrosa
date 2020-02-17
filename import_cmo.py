import bpy
from struct import unpack
from . import shared


def load(context, filepath):
    with open(filepath, 'rb') as f:
        f.read(4) # Magic number

        (version,) = unpack('<i', f.read(4))
        assert version <= 3, 'Unknown file version.'

        vertices = []
        faces = []
        vertex_uvs = []

        (vertex_count,) = unpack('<i', f.read(4))
        for _ in range(vertex_count):
            vertices.append(unpack('<fff', f.read(4 * 3)))
            if version >= 3:
                vertex_uvs.append(unpack('<ff', f.read(4 * 2)))
            else:
                vertex_uvs.append((0.0, 0.0))
            f.read(4)

        (face_count,) = unpack('<i', f.read(4))
        for _ in range(face_count):
            (num_vertices,) = unpack('<i', f.read(4))
            vertex_indices = []

            for _ in range(num_vertices):
                (vertex_id,) = unpack('<i', f.read(4))
                vertex_indices.append(vertex_id)
            
            vertex_indices.reverse()
            faces.append(tuple(vertex_indices))
            f.read(8 if version > 1 else 4)
        
        name = bpy.path.display_name_from_filepath(filepath)
        shared.load_mesh(context, name, vertices, faces, vertex_uvs)
    
    return {'FINISHED'}
