# MINI S922X 电视盒子开源工程定位

核查日期：2026-11-17。照片：[电路板.jpg](电路板.jpg)。

通用 Linux、驱动、启动程序及产品固件开发，另见 [S922X 开源研发工程与起步路线](S922X_DEVELOPMENT_SOURCES.zh-CN.md)，包含 Armbian、Yocto、主线 Linux/U-Boot 及启动固件的核查结果。

**目前最值得优先研究的游戏盒子系统工程是 [EmuELEC/EmuELEC](https://github.com/EmuELEC/EmuELEC)，对应 `Amlogic-ng` 目标；底层内核及设备树来源是 [CoreELEC/linux-amlogic](https://github.com/CoreELEC/linux-amlogic)。但本次未找到照片中 `MINI_S922X_V01` 同板号的原厂源码工程，不能把上述平台支持等同于这块主板已经适配。**

这里的“最对应”指已核实提供 S922X 支持、系统构建入口和可追踪内核来源的候选工程。若要找这块板出厂固件的原始工程，仅凭当前照片还无法确定；也无法由照片确认它出厂运行 EmuELEC、Batocera 或 Android。

## 1. 照片中的硬件线索

识别对象是手持的前景大板，背景桌上的其他主板不参与型号判断。

| 项目 | 照片观察 | 可以确定的范围 |
| --- | --- | --- |
| 主板丝印 | `MINI_S922X_V01` | 查找原厂工程的首要板号 |
| 日期丝印 | `2026-09-08` | 仅为板面可见文字，不作为固件版本或兼容性依据 |
| 主控 | `Amlogic S922X` | 应优先核查 Amlogic S922X / G12B 平台，与本仓库 RK3326 掌机配置不同 |
| 无线模块 | `AP6212` | 可用于进一步核对驱动、固件和供电接线；不能据此保证 Wi-Fi 或蓝牙可用 |
| 接口 | 可见卡槽、USB-A、HDMI 外形接口、RJ45 外形接口和电源插座等 | 接口外形不能证明 USB 速率、网口速率或 GPIO 接线 |
| 内存及存储 | 照片不足以可靠读取全部完整料号 | 不填写推测的 RAM/eMMC 容量，不据照片直接指定 2G/4G DTB |

## 2. 首选工程 EmuELEC

- 官方代码：[EmuELEC/EmuELEC](https://github.com/EmuELEC/EmuELEC)
- 官方支持说明：[Supported Devices](https://github.com/EmuELEC/EmuELEC/wiki/Supported-Devices)
- 官方发布入口：[Releases](https://github.com/EmuELEC/EmuELEC/releases)

选择依据：官方支持说明明确列出 S922X/A311D 及相关电视盒子，项目集成游戏前端和模拟器，README 提供 Amlogic 系统镜像的构建入口。它比单独的 RetroArch 或 EmulationStation 仓库更适合从整机系统层面研究电视游戏盒子。支持说明同时指出，不同盒子变体仍可能无法启动或有网络等外设问题。以上是平台与用途的匹配，尚无该板号的实测证据。

本次读取的 `dev` 提交为 `d4c7b2f143029e4e4d922a077d89eed42c9e37b9`。以下源码链接固定到该提交，便于复核：

| 入口 | 已核实的内容 |
| --- | --- |
| [README.md](https://github.com/EmuELEC/EmuELEC/blob/d4c7b2f143029e4e4d922a077d89eed42c9e37b9/README.md) | 项目用途、依赖和构建命令 |
| [Amlogic-ng/options](https://github.com/EmuELEC/EmuELEC/blob/d4c7b2f143029e4e4d922a077d89eed42c9e37b9/projects/Amlogic-ce/devices/Amlogic-ng/options) | aarch64、Cortex-A73/A53、`LINUX="amlogic-4.9"` 等平台选项 |
| [linux/package.mk](https://github.com/EmuELEC/EmuELEC/blob/d4c7b2f143029e4e4d922a077d89eed42c9e37b9/projects/Amlogic-ce/packages/linux/package.mk) | 内核源码下载地址、固定版本和构建打包逻辑 |
| [linux.aarch64.conf](https://github.com/EmuELEC/EmuELEC/blob/d4c7b2f143029e4e4d922a077d89eed42c9e37b9/projects/Amlogic-ce/devices/Amlogic-ng/linux/linux.aarch64.conf) | 目标内核配置入口；其路径已通过 GitHub 文件列表核实 |
| [bootloader/dtb.conf](https://github.com/EmuELEC/EmuELEC/blob/d4c7b2f143029e4e4d922a077d89eed42c9e37b9/projects/Amlogic-ce/devices/Amlogic-ng/bootloader/dtb.conf) | 包含 GT-King、AM6、Odroid N2 等 S922X DTB 组合配置；这些名称不是照片主板的认证型号 |

### 源码获取和构建入口

下面是 Linux shell 命令，应在满足上游依赖要求的 Debian/Ubuntu 环境中执行；本次未执行编译。先固定本次核查的提交，避免后续分支更新导致路径变化。

```sh
git clone --branch dev https://github.com/EmuELEC/EmuELEC.git
cd EmuELEC
git checkout d4c7b2f143029e4e4d922a077d89eed42c9e37b9
PROJECT=Amlogic-ce DEVICE=Amlogic-ng ARCH=aarch64 DISTRO=EmuELEC make image
```

该命令与所核查 README 的目标一致，是系统构建入口，不代表生成物已适配 `MINI_S922X_V01`。若编译其他版本，应重新核对该版本 README、设备目录和内核来源。

## 3. 底层源码 CoreELEC linux-amlogic

如果目的是修改板级硬件配置、内核驱动或设备树，最直接的代码入口是 [CoreELEC/linux-amlogic](https://github.com/CoreELEC/linux-amlogic)。EmuELEC 上述内核配方在 `amlogic-4.9` 分支条件下引用其提交 `ab03043a776354e02be86d06007751f652680c00`，并记录 `PKG_GIT_BRANCH="amlogic-4.9-20"`。

已读取的相关源码：

| 源文件 | 用途及匹配边界 |
| --- | --- |
| [coreelec_g12b.dtsi](https://github.com/CoreELEC/linux-amlogic/blob/ab03043a776354e02be86d06007751f652680c00/arch/arm64/boot/dts/amlogic/coreelec_g12b.dtsi) | G12B 公共配置，包含对其他 DTS/DTSI 的引用；应沿依赖继续核对 |
| [g12b_s922x_beelink_gt_king.dts](https://github.com/CoreELEC/linux-amlogic/blob/ab03043a776354e02be86d06007751f652680c00/arch/arm64/boot/dts/amlogic/g12b_s922x_beelink_gt_king.dts) | 已有 S922X 电视盒子的板级参考；不能因主控相同直接用于照片主板 |
| [g12b_s922x_ugoos_am6_2g.dts](https://github.com/CoreELEC/linux-amlogic/blob/ab03043a776354e02be86d06007751f652680c00/arch/arm64/boot/dts/amlogic/g12b_s922x_ugoos_am6_2g.dts) | 另一份盒子参考，含 Wi-Fi 电源及 USB 等板级设置，接线须另核实 |
| [g12b_s922x_ugoos_am6_4g.dts](https://github.com/CoreELEC/linux-amlogic/blob/ab03043a776354e02be86d06007751f652680c00/arch/arm64/boot/dts/amlogic/g12b_s922x_ugoos_am6_4g.dts) | 引用 2G 源文件并修改内存设置，说明内存配置不能只按芯片型号选择 |

尚不能在 GT-King、AM6 等参考中确定“哪份 DTB 最接近这块板”。至少还缺少原机设备树、实际内存、以太网 PHY、Wi-Fi/蓝牙接线、USB VBUS、红外和电源配置。AP6212 模块型号相同也不足以确认板级接线一致。

## 4. 其他候选的比较

| 工程 | 核查依据 | 本次定位 |
| --- | --- | --- |
| [EmuELEC/EmuELEC](https://github.com/EmuELEC/EmuELEC) | 官方列出 S922X 支持，具备系统镜像构建入口，并能追踪内核源码 | 游戏盒子系统开发首选候选；无该板号直接适配证据 |
| [CoreELEC/linux-amlogic](https://github.com/CoreELEC/linux-amlogic) | 上述 EmuELEC 配方实际引用的内核，存在多份 S922X DTS | 内核和板级适配的直接源码入口，不是完整游戏系统 |
| [batocera-linux/batocera.linux](https://github.com/batocera-linux/batocera.linux) | [S922X 构建配置](https://github.com/batocera-linux/batocera.linux/blob/3ac8c39892fb46c3bd3df0e8e1f0beabf74ae0e9/configs/batocera-s922x.board)列出 aarch64、Cortex-A73/A53、Linux 6.6.56、Panfrost 及 GT-King 等 DTB；[板级目录](https://github.com/batocera-linux/batocera.linux/tree/3ac8c39892fb46c3bd3df0e8e1f0beabf74ae0e9/board/batocera/amlogic/s922x)存在 | 有明确 S922X 目标的替代游戏系统；同样没有确认照片主板适配 |

Batocera 本次读取的 `master` 提交为 `3ac8c39892fb46c3bd3df0e8e1f0beabf74ae0e9`。其 S922X 配置没有列出 `MINI_S922X_V01`。选择 EmuELEC 优先，依据是其明确面向 Amlogic 电视盒子的模拟器集成和可追踪的厂商内核路线；不是经过两套系统在此板上的性能或兼容性测试得出的结论。

## 5. 精确板号检索的范围

本次使用网页搜索检索了 `"MINI_S922X_V01"`、`"MINI_S922X"`、`"S922X_V01"` 及 `S922X + AP6212 + GitHub` 等组合，并用 GitHub 公开仓库搜索 API 查询：

- [完整板号仓库搜索](https://api.github.com/search/repositories?q=%22MINI_S922X_V01%22)：本次返回 `total_count=0`。
- [板号前缀仓库搜索](https://api.github.com/search/repositories?q=%22MINI_S922X%22)：本次返回 `total_count=0`。

仓库搜索不等同于 GitHub 全量代码搜索。本次没有通过需认证的 GitHub Code Search 穷举全部文件内容，搜索引擎也可能未收录新板号。因此结论是“本次未找到可确认的同板号公开工程”，不能据此断言该板源码不存在或一定闭源。

## 6. 确认原厂工程还需要的证据

1. 向主板供方索取 `MINI_S922X_V01` 对应的 SDK/BSP 仓库、分支、提交号、板级 DTS、defconfig、U-Boot/DDR 配置和原厂恢复镜像。仅提供一个 S922X 通用仓库链接不足以建立对应关系。
2. 从仍能启动的原系统收集系统版本、内核版本、启动配置、启动日志和实际加载的 DTB。若原系统暴露 `/sys/firmware/fdt` 或 `/proc/device-tree`，可据此取得运行时设备树；路径是否存在取决于原系统。
3. 将原机设备树与上述候选 DTS 比较，重点检查内存、存储、网口 PHY、无线模块供电/复位、USB、HDMI 音频、红外及电源节点，随后才能决定移植基线。

如后续需要试运行，先备份原系统、启动文件和恢复镜像，使用独立介质一次验证一组配置，确认实际加载的内核和 DTB；失败后恢复本次更改的原文件，并按原系统方式启动。本报告不提供未经核对的整份启动配置覆盖方案。

## 7. 验证状态

已完成照片人工识别、GitHub 仓库和文件路径核查、上述关键源码内容读取，以及本地文档链接、代码块和差异空白检查。电视盒子目录目前没有可用于比对的 DTS 或 `boot.ini`，本仓库的 RK3326 掌机配置不作为此板的适配依据。

未执行系统构建、DTS 编译、刷机或硬件测试；未确认照片主板的出厂系统、RAM/eMMC 容量和外设兼容性。目录中的视频不作为本次固件身份或模拟器能力的证据，不能凭文件名 `PS2.mp4` 推断存在可复现的开源 PS2 方案。
