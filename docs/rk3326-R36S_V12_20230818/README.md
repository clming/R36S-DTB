# rf3536k3ka：设备树、内核源码与镜像下载

核查日期：2026-11-05。本文针对本目录 `zj_boot/` 原卡备份和 [原卡设备树 rf3536k3ka.dts](zj_boot/rf3536k3ka.dts)，记录实际验证过的下载来源。

**已找到与本地逐字节一致的 `uInitrd`、`extlinux.conf` 和启动图片下载来源；尚未确认与本地 `Image`、DTB 完全一致的公开下载，也未找到能确定重建本地内核的完整对应源码。** 同名文件不代表相同内容。

## 1. 官方来源与社区参考

| 来源 | 地址 | 已确认性质 |
| --- | --- | --- |
| Rockchip 官方内核 | [rockchip-linux/kernel develop-5.10](https://github.com/rockchip-linux/kernel/tree/develop-5.10) | 芯片厂商公开的平台基础源码 |
| Rockchip 官方 V12 DTS | [rk3326-evb-lp3-v12-linux.dts](https://github.com/rockchip-linux/kernel/blob/95a3ad83f7f90e0e672b9c99b0858b4964318667/arch/arm64/boot/dts/rockchip/rk3326-evb-lp3-v12-linux.dts) | model/compatible 相同的开发板参考，默认屏幕为 720×1280，并非当前掌机完整配置 |
| 同源 DTS 项目 | [immo2n/R36S-K36-DTB-PATCH](https://github.com/immo2n/R36S-K36-DTB-PATCH) | 个人社区项目，不是掌机厂商官方发布 |
| 相近原厂卡备份 | [ArkOS4Clone issue #530](https://github.com/lcdyk0517/arkos4clone/issues/530)、[issue #372](https://github.com/lcdyk0517/arkos4clone/issues/372) | 用户自行提取并上传的原厂卡文件，不是厂商下载站 |
| 社区系统发行版 | [lcdyk0517/arkos4clone](https://github.com/lcdyk0517/arkos4clone) | 维护者发布的 ArkOS/dArkOS 社区移植版，本轮未在本机测试 |

此前记录的“dts 官方文件”链接保留在下面，并按实际来源标记为社区参考。相同 model 字符串不能单独鉴定主板或证明固件兼容。

## 2. 已验证的 DTS / DTB 下载

| 文件 | 网页与下载地址 | 与当前文件的关系 |
| --- | --- | --- |
| 最近的原厂 DTB 样本 | [说明页 #530](https://github.com/lcdyk0517/arkos4clone/issues/530) / [rf3536k3ka.zip](https://github.com/user-attachments/files/33845333/rf3536k3ka.zip) | 解析 phandle 后仅 7 项属性不同，均为屏幕初始化和六个消隐参数；其他非元数据属性一致 |
| 可直接阅读的同源 DTS | [固定提交源码页](https://github.com/immo2n/R36S-K36-DTB-PATCH/blob/cdd88b87c74dca43828a6eda55bc76c98928556e/rf3536k3ka.dts) / [原始 DTS 下载](https://raw.githubusercontent.com/immo2n/R36S-K36-DTB-PATCH/cdd88b87c74dca43828a6eda55bc76c98928556e/rf3536k3ka.dts) | 9 项不同：屏幕配置和 BOOST 最小/最大电压 |
| #530 评论中的 batch 2549 样本 | [原厂 DTB ZIP](https://github.com/user-attachments/files/33850662/rf3536k3ka-stock-dtb.zip) | 9 项不同，不能因文件同名直接覆盖 |
| 启动分区文件备份 | [说明页 #372](https://github.com/lcdyk0517/arkos4clone/issues/372) / [Console.zip 下载](https://github.com/user-attachments/files/28431858/Console.zip) | 包含 Image、uInitrd、DTB、启动配置和图片，一致性见下一节 |

详细差异、候选 DTS 和下载来源见 [GitHub 参考对比报告](github-references-20261105/README.md)。整机主板配置参考优先看 #530；从屏幕初始化序列看，`R36S/Panel 6` 仍比这些外部样本接近。

## 3. Image、uInitrd 等启动文件的下载及一致性

### 3.1 已下载并逐字节核对的启动文件包

下载 [Console.zip](https://github.com/user-attachments/files/28431858/Console.zip)，解压后进入包内 `Consola/`。GitHub 附件没有分别提供每个内部文件的独立下载 URL，需下载 ZIP 后提取。

| 文件 | ZIP 内路径 | 本地字节数 | 与本地 `zj_boot/` 对比 |
| --- | --- | --- | --- |
| Linux 内核 | `Consola/Image` | 30,846,984 | **不一致**；大小相同，哈希和编译版本标识不同 |
| 初始内存盘 | `Consola/uInitrd` | 13,194,771 | **完全一致** |
| 启动配置 | `Consola/extlinux/extlinux.conf` | 283 | **完全一致** |
| 启动图片 | `Consola/logo.bmp` | 127,812 | **完全一致** |
| 内核启动图片 | `Consola/logo_kernel.bmp` | 127,812 | **完全一致** |
| 设备树 | `Consola/rf3536k3ka.dtb` | 本地 107,712；外部 107,328 | 不一致；此为 #372 样本，并非最近的 #530 样本 |

**这是启动分区文件备份，不是可直接烧录的完整系统镜像**，不含完整根文件系统及内核模块目录。本次没有把下载文件替换到本地备份。

| 核验对象 | SHA-256 |
| --- | --- |
| 本地与下载一致的 `uInitrd` | `6f72072ff6dcb16f2b3a064a8f0ebd41d98067e87335df2539ec6dfe94047a1a` |
| 本地 `Image` | `c280af82f967f93ad5a2b8a72734b969b7dafcbe162afb41ca6ef84df7a44b5a` |
| #372 附件内的 `Image` | `eb02faa8f4565f7beb4adce2b9a3b1c6e330848b62d7f3941d7c51435f9aff74` |
| 本地 DTB | `de0329eaede615231f8d0da5c4fac87babd56de22775c3c41e657681a91ab045` |
| 最接近的 #530 DTB | `eec8c4a043e7933392c337766d6f76e357cf8e545869802d955c90f0682ff32d` |

六个启动文件的完整哈希、字节数、内核字符串及 ZIP 哈希见 [启动文件核验记录](github-references-20261105/boot-files-verification.json)。

### 3.2 社区项目提供的独立 Image 下载

以下链接固定到 ArkOS4Clone 提交 `e387c76c192d50b9aaa467f1fa7e6e334febbb54`，本次已检查 HTTP 返回 200，文件大小来自该提交的仓库文件列表；未下载这些 Image 做运行验证。

| 内容 | 直接下载 | 仓库字节数 | 与本地内核的关系 |
| --- | --- | --- | --- |
| 社区 5.10 Image | [下载 Image](https://raw.githubusercontent.com/lcdyk0517/arkos4clone/e387c76c192d50b9aaa467f1fa7e6e334febbb54/boot/dArkOS/consoles/kernel/5.10/Image) | 21,604,360 | 社区 5.10 系列，未证明与本地 5.10.160 是同一构建 |
| 社区修正版 4.4 Image | [下载 Image](https://raw.githubusercontent.com/lcdyk0517/arkos4clone/e387c76c192d50b9aaa467f1fa7e6e334febbb54/boot/dArkOS/consoles/kernel/arkos4clone_fix/Image) | 12,083,208 | 社区旧内核适配方案 |
| 社区原始 4.4 Image | [下载 Image](https://raw.githubusercontent.com/lcdyk0517/arkos4clone/e387c76c192d50b9aaa467f1fa7e6e334febbb54/boot/dArkOS/consoles/kernel/original/Image) | 12,083,208 | 同大小不代表与修正版内容相同 |

本轮未在这些社区仓库中找到可单独下载、并证明与本机一致的配套 `uInitrd`；社区系统的配套启动文件可从其正式发布的整卡镜像中提取，地址见第 5 节。

## 4. 内核源码地址与对应程度

### 4.1 本地 Image 的实际版本

从本地二进制直接提取：

```text
Linux version 5.10.160-g3ee18cae74dc-dirty (pangjianwen@git)
aarch64-libreelec-linux-gnu-gcc-11.3.0 (GCC) 11.3.0
GNU ld (GNU Binutils) 2.39
#1 SMP Fri Jan 23 18:19:18 CST 2026
```

#372 的 Image 为 `5.10.160-g0bc6eae0eb0c-dirty`，编译用户 `bruce@zed`，编译时间为 2024-10-08；因此不能称为与本地一致的 Image。

### 4.2 已确认公开存在的源码

| 源码 | 地址与 ZIP 下载 | 已核实内容 |
| --- | --- | --- |
| Rockchip 官方 BSP 5.10 | [分支](https://github.com/rockchip-linux/kernel/tree/develop-5.10) / [固定提交](https://github.com/rockchip-linux/kernel/tree/95a3ad83f7f90e0e672b9c99b0858b4964318667) / [源码 ZIP](https://github.com/rockchip-linux/kernel/archive/95a3ad83f7f90e0e672b9c99b0858b4964318667.zip) | 此次读取的 Makefile 为 5.10.252；属于平台基础源码，不是本机 5.10.160 的确切源码 |
| ArkOS4Clone 5.10 适配源码 | [lcdyk0517/arkos.bsp.5.10](https://github.com/lcdyk0517/arkos.bsp.5.10/tree/arkos4clone-5.10) / [固定提交](https://github.com/lcdyk0517/arkos.bsp.5.10/tree/991f8ed53b554e377740b433955f3ac58daf8d87) / [源码 ZIP](https://github.com/lcdyk0517/arkos.bsp.5.10/archive/991f8ed53b554e377740b433955f3ac58daf8d87.zip) | Makefile 为 5.10.252，可参考社区驱动和掌机适配 |
| 另一维护者的 5.10 源码 | [jokubasver/rockchip-kernel](https://github.com/jokubasver/rockchip-kernel/tree/arkos4clone-5.10) / [本次核查提交](https://github.com/jokubasver/rockchip-kernel/tree/eeda79215a258f81260ca13ff6db3807c7efa6ae) | Makefile 为 5.10.252，是上述社区源码的来源之一 |
| 社区 4.4 适配源码 | [lcdyk0517/arkos.bsp.4.4，rg351](https://github.com/lcdyk0517/arkos.bsp.4.4/tree/rg351) | 用于研究旧社区内核，不能视为本地 5.10.160 源码 |

相关具体文件：

- [Rockchip 官方 rk3326-evb-lp3-v12-linux.dts](https://github.com/rockchip-linux/kernel/blob/95a3ad83f7f90e0e672b9c99b0858b4964318667/arch/arm64/boot/dts/rockchip/rk3326-evb-lp3-v12-linux.dts)：平台板级配置参考，屏幕与本机不同。
- [社区 odroidgo3-joypad.c](https://github.com/lcdyk0517/arkos.bsp.5.10/blob/991f8ed53b554e377740b433955f3ac58daf8d87/drivers/input/joystick/odroidgo3-joypad.c)：实际存在，但不是本机 `compatible = "play_joystick"` 的同名实现。

### 4.3 尚未确认的原厂源码

**尚未定位到本机 `5.10.160-g3ee18cae74dc-dirty` 的完整源码、`.config`、厂商补丁及构建记录，也未取得能确认对应本机的 `play_joystick` 完整实现。**

对 `3ee18cae74dc` 的公开 GitHub 提交检索没有找到结果，Rockchip 官方仓库按该提交查询也未找到对应项。这只能说明本轮未定位到，不能证明它没有公开过。`-dirty` 还表示编译时有未提交改动，即使有同一提交号，仍需补丁和配置才能重建相同内核。

后续应向原卡/整机提供方追索准确源码、`.config`、补丁及工具链。不能把上表通用或社区源码直接写成“原厂 Image 对应源码”。

`uInitrd` 属于启动用户空间，不是仅凭内核源码就能重建的文件，还需要发行版内容和打包过程。`Image`、DTB、`uInitrd`、引导程序和根文件系统的内核模块应成套核对。

## 5. 完整社区系统镜像地址

[ArkOS4Clone-20261008 发布页](https://github.com/lcdyk0517/arkos4clone/releases/tag/20261008)。本次通过 Releases API 核实了以下六个下载附件；它们是社区项目维护者的正式发布，不是掌机厂商原厂固件。

| 系统 | 分卷下载地址 |
| --- | --- |
| ArkOS4Clone 20261008 | [001](https://github.com/lcdyk0517/arkos4clone/releases/download/20261008/ArkOS4Clone-20261008.img.xz.7z.001) / [002](https://github.com/lcdyk0517/arkos4clone/releases/download/20261008/ArkOS4Clone-20261008.img.xz.7z.002) / [003](https://github.com/lcdyk0517/arkos4clone/releases/download/20261008/ArkOS4Clone-20261008.img.xz.7z.003) |
| dArkOS4Clone 20261008 | [001](https://github.com/lcdyk0517/arkos4clone/releases/download/20261008/dArkOS4Clone-20261008.img.xz.7z.001) / [002](https://github.com/lcdyk0517/arkos4clone/releases/download/20261008/dArkOS4Clone-20261008.img.xz.7z.002) / [003](https://github.com/lcdyk0517/arkos4clone/releases/download/20261008/dArkOS4Clone-20261008.img.xz.7z.003) |

同一系统的三个分卷全部下载到同一目录，从 `.001` 开始用 7-Zip 提取；得到 `.img.xz` 后再解压为 `.img`。本轮没有下载数 GB 的整卡镜像，也未验证本机适配。使用说明见 [ArkOS4Clone Wiki](https://github.com/lcdyk0517/arkos4clone/wiki)。

旧项目下载入口：[AeolusUX/ArkOS-K36](https://github.com/AeolusUX/ArkOS-K36#final-release-downloads)，其页面已宣布停止维护并转向 ArkOS4Clone。

**当前未找到与本地原厂系统完全一致的可烧录整卡镜像地址。** 前述 Console.zip 仅用于提取启动文件，不代表完整系统。

## 6. 本地资料与工具

- [原始设备树](zj_boot/rf3536k3ka.dts)、[原卡设备树 rf3536k3ka.dts](zj_boot/rf3536k3ka.dts)。
- [GitHub 相近样本对比与恢复后的来源记录](github-references-20261105/README.md)。
- [核心板 GPIO 使用表](核心板GPIO_20261105/rf3536k3ka_核心板GPIO使用表.xlsx)。
- [工具使用入口](../../tools/README.md)；DTC 上游：[dgibson/dtc](https://github.com/dgibson/dtc)，Windows/Linux 二进制来源：[MathWorks Releases](https://github.com/mathworks/dtc-build/releases)。

本轮只更新资料与核验记录，未修改启动二进制或设备参数。后续试用其他系统时，先备份原卡和实际启动配置，每次只验证一组配套文件，并保留恢复原卡的方法。

## 7. 核心板原理图设计用 GPIO 交付

已根据本目录 [原卡设备树 rf3536k3ka.dts](zj_boot/rf3536k3ka.dts) 重新生成 [核心板 GPIO 使用表与说明](核心板GPIO_20261105/README.md)，[直接打开 Excel](核心板GPIO_20261105/rf3536k3ka_核心板GPIO使用表.xlsx)。本次不使用之前的 resolved 文件或其他机型配置作为板级数据源。

表内包含 GPIO 用途、方向依据、有效极性、Pinmux 状态、ADC、接口、电源和 I/O 域，保留原理图网络名、精确封装脚和连接器脚号填写栏。GPIO/ADC 重复声明、19 路实体键名缺失及封装/电压待核实项均已列出，供硬件与 BSP 一起确认后冻结原理图。
