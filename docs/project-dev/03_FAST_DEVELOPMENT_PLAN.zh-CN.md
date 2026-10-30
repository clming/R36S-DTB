# 基于现有项目的掌机快速研发路线

版本：V0.2；资料核查日期：2026-10-28。主芯片固定为用户确认的 **Rockchip RK3326**。本版增加现有附图复核、GitHub 源码/镜像逐项入口、实际下载核查，以及同芯片参考原理图。配套文档：[产品需求书](01_PRODUCT_REQUIREMENTS.zh-CN.md)、[研发工作分解](02_ENGINEERING_WORK_BREAKDOWN.zh-CN.md)。本文的周期、样本数量和资源安排均为工程规划估计，不是供应商交期或已经执行的进度。

**建议先用可持续供货、接口和软件来源明确的成熟主板，搭配一款固定屏幕，完成整机与体验样机；待需求、功耗和软件路径稳定后，再决定是否自行设计 RK3326 主板。** 本仓库能缩短设备树理解和适配时间，不能单独提供完整产品设计。若必须拥有主板完整设计文件，应在立项时把原理图/PCB/BSP 的取得或自研列为关键任务。

本轮结论：原机照片显示 **ArkOS 2.0 (08232024) + EmulationStation**，优先从原卡保存匹配文件；GitHub 已找到可直接取得的 Image、DTB、DTS 和含 uInitrd 的历史更新包；电路方面找到 **Hardkernel ODROID-GO Advance Rev1.0、24 页 PDF**，但没有找到照片中这块 R36S 主板的完整原始设计包。该板正面与反面分别有 R36S-V12 和 V2.1 丝印，见第 0 节；具体链接及限制集中在第 3.4–3.8 节。

执行细化与官方联系补充（2026-10-29）：[10 项目采购与试产执行手册](10_PROJECT_PROCUREMENT_PILOT_EXECUTION.zh-CN.md)列出首十日任务、阶段放行、预算/试产记录、询价草稿，以及当日核实的瑞芯微、Hardkernel、嘉立创/JLCPCB 官方渠道。瑞芯微详细开发资料按合作流程申请；Hardkernel 采购邮件与技术论坛分别使用。目前未核实照片中 R36S 整机的实际制造主体。结构、硬件和软件执行清单分别见[07](07_MECHANICAL_DESIGN_AND_TOOLING.zh-CN.md)、[08](08_ELECTRONICS_SCHEMATIC_BRINGUP.zh-CN.md)、[09](09_FIRMWARE_EMULATORS_RELEASE.zh-CN.md)，验收基线见[06](06_PRODUCT_BASELINE_AND_ACCEPTANCE.zh-CN.md)。

