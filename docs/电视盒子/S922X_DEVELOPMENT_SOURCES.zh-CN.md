# S922X 开源研发工程与起步路线

核查日期：2026-11-17。照片主板的定位见 [MINI S922X 工程调查](GITHUB_SOURCE_RESEARCH.zh-CN.md)。

**以方便开发自己的 Linux 应用和外设为目标，优先采用 ODROID-N2/N2+ 的公开板级支持，配合 `armbian/build`；需要定制产品固件时研究 `meta-meson`；需要修改驱动和启动流程时使用主线 Linux、U-Boot 及 FIP 打包工程。** 这是根据已存在的源码、配置和构建入口作出的路线建议，未在照片主板上编译或实测。

照片中的 `MINI_S922X_V01` 尚未建立与任何公开板级工程的对应关系。以下 ODROID-N2 配置是 S922X 研发参考，不可直接当成这块电视盒子的启动配置。

## 1. 优先研究的代码工程

| 工程 | 已核实的 S922X 相关入口 | 研发用途和限制 |
| --- | --- | --- |
| [armbian/build](https://github.com/armbian/build) | [odroidn2.conf](https://github.com/armbian/build/blob/3e5ec6c2cf399b2a14436cbe7d18d06aaf5e87c5/config/boards/odroidn2.conf)，明确标注 S922X、`meson-g12b`，配置主线 U-Boot 及内核目标 | 通用 Linux 起步首选：构建 Debian/Ubuntu 系统，随后开发应用、服务、网络、音频和外设；目标是已支持的开发板 |
| [superna9999/meta-meson](https://github.com/superna9999/meta-meson) | [hardkernel-odroidn2.conf](https://github.com/superna9999/meta-meson/blob/bc4bced07a532742b6dc5eb1de4897673ffb5576/conf/machine/hardkernel-odroidn2.conf)，引用 `amlogic-s922x.inc`；README 列出 N2/N2+ 及 sdboot 机器配置 | 用 Yocto/OpenEmbedded 组装自己的嵌入式系统，适合裁剪 rootfs、维护软件配方和产品镜像；需要管理各层兼容版本 |
| [torvalds/linux](https://github.com/torvalds/linux) | [meson-g12b-odroid-n2.dts](https://github.com/torvalds/linux/blob/666539eecdf4db623f5e3c3e55cf9f2dfad24aa4/arch/arm64/boot/dts/amlogic/meson-g12b-odroid-n2.dts)，明确包含 `amlogic,s922x` 和 `amlogic,g12b` | 主线内核、设备树、驱动研发入口；内核源码本身不包含完整发行版和所有启动固件 |
| [u-boot/u-boot](https://github.com/u-boot/u-boot) | [odroid-n2_defconfig](https://github.com/u-boot/u-boot/blob/83b1ec64ede9998566e6a82b22848c20a33f4aff/configs/odroid-n2_defconfig)，[官方构建说明](https://docs.u-boot.org/en/latest/board/amlogic/odroid-n2.html) | 主线引导程序研发；可编译 U-Boot，但仍需打包板级早期启动组件 |
| [LibreELEC/amlogic-boot-fip](https://github.com/LibreELEC/amlogic-boot-fip) | [odroid-n2 目录](https://github.com/LibreELEC/amlogic-boot-fip/tree/b54e3bbbcf5613d451230d359d264844eeda7166/odroid-n2)、`build-fip.sh` | 把 U-Boot/BL33 与预编译固件组合成启动产物；不是全部固件的可重建源码 |
| [hardkernel/linux](https://github.com/hardkernel/linux) | `odroidg12-4.9.y` 分支；[odroidn2_drm_defconfig](https://github.com/hardkernel/linux/blob/0e658067af67835a625e41e289effc4ee390d62f/arch/arm64/configs/odroidn2_drm_defconfig)、`odroidg12_defconfig` 均存在 | 板厂旧 BSP 内核参考，适合追查原厂接口与驱动；4.9 路线需另行评估维护和迁移成本 |
| [hardkernel/u-boot](https://github.com/hardkernel/u-boot) | `odroidg12-v2015.01` 分支；[odroidn2_defconfig](https://github.com/hardkernel/u-boot/blob/7d5876d36f4120034f1902b12d6799b147bec884/configs/odroidn2_defconfig) | 板厂启动实现和固件来源参考；与主线的 `odroid-n2_defconfig` 名称不同，不混用构建步骤 |
| [superna9999/pyamlboot](https://github.com/superna9999/pyamlboot) | README 明确列出 S922X/G12B 协议及 Odroid N2/N2+，工具为 `boot-g12.py` | 开放的 USB Boot 协议库和调试工具；须先确认目标板 USB Boot 入口及可用的启动二进制 |

“源码入口存在”不等于“此版本已编译通过”，也不等于“照片主板已兼容”。以上优先级按研发用途选择，不按 GitHub 星数排列。

## 2. 如何选择起步路线

### 通用应用和外设开发

优先在已支持的 ODROID-N2/N2+ 上使用 Armbian。其系统构建框架会组织内核、引导程序、设备树、固件和根文件系统，比从裸内核自行拼接用户空间更方便。该判断依据 [Armbian README](https://github.com/armbian/build/blob/3e5ec6c2cf399b2a14436cbe7d18d06aaf5e87c5/README.md) 和对应板级配置。

下面只生成 N2 参考镜像，不向设备写入。命令在 Linux shell 中执行，主机环境和依赖按该版本 README 准备；本次没有运行构建。

```sh
git clone https://github.com/armbian/build.git armbian-s922x
cd armbian-s922x
git checkout 3e5ec6c2cf399b2a14436cbe7d18d06aaf5e87c5
./compile.sh BOARD=odroidn2 BRANCH=current RELEASE=trixie BUILD_MINIMAL=yes KERNEL_CONFIGURE=no
```

命令组合使用 README 的构建参数和已核实的 `odroidn2` 板名；不是上游对照片主板提供的命令。固定框架提交也不自动固定全部下载依赖，实际研发还应保存依赖版本、补丁和构建日志。

应用开发阶段可先实现自己的界面、音频服务、蓝牙服务和业务程序，再根据需求添加板级驱动。若需要外接 GPIO/I²C/SPI，先核实原理图、引脚复用和电压域，不把开发板排针编号套用到电视盒子。

### 自己维护产品固件

研究 `meta-meson`：它的 README 已给出 `hardkernel-odroidn2`、`hardkernel-odroidn2plus` 以及使用已有厂商 U-Boot 的 sdboot 配置。机器配置、内核配方、应用配方和镜像配方可以分别管理，适合将研发结果固化成产品系统。

版本约束需要特别核对：本次 [conf/layer.conf](https://github.com/superna9999/meta-meson/blob/bc4bced07a532742b6dc5eb1de4897673ffb5576/conf/layer.conf) 声明兼容 `walnascar whinlatter`；[kas 示例](https://github.com/superna9999/meta-meson/blob/bc4bced07a532742b6dc5eb1de4897673ffb5576/kas/kas-poky-meson.yml) 默认机器却是 `amediatech-x96-max`，且其他层跟随 `master`。不能原样运行该示例就声称生成 S922X 镜像；应先选择 N2 机器并固定兼容的 Poky/OpenEmbedded 版本。

### 修改内核或启动流程

先沿主线 Linux 的 N2 DTS 引用阅读 `meson-g12b-s922x.dtsi` 和 N2 公共 DTSI，再定位具体驱动。若使用板厂 4.9 BSP，应把其 DTS、驱动和模块作为同一套基线核对，不能与主线 DTB 任意混配。

主线 U-Boot 官方提供的 N2 编译入口如下。需要预先具备对应交叉编译器与构建依赖：

```sh
git clone https://github.com/u-boot/u-boot.git u-boot-s922x
cd u-boot-s922x
git checkout 83b1ec64ede9998566e6a82b22848c20a33f4aff
export CROSS_COMPILE=aarch64-none-elf-
make odroid-n2_defconfig
make
```

接着可按 [U-Boot 官方说明](https://docs.u-boot.org/en/latest/board/amlogic/odroid-n2.html) 使用 `amlogic-boot-fip`，将生成的 `u-boot.bin` 作为 BL33 打包。这里不提供向 eMMC、SPI 或存储卡写入的命令；能打包 N2 固件还不能证明它适用于照片主板。

## 3. 必须理解的启动固件边界

U-Boot 官方 N2 文档明确指出，创建完整启动镜像仍需取得 Amlogic 未提供源码的固件和工具。`amlogic-boot-fip/odroid-n2` 中实际可见 `bl2.bin`、`bl30.bin`、`bl31.img`、DDR 固件和加密工具等预编译内容。因此：

- 可以修改、编译 Linux 和 U-Boot 的公开部分。
- 可以利用已有板型的固件完成参考板启动镜像打包。
- 不能由这些仓库推出“可以从开源代码独立生成任意 S922X 新主板的完整启动链”。

如果计划自己画 S922X PCB，应在立项时落实芯片供方/BSP 支持、DDR 型号与布线、训练固件、ACS/板级参数、电源时序和原厂恢复路径。**开源设备树不能替代 DDR 初始化资料，也不能解决所有早期启动问题。**

## 4. 图形与现有电视盒子的补充项目

| 方向 | 项目与依据 | 使用边界 |
| --- | --- | --- |
| GPU 图形开发 | [Mesa 官方 Panfrost 文档](https://docs.mesa3d.org/drivers/panfrost.html)，列出 Mali-G52 支持；源码在 [Mesa 官方仓库](https://gitlab.freedesktop.org/mesa/mesa) | 可研究开放图形栈。实际 API、显示输出和性能取决于内核、Mesa 版本及系统集成；不能把 GPU 渲染支持当成视频编解码支持 |
| 通用盒子 Linux 移植参考 | [ophub/amlogic-s9xxx-armbian](https://github.com/ophub/amlogic-s9xxx-armbian)，README 列出 S922X 的 GT-King、AM6、N2、X88 King 等 | 独立社区项目，不是 `armbian/build` 官方工程本身。可参考其设备适配，但仍要找到照片主板的真实硬件配置 |
| 旧盒子内核/BSP | [CoreELEC/linux-amlogic](https://github.com/CoreELEC/linux-amlogic) | 此前报告已追踪 EmuELEC 引用的具体内核提交及 S922X DTS；适合与原机旧内核配置比较 |
| 游戏整机系统 | [EmuELEC](https://github.com/EmuELEC/EmuELEC)、[Batocera](https://github.com/batocera-linux/batocera.linux) | 游戏功能研究入口，详细核查见前份报告；通用研发不必先引入整套游戏发行版 |

主线图形栈与厂商旧内核图形栈应各自完整集成，避免混用不匹配的 GPU 内核模块、用户态库和显示配置。

## 5. 硬件资料入口

[U-Boot 官方 N2 文档](https://docs.u-boot.org/en/latest/board/amlogic/odroid-n2.html) 确认 N2/N2+ 使用 S922X，并指向厂商网站获取原理图。这使 N2 系列成为可结合软件和板级资料研究的参考对象。

- 厂商硬件入口：[ODROID-N2 hardware](https://wiki.odroid.com/odroid-n2/hardware/hardware)。
- 检索到的芯片资料：[S922X Public Datasheet V0.2](https://dn.odroid.com/S922X/ODROID-N2/Datasheet/S922X_Public_Datasheet_V0.2.pdf)。

本次直接读取上述 Wiki 和 PDF 受访问限制，未核查原理图内容或下载 PDF；不据此宣称已获得完整硬件设计包、PCB 工程或量产资料。公开数据手册的存在也不等于完整 TRM、DDR 工具及厂家 SDK 均已公开。

## 6. 对照片主板的实际推进顺序

1. **先保留原机可运行基线。** 备份原系统、启动文件和恢复镜像，记录主板板号、内核、系统版本及实际加载的 DTB；读取启动日志确认启动链。
2. **先做软件原型。** 若原系统具备合适的开发环境，先开发应用；否则在已支持的 N2 参考环境完成功能，减少板级问题和应用问题相互干扰。
3. **随后移植 MINI 主板。** 比较原机与参考板的内存、存储、网口 PHY、无线模块 GPIO、USB VBUS、音频、红外和供电。选择同一内核路线，逐项适配。
4. **分组验证并可恢复。** 使用独立介质，一次只验证一套内核/DTB/模块组合；检查实际加载文件，记录冷启动、显示、声音、输入、网络、USB 与电源行为。失败后恢复本次修改的原文件并返回原启动方式。
5. **最后再考虑自研 PCB。** 取得完整硬件资料、DDR/启动固件支持及可执行的恢复方法后，才把参考板结果迁移到新硬件。

## 7. 核查版本与验证范围

下列提交为本次通过 GitHub API 读取的相应分支 HEAD，方便后续复核；不是经过实机测试的推荐版本组合。

| 仓库 | 分支 | 提交 |
| --- | --- | --- |
| armbian/build | main | `3e5ec6c2cf399b2a14436cbe7d18d06aaf5e87c5` |
| superna9999/meta-meson | master | `bc4bced07a532742b6dc5eb1de4897673ffb5576` |
| torvalds/linux | master | `666539eecdf4db623f5e3c3e55cf9f2dfad24aa4` |
| u-boot/u-boot | main | `83b1ec64ede9998566e6a82b22848c20a33f4aff` |
| hardkernel/linux | odroidg12-4.9.y | `0e658067af67835a625e41e289effc4ee390d62f` |
| hardkernel/u-boot | odroidg12-v2015.01 | `7d5876d36f4120034f1902b12d6799b147bec884` |
| LibreELEC/amlogic-boot-fip | master | `b54e3bbbcf5613d451230d359d264844eeda7166` |
| superna9999/pyamlboot | master | `d2857f4371bcdb7a90d885f24987e03b6d647a8a` |

已核查仓库身份、关键配置/README 内容及相关文件列表，并检查本地链接、代码块和差异空白。未下载完整 SDK，未执行上述构建、固件打包、USB Boot 或硬件测试；未找到 `MINI_S922X_V01` 的直接板级支持证据。
