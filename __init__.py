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


class ImportCMC(bpy.types.Operator, ImportHelper):
    """Load a Sub Rosa Character File"""
    bl_idname = 'import_scene.cmc'
    bl_label = 'Import CMC'
    bl_options = {'UNDO'}

    filename_ext = '.cmo'
    filter_glob = StringProperty(
        default='*.cmc',
        options={'HIDDEN'}
    )

    def execute(self, context):
        from . import import_cmc

        keywords = self.as_keywords(ignore=('filter_glob',))
        return import_cmc.load(context, **keywords)


class ImportITM(bpy.types.Operator, ImportHelper):
    """Load a Sub Rosa Item File"""
    bl_idname = 'import_scene.itm'
    bl_label = 'Import ITM'
    bl_options = {'UNDO'}

    filename_ext = '.itm'
    filter_glob = StringProperty(
        default='*.itm',
        options={'HIDDEN'}
    )

    def execute(self, context):
        from . import import_itm

        keywords = self.as_keywords(ignore=('filter_glob',))
        return import_itm.load(context, **keywords)


class ImportSBV(bpy.types.Operator, ImportHelper):
    """Load a Sub Rosa Vehicle File"""
    bl_idname = 'import_scene.sbv'
    bl_label = 'Import SBV'
    bl_options = {'UNDO'}

    filename_ext = '.sbv'
    filter_glob = StringProperty(
        default='*.sbv',
        options={'HIDDEN'}
    )

    def execute(self, context):
        from . import import_sbv

        keywords = self.as_keywords(ignore=('filter_glob',))
        return import_sbv.load(context, **keywords)


def menu_func_import(self, context):
    self.layout.operator(ImportCMO.bl_idname, text="Sub Rosa Object (.cmo)")
    self.layout.operator(ImportCMC.bl_idname, text="Sub Rosa Character (.cmc)")
    self.layout.operator(ImportITM.bl_idname, text="Sub Rosa Item (.itm)")
    self.layout.operator(ImportSBV.bl_idname, text="Sub Rosa Vehicle (.sbv)")


# def menu_func_export(self, context):
#     self.layout.operator(ImportCMO.bl_idname, text="Wavefront (.obj)")


classes = (ImportCMO, ImportCMC, ImportITM, ImportSBV)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

    for cls in classes:
        bpy.utils.unregister_class(cls)
