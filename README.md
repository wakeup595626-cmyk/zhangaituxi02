# 怪人协会实验室之魔怔九杰 (zhangaituxi02)

English | [中文](README.zh.md)

A third-person 3D game prototype built on **Unreal Engine 5.8**, with a C++ runtime module, original characters and animations, UMG interface work and StateTree-driven behaviour logic.

## Play

A **Windows x64 playable build** — no Unreal Engine installation required — is published under [Releases](https://github.com/wakeup595626-cmyk/zhangaituxi02/releases). It is split into 11 parts; download all of them and merge:

```bat
copy /b part01.bin+part02.bin+part03.bin+part04.bin+part05.bin+part06.bin+part07.bin+part08.bin+part09.bin+part10.bin+part11.bin game.zip
```

Extract the resulting `game.zip` and run the executable inside `Windows/`.

## Build from source

1. Install **Unreal Engine 5.8** (must match `EngineAssociation` in `zhangaituxi02.uproject`).
2. Right-click `zhangaituxi02.uproject` — *Generate Visual Studio project files* (requires Visual Studio 2022 with the C++ desktop workload).
3. Build once from the generated solution — this produces `Binaries/` and `Intermediate/`.
4. Double-click the `.uproject` to open the editor.

Large original assets (for example the model and textures under `Content/GuoShu/Model_071909/`) are stored with **Git LFS**. Install [Git LFS](https://git-lfs.com/) *before* cloning, otherwise those files will only be small pointer stubs.

## Third-party assets are not included

For licensing reasons, the raw asset files of third-party packs are **not redistributed** in this repository. Obtain them yourself and restore them to the listed paths:

| Asset pack | Restore to |
|---|---|
| `Asian_Village` | `Content/Asian_Village/` |
| `Survival_Character` | `Content/Survival_Character/` |
| UE built-in template content (`ThirdPerson`, `LevelPrototyping`, `Variant_*`) | Ships with UE 5.8 — copy from a new template project |

Without them the project still compiles and opens, but some scene and character references will appear missing.

All other assets under `Content/` — including `Construction_VOL1`, `Characters`, `GuoShu`, `GuWu01`, `JiangJun`, `ZhangYuGe`, `FengLaoBan`, `OldLi`, `ShiHai`, `Zhi`, `YanLi`, `XuBuZhang`, `FriendCharacter`, `AiCharacter`, `Audio`, `Input` and `UI` — are original work by the author and **are included in this repository**.


## Project layout

| Path | Description |
|---|---|
| `Source/` | C++ runtime module (`zhangaituxi02`) |
| `Config/` | Engine and project configuration |
| `Content/` | Assets: original characters, animations, UMG widgets, levels |
| `Build/`, `Tools/` | Build scripts and Python helpers |
| `zhangaituxi02.uproject` | Unreal project descriptor |

## Third-party notices

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Community and support

- Report bugs through [GitHub Issues](https://github.com/wakeup595626-cmyk/zhangaituxi02/issues).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Citation

```bibtex
@misc{zhangaituxi02,
  title={Monster Association Lab: The Nine Bewitched},
  author={wakeUp595626-cmyk},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/wakeup595626-cmyk/zhangaituxi02}},
}
```

## License

[MIT](LICENSE) — covering the original code and art assets. Third-party marketplace assets are not covered and are not distributed here.
