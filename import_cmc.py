from struct import unpack
from . import shared


def load(context, filepath):
    with open(filepath, 'rb') as f:
        f.read(4) # Magic number

        (version,) = unpack('<i', f.read(4))
        assert version == 2, 'Unknown file version.'

        (bone_count,) = unpack('<i', f.read(4))
        f.read(4 * 3 * bone_count)

        vertices = []
        faces = []
        vertex_uvs = []

        (vertex_count,) = unpack('<i', f.read(4))
        for _ in range(vertex_count):
            vertices.append(unpack('<fff', f.read(4 * 3)))
            f.read(4 * 4 * bone_count)
            vertex_uvs.append(unpack('<ff', f.read(4 * 2)))

        (face_count,) = unpack('<i', f.read(4))
        for _ in range(face_count):
            vertex_indices = unpack('<iii', f.read(4 * 3))
            # Indices are reversed for correct normals
            faces.append(vertex_indices[::-1])
        
        shared.load_mesh(context, filepath, vertices, faces, vertex_uvs)
    
    return {'FINISHED'}
