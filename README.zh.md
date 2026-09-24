# 怪人协会实验室之魔怔九杰 (zhangaituxi02)

[English](README.md) | 中文

一款基于 **Unreal Engine 5.8** 的第三人称 3D 游戏原型，包含 C++ 运行时模块、原创角色与动画、UMG 界面，以及基于 StateTree 的行为逻辑。

## 试玩

[Releases](https://github.com/wakeup595626-cmyk/zhangaituxi02/releases) 中提供了 **Windows x64 可玩版**，无需安装 Unreal Engine。因体积原因分成 11 卷，请全部下载后合并：

```bat
copy /b part01.bin+part02.bin+part03.bin+part04.bin+part05.bin+part06.bin+part07.bin+part08.bin+part09.bin+part10.bin+part11.bin game.zip
```

解压得到的 `game.zip`，运行 `Windows/` 目录下的可执行文件即可。

## 从源码构建

1. 安装 **Unreal Engine 5.8**（版本必须与 `zhangaituxi02.uproject` 中的 `EngineAssociation` 一致）。
2. 右键 `zhangaituxi02.uproject`  *Generate Visual Studio project files*（需要 VS 2022 及 C++ 桌面开发工作负载）。
3. 用生成的解决方案编译一次会产出 `Binaries/` 与 `Intermediate/`。
4. 双击 `.uproject` 打开编辑器。

体积较大的原创资产（例如 `Content/GuoShu/Model_071909/` 下的模型与贴图）使用 **Git LFS** 存储。请**先**安装 [Git LFS](https://git-lfs.com/) 再克隆，否则这些文件只会是几 KB 的指针文件。

## 第三方资源未包含在本仓库中

出于授权限制，商城资源包的原始资产文件**不在本仓库中再分发**。请自行获取后放回对应路径：

| 需要获取的资源包 | 放回位置 |
|---|---|
| `Asian_Village` | `Content/Asian_Village/` |
| `Survival_Character` | `Content/Survival_Character/` |
| `Construction_VOL1` | `Content/Construction_VOL1/` |
| `Characters` | `Content/Characters/` |
| UE 官方模板内容（`ThirdPerson`、`LevelPrototyping`、`Variant_*`） | UE 5.8 自带，从新建模板项目拷贝即可 |

缺少它们时工程仍可编译与打开，但部分场景与角色的引用会显示缺失。

## 目录结构

| 路径 | 说明 |
|---|---|
| `Source/` | C++ 运行时模块（`zhangaituxi02`） |
| `Config/` | 引擎与项目配置 |
| `Content/` | 资产：原创角色、动画、UMG 界面、关卡 |
| `Build/`、`Tools/` | 构建脚本与 Python 辅助工具 |
| `zhangaituxi02.uproject` | UE 工程描述文件 |

## 第三方声明

参见 [THIRD_PARTY_NOTICES.zh.md](THIRD_PARTY_NOTICES.zh.md)。

## 社区与支持

- 通过 [GitHub Issues](https://github.com/wakeup595626-cmyk/zhangaituxi02/issues) 报告问题。

## 参与贡献

参见 [CONTRIBUTING.zh.md](CONTRIBUTING.zh.md)。

## 引用

```bibtex
@misc{zhangaituxi02,
  title={Monster Association Lab: The Nine Bewitched},
  author={wakeUp595626-cmyk},
  year={2026},
  publisher={GitHub},
  howpublished={\url{https://github.com/wakeup595626-cmyk/zhangaituxi02}},
}
```

## 许可证

[MIT](LICENSE)  覆盖原创代码与美术资源。第三方商城资源不在授权范围内，且未在此分发。
