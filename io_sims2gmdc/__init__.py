'''
Copyright (C) 2018 SmugTomato

Created by SmugTomato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy.props import PointerProperty

from .blender_import import ImportGMDC
from .blender_export import ExportGMDC
from .ui_panel       import(PROP_GmdcSettings,
                            OP_AddMorph,
                            OP_UpdateNeckFix,
                            OP_UpdateMorphNames,
                            OP_HideShadows,
                            OP_UnhideShadows,
                            OP_HideArmature,
                            OP_UnHideArmature,
                            OP_SyncMorphs,
                            OP_AddGMDCParams,
                            OP_NormalsToVertexColor,
                            GmdcPanel)


bl_info = {
    "name": "Sims 2 GMDC Tools (Blender 2.80)",
    "category": "Import-Export",
	"version": (0, 3, 1),
	"blender": (2, 80, 0),
	"location": "File > Import/Export",
	"description": "Importer and exporter for Sims 2 GMDC(.5gd) files"
}

classes = [
    ImportGMDC,
    ExportGMDC,
	GmdcPanel,
	OP_AddMorph,
	OP_UpdateMorphNames,
	OP_UpdateNeckFix,
	OP_HideShadows,
	OP_UnhideShadows,
	OP_HideArmature,
	OP_UnHideArmature,
	OP_SyncMorphs,
	OP_AddGMDCParams,
	OP_NormalsToVertexColor,
	PROP_GmdcSettings
]


def menu_func_im(self, context):
    self.layout.operator(ImportGMDC.bl_idname)

def menu_func_ex(self, context):
    self.layout.operator(ExportGMDC.bl_idname)

def register():
	for item in classes:
		bpy.utils.register_class(item)
		
	bpy.types.TOPBAR_MT_file_import.append(menu_func_im)
	bpy.types.TOPBAR_MT_file_export.append(menu_func_ex)
	
	bpy.types.Scene.gmdc_props = bpy.props.PointerProperty(type=PROP_GmdcSettings)


def unregister():
    for item in classes:
        bpy.utils.unregister_class(item)
		
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_im)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_ex)

    del bpy.types.Scene.gmdc_props


if __name__ == "__main__":
    register()
