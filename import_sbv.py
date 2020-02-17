import bpy
from struct import unpack
from . import shared


def load(context, filepath):
    with open(filepath, 'rb') as f:
        (version,) = unpack('<i', f.read(4))
        assert version <= 5, 'Unknown file version.'

        collision_vertices = []
        collision_faces = []

        if version >= 5:
            f.read(4 * 3)

        (collision_vertex_count,) = unpack('<i', f.read(4))
        for _ in range(collision_vertex_count):
            collision_vertices.append(unpack('<fff', f.read(4 * 3)))
            f.read(4)
        
        (unused_struct_count,) = unpack('<i', f.read(4))
        f.read(4 * 3 * unused_struct_count)

        (collision_face_count,) = unpack('<i', f.read(4))
        for _ in range(collision_face_count):
            (num_vertices,) = unpack('<i', f.read(4))
            vertex_indices = []

            for _ in range(num_vertices):
                (vertex_id,) = unpack('<i', f.read(4))
                vertex_indices.append(vertex_id)
            
            vertex_indices.reverse()
            collision_faces.append(tuple(vertex_indices))

        vertices = []
        faces = []

        (vertex_count,) = unpack('<i', f.read(4))
        for _ in range(vertex_count):
            vertices.append(unpack('<fff', f.read(4 * 3)))

        (face_count,) = unpack('<i', f.read(4))
        for _ in range(face_count):
            f.read(4)
            (num_vertices,) = unpack('<i', f.read(4))
            vertex_indices = []

            for _ in range(num_vertices):
                (vertex_id,) = unpack('<i', f.read(4))
                vertex_indices.append(vertex_id)
                f.read(4 * 4)
            
            f.read(4 * 4)
            
            vertex_indices.reverse()
            faces.append(tuple(vertex_indices))
        
        window_vertices = []
        window_faces = []

        (window_count,) = unpack('<i', f.read(4))
        for _ in range(window_count):
            (num_vertices,) = unpack('<i', f.read(4))
            vertex_indices = []

            for _ in range(num_vertices):
                vertex_indices.append(len(window_vertices))
                window_vertices.append(unpack('<fff', f.read(4 * 3)))
            
            vertex_indices.reverse()
            window_faces.append(tuple(vertex_indices))
        
        name = bpy.path.display_name_from_filepath(filepath)
        shared.load_mesh(context, name, vertices, faces, None)
        shared.load_mesh(context, name + '.collision', collision_vertices, collision_faces, None)
        shared.load_mesh(context, name + '.windows', window_vertices, window_faces, None)
    
    return {'FINISHED'}
