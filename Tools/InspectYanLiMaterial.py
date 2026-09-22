import unreal


def main():
    material = unreal.EditorAssetLibrary.load_asset("/Game/YanLi/Mesh/M_YanLi")
    texture = unreal.EditorAssetLibrary.load_asset("/Game/YanLi/Mesh/T_YanLi_BaseColor")
    if not material or not texture:
        raise RuntimeError("YanLi material or texture is missing")
    expressions = unreal.MaterialEditingLibrary.get_material_expressions(material)
    unreal.log("CODEX_YANLI_MATERIAL expressions={}".format(len(expressions)))
    for expression in expressions:
        try:
            texture_value = expression.get_editor_property("texture")
            texture_path = texture_value.get_path_name() if texture_value else "None"
        except Exception:
            texture_path = "<not-a-texture-expression>"
        unreal.log("CODEX_YANLI_MATERIAL expression={} texture={}".format(
            expression.get_class().get_name(), texture_path
        ))
    for prop in (unreal.MaterialProperty.MP_BASE_COLOR, unreal.MaterialProperty.MP_ROUGHNESS):
        node = unreal.MaterialEditingLibrary.get_material_property_input_node(material, prop)
        unreal.log("CODEX_YANLI_MATERIAL property={} node={}".format(
            prop, node.get_class().get_name() if node else "None"
        ))
    unreal.log("CODEX_YANLI_MATERIAL used={}".format([
        item.get_path_name() for item in unreal.MaterialEditingLibrary.get_used_textures(material)
    ]))
    unreal.log("CODEX_YANLI_MATERIAL END")


if __name__ == "__main__":
    main()
