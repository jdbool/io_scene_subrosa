import bpy
import bmesh
from math import pi


def load_mesh(context, name, vertices, faces, vertex_uvs):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(
        vertices,
        (),
        faces
    )

    if vertex_uvs:
        mesh.uv_layers.new(do_init=False)
        mesh.uv_layers[-1].data.foreach_set('uv', [uv for pair in [
            vertex_uvs[l.vertex_index] for l in mesh.loops] for uv in pair])

    bm = bmesh.new()
    bm.from_mesh(mesh)

    bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=0.001)

    bm.to_mesh(mesh)
    bm.free()

    mesh.validate()
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    obj.rotation_euler = (pi / 2, 0.0, 0.0)

    view_layer = context.view_layer
    collection = view_layer.active_layer_collection.collection

    collection.objects.link(obj)
    obj.select_set(True)

    view_layer.update()
