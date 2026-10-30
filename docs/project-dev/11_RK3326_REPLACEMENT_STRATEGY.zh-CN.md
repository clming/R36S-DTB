# RK3326 供货风险与新掌机平台替换方案

版本：V0.1；调查日期：2026-10-29。性质：公开资料核查与采购/研发决策稿，尚未取得芯片厂商书面生命周期确认、板卡报价或替代样机实测。结合[市场与切入调查](12_HANDHELD_MARKET_ENTRY_RESEARCH.zh-CN.md)及[项目落地手册](10_PROJECT_PROCUREMENT_PILOT_EXECUTION.zh-CN.md)使用。

## 1. 当前应采取的决定

**停止把 RK3326 视为新产品不可变的主控约束；保留现有机器作体验与恢复研究基线。首轮并行评估 H700 成熟掌机方案和 RK3566/RK3568 成熟方案，根据书面供货、完整 BSP、整机成本和样机验证选一条。** 若低价方案都无法提供可持续维护与供货依据，应缩小产品目标或换供应商，不把未知库存当成长供。

如果目标从经典平台升级到以 PS2/GameCube 等更高负载为卖点，应另立 Android 产品路线，向具备交付能力的 ODM 询问骁龙 G 系列、8 Gen 2 或天玑方案；不把它当成 RK3326 原板的小改。更高性能 CPU/GPU 也不意味着目标平台所有内容均能稳定运行。

“替换方案”在本文指重新选型的产品平台，**不是 BGA 原位替换料，也不是已经拿到的量产供应合同**。没有核实任何候选可与 RK3326 引脚兼容。

## 2. “RK3326 已停产”目前核实到哪一层