新项目路线更新（2026-10-29）：原机分析与源码/镜像链接继续保留，但新产品不再默认依赖 RK3326 原板供应。按[11 替换方案](11_RK3326_REPLACEMENT_STRATEGY.zh-CN.md)先并行审核 H700 和 RK3566/RK3568 的成熟方案，未获书面供货、工程交付和样机证据前不锁芯片、不投正式模具；[12 市场与切入调查](12_HANDHELD_MARKET_ENTRY_RESEARCH.zh-CN.md)提供当前官网样本和待执行的国内/海外调查。国内外 SKU、法规日期、认证/运输、软件维护及售后预算按[10 第 13 节](10_PROJECT_PROCUREMENT_PILOT_EXECUTION.zh-CN.md#13-国内与海外销售的新增工作包2026-10-29)进入关键路径。本文早先周期仅作历史规划，新平台和目标市场增加工作量后应重新排期。

## 0. 本轮附图复核与已确认条件

当前可见 `p1-2.png`、`p1-3.png` 和 `p1-5.jpg` 至 `p1-13.jpg`；先前的 `p1-1.png`、`p1-4.png` 当前不在目录中。本次使用现有图片，不修改任何图片。

| 依据 | 确认/观察结果 | 对研发的影响 |
| --- | --- | --- |
| 用户明确确认主芯片；[p1-13.jpg](p1-13.jpg) 主控区 | Rockchip RK3326 | 固定 SoC；不再只写“RK3326 级平台”；仍需取得完整订货型号与硬件资料 |
| [p1-10.jpg](p1-10.jpg) | 画面文字 `ArkOS 2.0 (08232024)` | 优先追溯该系统和原卡；日期标签不能证明内核构建来源 |
| [p1-7.jpg](p1-7.jpg)、[p1-8.jpg](p1-8.jpg)、[p1-9.jpg](p1-9.jpg) | `emulation station` 与多个平台的加载进度文字 | 确定前端家族，继续查实际分支、启动配置与核心，不能只找某个“万能模拟器” |
| [p1-5.jpg](p1-5.jpg) | CPS I 平台页与 `32 GAMES AVAILABLE` | 游戏库数量独立于模拟器数量；需要 ROM/元数据/核心/存档的对应清单 |
| [p1-11.jpg](p1-11.jpg) | 主板正面：`R36S-V12 2023-08-18`、四肩键、BAT/SPK/LEFT/RIGHT 和 UART 类焊盘 | 与 p1-12 反面合并建立一份主板档案及接口/测点表；有同名板号的网络 DTB 也须核对屏和线路 |
| [p1-12.jpg](p1-12.jpg) | 同一块主板的反面：`V2.1_20250331`、双 TF 卡座、`TYPE-C DC`/`OTG`、耳机座 | 用户已确认与 p1-11 的正反面关系；分别记录两面丝印，不作为另一块主板管理，也不等同于本仓库 Panel 4 - V22 |

2026-10-29 根据用户确认更正：`p1-11.jpg` 为主板正面，`p1-12.jpg` 为同一块主板的反面。两面丝印不同，其具体含义待核实，不能再据此判断为两块不同版本主板。本次仅更正照片关系，外部资料核查日期仍为 2026-10-28。

照片没有给出屏排线完整标识、电池规格和所有器件顶标，不能据此冻结 DDR 容量、PMIC 后缀、充电参数、Type-C 协议或接口电平。本轮结合用户确认与照片可读信息记录已知条件。

## 1. 三种路线怎么选

| 路线 | 实际研发内容 | 优点 | 主要限制 | 适用目标 |
| --- | --- | --- | --- | --- |
| A：成熟主板/ODM 方案定制 | 确认板卡、屏、输入、电池；定制机壳、软件与产测；签订交付约定 | 减少 DDR、PMIC、启动链和高速 PCB 首次调试 | 依赖供货和资料；成品零售机不等于可持续供应的方案板 | 快速做出产品，验证市场和体验；首版优先 |
| B：取得参考设计，自研/委托设计 RK3326 主板 | 完整硬件、DDR/电源/PCB、BSP、结构、产测 | 掌握接口、BOM 与长期演进 | 资料、芯片供货、BGA 制造和 BSP 是关键路径；至少预留改板 | 有明确量产与成本控制需求，具备硬件团队 |
| C：现成 SoM/开发板加输入与电池载板 | 采购计算模块，定制载板、屏/按键/电源和机壳 | 便于做软件/交互验证，可规避部分高速设计 | 体积、成本、待机和功耗可能偏离附图；并非可直接装进同款壳 | 无法拿到成熟掌机主板时的功能验证备选 |

第一阶段不同时更换 SoC、DDR、PMIC、屏、输入协议和系统。每增加一种变化，都会扩大无法归因的故障面。先固定一个能启动、显示、输入和播放声音的组合，再逐项替换。

### 1.1 建议周期与前提

| 结果 | 路线 A 规划 | 路线 B 规划 | 前提/不包含事项 |
| --- | --- | --- | --- |
| 可操作的功能演示 | 1–2 周 | 可先在参考板完成，独立新板不按此估计 | 合格样机与屏已到手、现成系统可运行；采购等待另计 |
| 装入原型壳的工程样机 | 4–8 周 | 10–16 周或更长 | 路线 A 以成熟硬件和既有可用软件为前提；完整自建固件可能并行延长 |
| 可进入小批量的冻结版本 | 8–16 周或更长 | 16–28 周或更长 | 已取得软件/硬件交付依据；需包括试产、改版和可靠性问题闭环 |
| 正式量产 | 不承诺固定日期 | 不承诺固定日期 | 受开模、产能、物料、可靠性、销售地区要求、授权及修正次数影响 |

“快速”优先压缩未知和返工，不等于省略充电、热、存储和恢复验证。以上区间不是附图产品的原始研发周期，也不是网络资料给出的交付承诺。

## 2. 本仓库能直接帮到哪里

| 仓库内容 | 可用于什么 | 尚缺什么 |
| --- | --- | --- |
| [Panel4.dts](../../DTS/Panel4.dts) 及其他 DTS | 研究 DSI 屏、背光、GPIO、joypad、ADC、音频、PMIC 的配置关系 | 对应具体实物的接线、供电依据、完整驱动版本和实机覆盖 |
| [Panel 4/boot.ini](../../R36S/Panel%204/boot.ini) | 理解 Image、uInitrd、DTB 的加载关系 | 目标卡 UUID、实际引导布局、适用 U-Boot 及完整镜像 |
| 已有 DTB | 比较已知配置，作为有来源记录的调试线索 | 并非每个文件都有可重建来源，不保证适用新板 |
| Panel 5/6 的 Image | 提供历史内核二进制线索 | 内核源码、defconfig、补丁、模块和构建记录不完整，不能作为可维护 SDK |
| [项目指南](../PROJECT_GUIDE.zh-CN.md) 与[前次分析](../PANEL4_DTS_KERNEL_ANALYSIS.zh-CN.md) | 用于团队入门、识别文件、备份恢复和修改边界 | 不能替代硬件设计包和整机验证报告 |

特别注意：Panel4 与 Panel4-V22 分开；Panel6 没有同名 DTS；`rg351mp-kernel.dtb` 是设备树而非内核。Panel4 还存在 `native-mode` 与时序节点 phandle 不匹配，以及模式名与计算刷新率不一致的问题，应在适配分支记录并验证，不能直接当黄金配置生产。

## 3. 已核实的网络资料与使用方法

### 3.1 硬件、内核与构建资料

| 一手来源 | 本次核实内容 | 如何用于本项目 |
| --- | --- | --- |
| [Rockchip RK3326 官方产品页](https://www.rock-chips.com/a/en/products/RK33_Series/2018/0514/900.html) | 芯片功能和接口概况 | 确认平台能力，再向芯片/方案供应商取得匹配修订的 Datasheet、参考设计和硬件规则 |
| [Hardkernel GO3 板级 DTS](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts) | 官方源码声明与本项目根节点相同的兼容字符串 | 追踪驱动、宏和板级定义，不能当作 R36S 主板原理图 |
| [Rockchip rkbin](https://github.com/rockchip-linux/rkbin) | 官方前置固件和工具二进制仓库 | 查找启动链来源；具体 DDR/loader 与授权仍需确认 |
| [ArkOS Building](https://github.com/christianhaitian/arkos/wiki/Building) 与[内核 README](https://github.com/christianhaitian/linux/blob/rg351/README) | 平台相关构建线索，README 说明 Image、DTB 和模块交付 | 用作源码追查，不能把 RG351 分支当作所有 R36S 的现成完整 BSP |
| [Buildroot 官方手册](https://buildroot.org/downloads/manual/manual.html) | rootfs、工具链、项目定制和构建管理方法 | 建立自己的可重复固件工程，包含必要的前端/核心包，不从零写 Linux |
| [genimage 官方项目](https://github.com/pengutronix/genimage) | 从配置生成文件系统及分区镜像 | 固定引导布局与分区构建；布局来自实际平台，不猜扇区偏移 |

本次仍未取得 **照片中 R36S 主板的完整可编辑原理图、PCB、机构 CAD 和生产 BOM**，但已找到可阅读的 Hardkernel 同芯片参考原理图，详见第 3.8 节。必须区分“参考电路已找到”和“目标板生产文件已取得”。

### 3.2 快速验证系统：优先验证硬件，再评估可交付性

| 系统 | 已核实入口/状态 | 建议角色 |
| --- | --- | --- |
| ROCKNIX | [R35S/R36S 设备说明](https://rocknix.org/devices/unbranded/game-console-r35s-r36s/)、[20261001 发布页](https://github.com/ROCKNIX/distribution/releases/tag/20261001)；发布表将 Gameconsole R36s 列入 RK3326 `a` 镜像组 | 可在符合条款的条件下评估支持组合和驱动；不能因支持 R36S 就认定支持所有变体 |
| ArkOS-R3XS | [维护者 Wiki](https://github.com/AeolusUX/ArkOS-R3XS/wiki) 有 R35S/R36S 入口；本次 GitHub API 显示仓库已归档 | 已知老硬件/旧系统的对照资料，不作为持续维护承诺 |
| dArkOS | [v08272026 发布页](https://github.com/christianhaitian/dArkOS/releases/tag/v08272026) 存在 RG351MP 系统资产 | 若供应商或实机证明匹配，可作为候选；发布名为 RG351MP 本身不能证明本机兼容 |

ROCKNIX 已核实的候选下载为 [ROCKNIX-RK3326.aarch64-20261001-a.img.gz](https://github.com/ROCKNIX/distribution/releases/download/20261001/ROCKNIX-RK3326.aarch64-20261001-a.img.gz)，配套[校验文件](https://github.com/ROCKNIX/distribution/releases/download/20261001/ROCKNIX-RK3326.aarch64-20261001-a.img.gz.sha256)。GitHub 资产元数据报告压缩文件 1,338,960,803 字节，SHA-256 为：

```text
d693d2bb3cd854a54a1c742c9952f20892c8344188c696beea00c77b5bd54392
```

这是**发布元数据中的压缩文件哈希**，本次未下载计算，不是解压后 `.img` 或内部 `Image` 的哈希。未来下载后应自行计算再比较。选定此固定版本便于复现，不代表它对每台机器最好，也不能以 nightly 自动替换已验收版本。

该设备文档介绍了新屏使用 `mipi-panel.dtbo` 及从旧 DTB 导入屏参数的机制。这只覆盖文档所述系统的屏适配能力，不能自动转换整块新板的 PMIC、输入或 USB，也不能把本项目旧 BSP DTB 直接覆盖主线系统。需要按选定版本再次检查工具存在及输出。

dArkOS 的具体候选资产为 [分卷 001](https://github.com/christianhaitian/dArkOS/releases/download/v08272026/dArkOS_RG351MP_trixie_09022026.img.7z.001) 和[分卷 002](https://github.com/christianhaitian/dArkOS/releases/download/v08272026/dArkOS_RG351MP_trixie_09022026.img.7z.002)。下载两卷后从 `.001` 解压；仍需验证主板和屏适配，不单独提取一个内核盲目替换现有系统。

### 3.3 从样机研究走到可销售产品的软件路径

本仓库 README 声明 [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)，其条款含非商业和禁止分发改编材料的限制。ROCKNIX 发布说明也明确包含非商业组件及品牌素材许可限制。故“能下载”“能运行”和“能随产品销售分发”必须分别核对，不能把移除开机 Logo 当成解决全部许可。

建议在项目启动时同时确定两条交付路径之一：

1. **供应商授权交付**：取得可用于预期销售方式的 BSP、前端、核心和素材清单、所需源码/通知，以及持续维护与再分发依据。只收到授权口头承诺或一个镜像不足以验收。
2. **自行集成可交付固件**：从来源明确的启动链、Linux、Buildroot、前端和核心构建，建立自有主题与配置；每个组件按实际版本核对许可并履约。Buildroot 是构建工具，不自动保证所有选中包都适合商业分发。

RetroArch 与各核心许可分别管理，参考 [Libretro 官方许可清单](https://docs.libretro.com/development/licenses/)。ROM、BIOS、封面、字体和主题也单独建立来源记录。必要源码交付、版权通知、书面提供方式等取决于实际组件许可，不能用一份笼统“开源声明”替代。已有代码许可的范围和权利来源有疑问时，在选型阶段澄清，避免做完固件再返工。

### 3.4 RK3326 的 GitHub 开源代码：按层选择，不混用分支

| 层次 | 已核实的仓库/分支或文件 | 得到什么 | 使用范围 |
| --- | --- | --- | --- |
| Rockchip 通用 BSP 内核 | [rockchip-linux/kernel：develop-4.4](https://github.com/rockchip-linux/kernel/tree/develop-4.4)，[rk3326.dtsi](https://github.com/rockchip-linux/kernel/blob/develop-4.4/arch/arm64/boot/dts/rockchip/rk3326.dtsi) | SoC 公共定义、驱动和内核构建系统 | 芯片厂商基础，不含照片中 R36S 主板的完整专用交付 |
| Hardkernel 掌机 BSP | [hardkernel/linux：odroidgoA-4.4.y](https://github.com/hardkernel/linux/tree/odroidgoA-4.4.y) | 同芯片掌机驱动和板级设备树 | 本仓库兼容字符串的直接参考；不是照片中原机 Image 的已证实源码 |
| BSP 板级 DTS | [rk3326-odroidgo3-linux.dts](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts)（[直接下载](https://raw.githubusercontent.com/hardkernel/linux/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts)） | 与本仓库相同的根兼容标识；GPIO/joypad/供电/屏配置参考 | 依赖同分支 DTSI、头文件和驱动；不能单独下载一个 DTS 就当完整 BSP |
| BSP 配置 | [odroidgoa_defconfig](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/arch/arm64/configs/odroidgoa_defconfig) | 一份真实存在的内核配置起点 | 需按新板增改，不能声称能重现原机内核 |
| ArkOS 相关内核 | [christianhaitian/linux：rg351](https://github.com/christianhaitian/linux/tree/rg351) 与[构建 README](https://github.com/christianhaitian/linux/blob/rg351/README) | RG351 系列源码和 Image/模块构建线索 | 对应设备和分支有边界，R36S 需核实差异 |
| 旧启动链 | [hardkernel/u-boot：odroidgoA-v2017.09](https://github.com/hardkernel/u-boot/tree/odroidgoA-v2017.09) | 同平台 U-Boot 源码 | 引导介质、DDR 初始化与镜像布局须与目标板匹配 |
| 社区 R36S 新内核参考 | [AndreRenaud/linux-r36s：r36s-v6.10](https://github.com/AndreRenaud/linux-r36s/tree/r36s-v6.10)，[R36S DTS](https://github.com/AndreRenaud/linux-r36s/blob/r36s-v6.10/arch/arm64/boot/dts/rockchip/rk3326-r36s.dts) | 开发者面向 R36S 的 Linux 分支及 DTS | 社区适配参考；不能与 4.4 BSP 的 DTB、模块和图形库随意混用 |
| 社区 R36S 新引导参考 | [AndreRenaud/u-boot-r36s：r36s-v2024.04](https://github.com/AndreRenaud/u-boot-r36s/tree/r36s-v2024.04) | R36S 相关 U-Boot 改动 | 需另做启动和显示验证；不是确认适配全部主板的通用替换件 |
| 前置二进制 | [rockchip-linux/rkbin](https://github.com/rockchip-linux/rkbin) | 平台前置固件/工具 | 部分为二进制，不应称为全部开源代码；核对 DDR、型号与许可 |
| 游戏系统 | [christianhaitian/arkos](https://github.com/christianhaitian/arkos)、[ROCKNIX/distribution](https://github.com/ROCKNIX/distribution)、[christianhaitian/dArkOS](https://github.com/christianhaitian/dArkOS) | 更新、构建与发行文件，具体范围各不相同 | 完整固件不等于单个仓库里每个二进制都有源码；逐组件追踪 |
| 前端/模拟器 | [EmulationStation 上游](https://github.com/Aloshi/EmulationStation)、[RetroArch](https://github.com/libretro/RetroArch)、[mGBA libretro](https://github.com/libretro/mgba)、[PPSSPP](https://github.com/hrydgard/ppsspp) | 界面、核心运行框架、模拟核心和独立模拟器代码 | 照片只确认 EmulationStation 家族，未确认原卡实际使用哪个分支/核心 |

以上仓库/文件通过 GitHub API 或原始内容核对；链接中的分支名会移动，开始开发时须记录 commit 和配置。RK3326 指定了架构与硬件平台，不能单靠芯片型号选择内核镜像，更不能据此把某个分支说成原机固件源码。

### 3.5 Image、uInitrd、DTB、DTS 到哪里下载：逐项清单

**优先级：原卡匹配套件 → 明确支持目标板的完整系统 → 单项文件用于分析。** 下表不同来源的文件不可直接凑成一套可启动系统。

| 文件/资源 | 已核实的具体入口 | 本次得到的证据 | 推荐用途 |
| --- | --- | --- | --- |
| 原机系统日期线索 | [ArkOS 08232024 目录](https://github.com/christianhaitian/arkos/tree/main/08232024) | 存在 `arkosupdate08232024.zip`，大小 8,351,216 字节，以及 Kodi 分卷 | 对照照片日期，查更新内容；这是增量更新目录，不是完整系统镜像，不证明就是原卡固件 |
| Image 直接文件 | [dArkOSRE 的 BOOT 目录](https://github.com/southoz/dArkOSRE-R36/tree/main/files/BOOT)，[本次核查固定提交的 Image](https://raw.githubusercontent.com/southoz/dArkOSRE-R36/3f372c85aa53a26b265c3dc0c2661ec0fae5faf0/files/BOOT/Image) | 实际下载 12,015,624 字节，偏移 0x38 为 ARM64 Image 标识 | 检查社区候选内核，必须配套模块/rootfs/DTB；未验证匹配附图主板 |
| uInitrd 的实际文件来源 | [ArkOS 01142023 目录](https://github.com/christianhaitian/arkos/tree/main/01142023)，[更新包直接下载](https://raw.githubusercontent.com/christianhaitian/arkos/main/01142023/arkosupdate01142023.zip) | 实际下载 ZIP 并解出 `boot/uInitrd`，6,670,221 字节 | 历史启动文件分析；不是 08232024 原机 uInitrd 的已确认副本，也不与上行 Image 默认匹配 |
| V12 + Panel4 的 DTB 候选 | [dArkOSRE V12 Panel4 目录](https://github.com/southoz/dArkOSRE-R36/tree/main/files/BOOT/dtb/r36s/R36S-V12%202023-08-18%20Panel%204)，[固定提交的主 DTB](https://raw.githubusercontent.com/southoz/dArkOSRE-R36/3f372c85aa53a26b265c3dc0c2661ec0fae5faf0/files/BOOT/dtb/r36s/R36S-V12%202023-08-18%20Panel%204/rk3326-r36s-linux.dtb) | 实际下载 90,267 字节，FDT magic 正确；目录还含 `rg351mp-uboot.dtb` | 板号与 p1-11 有对应线索，仍要确认屏型号、驱动和文件实际加载角色；不是按目录名自动判兼容 |
| 本仓库 DTS/DTB | [DTS 目录](../../DTS)、[Panel4.dts](../../DTS/Panel4.dts)、[Panel4 发布 DTB](../../R36S/Panel%204/rk3326-r35s-linux.dtb)；[上游 R36S-DTB 仓库](https://github.com/AeolusUX/R36S-DTB) | 本地文件可读，有多屏变体 | 用于配置对照，不推断所有历史二进制均可从现有源码重建 |
| 社区 R36S DTS | [Linux 6.10 分支 DTS 原文](https://raw.githubusercontent.com/AndreRenaud/linux-r36s/r36s-v6.10/arch/arm64/boot/dts/rockchip/rk3326-r36s.dts) | 已读取，使用 gpio-mux/adc-joystick 等描述 | 理解不同驱动方案，配合同分支源码；不是旧 BSP DTS 的直接替代 |
| 同时产生 Image/uInitrd/DTB 的构建参考 | [icefirex/nixos-r36s](https://github.com/icefirex/nixos-r36s)、[sd-image.nix](https://github.com/icefirex/nixos-r36s/blob/main/sd-image.nix)、[v0.1.0 发布](https://github.com/icefirex/nixos-r36s/releases/tag/v0.1.0) | 代码明确把内核/初始文件系统复制到 `boot/Image`、`boot/uInitrd`，并部署 DTB；发布资产存在 | 可重建路线研究，不能把 NixOS 的 initrd 直接用于 ArkOS；不是已集成附图全部游戏体验的现成替代 |

**uInitrd 特别说明：** 名称中的 `u` 不保证存在 U-Boot legacy 头。本次提取的 ArkOS 文件以 `1f 8b` 开头，是 gzip；解压得到 15,030,272 字节，起始为 CPIO `070701`。它是启动早期文件系统内容，不是 DTB，也不是内核。是否需要头部、是否传入长度以及 bootloader 如何识别，由对应启动方案决定。旧更新包里有这个文件，不代表应直接覆盖现在的启动分区。

在 dArkOSRE 当前 `files/BOOT` 根目录列表中，本次看到了 Image 和 DTB，但**没有看到 uInitrd**；其 boot.ini 却仍加载 uInitrd。因此不能声称下载这个目录就获得完整启动套件，应继续查看完整发行镜像/制作流程或使用原卡配套文件。

### 3.6 完整系统镜像库与配套文件提取

| 目的 | 下载位置 | 如何取得启动文件 |
| --- | --- | --- |
| 最大程度接近照片中的老 ArkOS | [ArkOS-R3XS 维护者下载页](https://github.com/AeolusUX/ArkOS-R3XS/wiki)、[原 ArkOS Wiki](https://github.com/christianhaitian/arkos/wiki) | 原卡优先；网络镜像需核对机型/发布日期。解压 `.img` 后只读查看实际启动分区，取得同一镜像内 Image/uInitrd/DTB 和启动配置 |
| dArkOS 候选 | [v08272026 发布及两个分卷](https://github.com/christianhaitian/dArkOS/releases/tag/v08272026)，具体链接见 3.2 | 两卷放同一目录，从 `.001` 解压；RG351MP 资产不自动等于 R36S 已验证兼容 |
| ROCKNIX 候选 | [20261001-a 镜像及 SHA-256](https://github.com/ROCKNIX/distribution/releases/tag/20261001)，具体直接链接见 3.2 | 按该系统启动机制处理，不能要求它一定采用 ArkOS 同名 uInitrd 或相同文件布局 |
| R36S 专项社区套件 | [southoz/dArkOSRE-R36 Releases](https://github.com/southoz/dArkOSRE-R36/releases) | 根据维护者发布说明取得完整镜像/安装包；BOOT 目录单独文件只作分析，不能替代完整发布说明 |
| NixOS 实验参考 | [nixos-r36s-sd-card.img.zst](https://github.com/icefirex/nixos-r36s/releases/download/v0.1.0/nixos-r36s-sd-card.img.zst) | GitHub API 确认资产 722,664,750 字节；构建代码显示文件放在 rootfs 的 `/boot`，不只在 FAT 启动分区；本次未下载 |

提取流程：记录下载 URL、版本和校验 → 解压镜像 → 用已有支持分区的工具只读打开 → 阅读启动配置 → 提取它真正引用的文件 → 连同 rootfs 模块/图形库版本一起归档。若现有 Windows 工具不能读取 ext4，只记录需要相应读取环境；本次不安装软件、不为了提取去格式化或修改镜像。

只有同一系统内配套的内核、initrd、模块、图形栈和 DTB 才有明确的验证起点。修改屏幕通常先保留内核与 initrd，调整已确认的屏配置；未知供电与 GPIO 不靠“同芯片”猜测。

### 3.7 本次实际下载与检查记录

为确认资源真实存在，本次只将一个约 20 MB 的历史更新包、其中的 uInitrd、一份约 12 MB 的 Image 和一份 DTB 放入**仓库外系统临时目录**进行只读检查；没有下载 GB 级完整系统、安装工具、编译或烧卡，仓库发布目录未写入任何二进制。检查结果如下：

| 对象 | 长度（字节） | SHA-256 | 检查范围 |
| --- | --- | --- | --- |
| `arkosupdate01142023.zip` | 20,702,936 | `5fc21978bdd36f2601cdc9629f219ebfa519f14a3f10b716adfe1aeef6013405` | ZIP 可打开，存在 `boot/uInitrd` |
| ZIP 中的 `boot/uInitrd` | 6,670,221 | `21b4184c5ef859f19a879dbb7a76ee5ab7d63d4aca41f6f266eb5a4a9f1b8db3` | gzip 可解压，起始 CPIO 格式可识别；未运行其中程序 |
| dArkOSRE 的 `Image` | 12,015,624 | `495429f04a227b7c4b67588f6e808c9195c7c79ebe50b32609e1c93d062fd480` | ARM64 Image 标识；未确认内核版本/构建配置，未启动 |
| dArkOSRE V12 Panel4 主 DTB | 90,267 | `8e7732f99d509ec675480c842b6c44cb71752bcf933fa6eb333f4e97d5044d97` | FDT magic；未以 dtc 反编译或证明与源码语义相同 |

dArkOSRE 两个文件固定到提交 `3f372c85aa53a26b265c3dc0c2661ec0fae5faf0`，避免后续 main 分支移动导致哈希无法对照。ZIP 来源为原 ArkOS 已归档仓库。哈希与文件头只能证明本次取得的内容及格式线索，不能证明这些不同来源文件能互相配套启动。

### 3.8 找到的参考设计电路图及如何用于这个产品

**已找到：Hardkernel 编制的 `ODROID_GO_ADVANCE_rev1.0.pdf`，PDF 共 24 页，图框为 Revision 1.0、2019-12-06。** 这是采用 RK3326/RK817 的掌机参考电路，适合用来理解最小系统和外设连接，不是照片中这块 R36S 主板的原始设计。

- [原发布服务器上的 PDF 地址](https://dn.odroid.com/ODROID_GO_ADVANCE/ODROID_GO_ADVANCE_rev1.0.pdf)：本次 HTTP/HTTPS 获取均返回 403，记录为原始来源入口，不能声称当前可直接下载。
- [同名参考图 PDF 镜像](https://device.report/m/0d5c9bb96a58f7f07489cd9fa7582dc0ece8082478040c00a46f66118e8ab2c3.pdf)（[在线阅读页](https://device.report/m/0d5c9bb96a58f7f07489cd9fa7582dc0ece8082478040c00a46f66118e8ab2c3)）：网页工具已读取 PDF 文本与图框，并调用页面截图核查。镜像托管方不是原作者；本次命令行直接下载也返回 403，未取得本地 PDF 或计算文件哈希。

图纸包含 RK3326 最小系统、DDR、RK817 电源/音频、LCD、SD、USB、UART、按键和供电接口等分册，可作为第 2 份文档原理图工作的参考；这里未取得原生 SchDoc、PCB 布线文件或商业复制授权，PDF 中出现源文件名不代表已提供这些源文件。

| 对照方面 | OGA 参考图与附图 R36S 的区别 | 研发必须补做 |
| --- | --- | --- |
| 屏幕 | OGA 图中是自己的 KD35T133-A2 接口方案；不能当作本机 640×480 屏的规格书 | 获取目标屏 FPC、初始化、lane、供电与时序，核对整个显示链 |
| 输入 | OGA 原版输入与附图双摇杆/四肩键/FN 布局不同 | 逐键和四轴测量，决定 ADC 多路器/引脚方案，再匹配驱动 |
| 存储 | 参考图与附图双 TF 布局不同 | 独立设计第二卡控制器、供电/检测及内容挂载策略 |
| USB/充电 | 参考图有自身的 USB/供电连接器；附图为 DC/OTG 两 Type-C | 设计并验证 CC、角色、VBUS、限流和反灌，不只更换插座封装 |
| 电源/DDR | 同芯片不等于相同电芯、DDR 型号和电源网络 | 核对实际料号、封装、电压、时序和初始化，不无条件复制参数 |
| 机构/PCB | 参考产品轮廓和内部堆叠不同 | 重新做板框、孔位、高速布局、热与装配设计 |

推荐执行：先读参考图理解功能 → 固定照片中的一块目标板 → 用高清双面照片和测量建立接口/网络对照 → 绘制自己的可编辑电路 → 结合 RK3326 原厂硬件约束完成 PCB → 逐阶段点亮与验证。照片看不到 BGA/内层网络，DTS 也不能补出所有电源、阻容与保护电路。

**本次没有找到可核实的目标 R36S 主板完整原厂电路图或生产 Gerber；该板正反面丝印已在第 0 节关联记录。** 若目标是快速生产同功能整机，优先采购资料交付明确的成熟方案；若目标是掌握主板设计，则以此同芯片参考图为起点，向原厂/方案商补齐设计资料并自行设计，不能把 PDF 改名为 R36S 后当成可投产资料。

## 4. 第一周：最大限度消除未知

### 4.1 建议准备的样机和工具

| 项目 | 建议数量/要求 | 用途 |
| --- | --- | --- |
| 同批次完整样机 | 至少 3 台：完整对照、拆机测绘、软件验证各一台 | 区分单机故障与方案问题；不混不同板号当同一设计 |
| 备用合格系统卡 | 至少 4 张并记录型号/容量 | 原卡封存、系统候选与恢复分开 |
| 供方主板/屏样件 | 有明确 PCB 版号、屏料号与持续供货承诺 | 证明未来买到的与本次验证相同 |
| 读卡器/测量工具 | 可靠读卡器、卡尺、万用表、可限流电源、USB 功率计、温度测量 | 备份和功耗、尺寸、热基线 |
| 串口与调试 | 匹配电平的 USB-UART，示波器/逻辑分析仪按调试需要 | 读取启动和总线故障，不默认 5 V TTL |
| 构建环境 | Linux 开发机、版本控制、独立备份盘 | 固定源码和日志；Windows 仓库本身不能替代 Linux 目标构建环境 |

### 4.2 供应商必须回答的十个问题

1. 芯片和主板准确型号、PCB 版本、BOM/替代料及变更通知机制是什么？是否会同订单混屏/混主板？
2. 能否提供原理图 PDF、接口定义、安装 STEP、尺寸、测试点和维修资料？若要完整设计所有权，能否交付原生 ECAD？
3. DDR、PMIC、屏、电池的完整料号是什么？可持续供货多久，替代料如何重新验证？
4. Linux、U-Boot、DTS 的源码、固定提交、配置、工具链和补丁能否取得？哪些部分只有二进制？
5. 完整镜像、模块、GPU 用户态库、前置固件分别是什么版本和来源？能否在干净环境构建？
6. 屏初始化命令、电源/复位时序、FPC 逐针定义是否可交付？屏替换是否通知？
7. FN、肩键、双摇杆、耳机、USB 口分别由什么驱动支持，能否提供验证记录？
8. 电池、充电、电源路径、边充边玩、温升、关机功耗是否有报告？
9. 报价是否分板卡/屏/电池/结构/烧录/产测，样件与 100/1,000/10,000 台各档交期、MOQ、良率和返修条款是什么？
10. 哪些软件/图片/字体/BIOS/游戏可以按本产品的销售方式分发，交付哪些授权和源码材料？

第 5 个工作日前若仍拿不到稳定板号、屏料号、接口和基本软件来源，应保留该方案作演示，暂停围绕它开模，启动另一家方案或路线 B 评估。这是建议决策点，不是自动采购动作。

### 4.3 每日目标

| 时间 | 产品/硬件/结构 | 软件/验证 | 当日可审查结果 |
| --- | --- | --- | --- |
| D1 | 编号样机、原卡封存、外观测量；明确首版需求 | 备份整卡与启动文件，采集系统/版本/哈希 | 资产表、备份位置与可读取验证 |
| D2 | 拆机拍照，记录屏、PCB、电池、摇杆、接口 | 读取启动日志、加载路径、输入设备、音频和电池状态 | 图纸资料缺口表、已知可用组合 |
| D3 | 建立堆叠草模、接口表；向供方索取资料 | 验证前端→核心→退出→存档完整闭环 | 功能基线与问题清单 |
| D4 | 功耗、温升、充电与按键/屏测量 | 备用卡验证一个候选系统；保持原卡可恢复 | 系统比较表，屏和驱动差异 |
| D5 | 选主板/屏/电池候选、决定路线、启动首轮手板 | 冻结演示固件组合，建立源码/许可追踪 | G0 评审包和下一轮采购/设计清单 |

掌机上可用的只读诊断命令示例（工具需目标系统实际提供）：

```bash
uname -a
cat /etc/os-release
cat /proc/cmdline
tr '\000' '\n' < /proc/device-tree/compatible
cat /proc/bus/input/devices
ls /lib/modules
dmesg
```

记录信息不能替代原理图。读取电池、时钟和电压配置不等于已测量真实数值。不要在系统卡仍挂载写入时制作唯一备份；保留关机取卡的原始备份。

## 5. 路线 A 的分阶段执行计划

阶段允许重叠，但只有出口条件满足才冻结下一批不可轻易变更的物料。EVT 为工程验证、DVT 为设计验证、PVT 为生产验证；下列数量是建议工程批次，不能作为统计可靠性证明。

| 阶段 | 规划窗口 | 工作重点 | 出口条件 |
| --- | --- | --- | --- |
| G0 基线与选型 | 第 1 周 | 样机、接口、来源、需求、供方交付范围、风险 | 至少一套可恢复的已知可用组合；主料号与资料缺口明确 |
| G1 功能闭环 | 第 2 周 | 前端、基础核心、中文、FN、保存/退出、恢复卡 | 两名人员可独立运行和恢复；P0 软件问题有复现记录 |
| G2 EVT 工程样机 | 第 3–6 周，建议 5–10 台 | 原型结构、输入手感、电源/热、板屏适配、工程产测 | 装壳后全部 P0 功能通过；无未解释的复位、发热或存档损坏 |
| G3 DVT 设计冻结 | 第 6–10 周，建议 10–20 台 | 修壳/修板、可靠性、显示/卡兼容、固件重建和交付来源 | BOM/机构/固件冻结；所有关键缺陷关闭，已知限制明确 |
| G4 PVT 小批试产 | 第 10–16 周，建议 30–100 台 | 装配、写卡、产测、追溯、包装、返修与售后演练 | 过程可重复、缺陷可追踪，良率与节拍达到立项约定 |

若没有可用且可交付的固件，需要增加独立构建和应用移植工期；若开新注塑模或出现改板，窗口相应后移。不得把可展示的一台样机直接当作 DVT 已通过。

## 6. 自研主板时如何增加任务

路线 B 应将[研发工作分解](02_ENGINEERING_WORK_BREAKDOWN.zh-CN.md)的 SCH-00 至 SCH-09 全部落实。规划中至少增加：

- 平台资料与供货确认：拿到足以设计的 SoC/DDR/PMIC 文档，先验证参考板和 BSP；缺资料时不能靠现有 DTS 推导完整电路。
- 原理图、接口和电源树评审：核心网络逐项复核，屏、键、USB、电池与结构共同冻结。
- PCB 叠层与布线：由具备 BGA/DDR/DSI 经验的工程师完成，预留 debug 和恢复测点。
- EVT 首板和改板预算：先电源/时钟/DDR/存储，再显示/输入/声音，最后充电/热/关机，不把首次点亮与全部外设联调并为一个任务。
- 软件分支：自有板级配置、启动链、内核、设备树、图形栈和产测；与旧板兼容性逐项验证。
- 工程资料所有权和维护：保存原生设计、制造文件、精确 BOM、源码与构建环境，避免换供应商时从头再来。

降低风险的次序是先保持参考设计的 SoC+DDR+PMIC 组合，再逐步优化非高速区。若商业目标只是尽快推出整机，不应仅为了“全自研”提前承担 DDR 与启动链风险。

## 7. 软件最短交付路径

### 7.1 样机与量产的软件工作并行推进

| 顺序 | 工作 | 最小结果 |
| --- | --- | --- |
| S1 | 保留原机可用系统并建立哈希基线 | 原卡+备用恢复卡，准确的 Image/DTB/模块对应关系 |
| S2 | 在许可允许范围验证成熟系统/供应商固件 | 一个支持显示、输入、声音、存档与关机的组合 |
| S3 | 固定前端和少量核心 | 先完成 5 类基础平台评估，再增加 PS1/PSP 等；每类单独记录性能 |
| S4 | 自有配置和主题 | 中文、热键、亮度音量、空内容引导、低电与异常提示 |
| S5 | 构建可交付基线 | 固定源码/配置/补丁、rootfs、引导布局、镜像打包和组件清单 |
| S6 | 恢复与产测 | 第二台开发机重建、第二人按文档恢复，产测可导出版本和结果 |

若选择 ROCKNIX 研究构建，其[官方本地构建说明](https://rocknix.org/contribute/build/)和[Makefile](https://github.com/ROCKNIX/distribution/blob/next/Makefile)提供 RK3326 路线；使用前固定提交和构建环境。官方说明提示单设备构建需要较大磁盘空间和较长首次构建时间，不能将“下载项目后立即出固件”写进工期承诺。本次未运行该构建。

商用自建路线建议用 Buildroot 管理 rootfs 和包，在团队固件工程内维护 board 配置、内核/引导补丁、前端/核心配方、主题和打包。不要在此设备树仓库中伪装已有整机 SDK；新工程目录是后续实施交付。

### 7.2 固件交付 manifest 最少字段

`product_id、hardware_revision、bom_revision、panel_part_number、dt_config_id、bootloader_commit、kernel_commit/config、module_version、gpu_stack、rootfs_build、frontend/core_versions、toolchain、build_date、image_sha256、component_licenses、known_issues、recovery_method`。

首版按确定的硬件配置发镜像，不追求自动识别所有屏。若确需多屏，必须有可靠硬件/供应链标识和各自经过验证的配置，不能按颜色、采购月份或目录编号猜测。

## 8. 烧录、恢复和版本验证

首版不自行开发通用图形刷机软件。采用[官方 Etcher](https://github.com/balena-io/etcher)等成熟写卡工具，工程工作放在标准镜像、校验、硬件匹配和恢复说明上。USB 板上烧录仅在硬件实现与 loader 确定后使用 [rkdeveloptool](https://github.com/rockchip-linux/rkdeveloptool)。

1. 保存原卡整镜像和启动文件，确认可以读取；原卡封存。
2. 从维护者/授权供应商取得选定版本，核对文件名、压缩分卷与 SHA-256。固件下载成功不等于文件校验通过。
3. 在独立备用卡写入完整系统镜像并启用写后校验；核对工具选中的物理卡，失败即停止该卡使用。
4. 按该系统实际加载机制设置必要的屏或 DTB，保留其根分区、地址和路径；本仓库 boot.ini 不能无条件整份覆盖。
5. 一轮只测试一个组合：冷启动、显示/背光、方向键/摇杆/FN、声音、充电/电量，涉及 USB 则补测对应模式；记录版本和问题。
6. 若失败，关机取卡恢复本轮改动；换内核时恢复配套模块与用户态依赖，无法确认时直接换回原卡。
7. 量产采用“受控母版镜像—批量写入—校验—机内首次启动—整机产测—结果追溯”，不能用若干手工复制的同名 DTB 代替流程。

## 9. 成本、人员与进度管理

### 9.1 成本模型

本次没有供应商实时报价，不给出伪精确 BOM 单价。应要求相同规格、相同交付范围的分项报价并建立：

```text
单台变动成本 = 主板 + 屏/镜片 + 输入组件 + 电池 + 扬声器/线束
             + 机构件 + 系统/内容卡 + 装配/烧录/测试 + 包装
             + 制造损耗 + 物流/税费 + 售后准备
项目总投入 = 固定研发/工具/模具/验证费用 + 计划数量 × 单台变动成本
```

成熟主板报价可能已经包含摇杆、卡座或音频，计算时先划定板卡边界，避免重复计入。对比方案不能只比主控单价，要加入软件交付、改板、良率和维护成本。

### 9.2 建议责任与周管理

| 角色 | 每周必须交付的可审查结果 |
| --- | --- |
| 产品/项目 | 需求变更、风险台账、版本计划、资料和交期缺口 |
| 采购/供应商接口 | 精确物料与交期、替代料、报价边界、变更通知 |
| 结构 | 堆叠/尺寸/手感问题闭环、手板与模具状态 |
| 硬件/BSP | 电气和驱动问题定位证据、启动/功耗/温度日志 |
| 应用 | 前端与核心版本、热键、性能和存档回归 |
| 测试/制造 | 验收矩阵、产测覆盖、试产缺陷与返修归因 |

每周冻结一组“硬件+屏+电池+固件”候选；需求新增先评估对 BOM、结构、驱动、测试和许可的影响。无线、触屏、HDMI、快充等功能都可能改变硬件关键路径，不能仅按菜单增加一项估算。

## 10. 风险与具体处理

| 风险 | 提前发现方式 | 处理策略 |
| --- | --- | --- |
| 主板/屏同名不同版本 | 每批板号/屏料号/固件记录，来料抽验 | 冻结 AVL 和变更审批；不同组合分别验收 |
| 显示点亮但刷新/输入有问题 | 计算时序、验证 native-mode，逐键/逐轴测试 | 按模块定位，不把“有画面”当适配完成 |
| 系统运行但无法持续交付 | 第一周核查源码/模块/许可/供方承诺 | 提前建立自有可构建系统或切换供方 |
| 续航与温升不达标 | 原型壳阶段测真实负载和充电工况 | 优化功耗/热/屏亮度；再选容量，不盲目提高电池规格 |
| 卡质量或掉电导致存档损坏 | 卡批次记录、卡满/只读/关机回归 | 合格卡、分离写入、正常关机同步和备份恢复 |
| 透明壳漏光、结构压键 | 首轮手板暗室观察和最差公差装配 | 遮光/导向/限位与尺寸链优化，再冻结模具 |
| 模拟器范围失控 | 首发矩阵、逐核心性能与来源评估 | 先少量基础平台做到稳定，不以所有平台图标充数 |
| 工程能做，产线不可重复 | 小批试产观察写卡/装配/产测 | 固定工装、版本、阈值、追溯与返修流程 |

## 11. 可以立即执行的启动清单

1. 将三份文档作为 V0.2，按已确认 RK3326、附图 ArkOS/EmulationStation 和同一主板的双面丝印记录，确认“成熟主板首版、固定一款屏、离线、基础平台优先”的候选范围。
2. 准备同批次样机、备用卡和测量工具，建立编号、备份和实测记录；本次尚未采购或接触样机。
3. 向至少两家方案供应商索取第 4 节资料和分档报价，尤其是主板/屏接口、BSP 与可分发组件。
4. 同时建立原型结构和软件功能闭环，不先开量产模具，也不先承诺全部平台性能。
5. 第一周 G0 评审后选择供应商、固件路径和是否需要自研主板；按出口条件推进 EVT/DVT/PVT。

本次完成的是研发方案补充、当前附图复核、GitHub 来源核查、少量启动文件下载/格式/哈希检查，以及参考原理图阅读，不是已经完成产品研发。完整系统未下载或编译；没有安装工具、运行候选固件或烧录设备，未验证任何候选固件与附图实物的兼容性，也未取得 R36S 制造级硬件资料和供应商报价。第 3.7 节的静态检查不能代替编译或实机验证。
