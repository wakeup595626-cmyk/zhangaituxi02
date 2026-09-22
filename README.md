# 怪人协会实验室之魔怔九杰 (zhangaituxi02)

> 用 **Unreal Engine 5.8** 做的 3D 游戏工程  C++ 玩法模块 + 原创角色与动画
> A 3D game project built with Unreal Engine 5.8  C++ gameplay module with original characters and animations.

---

## 中文

### 这是什么

《怪人协会实验室之魔怔九杰》是一个基于 Unreal Engine 5.8 的第三人称 3D 游戏原型。工程包含 C++ 运行时模块、原创角色模型与动画、UMG 界面，以及一套基于 StateTree 的行为逻辑。

### 怎么跑起来

1. 安装 **Unreal Engine 5.8**（版本必须匹配，见 `zhangaituxi02.uproject` 的 `EngineAssociation`）
2. 右键 `zhangaituxi02.uproject`  *Generate Visual Studio project files*（需要 VS 2022 + C++ 桌面开发工作负载）
3. 用 Visual Studio 打开生成的 `.sln` 编译一次（首次编译会生成 `Binaries/` 与 `Intermediate/`）
4. 双击 `.uproject` 启动编辑器

###  第三方资源未包含在本仓库中

出于**授权限制**（Epic 商城 / Fab 的资产许可不允许再分发原始资源文件），以下资源包**已从仓库排除**，请自行获取后放回对应路径：

| 需要自行获取的资源 | 放回位置 |
|---|---|
| `Asian_Village`（亚洲村庄场景） | `Content/Asian_Village/` |
| `Survival_Character`（生存角色） | `Content/Survival_Character/` |
| `Construction_VOL1`（建筑资源包） | `Content/Construction_VOL1/` |
| `Characters`（通用角色资源） | `Content/Characters/` |
| UE 官方模板（`ThirdPerson`、`LevelPrototyping`、`Variant_*`） | UE 5.8 自带，新建模板项目即可拷入 |

**仓库包含的原创内容**（可直接使用）：`GuoShu`、`GuWu01`、`JiangJun`、`ZhangYuGe`、`FengLaoBan`、`OldLi`、`ShiHai`、`Zhi`、`YanLi`、`XuBuZhang`、`FriendCharacter`、`AiCharacter`、`Audio`、`Input`、`UI`、`MyStuff`、`Generated` 等。

> 缺少第三方资源时，工程仍可编译和打开，但部分场景与角色的引用会显示缺失。

### 目录结构

| 目录 | 说明 |
|---|---|
| `Source/` | C++ 运行时模块（`zhangaituxi02`） |
| `Config/` | 引擎与项目配置（`DefaultEngine.ini` 等） |
| `Content/` | 资产：原创角色、动画、UMG 界面、关卡 |
| `Build/` `Tools/` | 构建脚本与 Python 辅助工具 |
| `zhangaituxi02.uproject` | UE 工程描述文件 |

### 大文件说明

超过 GitHub 100 MB 单文件限制的原创资产（如 `Content/GuoShu/Model_071909/` 下的模型与贴图）通过 **Git LFS** 管理。克隆前请先安装 [Git LFS](https://git-lfs.com/)，否则这些文件只会是几 KB 的指针文件：

```bash
git lfs install
git clone https://github.com/wakeup595626-cmyk/zhangaituxi02.git
```

### 许可证

代码与原创美术资源均以 **MIT** 发布，详见 [LICENSE](LICENSE)。**第三方商城资源不在此许可范围内**（本仓库本就未包含它们）。

---

## English

### What is this

*Monster Association Lab: The Nine Bewitched* is a third-person 3D game prototype built on Unreal Engine 5.8. It ships a C++ runtime module, original character models and animations, UMG UI, and StateTree-based behaviour logic.

### Getting started

1. Install **Unreal Engine 5.8** (must match `EngineAssociation` in `zhangaituxi02.uproject`)
2. Right-click `zhangaituxi02.uproject`  *Generate Visual Studio project files* (requires VS 2022 with the C++ desktop workload)
3. Build once from the generated `.sln` (this produces `Binaries/` and `Intermediate/`)
4. Double-click the `.uproject` to open the editor

###  Third-party assets are NOT included

For **licensing reasons** (Epic Marketplace / Fab asset licences do not permit redistributing the raw asset files), the following packs were excluded. Obtain them yourself and restore them to the listed paths:

| Asset pack you need to obtain | Restore to |
|---|---|
| `Asian_Village` | `Content/Asian_Village/` |
| `Survival_Character` | `Content/Survival_Character/` |
| `Construction_VOL1` | `Content/Construction_VOL1/` |
| `Characters` | `Content/Characters/` |
| UE built-in template content (`ThirdPerson`, `LevelPrototyping`, `Variant_*`) | Ships with UE 5.8  copy from a new template project |

The repository **does** include all original content: `GuoShu`, `GuWu01`, `JiangJun`, `ZhangYuGe`, `FengLaoBan`, `OldLi`, `ShiHai`, `Zhi`, `YanLi`, `XuBuZhang`, `FriendCharacter`, `AiCharacter`, `Audio`, `Input`, `UI`, `MyStuff`, `Generated`, and more.

> Without the third-party packs the project still compiles and opens, but some scene and character references will appear missing.

### Large files

Original assets exceeding GitHub's 100 MB per-file limit (e.g. the model and textures under `Content/GuoShu/Model_071909/`) are stored via **Git LFS**. Install [Git LFS](https://git-lfs.com/) before cloning, otherwise those files will only be small pointer stubs.

### License

Code and original art assets are released under **MIT**  see [LICENSE](LICENSE). **Third-party marketplace assets are not covered** (and are not included in this repository).
