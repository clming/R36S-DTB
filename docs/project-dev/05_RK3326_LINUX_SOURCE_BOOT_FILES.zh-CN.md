# 由 Panel4 compatible 定位 Linux 源码及掌机启动必需文件

版本：V0.1；核查日期：2026-10-29。对象为本仓库 [Panel4.dts](../../DTS/Panel4.dts) 和 [Panel 4/boot.ini](../../R36S/Panel%204/boot.ini)。本文回答：**Linux 源码工程在哪里、能生成什么、掌机真正运行起来还缺哪些文件、分别去哪里取得。**

## 1. 结论：最直接对应的是 Hardkernel 的 Linux BSP 工程

与题述 compatible 直接对应的源码起点为：

| 项目 | 明确位置 |
| --- | --- |
| Linux 源码工程 | [hardkernel/linux](https://github.com/hardkernel/linux) |
| 应选分支 | [odroidgoA-4.4.y](https://github.com/hardkernel/linux/tree/odroidgoA-4.4.y)，不是仓库默认显示的其他设备分支 |
| 对应板级源文件 | [arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts) |
| DTS 原始文本 | [直接读取/保存 DTS](https://raw.githubusercontent.com/hardkernel/linux/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts) |
| 本次 API 查询到的分支提交 | `faeb665a41b53ebb386e69fe737ccf0707aaf07b` |
| 固定提交的源码树 | [按该提交查看工程](https://github.com/hardkernel/linux/tree/faeb665a41b53ebb386e69fe737ccf0707aaf07b) |
| 分支源码 ZIP | [下载分支源码 ZIP](https://github.com/hardkernel/linux/archive/refs/heads/odroidgoA-4.4.y.zip)；分支可移动，正式开发需固定提交 |

**找到的是具有明确配置关联的参考内核工程，尚未找到原卡 Image 的确切构建记录。** 不能仅凭 compatible 就断言这个公开分支未经修改便能生成原卡内核，或直接适配本机屏幕、按键和电源。

### 1.1 匹配依据

本仓库第 4 行为：

```dts
compatible = "rockchip,rk3326-odroidgo3-linux\0rockchip,rk3326";
```

Hardkernel 对应板级 DTS 的根节点为：

```dts
compatible = "rockchip,rk3326-odroidgo3-linux", "rockchip,rk3326";
```

前者的 `\0` 将字符串分开，表达的两个兼容标识与后者相同。前一个是板级兼容标识，后一个是 SoC 通用标识。该属性是硬件/软件匹配信息，不是内核下载地址、构建版本号或完整来源证明。[对应上游源码](https://raw.githubusercontent.com/hardkernel/linux/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts)

本仓库的 `model` 已改为 `Game Console R35S/R36S fix by lxc`，说明文件并非仅按根节点名称理解即可。即使两份树的根 compatible 相同，它们的屏、GPIO、供电和驱动依赖仍可能不同。

### 1.2 除字符串外，本次还核实了什么？

在上述固定提交中，通过 GitHub API 读取了以下配置：

| 文件 | 核实内容 | 意义 |
| --- | --- | --- |
| [设备树构建清单](https://github.com/hardkernel/linux/blob/faeb665a41b53ebb386e69fe737ccf0707aaf07b/arch/arm64/boot/dts/rockchip/Makefile) | 包含 `rk3326-odroidgo3-linux.dtb` 构建项 | 对应 DTS 在该工程中有真实构建目标 |
| [odroidgoa_defconfig](https://github.com/hardkernel/linux/blob/faeb665a41b53ebb386e69fe737ccf0707aaf07b/arch/arm64/configs/odroidgoa_defconfig) | `CONFIG_ARCH_ROCKCHIP_ODROIDGOA=y`、`CONFIG_JOYSTICK_ODROIDGO3=y` | 有同平台/输入支持的配置起点 |
| 同一配置 | `CONFIG_BATTERY_RK817=y`、`CONFIG_CHARGER_RK817=y`、`CONFIG_SND_SOC_RK817=y` | 包含 RK817 电池、充电与音频功能的配置 |
| 同一配置 | `CONFIG_DRM_PANEL_SIMPLE=y` | 包含通用 panel 驱动配置，但仍要确认目标屏的属性与命令支持 |

这些是“源码及配置已存在”的证据，不是本次编译成功或实机通过的证据。部分文件请求遇到 HTTP 429，本文未据此虚构具体内核小版本、额外驱动文件内容或构建结果。

### 1.3 如何取得完整工程？

可以使用 GitHub 的 Download ZIP，或以后在选定工作目录执行以下命令。这里仅提供示例，本次未克隆或安装任何内容：

```powershell
git clone --single-branch --branch odroidgoA-4.4.y https://github.com/hardkernel/linux.git linux-rk3326-hardkernel
git -C linux-rk3326-hardkernel rev-parse HEAD
```

克隆的是该分支当时的最新状态；应记录实际输出的提交。若需要完全固定本次源码快照，可使用[固定提交 ZIP](https://github.com/hardkernel/linux/archive/faeb665a41b53ebb386e69fe737ccf0707aaf07b.zip)。ZIP 不包含 Git 历史，仍需另行记录来源与提交。

不要只下载一个 DTS 就认为已取得 Linux 工程：它还引用同目录 DTSI、`include/dt-bindings/` 头文件，并依赖对应驱动、配置和内核构建系统。带头文件/宏的内核 DTS 应通过对应内核构建系统处理，不能直接套用纯展开式 DTS 的 dtc 命令。

### 1.4 其他源码应放在什么位置理解？

| 源码 | 用途 | 与上述精确匹配工程的关系 |
| --- | --- | --- |
| [rockchip-linux/kernel：develop-4.4](https://github.com/rockchip-linux/kernel/tree/develop-4.4) | 芯片厂商通用 BSP 参考 | 适合查公共 SoC/驱动，不等于本掌机专用系统 |
| [christianhaitian/linux：rg351](https://github.com/christianhaitian/linux/tree/rg351) | ArkOS/RG351 相关内核研究；[README](https://github.com/christianhaitian/linux/blob/rg351/README)有构建说明 | 可以追查发行版改动，但不能由 RG351 名称直接保证 R36S 适配 |
| [AndreRenaud/linux-r36s：r36s-v6.10](https://github.com/AndreRenaud/linux-r36s/tree/r36s-v6.10) | 社区较新 Linux 的 R36S 适配参考 | 另一内核路线，不能混用旧 BSP 的模块、设备树属性和图形栈 |

若目标是先研究 Panel4 的旧 BSP 配置，优先读 Hardkernel `odroidgoA-4.4.y`；若目标是重现原卡，则必须继续取得原卡内核版本、配置、模块、厂商补丁和实际源提交。

## 2. Linux 内核工程能生成什么，不能替代什么？

| 输出或资料 | 通常由哪里产生 | 在运行系统中的位置/作用 |
| --- | --- | --- |
| `Image` | 内核源码按目标配置编译 | Linux 内核，放到启动配置指定位置 |
| 板级 `.dtb` | 同工程内的 DTS/DTSI 经构建生成 | 启动时交给内核描述硬件 |
| `.ko` 模块及依赖信息 | 选择模块化驱动时随内核构建/部署 | 根文件系统中，通常为 `/lib/modules/<kernel-release>/` |
| `.config`、源码提交、构建日志 | 开发过程记录 | 用于复现和维护，通常不是启动器加载的文件 |
| 发行版 `uInitrd` | 发行版/项目的初始文件系统生成与必要封装流程 | 启动早期环境；不是普通内核构建自动提供的完整发行版产物 |
| 正式 rootfs | 发行版制作流程、Buildroot 等系统构建工具 | 包含 init、库、服务和应用，不能由一个 DTB 代替 |
| U-Boot/早期加载器 | 单独的引导工程及平台固件流程 | 在 Linux 之前运行，不属于 Image 本身 |
| 前端、模拟器、游戏库 | 应用构建/系统集成及内容准备 | 进入菜单、游玩所需，不包含在普通 Linux 内核产物中 |

内核也支持将特定 initramfs 编进镜像，但这需要明确配置与内容；不能据此认为下载内核源码就自带原机 rootfs 或游戏系统。[Linux initramfs 说明](https://docs.kernel.org/filesystems/ramfs-rootfs-initramfs.html)

## 3. 明确“掌机运行起来”的三个层次

| 目标 | 至少要具备的内容 | 完成标志 |
| --- | --- | --- |
| A：Linux 能进入初始用户态 | 正确的硬件/供电、早期引导与 DDR 初始化、内核、匹配 DT、可执行的 init 及其所需环境 | 能进入终端或目标 init；不代表有游戏菜单 |
| B：进入掌机菜单 | A 加正式用户态、必要驱动/库、显示/音频/输入配置和前端 | 可用实体按键操作菜单，能正常关机 |
| C：实际游玩并保存 | B 加匹配模拟器/核心、内容、必要 BIOS、存档路径和热键 | 游戏能启动、控制、播放声音、保存、退出并恢复进度 |

“只有 Image + DTB”一般不足以形成完整掌机系统；“能进 Linux”也不等于前端和游戏体验已经完成。下面按本仓库 boot.ini 这种启动方案列出具体文件。

## 4. 本仓库启动方案必要的镜像和文件

### 4.1 必需项、条件项和非运行文件

| 项目 | 对本方案是否需要 | 作用及取得方式 |
| --- | --- | --- |
| 芯片 BootROM | 上电必需，已固化在 SoC | 无需向卡里下载一个同名文件；它按平台规则寻找后续引导内容 |
| 早期引导/DDR 初始化 | 冷启动必需，具体组成依方案 | 可包含 DDR 初始化、SPL/TPL/miniloader 等环节，名称/组合各异；优先从匹配完整系统或方案商取得 |
| U-Boot 及所需平台固件 | 本模板运行前需要已有可用引导链 | 从完整镜像保留；自行开发参考对应 U-Boot 工程及配套固件，不能只复制普通 BOOT 文件替代 |
| 分区表和正确引导布局 | 系统卡启动需要 | 完整 `.img` 通常包含这些布局；实际以系统说明为准 |
| `boot.ini` | 目标 U-Boot 确实使用它时需要 | 指定加载项和 root 参数；使用原系统自己的配置，仓库只作参考 |
| `Image` | 本模板需要 | 内核；从原卡/同一系统镜像取得，或由匹配源码配置构建 |
| `uInitrd` | 本模板明确加载，按此方案保留 | 早期文件系统；优先同一原卡或镜像配套文件，不从其他系统随意拼接 |
| `rk3326-r35s-linux.dtb` | 本模板明确加载 | 目标硬件设备树；文件名由加载行决定，内容仍需与主板/屏/内核一致 |
| 正式根文件系统 rootfs | 本模板的 `root=` 指向正式根分区，因此需要 | 至少含可用 init 及其依赖；掌机系统还含库、服务、前端等；优先保留完整系统的配套根分区 |
| 内核模块 `.ko` | 所需驱动编为模块时需要 | 与内核发布号、配置、符号等匹配；驱动全内建时相应模块不必存在 |
| `/lib/firmware` 等固件数据 | 具体驱动需要时才需要 | 由驱动及外设决定，不是所有 RK3326 都使用同一组文件 |
| 图形/音频/输入用户态库 | 要运行对应掌机应用时需要 | 例如匹配的图形栈、SDL/ALSA 等，依选用系统/程序决定；不是强制固定为某一套 GPU 二进制 |
| EmulationStation 等前端 | 要进入图形游戏菜单时需要 | 由完整掌机系统集成，或自行编译/配置 |
| RetroArch+核心/独立模拟器 | 要运行对应游戏时需要 | 从系统、上游或自己的匹配构建取得 |
| 游戏内容、部分平台的 BIOS | 玩相应内容时需要 | 与系统软件分开准备，核对格式、来源和分发条件 |
| `.dts`、`.dtsi`、dtc 工具 | 开发需要，启动器不必加载 | 属于源码与主机侧工具，不能将 DTS 当作 DTB 直接加载 |
| `logo.bmp`、主题、开机动画 | 仅特定流程引用时需要 | 是否缺失影响启动由实际流程决定，不能一概列为 Linux 必需项 |

**外部 uInitrd 并非所有 Linux 启动方案的普遍必需项。** 内建驱动并直接挂载 rootfs，或采用其他早期用户态设计时可以不同；但本仓库模板明确加载它，在没有验证新方案前不能直接删除、改为空文件或省略参数。[U-Boot booti 说明](https://docs.u-boot.org/en/latest/usage/cmd/booti.html)

### 4.2 直接从 boot.ini 看出要读什么

```text
load mmc 1:1 ${loadaddr} Image
load mmc 1:1 ${initrd_loadaddr} uInitrd
load mmc 1:1 ${dtb_loadaddr} rk3326-r35s-linux.dtb
booti ${loadaddr} ${initrd_loadaddr} ${dtb_loadaddr}
```

三行分别加载内核、初始文件系统、设备树；最后启动 Linux。这里的 `mmc 1:1` 是 U-Boot 的设备/分区编号，不直接等于 Linux 设备名或外壳 TF1/TF2 标记。

模板还包含固定根分区 UUID `e139ce78-9841-40fe-8823-96a304a09859`。它指向正式 rootfs；因此即便三个文件都在，根分区错误、损坏或缺少 init 仍无法正常进入系统。详细参数解释见[boot.ini 专题](04_CHIPS_BOOT_EMULATORS_GAMES.zh-CN.md#2-bootini-是什么文件)。

本模板没有加载 `rg351mp-kernel.dtb`。它是另一个设备树文件，不是 Image 内核的替代品；同目录存在并不代表正在使用。

### 4.3 文件可能不在资源管理器能看到的位置

系统卡可能同时包含：分区表、分区外原始引导区域、BOOT 文件系统、正式 Linux 根文件系统，以及内容分区。确切布局取决于系统，并非所有发行版都有相同数量或名称的分区。

Windows 能看到 BOOT 或 EASYROMS，不等于已看到整套系统；ext4 根分区和引导区域可能不在普通资源管理器中显示。**只备份 boot.ini、Image、uInitrd、DTB，不能代替整卡备份。** 反过来，将这几项复制到空白 FAT 卡，也不等于制作了一张可启动系统卡。

## 5. 每个必需项在哪里找？

### 5.1 第一优先：保留原卡的整套匹配文件

照片中的系统为 ArkOS 2.0 (08232024)。最快取得可用基线的方法是对原卡做完整备份，并记录实际加载配置、分区、内核版本、模块和 DTB；不先把来自多个项目的文件混到一起。

| 原卡资料 | 如何帮助定位 |
| --- | --- |
| 整卡镜像 | 保留分区表、引导区域、BOOT、rootfs 和原有数据 |
| 启动配置 | 确认真正加载的文件名、存储位置和 root 参数 |
| `uname -a`、可用时的内核配置、启动日志 | 查内核发布号、构建线索和硬件驱动 |
| `/lib/modules/`、图形栈和程序版本 | 确认配套依赖，防止仅换 Image 后失效 |
| 主板丝印、屏排线、文件哈希 | 建立实物到软件的对应关系 |

这些资料能缩小来源范围，但字符串、版本号和 compatible 都不能单独证明某个 GitHub 提交就是原机的完整源码。

### 5.2 第二优先：匹配机型的完整系统镜像

| 系统来源 | 已核实入口/文件 | 能取得什么及限制 |
| --- | --- | --- |
| R35S/R36S 社区 ArkOS | [ArkOS-R3XS Wiki 下载页](https://github.com/AeolusUX/ArkOS-R3XS/wiki) | 维护者提供 R35S/R36S 系统入口；项目已归档。下载版本仍需核对硬件与配套，不能认定就是照片原卡 |
| 原 ArkOS | [官方 Wiki](https://github.com/christianhaitian/arkos/wiki)、[Building](https://github.com/christianhaitian/arkos/wiki/Building) | 下载与构建线索；更新仓库不等于所有目录都是完整镜像 |
| dArkOS 候选 | [v08272026 发布页](https://github.com/christianhaitian/dArkOS/releases/tag/v08272026)，[分卷 001](https://github.com/christianhaitian/dArkOS/releases/download/v08272026/dArkOS_RG351MP_trixie_09022026.img.7z.001)、[分卷 002](https://github.com/christianhaitian/dArkOS/releases/download/v08272026/dArkOS_RG351MP_trixie_09022026.img.7z.002) | API 核实两卷资产存在；需要两卷解压完整 `.img`。RG351MP 文件名不是本机兼容保证 |
| ROCKNIX 候选 | [20261001 发布页](https://github.com/ROCKNIX/distribution/releases/tag/20261001)、[RK3326-a 镜像](https://github.com/ROCKNIX/distribution/releases/download/20261001/ROCKNIX-RK3326.aarch64-20261001-a.img.gz)、[SHA-256 文件](https://github.com/ROCKNIX/distribution/releases/download/20261001/ROCKNIX-RK3326.aarch64-20261001-a.img.gz.sha256) | 维护者发布表将 R36S 列入相应镜像组，仍需核对主板/屏。系统采用自己的内核/DT/启动机制，不要求沿用 ArkOS 的文件布局 |

取得完整镜像后：校验下载 → 解压 → 用已有工具只读检查分区及启动配置 → 保留同一镜像内的引导、Image、initrd、DTB、rootfs 和模块对应关系。提取 BOOT 文件用于分析时，也要保存其来源版本；不要把分析文件直接当作可替换套件。

上述固定版本用于说明明确可追溯的下载入口，不表示它们一定是当前最好版本；本次未下载这些完整镜像，也未验证其与实物兼容。

### 5.3 第三优先：单项文件用于研究或有依据的适配

| 需要的内容 | 可追溯来源 | 使用边界 |
| --- | --- | --- |
| Image | 原卡/同一完整镜像；或匹配内核源码构建。单项候选：[dArkOSRE 固定提交 Image](https://raw.githubusercontent.com/southoz/dArkOSRE-R36/3f372c85aa53a26b265c3dc0c2661ec0fae5faf0/files/BOOT/Image) | 前次会话已检查 ARM64 Image 标识及哈希，见第 3 份文档；没有证明它与原卡或下行历史 initrd 匹配 |
| uInitrd | 原卡/同一系统；历史分析文件：[ArkOS 更新包](https://raw.githubusercontent.com/christianhaitian/arkos/main/01142023/arkosupdate01142023.zip)中的 `boot/uInitrd` | 前次已解包验证存在。该包为历史增量更新，不是完整系统，更不是原卡 08232024 文件的确切副本 |
| Panel4 的 DTS | [本地 Panel4.dts](../../DTS/Panel4.dts)；上游结构参考见第 1 节 | 本地是展开后的硬件配置形式；不要整文件覆盖上游 DTS 后就宣称已完成移植 |
| 本模板的主 DTB | [R36S/Panel 4/rk3326-r35s-linux.dtb](../../R36S/Panel%204/rk3326-r35s-linux.dtb) | 本次目录核对为 90,315 字节；仍需核实硬件/驱动及实际加载路径 |
| V12 Panel4 社区 DTB | [dArkOSRE 对应目录](https://github.com/southoz/dArkOSRE-R36/tree/main/files/BOOT/dtb/r36s/R36S-V12%202023-08-18%20Panel%204) | 板号只提供对应线索，屏、GPIO、电源和内核要分别验证；文件名与本模板不同 |
| 模块与 rootfs | 同一完整系统的根分区；自行开发可参考 [Buildroot](https://buildroot.org/downloads/manual/manual.html) | 没有一份由 compatible 唯一指定的通用 rootfs 下载包；Buildroot 还需配置和移植 |
| U-Boot | 原卡/同一完整镜像；源码参考 [hardkernel/u-boot：odroidgoA-v2017.09](https://github.com/hardkernel/u-boot/tree/odroidgoA-v2017.09) | 原始引导位置、DDR 初始化和打包由平台决定；不提供未经核实的烧录偏移 |
| DDR/启动前置固件 | 匹配 BSP/方案商，及 [Rockchip rkbin](https://github.com/rockchip-linux/rkbin) | 部分是二进制，按具体芯片/DDR/启动方案选择，不要求把仓库里所有文件都装上 |
| 前端与模拟器 | 完整掌机系统；或 [EmulationStation](https://github.com/Aloshi/EmulationStation)、[RetroArch](https://github.com/libretro/RetroArch)、[PPSSPP](https://github.com/hrydgard/ppsspp) 等的匹配构建 | 取得软件不代表已适配全部键位/渲染/声音；核心和内容还需单独准备 |

前次实际下载、长度和哈希记录统一见[第 3 份文档的核查记录](03_FAST_DEVELOPMENT_PLAN.zh-CN.md#37-本次实际下载与检查记录)。本次未重新下载或重复验证这些单项二进制；它们的存在不构成可以跨来源拼装的依据。

## 6. 最快形成一套可维护系统的顺序

1. **先恢复基线**：完整备份原卡，记录它实际使用的 Image、uInitrd、DTB、rootfs、模块和引导布局。
2. **建立源码工作副本**：取得本次定位的 Hardkernel 分支，固定提交，记录 defconfig 与依赖，先理解与原树相同和不同的部分。
3. **对照板级差异**：比较主板/屏、GPIO、RK817、输入、USB；Panel4 已有 `native-mode` 引用等问题需审查，不能直接当生产配置。详细分析见[Panel4 专题](../PANEL4_DTS_KERNEL_ANALYSIS.zh-CN.md)。
4. **分别验证产物**：内核构建要记录 Image/模块；DTS 修改要编译、保留警告并反编译检查；完成后才在可恢复的备用卡上验证。
5. **配套部署**：确认内核/模块/图形栈与 rootfs 匹配，DTB 文件名与加载行一致。只改必要项，保留目标卡原 UUID、内存地址及 initrd 配置。
6. **验收功能**：冷启动、显示/背光、方向键/摇杆/FN、声音、充电/电量；涉及 USB/供电时补测相应功能。
7. **验证游戏体验**：进入前端后，再检查模拟器、合法测试内容、保存、退出和重启读取，不以“能点亮屏”替代整机完成。

失败时先关机取卡，恢复该轮修改前的文件；改过内核则恢复配套模块/依赖，无法确认时换回原卡。不要为了换屏无条件换 Image，也不要整份覆盖本仓库 boot.ini。

## 7. 可以明确交付与仍缺少的证据

| 结论/事项 | 当前状态 |
| --- | --- |
| 找到含完全相同 compatible 的 Linux 工程 | 已找到：Hardkernel `odroidgoA-4.4.y`，对应文件和构建目标见第 1 节 |
| 确认同分支的输入/PMIC/屏驱动配置起点 | 已读取 defconfig 核实相关配置项 |
| 确定原卡 Image 的全部源码/配置/补丁 | 未确定；需要原卡和供方构建证据 |
| Linux 编译、DTB 编译及实机启动 | 本次均未执行，不宣称通过 |
| 定位完整系统候选和单项文件入口 | 已列出；完整镜像本次只检查发布入口/资产元数据 |
| 安装软件、克隆完整内核、刷卡或替换启动文件 | 本次未执行 |

本文的“源码支持”“文件存在”“编译通过”“实机验证”分别记录。`compatible` 提供了可靠的工程搜索线索，但不足以保证系统所有组成均配套。仓库及各上游的许可分别保留，若用于产品出货需按实际采用文件核对来源和履约要求，不改变现有 README 声明。
