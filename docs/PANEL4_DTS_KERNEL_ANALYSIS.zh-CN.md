# Panel4 设备树、GPIO 与 RK3326 内核镜像查找说明

核查日期：2026-10-27。本文回答 `compatible` 的资料来源、换屏/GPIO 的修改位置、`rg351mp-kernel.dtb` 的性质及内核下载来源。以本仓库 [Panel4.dts](../DTS/Panel4.dts) 和 [Panel 4/boot.ini](../R36S/Panel%204/boot.ini) 为本地分析对象；其他使用说明见[项目指南](PROJECT_GUIDE.zh-CN.md)。

## 1. `rockchip,rk3326-odroidgo3-linux\0rockchip,rk3326` 是什么，官方资料在哪里？

### 1.1 这是兼容标识列表，不是芯片完整型号或驱动下载地址

Panel4.dts 第 4 行：

```dts
compatible = "rockchip,rk3326-odroidgo3-linux\0rockchip,rk3326";
```

这里的 `\0` 是字符串终止符，属性实际上包含两个字符串，等价于更易读的写法：

```dts
compatible = "rockchip,rk3326-odroidgo3-linux", "rockchip,rk3326";
```

前者是板级兼容标识，后者是较通用的 SoC 标识。内核用兼容标识匹配平台或设备支持，具体外设还要看各自节点的 `compatible`。顺序通常由具体到通用；其格式与匹配含义见 [Devicetree Specification：compatible](https://devicetree-specification.readthedocs.io/en/stable/devicetree-basics.html#compatible)。

它不能单独证明机器就是 ODROID-GO3，更不能保证所有 RK3326 设备都能使用同一份内核和设备树。本文件的 `model` 已是 `Game Console R35S/R36S fix by lxc`，而根节点兼容标识仍保留 ODROID-GO3 命名。

### 1.2 应分别查阅的官方资料

| 要查什么 | 一手资料入口 | 可以确认的内容与边界 |
| --- | --- | --- |
| 这个完整兼容字符串在哪里定义 | [Hardkernel 官方 rk3326-odroidgo3-linux.dts](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts)（[原始文本](https://raw.githubusercontent.com/hardkernel/linux/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326-odroidgo3-linux.dts)） | 已核对，根节点声明相同的两个兼容字符串；这是 ODROID-GO3 的官方参考源码，不能由此认定本仓库文件的完整修改历史 |
| RK3326 芯片能力 | [Rockchip 官方 RK3326 产品页](https://www.rock-chips.com/a/en/products/RK33_Series/2018/0514/900.html) | CPU、GPU、存储和显示接口等；不提供本掌机的接线表或换屏初始化命令 |
| SoC 公共设备节点 | [Hardkernel rk3326.dtsi](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/arch/arm64/boot/dts/rockchip/rk3326.dtsi) 与同目录包含文件 | 配合板级 DTS 追踪控制器、时钟、引脚等定义 |
| GPIO 编号与有效电平 | [Rockchip 引脚宏](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/include/dt-bindings/pinctrl/rockchip.h)、[GPIO 宏](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/include/dt-bindings/gpio/gpio.h) | 对照 `RK_PA0` 等引脚编号及 `GPIO_ACTIVE_LOW`；必须结合目标板实接线路 |
| 屏幕属性的具体解析 | [同分支 panel-simple 驱动](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/drivers/gpu/drm/panel/panel-simple.c) | 作为 BSP 驱动参考；最终以实际运行内核的驱动版本为准 |

需要芯片寄存器、封装引脚或电气限制时，还应取得对应型号和修订的 Datasheet/TRM；本次核实的官方产品页不能替代这些资料。掌机主板原理图和屏幕规格书也不能从根节点字符串推导出来。

## 2. 换屏幕、GPIO 时，一般修改 Panel4.dts 哪里？

### 2.1 换屏幕的主要修改位置

下列行号对应本次读取的文件，后续修改可能变化；以节点路径和属性名定位更可靠。

| 修改对象 | Panel4.dts 位置 | 需要核对的属性 |
| --- | --- | --- |
| DSI 控制器 | `/dsi@ff450000`，约第 2029 行 | `status`、端点连接；仅在显示链路确实变化时调整 |
| 屏幕本体 | `/dsi@ff450000/panel@0`，约第 2064 行 | `compatible`、`dsi,lanes`、`dsi,format`、`dsi,flags`、物理尺寸 |
| 复位与上电时序 | 同一 `panel@0` | `reset-gpios`、`reset-delay-ms`、`init-delay-ms`、`prepare/enable/disable/unprepare-delay-ms` |
| 屏幕初始化和退出 | 同一 `panel@0` | `panel-init-sequence`、`panel-exit-sequence`；需要屏厂资料或已验证配置作依据 |
| 显示时序 | `panel@0/display-timings`，约第 2085 行 | 像素时钟、有效分辨率、前后肩、同步长度、极性和 `native-mode` |
| 背光 | `/backlight`，约第 3689 行 | `pwms`、亮度表、默认亮度；同时追踪 PWM 控制器和引脚复用 |
| 屏幕供电 | `panel@0` 的供电引用，以及 `/i2c@ff180000/pmic@20/regulators` | `power-supply`、`backlight-supply` 对应电源；电压不可凭猜测修改 |

Panel4 当前配置为 4 条 DSI lane，`dsi,format = <0>`；在相应 BSP 的 MIPI DSI 定义中，格式 0 对应 RGB888。`dsi,flags = <0xa03>` 是多个标志的组合，需对照[对应分支的 DSI 宏定义](https://github.com/hardkernel/linux/blob/odroidgoA-4.4.y/include/dt-bindings/display/drm_mipi_dsi.h)，不能把其他内核中的数值含义直接套用。

Panel4 的初始化序列主要采用“包类型、延时毫秒数、载荷长度、载荷”的排列。例如末尾 `05 c8 01 11` 表示类型 `0x05`、延时 200 ms、载荷 1 字节 `0x11`。具体发送逻辑仍以目标内核驱动为准。换屏时需要记录命令来源、目标屏幕及延时，并逐条核对载荷长度；仅改分辨率通常不够。

当前供电引用：`backlight = <0x9d>` 指向 `/backlight`；`backlight-supply = <0x9e>` 指向 `LDO_REG7`（`vcc_backlight`，配置 3.3 V）；`power-supply = <0x9f>` 指向 `LDO_REG8`（`vcc_lcd`，配置 2.8 V）。这些是源码配置值，不是本次测量结果。

**本次发现的已有时序问题：**

- `native-mode = <0xa0>`，但三个时序节点的 `phandle` 分别为 `0xaa1`、`0xa00`、`0xa01`；全文件未找到 `phandle = <0xa0>`。这是源码中的悬空引用，选择默认模式前必须核对，不能只看 `__symbols__.timing0` 的路径便认为引用正确。本次未修改或实测其运行影响。
- 三个模式的像素时钟均为 29,000,000 Hz，水平总周期均为 `640 + 46 + 2 + 44 = 732`。`60Hz` 节点的垂直总周期为 `480 + 165 + 2 + 14 = 661`，按时序计算约 **59.94 Hz**。
- `50Hz` 和 `75Hz` 的垂直参数相同，总周期均为 `480 + 16 + 2 + 14 = 512`，计算均约 **77.38 Hz**。因此节点名不能当作实际刷新率；这些是参数计算值，尚非实机测量值。

### 2.2 GPIO 怎么读、怎么改？

本文件 GPIO 控制器声明了 `#gpio-cells = <2>`，所以常见引用的结构是：

```text
gpios = <控制器phandle 控制器内引脚号 标志>;
```

**Panel4 文件内部**的映射如下，数字不得跨 DTS 照搬：

| 控制器 phandle | 节点 | GPIO bank |
| --- | --- | --- |
| `0x5c` | `/pinctrl/gpio0@ff040000` | GPIO0 |
| `0xbf` | `/pinctrl/gpio1@ff250000` | GPIO1 |
| `0x66` | `/pinctrl/gpio2@ff260000` | GPIO2 |
| `0x97` | `/pinctrl/gpio3@ff270000` | GPIO3 |

每个 bank 的 A/B/C/D 组各 8 个引脚：A0–A7 对应 0–7，B0–B7 对应 8–15，C0–C7 对应 16–23，D0–D7 对应 24–31。这是控制器内编号，不是芯片封装脚号，也不是排线针脚号。

例如屏幕复位：

```dts
reset-gpios = <0x97 0x10 0x01>;
```

这里是 GPIO3_C0（编号 16），标志 1 表示低电平有效。若原理图和屏幕规格确认改接 GPIO3_C1，且仍低有效，则本文件对应值可改为 `<0x97 0x11 0x01>`。这只是语法示例，**不表示推荐该引脚或已确认它空闲**；还必须检查引脚复用、电气限制、供电域和其他占用。

| 要改变的线路或功能 | 修改位置 | 同时检查 |
| --- | --- | --- |
| 游戏按键 | `/odroidgo3-joypad/sw*`，约第 3573 行起 | `gpios`、`linux,code`、输入驱动、前端映射，以及 `pinctrl-0` 引用的按键引脚配置 |
| 音量键 | `/odroidgo3-keys/button@*`，约第 3517 行起 | `gpios`、`linux,code` 与 `gpio-keys` 支持 |
| 摇杆模拟多路选择 | `/odroidgo3-joypad` | `amux-a/b/en-gpios`、`io-channels`、ADC 通道与轴方向 |
| 屏幕复位 | `panel@0/reset-gpios` | 有效电平、延时和对应引脚状态 |
| 背光控制 | `/backlight/pwms` 和对应 PWM 节点 | 当前 `0xc1` 指向 `/pwm@ff200010`；不是把 GPIO 编号直接填进 `pwms` |
| 指示灯 | `/gpio_leds/heartbeat` | `gpios` 以及 `pinctrl-0` 引用 |

例如 `/odroidgo3-joypad/sw1` 的 `<0xbf 0x0c 0x01>` 表示 GPIO1_B4、低电平有效，`linux,code = <0x220>` 是上报事件码。改线路主要改 `gpios`；改按键语义还要核对事件码和用户态映射。`label` 只是描述，`GPIO F1` 等文字不能单独识别机身 FN 键。

**常规换屏/GPIO 适配通常不修改根节点 `compatible`。** 若目标内核已有相应 DSI、panel、PWM、GPIO 和 joypad 驱动，先评估通过设备树完成；若驱动不支持新屏协议或所需属性，才需要修改并构建内核。普通 Panel 4 与 Panel 4 - V22 必须分开，不能将 V22 当作别名。

## 3. `rg351mp-kernel.dtb` 是内核吗？

**本仓库 `R36S/Panel 4/rg351mp-kernel.dtb` 是二进制设备树 DTB，不是 Linux 内核镜像。** 文件名里的 `kernel` 不改变文件格式。

本次直接读取二进制并解析 FDT 头和结构块，得到：

| 检查项 | 结果 |
| --- | --- |
| 文件长度 / FDT 总长度 | 59,133 / 59,133 字节 |
| FDT magic / 版本 | `0xd00dfeed` / 17 |
| 根节点 `compatible` | `rockchip,rk3326-rg351mp-linux`、`rockchip,rk3326` |
| 根节点 `model` | `RG351MP for linux based on Rockchip rk3326` |
| 结构块解析 | 1,780 个属性，节点栈闭合，正常读到结束标记 |
| SHA-256 | `fcd325ee957987c8c2fb68d3098594bc58a22fb93ed7c8febe399ce5a6527c98` |

DTB 是 DTS 的二进制表示，通常由 `dtc` 编译生成；头部格式见 [Devicetree Specification：Flattened Devicetree](https://devicetree-specification.readthedocs.io/en/stable/flattened-format.html)。但二进制本身不记录完整构建过程，不能据此断言这个历史文件具体来自哪个 DTS 或编译命令。本次也没有证明它能由 Panel4.dts 重建，两者根节点兼容标识就不同。

Panel 4 的 boot.ini 明确分开加载：

```text
load mmc 1:1 ${loadaddr} Image
load mmc 1:1 ${initrd_loadaddr} uInitrd
load mmc 1:1 ${dtb_loadaddr} rk3326-r35s-linux.dtb
booti ${loadaddr} ${initrd_loadaddr} ${dtb_loadaddr}
```

因此该模板实际使用 `Image` 作为内核、`rk3326-r35s-linux.dtb` 作为设备树；并没有加载 `rg351mp-kernel.dtb`。这段只是仓库配置摘录，不应整份覆盖系统卡，因为模板含固定根分区 UUID。

## 4. 去哪里找到这块板能用的内核镜像？

### 4.1 先确定目标：RK3326 没有一份通用于所有主板的 `Image`

优先使用原卡或同一发行版为目标机型提供的内核，与 DTB、`uInitrd`、内核模块及图形驱动配套。若掌机可启动，在掌机终端收集以下只读信息（不是在 Windows PowerShell 中执行）：

```bash
uname -a
cat /etc/os-release
cat /proc/cmdline
tr '\000' '\n' < /proc/device-tree/compatible
ls /lib/modules
```

再读取实际启动配置确认内核和 DTB 的加载路径。`uname` 能帮助识别内核版本，但版本字符串和 `compatible` 都不能独立证明构建来源或主板兼容性。

### 4.2 本次已经找到的网络来源

| 来源 | 链接 | 应如何理解 |
| --- | --- | --- |
| 明确面向 R35S/R36S 的社区系统 | [AeolusUX/ArkOS-R3XS Wiki 下载入口](https://github.com/AeolusUX/ArkOS-R3XS/wiki)，页面有 R35S/R36S 下载项 | 是完整系统镜像入口；可从对应系统镜像的启动分区取得配套内核。仓库已于 2026-06-09 归档，不应称为持续更新的最新系统 |
| dArkOS 的 RG351MP 系统 | [维护者发布页 v08272026](https://github.com/christianhaitian/dArkOS/releases/tag/v08272026) | 已通过 GitHub API 核实下方两个分卷资产存在；这是 RG351MP 发布物，尚未确认与本机 Panel4/主板兼容 |
| ArkOS 内核源码与构建依据 | [ArkOS 官方 Building](https://github.com/christianhaitian/arkos/wiki/Building)、[维护者 linux/rg351 README](https://github.com/christianhaitian/linux/blob/rg351/README) | 用于追查驱动及构建方法，不是可直接安装的 `Image`。README 指明构建产物位置为 `arch/arm64/boot/Image`，并要求安装配套模块；该分支说明面向 RG351，不能直接承诺用于 R36S |
| Hardkernel 官方 BSP 源码 | [hardkernel/linux：odroidgoA-4.4.y](https://github.com/hardkernel/linux/tree/odroidgoA-4.4.y) | 用于核对 GO3 兼容字符串与 BSP 驱动；不是 R36S 专用完整系统或已验证内核包 |

dArkOS 本次核实的具体下载链接如下。**它们是完整系统镜像的压缩分卷，不是单独的内核文件：**

- [dArkOS_RG351MP_trixie_09022026.img.7z.001](https://github.com/christianhaitian/dArkOS/releases/download/v08272026/dArkOS_RG351MP_trixie_09022026.img.7z.001)
- [dArkOS_RG351MP_trixie_09022026.img.7z.002](https://github.com/christianhaitian/dArkOS/releases/download/v08272026/dArkOS_RG351MP_trixie_09022026.img.7z.002)

需要从该候选系统提取内核时：下载两个分卷到同一目录，从 `.001` 开始解压出 `.img`，用支持分区镜像的工具只读打开，检查启动分区的实际配置，再提取配置指向的内核文件，同时记录镜像版本和模块目录。不要把整卡 `.img` 改名为 `Image`；也不要把提取出的内核单独覆盖到现有系统便认为完成适配。

本次仅核实发布入口、资产名称和下载 URL，未下载完整系统、检查其分区内容或验证镜像内核版本。RG351MP 与 R36S 的适配关系仍需发行版说明及具体硬件验证，不能仅因本仓库出现 `rg351mp` 文件名就认定兼容。

### 4.3 本仓库已有的 `Image`

仓库的 [Panel 5/Image](../R36S/Panel%205/Image) 和 [Panel 6/Image](../R36S/Panel%206/Image) 都为 10,895,368 字节，SHA-256 均为：

```text
3305f6b8d32b5978ef72e8461b167dce849dd608ad2a19228670ec400cdc9eb7
```

本次读取它们偏移 `0x38` 的 4 字节均为 `41 52 4d 64`（`ARMd`），与 [Linux ARM64 Image 头格式](https://docs.kernel.org/arch/arm64/booting.html) 一致。但仓库没有提供可确认该镜像来源的内核源码、配置和完整构建记录，不能保证可复现，也不能认为它适合 Panel4。Panel4 目录本身没有 `Image`。

### 4.4 实际选择与恢复顺序

1. 已有系统能正常启动，只换屏或 GPIO：优先保留现有内核，核对驱动后仅调整所需设备树。
2. 需要重建系统：先从明确面向 R35S/R36S 的发行版入口确认硬件支持；RG351MP 发布物仅作有待核对的候选。
3. 操作前备份原卡启动分区、实际加载配置、DTB、内核和 initrd；更换系统前另外保留整卡备份，更换内核还应保留原模块。
4. 一次只验证一组配置，保留现有 `root=`、UUID、内存地址及其他系统参数，确认配置确实加载了本次测试文件。
5. 冷启动检查显示、背光、方向键/摇杆/FN、声音、充电及电量；涉及 USB/供电时补测相应功能。失败后关机取卡，恢复本次改动前的文件及配套模块。

目前缺少这块实物主板的板号、屏幕标识和现有系统/内核信息，所以查到了可追溯的下载入口和候选发布物，但尚不能指定一份“已验证可直接替换”的内核。

## 5. 本次验证范围

已阅读 README、项目指南、Panel4.dts 与 Panel 4/boot.ini；核查官方兼容字符串、网络发布入口和 GitHub 资产元数据；检查本地 DTB 的 FDT 头与结构、根属性及哈希，检查两份 Image 的头部标识与哈希，并计算显示时序。

本次仅新增本文档，未修改 DTS、DTB、Image 或启动参数。当前环境未找到 `dtc`，所以未运行 dtc 编译/反编译；自定义 FDT 结构解析不能替代 dtc 检查。未连接掌机，未进行刷卡、启动或任何硬件验证。
