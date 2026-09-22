import unreal


def public_members(value):
    return sorted(name for name in dir(value) if not name.startswith("_"))


def main():
    unreal.log("CODEX_IMPORT_API_BEGIN")
    for name, value in (
        ("AssetImportTask", unreal.AssetImportTask()),
        ("FbxImportUI", unreal.FbxImportUI()),
        ("FbxSkeletalMeshImportData", unreal.FbxSkeletalMeshImportData()),
        ("FbxAnimSequenceImportData", unreal.FbxAnimSequenceImportData()),
        ("SkeletalMeshComponent", unreal.SkeletalMeshComponent()),
        ("EditorLoadingAndSavingUtils", unreal.EditorLoadingAndSavingUtils),
    ):
        unreal.log("CODEX_IMPORT_API {}={}".format(name, ",".join(public_members(value))))
    unreal.log("CODEX_IMPORT_API_ENUM {}".format(",".join(name for name in dir(unreal.FBXImportType) if not name.startswith("_"))))
    unreal.log("CODEX_IMPORT_API_ANIM_ENUM {}".format(",".join(name for name in dir(unreal.FBXAnimationLengthImportType) if not name.startswith("_"))))
    mesh = unreal.EditorAssetLibrary.load_asset("/Game/ShiHai/Rig/SK_ShiHai_Animated")
    unreal.log("CODEX_IMPORT_API SHIHAI_MESH_CLASS={}".format(mesh.get_class().get_name() if mesh else "None"))
    if mesh:
        unreal.log("CODEX_IMPORT_API SHIHAI_MESH_MEMBERS={}".format(",".join(public_members(mesh))))
        try:
            materials = mesh.get_materials()
            unreal.log("CODEX_IMPORT_API SHIHAI_MATERIALS={}".format(",".join(m.material_interface.get_path_name() if m.material_interface else "None" for m in materials)))
        except Exception as error:
            unreal.log_warning("CODEX_IMPORT_API MATERIAL_ERROR={}".format(error))
    unreal.log("CODEX_IMPORT_API_END")


if __name__ == "__main__":
    main()
