import bpy
import bmesh
from struct import unpack


def load(context, filepath):
    with open(filepath, 'rb') as f:
        f.read(4) # Magic number

        (version,) = unpack('<i', f.read(4))
        assert version == 3, 'Unknown file version.'

        vertices = []
        faces = []

        (vertex_count,) = unpack('<i', f.read(4))
        for _ in range(vertex_count):
            pos = unpack('<fff', f.read(4 * 3))
            vertices.append(pos)
            f.read(4 * 3)

        (face_count,) = unpack('<i', f.read(4))
        for _ in range(face_count):
            (num_vertices,) = unpack('<i', f.read(4))
            vertex_indices = []

            for _ in range(num_vertices):
                (vertex_id,) = unpack('<i', f.read(4))
                vertex_indices.append(vertex_id)
            
            vertex_indices.reverse()
            faces.append(tuple(vertex_indices))
            f.read(8)
        
        name = bpy.path.display_name_from_filepath(filepath)
        
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(
            vertices,
            (),
            faces
        )

        bm = bmesh.new()
        bm.from_mesh(mesh)

        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.001)

        bm.to_mesh(mesh)
        bm.free()

        mesh.validate()
        mesh.update()

        obj = bpy.data.objects.new(name, mesh)
        
        view_layer = context.view_layer
        collection = view_layer.active_layer_collection.collection

        collection.objects.link(obj)
        obj.select_set(True)

        view_layer.update()

    
    return {'FINISHED'}