| 命题 | 本次调查结果 | 应如何用于决策 |
| --- | --- | --- |
| 瑞芯微已正式宣布 RK3326 全型号 EOL | 搜索官方域名及公开资料，未取得可核实的 RK3326 专属 EOL/PCN 公告或最后订购/交付日期 | 不能把传闻写成已证实，也不能反向宣称仍正常生产 |
| 原 R36S 板厂已停止供应 | 用户提供了这一供货风险；当前没有板厂法律主体、原始停供函与确切板卡 MPN | 作为项目高风险处理，暂停依赖该供方锁定新订单；继续索取书面确认 |
| 公开页面/固件仍存在 | [原厂产品页](https://www.rock-chips.com/a/en/products/RK33_Series/2018/0514/900.html)和 [rkbin RK3326 发布记录](https://github.com/rockchip-linux/rkbin/blob/master/doc/release/RK3326_EN.md)可提供技术线索 | 页面或软件维护存在，不证明晶圆仍在生产；不能据此承诺芯片供货 |
| 零售仍能买到同名掌机/芯片 | 本次未建立可追溯的现货与批次证据 | 即便可买，也可能是库存、换板或渠道存量；需查批次与质保 |

芯片停产、板厂停供、代理缺货、MOQ 提高、DDR/PMIC 配套缺货和发行版停止维护是六种不同问题。某份 eMMC 支持列表中的“EOL”也不能直接解释为 RK3326 芯片 EOL。

### 必须向原厂/原供方追问的字段

`准确芯片/板卡MPN、停产或变更通知编号、适用修订、公告日期、最后订购日LTB、最后交付日LTS、已承诺订单、可追溯库存、替代型号、BSP支持期限、配套DDR/PMIC状态、原镜像/源码交付与售后备件`。对“没有公告但以后不做了”的板厂，也要形成书面供货终止/交付说明。

## 3. 候选平台比较

以下硬件架构和产品使用证据来自芯片/整机/开发板或固件项目的一手资料；供货期限、裸芯价、性能差值和新板工作量未实测，不提供虚构的百分比提升或成本。

| 候选 | 可核实的架构/市场证据 | 对本项目的价值 | 主要代价和不确定性 | 初步定位 |
| --- | --- | --- | --- | --- |
| Allwinner H700 成熟掌机方案 | [全志 H700 简介](https://www.allwinnertech.com/uploads/pdf/2021070513595227.pdf)；[RG35XXSP](https://anbernic.com/products/rg35xxsp)和[当前 RGSP](https://anbernic.com/products/rg-sp)标注四核 A53、Linux | 有同价位、同类屏/操作方式的产品证据，可优先问成熟板卡/ODM | 芯片采购、完整 SDK、屏/休眠/充电、GPU 栈和可分发范围需验证；整机在售不等于板卡开放销售 | 低价经典平台首选询价路线之一 |
| Rockchip RK3566/RK3568 | [RG353V/VS](https://anbernic.com/products/rg353v-rg353vs)使用 RK3566；[RG DS Plus](https://anbernic.com/products/rg-ds-plus)使用 RK3568；均为四核 A55 类平台 | 延续 Rockchip 工具/资料习惯，有 Linux 掌机与开发板参考 | 不是新发布或长寿命保证；电源、DDR、引导和显示重做；SoM 体积/功耗不一定适合 | 资料可控、希望保留 Linux 工程路线时优先 |
| Allwinner A133/A133 衍生板 | [全志 A133](https://www.allwinnertech.com/index.php?c=product&id=93)为四核 A53、PowerVR GE8300；[KNULLI Brick 设备源码说明](https://github.com/knulli-cfw/knulli.org/blob/main/docs/devices/trimui/brick.md)列出 A133/BSP 图形栈 | 小型掌机已有参考；[Trimui 厂商固件库](https://github.com/trimui/firmware_brick)可研究体验和发行方式 | A133/A133P 完整后缀需供方确认；PowerVR/BSP 配套及源码交付需审；不能假设可直接使用 Mali 库 | 有完整 ODM 交付时的备选，不因 CPU 核数相同就默认等价 |
| Allwinner A527 类 | [原厂页](https://www.allwinnertech.com/index.php?a=index&c=product&id=109)列八核 A55、Mali-G57、Tina Linux/Android | 可评估较新带屏产品方案，丰富接口利于原型 | 本次未证实低价掌机成熟供方、功耗/续航与维护方案；八个小核不是高端模拟能力保证 | 预研候选，不作首轮最快路线 |
| Rockchip RK3576 类 | [原厂 Brief Datasheet](https://www.rock-chips.com/uploads/pdf/2024.3.18/191/RK3576%20Brief%20Datasheet%20V1.2-20250828.pdf)、[Radxa 软件矩阵](https://docs.radxa.com/software-support-matrix/rockchip)提供平台参考 | 需要更高运算能力和自有硬件时可预研 | 板级成本、散热、电源与游戏系统适配工作增加，未核实适合本项目的量产板报价 | 有硬件团队和更高预算才进入 |
| Android ODM：骁龙/天玑 | [RG55G1](https://anbernic.com/products/rg-55g1)采用 Snapdragon G1 Gen 2；[Retroid Pocket 6](https://www.goretroid.com/products/retroid-pocket-6-handheld)采用 8 Gen 2；[RG477V](https://anbernic.com/products/rg477v)采用天玑 8300 | 性能、Android 应用和较高价位产品有直接市场样本 | 需要 Android BSP/授权、输入/休眠/散热/OTA、触屏和安全维护；成熟品牌方案不一定允许供板/OEM | 高一档产品线，另行立项 |

H700、RK3566/RK3568 和 A133 本身也已有多年历史，不能以“换了型号”替代生命周期管理。芯片发布日期、核心数量、NPU TOPS 和视频解码规格均不能直接给出模拟器性能结论。

## 4. 本项目的推荐顺序和决胜条件

| 路线 | 先评估对象 | 推荐成立条件 | 何时淘汰 |
| --- | --- | --- | --- |
| L：低价 Linux 经典掌机 | H700 成熟板/ODM，与 RK3566/RK3568 方案并行 | 完整可恢复系统、明确料号与供货、可维护 BSP、同目标内容测试通过、成本闭合 | 只卖零售机、不提供工程交付，或拒绝批次一致性和变更通知 |
| C：工程可控的 Linux 设计 | RK3566/3568 板/SoM；必要时再看 RK3576 | 有结构/功耗匹配、可取得硬件资料、团队能移植并完成验证 | 参考板过大/功耗不合适、设计资料不足、预算无法覆盖改板 |
| A：性能和更高客单 | Android ODM，按合法应用和内容实测挑 SoC | 明确售价与用户群、支持期、软件分发和 OTA 责任，具备热/功耗余量 | 为追热度而选旗舰，但售价、散热或供应协议没有依据 |

**当前建议选 L 作为第一轮取样方向，不在没有报价和样机的情况下预先宣布 H700 或 RK3566 胜出。** 如果供方仅能提供 RK3326 库存，可作为封顶数量、来源明确的研究/备件采购候选，不作为新产品默认长期 BOM；是否采购另行决策，本轮未下单。

## 5. 原项目能复用什么，必须重做什么

| 模块 | 可复用的资产 | 切平台必须重新完成 |
| --- | --- | --- |
| 产品/体验 | 需求、实体布局目标、菜单流程、验收用例 | 性能、扩展平台、续航、售价和地区需求重新冻结 |
| 结构 | 人机布局、测绘方法、辅料设计思路 | 新 PCB 外形、器件高度、散热、电池、接口和屏排线堆叠 |
| 屏 | 若同一料号可保留模组及厂商初始化资料 | 新 SoC 接口/驱动/电源时序/背光重新验证，连接器相同不证明兼容 |
| 输入 | 物理键语义、应用层热键、测试页面需求 | GPIO/pinmux、ADC、驱动、校准、Linux/Android 事件和映射 |
| 电源/音频 | 功率预算方法、负载与声学目标 | PMIC/codec 型号、轨、电池、充电、NTC、USB 角色和关机链 |
| 启动与内核 | 备份/恢复、版本记录和模块检查方法 | loader、U-Boot、内核、DTS/DTB、initramfs、模块及 GPU 库整套匹配 |
| 应用/内容 | 有权使用的源码、主题、游戏/存档管理和元数据 | ABI、核心编译、运行命令、许可、存档兼容和性能回归 |

RK817 不能随 RK3326 被“自动继承”到新平台；是否继续采用由电源和音频设计决定。Android 不保证存在 ArkOS 同名 `boot.ini`、`Image` 和 `uInitrd` 布局。原 Panel4 的 DTB 或旧 initrd 不应直接放进 H700/RK3566 新系统试运气。

## 6. 源码、系统、参考电路到哪里找

| 平台 | 一手资料入口 | 本次核实到的范围 | 尚需取得 |
| --- | --- | --- | --- |
| H700 | [原厂简介](https://www.allwinnertech.com/uploads/pdf/2021070513595227.pdf)、[ANBERNIC 支持入口](https://support.anbernic.com/)、[KNULLI 工程](https://github.com/knulli-cfw/knulli-linux) | 芯片能力、同平台整机及固件项目存在 | 对应新板 SDK/配置/PMIC、引导布局、完整模块/库、可再分发依据 |
| RK3566 | [Radxa ROCK3C 资源页](https://docs.radxa.com/en/rock3/rock3c/download)、[官方硬件资源](https://wiki.radxa.com/Rock3/hardware)、[ROCKNIX 工程](https://github.com/ROCKNIX/distribution) | 开发板原理图/资源下载入口和系统工程存在 | 掌机的电池/音频/输入与屏适配；参考板镜像不等于掌机镜像 |
| RK3568 | [Rockchip 公共文档](https://opensource.rock-chips.com/)、[RG DS Plus 官方页](https://anbernic.com/products/rg-ds-plus) | 公共平台资料和当前 Linux 掌机产品证据 | 目标板硬件设计包、软件交付及新产品可使用范围 |
| A133 | [全志资料](https://www.allwinnertech.com/index.php?c=product&id=93)、[厂商 Brick 发布库](https://github.com/trimui/firmware_brick/releases)、[KNULLI 文档工程](https://github.com/knulli-cfw/knulli.org) | 固件发布、设备描述和 BSP 线索 | 新板完整内核/boot/rootfs/图形源码与二进制清单；发布库存在不等于包含完整源码 |
| Android ODM | 对应 ODM 的受控 SDK、[Android AOSP](https://source.android.com/) | 公共 Android 工程入口 | SoC vendor BSP、驱动/固件、量产签名、OTA、应用和 Google 服务授权边界 |

本轮没有下载替代完整固件或参考电路文件，也未编译这些项目；表中是已查询的来源和索取路径，不把仓库存在说成适配完成。社区发行版的商用与再分发须逐组件核对，不能把社区维护者当成 ODM 合同主体。

## 7. 十个工作日完成“候选缩圈”的任务

| 时间 | 任务 | 输出/停止条件 |
| --- | --- | --- |
| D1–D2 | 向原厂核实 RK3326 生命周期，索取板厂停供说明；同时给 H700、RK3566/3568 两条路径发资料/报价需求 | 把停产证据与供货回复分开存档；没有回复标“未知” |
| D2–D3 | 约定同口径功能、卡/屏/电池边界和数量档位 | 可比较报价，不把完整掌机价和裸主板价放同一列 |
| D3–D5 | 审核资料，决定是否申请/购买可追溯样品 | 主体、硬件、软件与支持条件不清就停止该候选，不先开模 |
| 到样后 D1–D3 | 备份、恢复、显示/键轴/音频/电源/USB 测试 | 同一配置的可恢复基线与全部 P0 结果 |
| 到样后 D4–D5 | 同内容/核心条件下测负载、帧时间、续航和温升，做结构包络 | 可重现的比较表；不以菜单截图比较性能 |
| 评审日 | 硬件/软件/结构/采购/产品共同决定一条主路线及一条有界备选 | 冻结精确配置、交付、预算与下一阶段；未到样不宣称验证结束 |

采购/物流和 SDK 审批等待另计，十个工作日不是量产承诺。

### 统一评分建议

满分 100 的项目内部权重：生命周期/供货 25、BSP/资料/维护 25、整机成本 15、目标内容性能 15、功耗/结构 10、国内外合规支持 10。每项写证据等级（未知、书面、样机、受控量产），无有效证据不得主观打满。无合法交付/供货主体、无法恢复或存在关键电源风险时直接不放行，不用总分掩盖。

## 8. 官方联系和询价重点

| 官方渠道 | 已核实公开信息 | 本项目具体问题 |
| --- | --- | --- |
| [瑞芯微](https://www.rock-chips.com/a/en/contact/index.html) | `service@rock-chips.com`；`400-7700-590` | RK3326 完整 MPN 的生命周期、LTB/LTS；RK3566/3568/3576 的推荐渠道、SDK/设计资料、供货与支持范围 |
| [全志官方联系页](https://www.allwinnertech.com/index.php?a=index&c=message) | 消费终端：`sales.consumer@allwinnertech.com` / `product.consumer@allwinnertech.com`；H/TV 多媒体业务：`sales.video@allwinnertech.com` | A133/A527/H700 游戏机项目路由、推荐方案商、精确后缀、PMIC/DDR/BSP 和生命周期；先请求转对应团队 |
| [ANBERNIC 官方联系页](https://anbernic.com/pages/contact-us) | `contact@anbernic.com`；官网另有合作咨询入口 | 样机/官方产品、合作方式及是否开放供板/ODM；不假设其愿意出售原始设计或给竞争品牌供货 |
| [Radxa 官方资源与支持](https://docs.radxa.com/en/rock3/rock3c/download) | 资源页可用于获取开发板资料，再由其官方支持/商务入口咨询 | 参考设计使用边界、计算模块供应和项目匹配；不把开发板能力当掌机量产支持 |

给所有候选供方增加四项书面问询：①可承诺的供货窗口与变更提前期；②精确板/屏/DDR/PMIC 固定清单；③源码、工具链、模块/GPU 库及恢复交付；④国内/美国/欧盟目标 SKU 的测试报告覆盖与改版复测责任。未取得书面承诺，不标“可长期供应”。

## 9. 与旧文档的优先级

01–10 中的 RK3326、RK817 和 Panel4 描述保留为**参考机器的事实与历史方案**。新产品平台以本文件及后续 G0 决议为准；产品验收方法、结构/硬件/软件工作包继续适用，但参数、料号、原理图和镜像要按新平台重新冻结。国内外差异任务集中见[10 手册第 13 节](10_PROJECT_PROCUREMENT_PILOT_EXECUTION.zh-CN.md#13-国内与海外销售的新增工作包2026-10-29)。
