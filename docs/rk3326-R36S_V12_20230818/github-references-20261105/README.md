# GitHub 参考资料与文件核验

本目录重新整理于 2026-11-05。当前唯一比较基准为 [zj_boot/rf3536k3ka.dts](../zj_boot/rf3536k3ka.dts)。原先的 resolved 目录已经不存在，本次没有恢复其他被用户删除的目录。

重新编译本地 DTS 并比较四份公开样本，结果仍为 **7 / 9 / 9 / 18 项属性差异**。引用按类型解析为节点路径，排除 phandle 定义与符号元数据；最近样本硬件节点路径相同，其余非屏幕属性一致。

## 候选与来源

| 样本 | 差异数 | 本地文件 | 来源 |
| --- | --- | --- | --- |
| #530 主帖原厂 DTB | 7，全部在屏幕 | [DTS](issue530-original.dts) / [DTB](issue530-original.dtb) | [问题页](https://github.com/lcdyk0517/arkos4clone/issues/530) / [原附件](https://github.com/user-attachments/files/33845333/rf3536k3ka.zip) |
| immo2n 同源 DTS | 9，屏幕 + BOOST 电压 | [DTS](immo2n-rf3536k3ka.dts) | [固定提交](https://github.com/immo2n/R36S-K36-DTB-PATCH/blob/cdd88b87c74dca43828a6eda55bc76c98928556e/rf3536k3ka.dts) |
| #530 评论 batch2549 | 9 | [DTS](issue530-stock-2549.dts) / [DTB](issue530-stock-2549.dtb) | [原附件](https://github.com/user-attachments/files/33850662/rf3536k3ka-stock-dtb.zip) |
| #372 原厂样本 | 18，含节点大小写产生的8项单侧属性 | [DTS](issue372-original.dts) / [DTB](issue372-original.dtb) | [问题页](https://github.com/lcdyk0517/arkos4clone/issues/372) / [启动备份ZIP](https://github.com/user-attachments/files/28431858/Console.zip) |

这些文件来自社区项目和用户上传的原厂卡备份，不能统称为芯片/整机厂商官方发布。19 路按键 GPIO 数组与本地一致；这些 DTS 同样没有逐键给出 A/B/FN 等实体名称。

## 最近样本的全部七项差异

| 节点 | 属性 | 本地 | #530 样本 |
| --- | --- | --- | --- |
| <code>/dsi@ff450000/panel@0</code> | <code>panel-init-sequence</code> | <code>753 字节；完整序列见两份 DTS</code> | <code>370 字节；完整序列见两份 DTS</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>hback-porch</code> | <code>[44]</code> | <code>[150]</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>hfront-porch</code> | <code>[46]</code> | <code>[150]</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>hsync-len</code> | <code>[2]</code> | <code>[50]</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>vback-porch</code> | <code>[14]</code> | <code>[12]</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>vfront-porch</code> | <code>[16]</code> | <code>[20]</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>vsync-len</code> | <code>[2]</code> | <code>[6]</code> |

[Excel 可读 CSV](closest-seven-differences.csv)。屏幕初始化需保留本机配置；整机属性更接近不代表屏幕可替换。Panel 6 初始化字节序列约 99.337% 接近，而以上样本约 12.11%；两者参考用途不同。

## 启动文件下载与一致性

下载 [Console.zip](https://github.com/user-attachments/files/28431858/Console.zip)，从 `Consola/` 提取。该包不是完整可烧录系统镜像。

| 文件 | 包内位置 | 与当前本地比较 |
| --- | --- | --- |
| Image | `Consola/Image` | 不一致 |
| uInitrd | `Consola/uInitrd` | 逐字节一致 |
| rf3536k3ka.dtb | `Consola/rf3536k3ka.dtb` | 不一致 |
| extlinux/extlinux.conf | `Consola/extlinux/extlinux.conf` | 逐字节一致 |
| logo.bmp | `Consola/logo.bmp` | 逐字节一致 |
| logo_kernel.bmp | `Consola/logo_kernel.bmp` | 逐字节一致 |

哈希、长度和内核编译字符串见 [boot-files-verification.json](boot-files-verification.json)。本地 Image 为 5.10.160-g3ee18cae74dc-dirty，下载样本为 5.10.160-g0bc6eae0eb0c-dirty，不能称为同一构建。

## 内核源码与整卡镜像入口

- [Rockchip 官方平台源码](https://github.com/rockchip-linux/kernel/tree/develop-5.10)：平台参考，尚未确认是本机原厂构建的确切源码。
- [ArkOS4Clone 社区5.10源码](https://github.com/lcdyk0517/arkos.bsp.5.10/tree/arkos4clone-5.10)：社区适配方案，与本机 play_joystick 驱动不能直接视为同一实现。
- [社区整卡镜像发布](https://github.com/lcdyk0517/arkos4clone/releases/tag/20261008)：分卷地址、独立 Image 下载和固定源码提交见[父目录资料总览](../README.md)。
- [核心板 GPIO 交付](../核心板GPIO_20261105/README.md)：以当前原卡 DTS 生成，包含硬件原理图审查待核实项。

## 文件与验证

[sources.json](sources.json)记录来源和逐文件 SHA-256；[normalization-rules.json](normalization-rules.json)保留引用解析规则；[comparison-results.json](comparison-results.json)为统计。各样本的 `*-differences.json` 保留完整参数数据。

所有候选经 DTC 1.7.2 编译或回编译验证，引用解析无失败；[dtc-warnings.txt](dtc-warnings.txt)保留结构警告。原卡 DTS / DTB、Image、uInitrd 未修改；未做掌机启动测试。

