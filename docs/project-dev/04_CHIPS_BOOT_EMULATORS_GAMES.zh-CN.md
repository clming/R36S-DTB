# RK3326、RK817、boot.ini 与模拟器及游戏文件说明

版本：V0.1；资料核查日期：2026-10-29。本文将芯片、电源、启动文件、模拟器和游戏内容放在同一条使用链上解释。依据包括本地参考电路图、[Panel4.dts](../../DTS/Panel4.dts)、[Panel 4/boot.ini](../../R36S/Panel%204/boot.ini)、附图和官方项目资料。

本地主图使用 [ODROID_GO_ADVANCE_rev1.0.pdf](ODROID_GO_ADVANCE_rev1.0.pdf)，已确认共 24 页。RK817 电路在 **PDF 第 12 页**，图框编号为 13，文件名 `PWR_PMIC_RK817.SchDoc`；PDF 阅读器页码与图框编号不同。它是 Hardkernel ODROID-GO Advance 参考设计，不是照片中 R36S 主板的完整原厂电路。2026-10-29 按当前目录中的文件名更新链接并复核页数及标题。

已确认条件：用户指定主芯片 RK3326；`p1-11.jpg` 为同一块主板正面，`p1-12.jpg` 为反面；照片显示 ArkOS 2.0 (08232024) 和 EmulationStation。具体镜像与源码下载记录见[快速研发路线第 3 节](03_FAST_DEVELOPMENT_PLAN.zh-CN.md#3-已核实的网络资料与使用方法)。

## 1. RK3326 和 RK817 分别做什么？

### 1.1 先看两颗芯片的分工

| 对比项 | RK3326 | RK817 |
| --- | --- | --- |
| 类型 | 主控 SoC，集成 CPU、GPU 和外设控制器 | PMIC 电源管理芯片，集成音频 Codec 等功能 |
| 核心职责 | 运行 Linux、菜单、模拟器，处理计算和画面 | 为系统产生多路电源，参与充电、开关机和音频转换 |
| 游戏逻辑/模拟运算 | 在 CPU 上执行 | 不执行模拟器程序 |
| 图形 | GPU/显示控制器参与渲染和输出 | 为相关电路供电，不生成游戏画面 |
| 内存与存储 | 控制器访问外部 DDR、SD 等 | 为相关器件提供所需电源，具体取决于接线 |
| 音频 | 软件生成数字音频，通过 I²S 等接口输出 | Codec 将数字音频转换为模拟输出，也有输入功能 |
| 软件对应 | Linux 内核、驱动、前端、模拟器 | 由内核运行的 PMIC、regulator、充电、音频等驱动控制 |

### 1.2 RK3326：运行系统与游戏的主控

RK3326 集成四核 ARM Cortex-A35 CPU、Mali-G31 GPU，以及内存、存储、显示、USB、I²C、I²S、GPIO 等接口。芯片能力参考 [Rockchip 官方 RK3326 产品页](https://www.rock-chips.com/a/en/products/RK33_Series/2018/0514/900.html)，其中标注的最高能力不等于本机实际运行频率或已验证性能。

在掌机中，它主要承担以下工作：

1. **执行启动软件和 Linux**：完成早期启动后运行内核，再启动系统服务和用户程序。
2. **运行前端和模拟器**：EmulationStation、RetroArch、模拟核心、PPSSPP 等程序都由 CPU 执行；GPU 是否参与及参与多少，由程序、渲染后端和驱动决定。
3. **连接外部内存和系统卡**：DDR 芯片是外部器件，系统卡也不是 RK3326 内置游戏库。
4. **输出显示**：通过显示控制器和 DSI 等接口连接屏幕；具体屏幕仍需匹配初始化命令、供电、时序和驱动。
5. **处理输入和外设**：读取按键/ADC 摇杆、控制 USB 外设，配合其他芯片读取状态。

因此模拟器是否流畅，既取决于 RK3326，也取决于模拟器实现、核心/游戏、渲染方式、内存、散热和设置。仅凭“支持某个平台”的图标不能证明该平台全部游戏可流畅运行。

### 1.3 RK817：电源、充电和音频管理

参考电路图第 12 页将同一颗 RK817 拆成 `U2A`、`U2B`、`U2C`、`U2D` 多个符号展示，**不是四颗 RK817**。这些分部体现了以下功能：

| 功能 | 电路图中可见的线索 | 对掌机的作用 |
| --- | --- | --- |
| BUCK 降压电源 | 电感、反馈和输出电容；`VDD_ARM`、`VDD_LOG`、`VCC_DDR` 等网络 | 将输入电源转换为主控/内存需要的电源 |
| LDO 稳压 | 多路 LDO 输出；`VCC_1V8`、`VCCIO_SD`、`VCC_SD`、`VCC_LCD` 等 | 为指定外围电路提供稳定电源；名称和连接属于这份参考图 |
| 电池和充电 | USB/系统输入、电池连接、检测电阻等 | 配合外围电路管理充电和监测电池状态 |
| 电源状态控制 | `PWRON`、`RESET`、`PMIC_SLEEP`、`PMIC_INT` | 与主控配合处理开关机、休眠、复位和状态通知 |
| 音频 Codec | I²S、耳机/扬声器相关输出、麦克风输入 | 数字音频与模拟音频之间转换，具体输出按负载与电路设计验证 |
| RTC/时钟 | 低频晶体与时钟引脚 | 支持实时时钟等辅助功能，最终以本板连接为准 |

Linux 的 [RK817 官方设备树绑定](https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/mfd/rockchip%2Crk817.yaml)说明它包含稳压器、RTC、电源键、音频 Codec 和充电管理功能。芯片具备功能，不代表目标主板一定使用了全部功能；电池保护、USB 角色和外围功放也不能仅凭 PMIC 名称判断是否齐全。

### 1.4 两颗芯片怎样协作？

**供电**：RK817 及外围电源电路向 RK3326、DDR 和外设提供不同电源；主控不是简单地直接接电池运行。

**控制**：RK3326 通过 I²C 配置/读取 RK817，RK817 通过中断及相关信号向主控报告事件。上电初期还涉及 PMIC 默认配置和启动时序，并不是一定要先运行 Linux 才有电源输出。

**声音**：模拟器在 RK3326 上生成数字音频，经 I²S 送到 RK817 Codec，再进入耳机/扬声器输出通路。主控负责软件运算，Codec 负责转换及相应模拟电路功能。

**调频与关机**：主控的软件策略可调用电源驱动配合工作；CPU 电压、工作点、充电电流、温控与电量参数必须有硬件依据，不应为了提升帧率凭猜测修改。

在 [Panel4.dts](../../DTS/Panel4.dts) 中，`/i2c@ff180000/pmic@20` 使用 `compatible = "rockchip,rk817"`，下有供电、battery、charger、codec 等节点，声卡在 `/rk817-sound`。这些是源码配置，不是本次对实机的电气测量。

## 2. boot.ini 是什么文件？

### 2.1 它是特定启动方案中的启动配置

本仓库的 boot.ini 是面向相应 U-Boot/系统启动流程的文本配置，内容包含 U-Boot 命令和板级约定。它告诉启动器：**从哪个存储分区取文件、把文件放到哪个内存地址、向 Linux 传哪些参数、最后如何启动内核**。

它与 Windows 常见的 INI 配置格式不同，也不是 Linux 启动后执行的普通 shell 脚本。只有目标启动链实际读取它，修改才会生效。其他系统可能使用 `extlinux.conf`、`boot.scr` 或其他配置，不能仅因为 BOOT 分区有 boot.ini 就认为一定被执行。

Hardkernel 同平台 U-Boot 的 [cfgload 源码](https://github.com/hardkernel/u-boot/blob/odroidgoA-v2017.09/cmd/cfgload.c)包含加载 boot.ini 的逻辑，可作为参考；照片中的固件具体使用哪一版引导程序，仍需原卡和启动日志确认。

### 2.2 本仓库配置摘录

以下保留 [Panel 4/boot.ini](../../R36S/Panel%204/boot.ini) 的有效配置与原始参数，便于对照阅读，**不是用于整份覆盖系统卡的安装模板**：

```text
odroidgoa-uboot-config

setenv bootargs "root=UUID='e139ce78-9841-40fe-8823-96a304a09859' rootwait rw fsck.repair=yes net.ifnames=0 fbcon=rotate:0 console=/dev/ttyFIQ0 quiet splash plymouth.ignore-serial-consoles consoleblank=0 vt.global_cursor_default=0"

setenv loadaddr "0x02000000"
setenv initrd_loadaddr "0x01100000"
setenv dtb_loadaddr "0x01f00000"

load mmc 1:1 ${loadaddr} Image
load mmc 1:1 ${initrd_loadaddr} uInitrd
load mmc 1:1 ${dtb_loadaddr} rk3326-r35s-linux.dtb

booti ${loadaddr} ${initrd_loadaddr} ${dtb_loadaddr}
```

### 2.3 第一行、注释和环境变量

- `odroidgoa-uboot-config` 是该启动方案的头部约定，不是模拟器名称或通用 Windows INI 节名。应随原系统保留，具体解析由对应启动器决定。
- `#` 开头的说明是注释，例如模板中关于升级覆盖 boot.ini 的提醒。
- `setenv 名称 值` 设置 U-Boot 环境变量；`${名称}` 在后续命令中引用变量。它们不是 PowerShell 的变量写法。
- `setenv` 本身通常只更改当前内存中的环境；并不等于执行了持久化 `saveenv`。但每次启动若重新读取 boot.ini，文件里的设置又会被应用。[U-Boot 环境变量说明](https://docs.u-boot.org/en/latest/usage/environment.html)

### 2.4 bootargs：内核和早期用户态收到的启动参数

| 模板参数 | 目的 | 使用注意 |
| --- | --- | --- |
| `root=UUID='e139ce78-9841-40fe-8823-96a304a09859'` | 指向正式根文件系统分区 | UUID 为仓库模板中的固定值，不一定属于用户卡；保留目标系统原值与原有引号规则 |
| `rootwait` | 等待根设备出现 | 常用于 SD/MMC 启动，不能修复错误 UUID |
| `rw` | 请求以可读写方式挂载根文件系统 | 最终挂载策略还受 initramfs 和系统服务影响 |
| `fsck.repair=yes` | 向支持该参数的早期系统传达文件系统修复策略 | 依赖发行版组件；不是保证所有损坏都会自动修好 |
| `net.ifnames=0` | 在支持该机制的系统中关闭可预测网络接口命名 | 不会给没有网络硬件的主板增加 Wi-Fi |
| `fbcon=rotate:0` | framebuffer 控制台不旋转 | 不等于给所有模拟器设置画面方向 |
| `console=/dev/ttyFIQ0` | 模板指定的控制台参数 | 依赖对应内核串口驱动及参数解析；这里忠实记录源码，不将其通用于其他内核 |
| `quiet`、`splash` | 减少日志显示并配合启动画面 | 调试时可能需要查看更完整日志；不是模拟器主题配置 |
| `plymouth.ignore-serial-consoles` | Plymouth 启动画面相关策略 | 只有使用相关组件时才有相应作用 |
| `consoleblank=0` | 控制台不按空闲计时自动黑屏 | 不等于设置游戏待机策略 |
| `vt.global_cursor_default=0` | 虚拟终端默认隐藏光标 | 不影响模拟器内部光标逻辑 |

bootargs 中既有内核参数，也有早期用户态组件识别的参数，并非所有项目都由内核直接执行。[Linux 内核参数说明](https://docs.kernel.org/admin-guide/kernel-parameters.html)

`root=` 指向系统根分区，不是游戏目录，也不是启动分区的盘符。U-Boot 能读到 Image，仍可能因为根分区不匹配而无法进入正式系统。

### 2.5 三个加载地址：都是运行内存位置

| 变量 | 模板值 | 此模板中的用途 |
| --- | --- | --- |
| `loadaddr` | `0x02000000`，即 32 MiB 地址位置 | 暂存内核 Image |
| `initrd_loadaddr` | `0x01100000`，即 17 MiB 地址位置 | 暂存 uInitrd |
| `dtb_loadaddr` | `0x01f00000`，即 31 MiB 地址位置 | 暂存设备树 DTB |

这些是目标机器的 RAM 地址，不是文件大小、卡容量或 SD 卡烧录扇区。能否使用这些地址取决于内存布局、文件长度、解压位置和引导程序约束；文件变大可能发生重叠。不要把另一系统的地址配置机械复制到本机，也不要根据这三个数字推断整机只有 32 MB 内存。

### 2.6 load 命令：文件从哪里来、放到哪里？

以这一行为例：

```text
load mmc 1:1 ${dtb_loadaddr} rk3326-r35s-linux.dtb
```

| 字段 | 含义 |
| --- | --- |
| `load` | 从文件系统读取文件到内存 |
| `mmc` | 使用 MMC/SD 接口访问存储 |
| `1:1` | U-Boot 编号的设备 1、分区 1；不能直接等同于机壳 TF1 丝印或 Linux 的 `/dev/mmcblk1p1` |
| `${dtb_loadaddr}` | 使用前面设置的 DTB 内存地址 |
| `rk3326-r35s-linux.dtb` | 在选定分区中读取的文件名 |

同理，前两行分别加载 Image 和 uInitrd。**加载文件不等于已经执行文件**，`load` 只是把数据送入内存。它还会更新 `filesize` 等环境变量，随后再次 load 会覆盖相关值。[U-Boot load 官方说明](https://docs.u-boot.org/en/latest/usage/cmd/load.html)

因此，将一个名为 `rg351mp-kernel.dtb` 的文件放在同目录，并不会让这行配置自动使用它；需要以实际加载行和目标文件内容为准。

### 2.7 booti：把控制权交给 Linux

```text
booti ${loadaddr} ${initrd_loadaddr} ${dtb_loadaddr}
```

这行以加载的 Image 为内核，把初始内存盘和设备树一起交给 Linux。U-Boot 的通用形式为 `booti <内核地址> <initrd地址[:长度]> <DTB地址>`；具体格式支持还受目标版本和构建配置限制。

官方文档说明，原始 initrd 需要长度参数，支持的封装格式应按相应启动器核实。本模板仅传 initrd 地址，不能据此断言任意名为 uInitrd 的文件都能直接替换。[U-Boot booti 官方说明](https://docs.u-boot.org/en/latest/usage/cmd/booti.html)

尤其不能在加载 DTB 后，直接把当时的 `${filesize}` 当作 uInitrd 长度；那通常已是最后加载文件的长度。本文只解释原配置，不提供未经验证的改写版本。

### 2.8 从启动到游戏菜单，中间还有哪些步骤？

1. 上电后，SoC 的 BootROM 和后续加载器按硬件启动方案工作，完成内存等必要初始化并进入 U-Boot。
2. U-Boot 读取其实际使用的启动配置，加载内核、必要的 initrd 和 DTB。
3. 内核在 RK3326 上运行，结合设备树和驱动初始化显示、输入、存储、RK817 等。
4. 若使用 initramfs，它先运行早期程序，准备并切换到正式根文件系统；具体行为由镜像内容决定。
5. 正式系统的 init/服务启动前端，前端扫描配置指定的内容目录并显示游戏列表。
6. 用户选游戏，前端调用 RetroArch + 核心，或者调用独立模拟器。

所以 boot.ini 不负责安装模拟器、生成游戏库、配置封面或实现 FN 热键。这些工作分别属于 rootfs、应用配置和输入映射。

### 2.9 正确修改与恢复方式

1. 完全关机取卡，备份实际启动分区全部文件；需要完整恢复时保留整卡镜像。
2. 确认该系统确实读取 boot.ini，再确认实际加载的内核、initrd 和 DTB 文件。
3. 换屏通常先保留已有 Image/uInitrd/模块，只改必要的 DTB 或目标系统要求的屏配置；若原文件名已正确，不需要额外改 boot.ini。
4. 保留目标系统自己的 `root=`、UUID、加载地址和其他参数；一次只验证一组配置。
5. 失败后关机取卡，恢复本轮改动前的文件；换过内核时还需恢复配套模块和相关依赖。
6. 模板注释提到的 `boot.ini.default` 和 `bootini`，仅在目标发行版确实提供该机制时采用，不能当作所有 U-Boot 的通用命令。

## 3. 掌机上的模拟器究竟是哪几层软件？

| 层次 | 例子 | 需要的文件 |
| --- | --- | --- |
| 游戏库前端 | EmulationStation 类前端 | 程序、平台/启动配置、字体、主题、封面和元数据 |
| 模拟器运行框架 | RetroArch | 可执行程序、依赖库、视频/音频/输入配置 |
| libretro 核心 | mGBA、Snes9x 等核心 | 针对目标平台构建的核心 `.so`；按具体核心确定功能 |
| 独立模拟器 | PPSSPP、独立版 mGBA 等 | 独立程序、依赖库、配置和必要资源 |
| 游戏内容 | ROM、光盘镜像或移植游戏数据 | 游戏自身文件，不由设备树生成 |
| BIOS/固件 | 部分原平台的系统固件 | 某些核心运行内容时需要；与游戏、模拟器许可分开处理 |

照片中 EmulationStation 可以确认前端家族，但不能确认全部模拟核心和版本。`32 GAMES AVAILABLE` 一般是一个分类的游戏条目计数，不是 32 个模拟器，也不是 CPU 内置 32 款游戏。

## 4. 模拟器在哪里下载？

### 4.1 已核实的官方项目入口

| 软件/用途 | 源码 | 下载/使用说明 | 对 RK3326 掌机的注意点 |
| --- | --- | --- | --- |
| RetroArch | [libretro/RetroArch](https://github.com/libretro/RetroArch) | [官方下载页](https://www.retroarch.com/platforms.html)、[GitHub 发布页](https://github.com/libretro/RetroArch/releases) | 核对 Linux、ARM 位数、动态库与渲染后端；官网下载不代表提供原机专用包 |
| libretro 核心 | [Libretro 官方组织](https://github.com/libretro)，例如 [libretro/mgba](https://github.com/libretro/mgba) | [官方核心安装说明](https://docs.libretro.com/guides/download-cores/) | 先看实际运行核心的 RetroArch 是 32 位还是 64 位，不仅看 CPU 位数 |
| PPSSPP（PSP） | [hrydgard/ppsspp](https://github.com/hrydgard/ppsspp) | [官方下载页](https://www.ppsspp.org/download/) | Linux 包、Windows ARM64 包、Android APK 不能互换；RK3326 性能需逐内容验证 |
| mGBA（GB/GBC/GBA） | [mgba-emu/mgba](https://github.com/mgba-emu/mgba) | [官方下载页](https://mgba.io/downloads.html) | 页面有 Linux ARM64 AppImage；是否能在老掌机系统运行仍取决于依赖与图形环境；也可选 libretro 形式 |
| EmulationStation 原始项目 | [Aloshi/EmulationStation](https://github.com/Aloshi/EmulationStation) | 上游 README 和源码 | 用于理解前端；实际掌机多用特定分支，不由照片直接认定版本 |
| RK3326 社区构建脚本 | [christianhaitian/rk3326_core_builds](https://github.com/christianhaitian/rk3326_core_builds) | 仓库脚本及说明 | 可追踪适配/编译方式，不保证所有脚本今天均构建成功，也不是点一下就得到整套系统 |
| ArkOS 平台与路径配置 | [ArkOS 仓库](https://github.com/christianhaitian/arkos) | [官方模拟器与 Ports 对照页](https://github.com/christianhaitian/arkos/wiki/ArkOS-Emulators-and-Ports-information) | 查具体平台对应的核心、目录、格式和 BIOS；以原卡实际版本为准 |

Libretro 官方说明提供通过菜单下载核心、手动安装核心和特定发行版包管理器等方式，并列出 Linux aarch64 的构建服务目录示例。该目录是通用架构构建，不是 RK3326 原机适配承诺；本次直接访问目录超时，未下载或验证其中核心二进制。

RK3326 能运行 ARM64 软件，也可在配套环境中运行 ARM32 软件。**Windows ARM64 的 `.exe`、Android `.apk`、Linux x86_64 程序和 Linux ARM 程序不是同一种软件包。** `.so` 核心必须与加载它的程序及 ABI 匹配，不能仅凭后缀相同就替换。

### 4.2 掌机出厂前，模拟器一般怎样装进去？

系统制作者取得源码或允许分发的匹配二进制后，完成以下集成：

1. 为目标 Linux/ARM 环境编译前端、模拟器和所需核心，准备配套图形/音频/输入库。
2. 将程序、核心、字体、配置、启动脚本安装到 rootfs 或发行版指定目录。
3. 配置平台分类、内容路径、文件扩展名、启动命令、输入映射和存档位置。
4. 将系统文件、内核、设备树和启动链打包为完整固件镜像。
5. 工厂或用户将镜像写入系统卡，首次启动后即可使用预集成的模拟器。

这解释了为什么普通用户没有逐个安装，却看到许多平台。部分系统后续还能通过自身更新机制更新程序/核心，但更新能力与网络支持由具体系统决定。

**对现有 ArkOS 原机**：优先保留并确认现有模拟器，再按对应发行版更新或集成；不建议为了“版本最新”任意覆盖核心。

**对自研产品**：在固件构建中固定版本、工具链、核心、配置和来源，生成可重复制作的镜像；不能把单台机器手工安装成功当作量产软件交付完成。

### 4.3 选中游戏后，实际发生了什么？

RetroArch 的启动命令概念示例，路径均需换成目标系统真实位置：

```bash
retroarch -L /path/to/mgba_libretro.so /path/to/demo.gba
```

这里 RetroArch 加载一个核心，核心再读取游戏内容。独立模拟器则使用自己的程序和启动参数。前端通过配置替用户调用，并处理退出后返回菜单。[RetroArch 官方命令行说明](https://docs.libretro.com/guides/cli-intro/)

识别原机时，可在掌机 Linux 终端使用以下只读命令，工具须实际存在：

```bash
uname -m
getconf LONG_BIT
command -v retroarch
```

前两个命令不能独立证明每个程序的位数。取得真实可执行文件路径后，若系统有 `file` 工具，再查看该文件的 ELF 类型。继续检查实际生效的 `es_systems.cfg`、用户覆盖配置及启动脚本，确认核心路径、ROM 路径和启动命令；这些文件的位置随发行版/用户配置变化，不能拿一份示例当全部机器的固定路径。

## 5. 里面很多游戏是怎么来的？

### 5.1 游戏内容一般是另行准备和拷入的

常见来源包括作者/发行商提供的文件、自制 Homebrew 游戏、按相应规则取得的原介质备份，或由装卡方整理的内容包。**照片只能证明界面显示了条目，不能证明本机每个文件来自哪家网站、是否完整、是否匹配核心或具有什么分发许可。** 要确认原卡来源，需要游戏文件清单、哈希、供货记录和相应授权材料。

模拟器的开源项目通常提供运行软件，而不是自动附带照片中那些商业游戏。游戏可以由工厂、卖家或用户另行拷入系统卡/内容卡；也可能随某个内容包部署。不能因为把系统镜像写入卡后看到了游戏，就认定游戏由芯片厂商、内核或模拟器开发者提供。

| 文件种类 | 常见表现 | 需要注意 |
| --- | --- | --- |
| 卡带 ROM | `.nes`、`.gb`、`.gbc`、`.gba` 等 | 平台/格式与核心匹配；扩展名不是质量或来源证明 |
| 光盘内容 | `.cue`/`.bin`、`.iso`、`.chd` 等 | 是否支持由核心决定；多文件/多碟需保持引用与组织关系 |
| 街机 ROM 集 | 经常以 `.zip` 存放 | 可能依赖母集、设备/BIOS 文件和特定 ROM 集版本；不是所有 ZIP 都应解压 |
| Homebrew/移植游戏 | ROM 或程序加资源数据 | 依作者发行格式，可能需要单独运行时或资源 |
| BIOS | 固定名称/哈希的原平台固件 | 不等于游戏；不能随意改名伪装成所需版本 |
| 元数据/封面 | 例如 `gamelist.xml`、图片和视频 | 用于列表和展示；抓取封面不会生成可运行游戏 |
| 存档 | 原生保存、即时状态等 | 单独备份；即时存档未必跨核心/版本兼容 |

### 5.2 可以从哪些明确入口取得测试内容？

| 来源 | 入口 | 能解决什么问题 | 分发边界 |
| --- | --- | --- | --- |
| MAME 官方获准提供的游戏 | [MAME ROMs for Free Download](https://www.mamedev.org/roms/) | 获取其列出的部分经典游戏作测试 | 页面明确为免费非商业用途，站点获准提供下载不自动允许随产品/软件捆绑，需原权利人许可 |
| GBDev Homebrew 社区 | [Homebrew Hub 项目与入口说明](https://github.com/gbdev/homebrewhub) | 查找开发者发布的自制内容，再查看各作品作者与文件 | 按具体作品条款处理，社区收录不等于统一授予商业预装权 |
| 自制测试程序 | [240p Test Suite 作者仓库](https://github.com/ArtemioUrbina/240pTestSuite) | 做显示比例、颜色等测试；它是测试套件，不是商业游戏合集 | 按目标平台版本和仓库/组件许可使用，不把它当全部游戏兼容性测试 |
| 作品作者/发行商 | 对应作品的官方发布页或商店 | 取得自制或正式发行的内容 | 确认下载的是 ROM/资源包还是电脑程序，以及能否用于本产品预装 |

本次未寻找或下载来源不明的整卡游戏合集，也未确认原卡各游戏授权。若要商业出货，应将“允许个人游玩”和“允许复制到出售的设备”分开核对；这一点会直接决定产品内容交付方案。

### 5.3 原卡游戏库通常怎样部署？

1. 固件制作者先确定每个平台使用哪个核心/独立模拟器，以及内容目录、支持格式和必要 BIOS。
2. 装卡方准备匹配内容、必要固件及封面/元数据，按平台导入内容分区或第二张卡。
3. 前端扫描或读取清单，显示分类、标题、封面和数量；有些前端没有有效内容就隐藏相应分类。
4. 用户选游戏，前端按平台配置调用模拟器；模拟器读取 ROM、必要 BIOS 和配置。
5. 游玩产生存档、即时状态、截图等，存放于该系统配置指定的位置。

例如某些 ArkOS 布局使用 `/roms`，启用第二张内容卡后可能使用 `/roms2`，在 Windows 上还可能看到 `EASYROMS` 分区。**这些是布局例子，不是每台 R36S 的固定规则**；以[ArkOS 官方平台对照](https://github.com/christianhaitian/arkos/wiki/ArkOS-Emulators-and-Ports-information)及原机实际启动配置为准。

### 5.4 用户怎样添加一个游戏？

1. 先备份内容卡和存档，确定目标系统、平台、默认核心、目录和支持格式。
2. 按当前系统支持的方式传输。首版可采用安全关机后取内容卡，用读卡器拷入；有网络或 USB 功能时按该系统说明使用，不能因接口存在就假设支持电脑传文件。
3. 将取得的内容放入正确平台目录，按核心要求处理压缩包、多碟引用和必要 BIOS。
4. 安全弹出卡，插回原槽，启动后按前端要求刷新列表或重启前端。
5. 检查能否启动、声音/输入是否正常，完成保存、退出、重新启动后的读取测试。

添加 ROM 通常不改 boot.ini、DTS、DTB、Image 或 uInitrd。扫描到标题不等于已经通过运行验证；没有封面也不一定影响运行。

## 6. 对研发和售后的具体落地

建议建立三份相互独立、可以关联的清单：

| 清单 | 最少记录字段 |
| --- | --- |
| 硬件与启动套件 | 主板双面丝印、屏料号、内核/模块/DTB/initrd 版本与哈希、实际启动配置、恢复方法 |
| 模拟器软件 | 前端分支、模拟器/核心、提交/版本、目标架构、依赖、启动参数、热键、存档位置、来源与许可 |
| 游戏内容 | 平台、标题、文件哈希、格式/地区/版本、来源/授权、核心与 BIOS 依赖、测试结果、封面来源 |

故障定位也按层区分：不开机先查电源/引导；内核已启动但挂载失败查 root/initrd；黑屏或输入异常查驱动与 DT；只有某个平台出错查模拟器/核心；只有某个内容打不开查文件、BIOS 和兼容性。不能把所有问题都归结为“换一个 DTB”。

组件许可也分别记录。[Libretro 官方许可表](https://docs.libretro.com/development/licenses/)明确不同核心可能有不同限制。RetroArch 的授权不自动覆盖所有核心、BIOS、ROM、封面或主题；本仓库 README 的声明也不代表所有上游素材都获得新的商业使用授权。

## 7. 本次核查范围

已读取本地 24 页参考 PDF 的总览和 RK817 页、核对 Panel4 DTS 与 boot.ini，并访问上述官方下载/文档和维护者仓库。未连接掌机，未取得原卡文件清单，因此不能确认原机全部模拟器版本、每个游戏的来源或实际运行结果。

本次仅新增本文并在项目指南增加阅读入口；未安装软件、下载模拟器/游戏包、运行构建或烧录，也未修改 DTS、DTB、Image、uInitrd 或 boot.ini。文中命令为说明或未来只读检查示例，启动配置摘录不能直接当作跨系统安装指令。
