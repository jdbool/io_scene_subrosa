bl_info = {
    'name': 'Sub Rosa formats',
    'author': 'jdbool',
    'version': (0, 1, 0),
    'blender': (2, 80, 0),
    'location': 'File > Import-Export',
    'description': 'Import-Export CMO and CMC',
    'warning': '',
    'support': 'COMMUNITY',
    'category': 'Import-Export'
}

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper


class ImportCMO(bpy.types.Operator, ImportHelper):
    """Load a Sub Rosa Object File"""
    bl_idname = 'import_scene.cmo'
    bl_label = 'Import CMO'
    bl_options = {'UNDO'}

    filename_ext = '.cmo'
    filter_glob = StringProperty(
        default='*.cmo',
        options={'HIDDEN'}
    )

    def execute(self, context):
        from . import import_cmo

        keywords = self.as_keywords(ignore=('filter_glob',))
        return import_cmo.load(context, **keywords)


def menu_func_import(self, context):
    self.layout.operator(ImportCMO.bl_idname, text="Sub Rosa Object (.cmo)")


# def menu_func_export(self, context):
#     self.layout.operator(ImportCMO.bl_idname, text="Wavefront (.obj)")


classes = (ImportCMO,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in classes:
        bpy.utils.unregister_class(cls)
