import unreal


def members(value):
    return ",".join(sorted(name for name in dir(value) if not name.startswith("_")))


def main():
    unreal.log("CODEX_MATERIAL_API_BEGIN")
    unreal.log("CODEX_MATERIAL_API LIB={}".format(members(unreal.MaterialEditingLibrary)))
    unreal.log("CODEX_MATERIAL_API PROPERTY={}".format(members(unreal.MaterialProperty)))
    unreal.log("CODEX_MATERIAL_API FACTORY={}".format(members(unreal.MaterialFactoryNew())))
    unreal.log("CODEX_MATERIAL_API TEXSAMPLE={}".format(members(unreal.MaterialExpressionTextureSample())))
    unreal.log("CODEX_MATERIAL_API CONSTANT={}".format(members(unreal.MaterialExpressionConstant())))
    unreal.log("CODEX_MATERIAL_API END")


if __name__ == "__main__":
    main()
