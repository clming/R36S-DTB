# rf3536k3ka 与 Panel 6：解析引用后的参数差异

两份原 DTS 的副本及完整归一化结果与本报告放在同一目录。原项目文件未修改。

phandle 按属性类型解析成节点路径，提供者参数数量取自 `#clock-cells`、`#gpio-cells` 等定义；GPIO、时钟编号及标志位保持为参数，不会误当成引用。`rockchip,pins` 的第 4 项解析为 pin-config 节点。共同符号、同父节点唯一 reg / compatible 和完全相同的引脚配置用于建立一对一对应关系；匹配节点的 compatible、reg 等变化仍保留。

删除 phandle 定义与符号/修正表，不以其编号差异计数；对齐 `timing0` 与 `60Hz`、DMA 总线、OTP 和电源域等名称变化。**归一化不代表两块板兼容，也不会隐藏独有节点或不同驱动。**

## 统计

| 项目 | 数量 |
| --- | --- |
| <code>原始普通属性差异</code> | <code>1598</code> |
| <code>成功对齐节点</code> | <code>427</code> |
| <code>其中名称/路径不同</code> | <code>22</code> |
| <code>参考侧已解析引用属性</code> | <code>497</code> |
| <code>Panel 6 已解析引用属性</code> | <code>472</code> |
| <code>引用解析失败</code> | <code>0</code> |
| <code>已对齐节点仍变化的属性</code> | <code>277</code> |
| <code>仅参考侧的节点/子树</code> | <code>119 / 75</code> |
| <code>仅 Panel 6 的节点/子树</code> | <code>43 / 21</code> |

计数不能直接相减：节点对齐后，原先“仅左存在 + 仅右存在”的两组属性会合并比较。独有子树在下面按子树根汇总；其所有参数仍保留在 CSV 和 JSON 中。

## 已对齐节点中真正变化的参数

只列归一化后不同的参数；相同参数省略。长数组只显示变化区间，区间从 0 开始、右端不包含；完整数据保留在 JSON。屏幕命令在下一节逐条列出。

| 统一节点路径 | 属性 | 参考 rf3536k3ka | Panel 6 |
| --- | --- | --- | --- |
| <code>/</code> | <code>compatible</code> | <code>["rockchip,rk3326-evb-lp3-v12-linux", "rockchip,rk3326"]</code> | <code>["rockchip,rk3326-odroidgo3-linux", "rockchip,rk3326"]</code> |
| <code>/</code> | <code>model</code> | <code>["Rockchip rk3326 evb lpddr3 v12 board for linux"]</code> | <code>["Rockchip RK3326"]</code> |
| <code>/aliases</code> | <code>mmc0</code> | <code>["/dwmmc@ff390000"]</code> | <code>不存在</code> |
| <code>/aliases</code> | <code>mmc1</code> | <code>["/dwmmc@ff370000"]</code> | <code>不存在</code> |
| <code>/aliases</code> | <code>mmc2</code> | <code>["/dwmmc@ff380000"]</code> | <code>不存在</code> |
| <code>/aliases</code> | <code>spi2</code> | <code>["/spi@ff3a0000"]</code> | <code>不存在</code> |
| <code>/arm-pmu</code> | <code>compatible</code> | <code>["arm,cortex-a35-pmu"]</code> | <code>["arm,cortex-a53-pmu"]</code> |
| <code>/backlight</code> | <code>brightness-levels</code> | <code>[161:256] [161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]</code> | <code>[161:161] []</code> |
| <code>/backlight</code> | <code>default-brightness-level</code> | <code>200 (0xc8)</code> | <code>80 (0x50)</code> |
| <code>/backlight</code> | <code>pwms</code> | <code>&amp;{/pwm@ff200010} 参数 [0, 25000, 0]</code> | <code>&amp;{/pwm@ff200010} 参数 [0, 40000, 0]</code> |
| <code>/bus-soc/soc-bus0</code> | <code>status</code> | <code>不存在</code> | <code>["disabled"]</code> |
| <code>/bus/dmac@ff240000</code> | <code>arm,pl330-periph-burst</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/bus/dmac@ff240000</code> | <code>peripherals-req-type-burst</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/cif-new@ff490000</code> | <code>status</code> | <code>["okay"]</code> | <code>["disabled"]</code> |
| <code>/clock-controller@ff2b0000</code> | <code>rockchip,boost</code> | <code>不存在</code> | <code>&amp;{/cpu-boost@ff2b8000}</code> |
| <code>/cpu0-opp-table</code> | <code>rockchip,bin-scaling-sel</code> | <code>[0, 13, 1, 15, 2, 18]</code> | <code>[0, 13, 1, 13]</code> |
| <code>/cpus/cpu@0</code> | <code>compatible</code> | <code>["arm,cortex-a35"]</code> | <code>["arm,cortex-a35", "arm,armv8"]</code> |
| <code>/cpus/cpu@1</code> | <code>#cooling-cells</code> | <code>2 (0x2)</code> | <code>不存在</code> |
| <code>/cpus/cpu@1</code> | <code>clocks</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [7]</code> | <code>不存在</code> |
| <code>/cpus/cpu@1</code> | <code>compatible</code> | <code>["arm,cortex-a35"]</code> | <code>["arm,cortex-a35", "arm,armv8"]</code> |
| <code>/cpus/cpu@1</code> | <code>dynamic-power-coefficient</code> | <code>90 (0x5a)</code> | <code>不存在</code> |
| <code>/cpus/cpu@2</code> | <code>#cooling-cells</code> | <code>2 (0x2)</code> | <code>不存在</code> |
| <code>/cpus/cpu@2</code> | <code>clocks</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [7]</code> | <code>不存在</code> |
| <code>/cpus/cpu@2</code> | <code>compatible</code> | <code>["arm,cortex-a35"]</code> | <code>["arm,cortex-a35", "arm,armv8"]</code> |
| <code>/cpus/cpu@2</code> | <code>dynamic-power-coefficient</code> | <code>90 (0x5a)</code> | <code>不存在</code> |
| <code>/cpus/cpu@3</code> | <code>#cooling-cells</code> | <code>2 (0x2)</code> | <code>不存在</code> |
| <code>/cpus/cpu@3</code> | <code>clocks</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [7]</code> | <code>不存在</code> |
| <code>/cpus/cpu@3</code> | <code>compatible</code> | <code>["arm,cortex-a35"]</code> | <code>["arm,cortex-a35", "arm,armv8"]</code> |
| <code>/cpus/cpu@3</code> | <code>dynamic-power-coefficient</code> | <code>90 (0x5a)</code> | <code>不存在</code> |
| <code>/crypto@ff0b0000</code> | <code>reg</code> | <code>[0, 4278910976, 0, 1024, 0, 4278912128, 0, 15232]</code> | <code>[0, 4278910976, 0, 16384]</code> |
| <code>/ddr_timing</code> | <code>ddr4_odt_dis_freq</code> | <code>625 (0x271)</code> | <code>666 (0x29a)</code> |
| <code>/ddr_timing</code> | <code>phy_ddr3_odt</code> | <code>4 (0x4)</code> | <code>2 (0x2)</code> |
| <code>/ddr_timing</code> | <code>phy_ddr4_odt_dis_freq</code> | <code>625 (0x271)</code> | <code>666 (0x29a)</code> |
| <code>/dfi@ff610000</code> | <code>status</code> | <code>["okay"]</code> | <code>["disabled"]</code> |
| <code>/dmc</code> | <code>auto-freq-en</code> | <code>0 (0x0)</code> | <code>1 (0x1)</code> |
| <code>/dmc</code> | <code>auto-min-freq</code> | <code>450000 (0x6ddd0)</code> | <code>328000 (0x50140)</code> |
| <code>/dmc</code> | <code>status</code> | <code>["okay"]</code> | <code>["disabled"]</code> |
| <code>/dmc</code> | <code>system-status-freq</code> | <code>[3:4] [528000]; [7:8] [528000]; [11:12] [528000]; [13:14] [528000]</code> | <code>[3:4] [450000]; [7:8] [450000]; [11:12] [666000]; [13:14] [666000]</code> |
| <code>/dmc-opp-table/opp-666000000</code> | <code>status</code> | <code>["disabled"]</code> | <code>不存在</code> |
| <code>/dmc-opp-table/opp-786000000</code> | <code>status</code> | <code>["disabled"]</code> | <code>["okay"]</code> |
| <code>/dsi@ff450000</code> | <code>clock-names</code> | <code>["pclk"]</code> | <code>["pclk", "hs_clk"]</code> |
| <code>/dsi@ff450000</code> | <code>clocks</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [324]</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [324]; &amp;{/phy@ff2e0000}</code> |
| <code>/dsi@ff450000</code> | <code>phy-names</code> | <code>["dphy"]</code> | <code>["mipi_dphy"]</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>compatible</code> | <code>["sitronix,st7703", "simple-panel-dsi"]</code> | <code>["elida,kd35t133", "simple-panel-dsi"]</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>disable-delay-ms</code> | <code>20 (0x14)</code> | <code>50 (0x32)</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>enable-delay-ms</code> | <code>120 (0x78)</code> | <code>200 (0xc8)</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>enable-gpios</code> | <code>不存在</code> | <code>&amp;{/pinctrl/gpio1@ff250000} 参数 [18, 1]</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>height-mm</code> | <code>85 (0x55)</code> | <code>71 (0x47)</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>led-blue1-gpios</code> | <code>不存在</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [0, 0]</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>led-red-gpios</code> | <code>不存在</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [5, 0]</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>power-supply</code> | <code>&amp;{/vcc18-lcd-n}</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG8}</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>prepare-delay-ms</code> | <code>20 (0x14)</code> | <code>100 (0x64)</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>reset-delay-ms</code> | <code>20 (0x14)</code> | <code>50 (0x32)</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>reset-gpios</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [15, 1]</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [16, 1]</code> |
| <code>/dsi@ff450000/panel@0</code> | <code>width-mm</code> | <code>153 (0x99)</code> | <code>71 (0x47)</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>clock-frequency</code> | <code>30000000 (0x1c9c380)</code> | <code>40000000 (0x2625a00)</code> |
| <code>/dsi@ff450000/ports/port@0/endpoint@0</code> | <code>remote-endpoint</code> | <code>&amp;{/vop@ff460000/port/endpoint@0}</code> | <code>&amp;{/vop@ff460000/port/endpoint@1}</code> |
| <code>/dwmmc@ff370000</code> | <code>assigned-clock-parents</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [87]</code> |
| <code>/dwmmc@ff370000</code> | <code>assigned-clocks</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [59]</code> |
| <code>/dwmmc@ff370000</code> | <code>cap-mmc-highspeed</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/dwmmc@ff370000</code> | <code>clock-names</code> | <code>["biu", "ciu", "ciu-drive", "ciu-sample"]</code> | <code>["biu", "ciu", "ciu-drv", "ciu-sample"]</code> |
| <code>/dwmmc@ff370000</code> | <code>max-frequency</code> | <code>100000000 (0x5f5e100)</code> | <code>150000000 (0x8f0d180)</code> |
| <code>/dwmmc@ff380000</code> | <code>assigned-clock-parents</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [81]</code> |
| <code>/dwmmc@ff380000</code> | <code>assigned-clocks</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [56]</code> |
| <code>/dwmmc@ff380000</code> | <code>cap-mmc-highspeed</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/dwmmc@ff380000</code> | <code>cd-gpios</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [2, 1]</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [10, 1]</code> |
| <code>/dwmmc@ff380000</code> | <code>clock-names</code> | <code>["biu", "ciu", "ciu-drive", "ciu-sample"]</code> | <code>["biu", "ciu", "ciu-drv", "ciu-sample"]</code> |
| <code>/dwmmc@ff380000</code> | <code>max-frequency</code> | <code>100000000 (0x5f5e100)</code> | <code>150000000 (0x8f0d180)</code> |
| <code>/dwmmc@ff380000</code> | <code>vmmc-supply</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG8}</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG6}</code> |
| <code>/dwmmc@ff380000</code> | <code>vqmmc-supply</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG7}</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG5}</code> |
| <code>/dwmmc@ff390000</code> | <code>assigned-clock-parents</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [83]</code> |
| <code>/dwmmc@ff390000</code> | <code>assigned-clocks</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [57]</code> |
| <code>/dwmmc@ff390000</code> | <code>bus-width</code> | <code>8 (0x8)</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>cap-mmc-highspeed</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>clock-names</code> | <code>["biu", "ciu", "ciu-drive", "ciu-sample"]</code> | <code>["biu", "ciu", "ciu-drv", "ciu-sample"]</code> |
| <code>/dwmmc@ff390000</code> | <code>disable-wp</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>no-sd</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>no-sdio</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>non-removable</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>num-slots</code> | <code>1 (0x1)</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>pinctrl-0</code> | <code>&amp;{/pinctrl/emmc/emmc-clk}; &amp;{/pinctrl/emmc/emmc-cmd}; &amp;{/pinctrl/emmc/emmc-bus8}</code> | <code>不存在</code> |
| <code>/dwmmc@ff390000</code> | <code>pinctrl-names</code> | <code>["default"]</code> | <code>不存在</code> |
| <code>/fiq-debugger</code> | <code>pinctrl-0</code> | <code>&amp;{/pinctrl/uart5/uart5-xfer}</code> | <code>&amp;{/pinctrl/uart2-m1/uart2m1-xfer}</code> |
| <code>/fiq-debugger</code> | <code>rockchip,irq-mode-enable</code> | <code>1 (0x1)</code> | <code>0 (0x0)</code> |
| <code>/fiq-debugger</code> | <code>rockchip,serial-id</code> | <code>5 (0x5)</code> | <code>2 (0x2)</code> |
| <code>/gpu-opp-table/opp-520000000</code> | <code>opp-microvolt</code> | <code>1175000 (0x11edd8)</code> | <code>1150000 (0x118c30)</code> |
| <code>/gpu-opp-table/opp-520000000</code> | <code>opp-microvolt-L0</code> | <code>1175000 (0x11edd8)</code> | <code>1150000 (0x118c30)</code> |
| <code>/gpu@ff400000</code> | <code>clock-names</code> | <code>不存在</code> | <code>["clk_mali"]</code> |
| <code>/gpu@ff400000</code> | <code>compatible</code> | <code>["rockchip,px30-mali", "arm,mali-bifrost"]</code> | <code>["arm,malit602", "arm,malit60x", "arm,malit6xx", "arm,mali-midgard"]</code> |
| <code>/gpu@ff400000</code> | <code>downdifferential</code> | <code>10 (0xa)</code> | <code>不存在</code> |
| <code>/gpu@ff400000</code> | <code>upthreshold</code> | <code>40 (0x28)</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>allocator</code> | <code>不存在</code> | <code>1 (0x1)</code> |
| <code>/hevc@ff440000</code> | <code>clock-names</code> | <code>["aclk_vcodec", "hclk_vcodec", "clk_core"]</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>clocks</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [175]; &amp;{/clock-controller@ff2b0000} 参数 [244]; &amp;{/clock-controller@ff2b0000} 参数 [75]</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>compatible</code> | <code>["rockchip,hevc-decoder-px30"]</code> | <code>["rockchip,hevc_sub"]</code> |
| <code>/hevc@ff440000</code> | <code>dev_mode</code> | <code>不存在</code> | <code>1 (0x1)</code> |
| <code>/hevc@ff440000</code> | <code>iommu_enabled</code> | <code>不存在</code> | <code>1 (0x1)</code> |
| <code>/hevc@ff440000</code> | <code>power-domains</code> | <code>&amp;{/power-management@ff000000/power-controller} 参数 [11]</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>reset-names</code> | <code>["shared_video_a", "shared_video_h", "niu_a", "niu_h", "video_core"]</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>resets</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [36]; &amp;{/clock-controller@ff2b0000} 参数 [38]; &amp;{/clock-controller@ff2b0000} 参数 [37]; &amp;{/clock-controller@ff2b0000} 参数 [39]; &amp;{/clock-controller@ff2b0000} 参数 [63]</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>rockchip,resetgroup-node</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>rockchip,srv</code> | <code>&amp;{/mpp-srv}</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>rockchip,taskqueue-node</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/hevc@ff440000</code> | <code>status</code> | <code>["okay"]</code> | <code>不存在</code> |
| <code>/i2c@ff180000</code> | <code>compatible</code> | <code>["rockchip,px30-i2c", "rockchip,rk3399-i2c"]</code> | <code>["rockchip,rk3399-i2c"]</code> |
| <code>/i2c@ff180000/pmic@20</code> | <code>interrupts</code> | <code>[10, 8]</code> | <code>[7, 8]</code> |
| <code>/i2c@ff180000/pmic@20</code> | <code>vcc7-supply</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/DCDC_REG4}</code> | <code>&amp;{/vccsys}</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>bat_res</code> | <code>150 (0x96)</code> | <code>132 (0x84)</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>charge_blue_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [0, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>charge_red_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [17, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>dc_det_gpio</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [5, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>design_capacity</code> | <code>2808 (0xaf8)</code> | <code>3156 (0xc54)</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>design_qmax</code> | <code>3089 (0xc11)</code> | <code>3471 (0xd8f)</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>ocv_table</code> | <code>[0:6] [3500, 3531, 3558, 3578, 3595, 3611]; [7:21] [3649, 3675, 3718, 3767, 3810, 3849, 3886, 3919, 3958, 4006, 4051, 4081, 4105, 4172]</code> | <code>[0:9] [3400, 3438, 3486, 3521, 3550, 3571, 3586, 3599, 3612]; [10:21] [3655, 3689, 3719, 3754, 3794, 3838, 3887, 3942, 4005, 4087, 4177]</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>power_off_thresd</code> | <code>3500 (0xdac)</code> | <code>3300 (0xce4)</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>work_blue_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [11, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/battery</code> | <code>work_red_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [12, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>charge_blue_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [0, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>charge_red_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [17, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>chg_led_gpio</code> | <code>不存在</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [1, 0]</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>chrg_finish_cur</code> | <code>300 (0x12c)</code> | <code>52 (0x34)</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>dc_det_adc</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>dc_det_gpio</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [5, 0]</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [23, 0]</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>max_chrg_current</code> | <code>800 (0x320)</code> | <code>2000 (0x7d0)</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>max_input_current</code> | <code>800 (0x320)</code> | <code>1500 (0x5dc)</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>pinctrl-0</code> | <code>&amp;{/pinctrl/led/charge-led-gpio}</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>pinctrl-names</code> | <code>["default"]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>sample_res</code> | <code>不存在</code> | <code>10 (0xa)</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>work_blue_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [11, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/charger</code> | <code>work_red_gpio</code> | <code>&amp;{/pinctrl/gpio0@ff040000} 参数 [12, 0]</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/codec</code> | <code>spk-ctl-gpios</code> | <code>不存在</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [20, 0]</code> |
| <code>/i2c@ff180000/pmic@20/codec</code> | <code>spk-volume</code> | <code>6 (0x6)</code> | <code>1 (0x1)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/BOOST</code> | <code>regulator-max-microvolt</code> | <code>["", "I&gt;"]</code> | <code>5400000 (0x5265c0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/BOOST</code> | <code>regulator-min-microvolt</code> | <code>["", "I&gt;"]</code> | <code>4700000 (0x47b760)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/DCDC_REG1</code> | <code>regulator-init-microvolt</code> | <code>1150000 (0x118c30)</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/regulators/DCDC_REG2</code> | <code>regulator-init-microvolt</code> | <code>1250000 (0x1312d0)</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/regulators/DCDC_REG4</code> | <code>regulator-max-microvolt</code> | <code>3000000 (0x2dc6c0)</code> | <code>3300000 (0x325aa0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/DCDC_REG4</code> | <code>regulator-min-microvolt</code> | <code>3000000 (0x2dc6c0)</code> | <code>3300000 (0x325aa0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/DCDC_REG4</code> | <code>regulator-name</code> | <code>["vcc_3v0"]</code> | <code>["vcc_3v3"]</code> |
| <code>/i2c@ff180000/pmic@20/regulators/DCDC_REG4/regulator-state-mem</code> | <code>regulator-suspend-microvolt</code> | <code>3000000 (0x2dc6c0)</code> | <code>3300000 (0x325aa0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG1/regulator-state-mem</code> | <code>regulator-off-in-suspend</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG1/regulator-state-mem</code> | <code>regulator-on-in-suspend</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG4</code> | <code>regulator-name</code> | <code>["vcc3v0_pmu"]</code> | <code>["vcc3v3_pmu"]</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG7</code> | <code>regulator-min-microvolt</code> | <code>1800000 (0x1b7740)</code> | <code>3300000 (0x325aa0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG7/regulator-state-mem</code> | <code>regulator-off-in-suspend</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG7/regulator-state-mem</code> | <code>regulator-on-in-suspend</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG8</code> | <code>regulator-name</code> | <code>["vcc1v8_dvp"]</code> | <code>["vcc_lcd"]</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG8/regulator-state-mem</code> | <code>regulator-off-in-suspend</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG8/regulator-state-mem</code> | <code>regulator-on-in-suspend</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG9</code> | <code>regulator-max-microvolt</code> | <code>1500000 (0x16e360)</code> | <code>1100000 (0x10c8e0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG9</code> | <code>regulator-min-microvolt</code> | <code>1500000 (0x16e360)</code> | <code>1100000 (0x10c8e0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG9</code> | <code>regulator-name</code> | <code>["vdd1v5_dvp"]</code> | <code>["vdd_11"]</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG9/regulator-state-mem</code> | <code>regulator-off-in-suspend</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG9/regulator-state-mem</code> | <code>regulator-on-in-suspend</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/i2c@ff180000/pmic@20/regulators/LDO_REG9/regulator-state-mem</code> | <code>regulator-suspend-microvolt</code> | <code>1500000 (0x16e360)</code> | <code>1100000 (0x10c8e0)</code> |
| <code>/i2c@ff180000/pmic@20/regulators/OTG_SWITCH</code> | <code>regulator-boot-on</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/i2c@ff190000</code> | <code>compatible</code> | <code>["rockchip,px30-i2c", "rockchip,rk3399-i2c"]</code> | <code>["rockchip,rk3399-i2c"]</code> |
| <code>/i2c@ff190000</code> | <code>i2c-scl-falling-time-ns</code> | <code>16 (0x10)</code> | <code>不存在</code> |
| <code>/i2c@ff190000</code> | <code>i2c-scl-rising-time-ns</code> | <code>275 (0x113)</code> | <code>不存在</code> |
| <code>/i2c@ff1a0000</code> | <code>clock-frequency</code> | <code>400000 (0x61a80)</code> | <code>不存在</code> |
| <code>/i2c@ff1a0000</code> | <code>compatible</code> | <code>["rockchip,px30-i2c", "rockchip,rk3399-i2c"]</code> | <code>["rockchip,rk3399-i2c"]</code> |
| <code>/i2c@ff1a0000</code> | <code>i2c-scl-falling-time-ns</code> | <code>50 (0x32)</code> | <code>不存在</code> |
| <code>/i2c@ff1a0000</code> | <code>i2c-scl-rising-time-ns</code> | <code>300 (0x12c)</code> | <code>不存在</code> |
| <code>/i2c@ff1a0000</code> | <code>pinctrl-0</code> | <code>&amp;{/pinctrl/i2c2/i2c2-xfer}; &amp;{/pinctrl/cif-m0/cif-clkout-m0}</code> | <code>&amp;{/pinctrl/i2c2/i2c2-xfer}</code> |
| <code>/i2c@ff1b0000</code> | <code>compatible</code> | <code>["rockchip,px30-i2c", "rockchip,rk3399-i2c"]</code> | <code>["rockchip,rk3399-i2c"]</code> |
| <code>/i2s@ff070000</code> | <code>reset-names</code> | <code>不存在</code> | <code>["reset-m", "reset-h"]</code> |
| <code>/i2s@ff070000</code> | <code>resets</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [134]; &amp;{/clock-controller@ff2b0000} 参数 [133]</code> |
| <code>/i2s@ff080000</code> | <code>#sound-dai-cells</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/i2s@ff080000</code> | <code>reset-names</code> | <code>不存在</code> | <code>["reset-m", "reset-h"]</code> |
| <code>/i2s@ff080000</code> | <code>resets</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [136]; &amp;{/clock-controller@ff2b0000} 参数 [135]</code> |
| <code>/iommu@ff440440</code> | <code>clock-names</code> | <code>["aclk", "iface"]</code> | <code>["aclk", "hclk"]</code> |
| <code>/iommu@ff440440</code> | <code>rockchip,shootdown-entire</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/iommu@ff440440</code> | <code>status</code> | <code>["okay"]</code> | <code>不存在</code> |
| <code>/iommu@ff442800</code> | <code>clock-names</code> | <code>["aclk", "iface"]</code> | <code>["aclk", "hclk"]</code> |
| <code>/iommu@ff442800</code> | <code>rockchip,shootdown-entire</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/iommu@ff442800</code> | <code>status</code> | <code>["okay"]</code> | <code>不存在</code> |
| <code>/iommu@ff460f00</code> | <code>clock-names</code> | <code>["aclk", "iface"]</code> | <code>["aclk", "hclk"]</code> |
| <code>/iommu@ff460f00</code> | <code>rockchip,disable-device-link-resume</code> | <code>存在（布尔属性）</code> | <code>不存在</code> |
| <code>/iommu@ff490800</code> | <code>clock-names</code> | <code>["aclk", "iface"]</code> | <code>["aclk", "hclk"]</code> |
| <code>/iommu@ff490800</code> | <code>status</code> | <code>["disabled"]</code> | <code>["okay"]</code> |
| <code>/iommu@ff4a8000</code> | <code>clock-names</code> | <code>["aclk", "iface"]</code> | <code>["aclk", "hclk"]</code> |
| <code>/mipi-dphy-rx0@ff2f0000</code> | <code>status</code> | <code>["disabled"]</code> | <code>["okay"]</code> |
| <code>/nandc@ff3b0000</code> | <code>status</code> | <code>["okay"]</code> | <code>["disabled"]</code> |
| <code>/nvmem@ff290000</code> | <code>clock-names</code> | <code>["otp", "apb_pclk", "phy"]</code> | <code>["clk_otp", "pclk_otp", "pclk_otp_phy"]</code> |
| <code>/nvmem@ff290000</code> | <code>reset-names</code> | <code>["phy"]</code> | <code>["otp_phy"]</code> |
| <code>/phy@ff2e0000</code> | <code>#clock-cells</code> | <code>不存在</code> | <code>0 (0x0)</code> |
| <code>/phy@ff2e0000</code> | <code>clock-names</code> | <code>["ref", "pclk", "pclk_host"]</code> | <code>["ref", "pclk_phy", "pclk_host"]</code> |
| <code>/phy@ff2e0000</code> | <code>compatible</code> | <code>["rockchip,px30-dsi-dphy", "rockchip,px30-video-phy"]</code> | <code>["rockchip,px30-video-phy"]</code> |
| <code>/phy@ff2e0000</code> | <code>reg-names</code> | <code>["phy", "host"]</code> | <code>不存在</code> |
| <code>/phy@ff2e0000</code> | <code>reset-names</code> | <code>["apb"]</code> | <code>["rst"]</code> |
| <code>/pinctrl/cif-m1/d10-d11-m1</code> | <code>rockchip,pins</code> | <code>GPIO3_22 function=3 config=&amp;{/pinctrl/pcfg-pull-none}; GPIO3_23 function=3 config=&amp;{/pinctrl/pcfg-pull-none}</code> | <code>GPIO3_23 function=3 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/emmc/emmc-bus1</code> | <code>rockchip,pins</code> | <code>GPIO1_0 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}</code> | <code>GPIO1_0 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}</code> |
| <code>/pinctrl/emmc/emmc-bus4</code> | <code>rockchip,pins</code> | <code>GPIO1_0 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_1 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_2 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_3 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}</code> | <code>GPIO1_0 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_1 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_2 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_3 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}</code> |
| <code>/pinctrl/emmc/emmc-bus8</code> | <code>rockchip,pins</code> | <code>GPIO1_0 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_1 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_2 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_3 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_4 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_5 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_6 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}; GPIO1_7 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}</code> | <code>GPIO1_0 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_1 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_2 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_3 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_4 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_5 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_6 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}; GPIO1_7 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}</code> |
| <code>/pinctrl/emmc/emmc-clk</code> | <code>rockchip,pins</code> | <code>GPIO1_9 function=2 config=&amp;{/pinctrl/pcfg-pull-none-8-6ma}</code> | <code>GPIO1_9 function=2 config=&amp;{/pinctrl/pcfg-pull-none-8ma}</code> |
| <code>/pinctrl/emmc/emmc-cmd</code> | <code>rockchip,pins</code> | <code>GPIO1_10 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8-6ma}</code> | <code>GPIO1_10 function=2 config=&amp;{/pinctrl/pcfg-pull-up-8ma}</code> |
| <code>/pinctrl/headphone/hp-det</code> | <code>rockchip,pins</code> | <code>GPIO2_22 function=0 config=&amp;{/pinctrl/pcfg-pull-up}</code> | <code>GPIO2_22 function=0 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s0/i2s0-8ch-lrckrx</code> | <code>rockchip,pins</code> | <code>GPIO3_13 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_13 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s0/i2s0-8ch-lrcktx</code> | <code>rockchip,pins</code> | <code>GPIO3_18 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_18 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s0/i2s0-8ch-mclk</code> | <code>rockchip,pins</code> | <code>GPIO3_17 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_17 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s0/i2s0-8ch-sclkrx</code> | <code>rockchip,pins</code> | <code>GPIO3_12 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_12 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s0/i2s0-8ch-sclktx</code> | <code>rockchip,pins</code> | <code>GPIO3_19 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_19 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s1/i2s1-2ch-lrck</code> | <code>rockchip,pins</code> | <code>GPIO2_17 function=1 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO2_17 function=1 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s1/i2s1-2ch-mclk</code> | <code>rockchip,pins</code> | <code>GPIO2_19 function=1 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO2_19 function=1 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s1/i2s1-2ch-sclk</code> | <code>rockchip,pins</code> | <code>GPIO2_18 function=1 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO2_18 function=1 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s2/i2s2-2ch-lrck</code> | <code>rockchip,pins</code> | <code>GPIO3_3 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_3 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s2/i2s2-2ch-mclk</code> | <code>rockchip,pins</code> | <code>GPIO3_1 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_1 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/i2s2/i2s2-2ch-sclk</code> | <code>rockchip,pins</code> | <code>GPIO3_2 function=2 config=&amp;{/pinctrl/pcfg-pull-none-smt}</code> | <code>GPIO3_2 function=2 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pinctrl/pmic/pmic_int</code> | <code>rockchip,pins</code> | <code>GPIO0_10 function=0 config=&amp;{/pinctrl/pcfg-pull-up}</code> | <code>GPIO0_7 function=0 config=&amp;{/pinctrl/pcfg-pull-up}; GPIO3_23 function=0 config=&amp;{/pinctrl/pcfg-pull-none}</code> |
| <code>/pwm@ff200000</code> | <code>status</code> | <code>["disabled"]</code> | <code>["okay"]</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>compatible</code> | <code>["ramoops"]</code> | <code>不存在</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>console-size</code> | <code>524288 (0x80000)</code> | <code>不存在</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>ftrace-size</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>pmsg-size</code> | <code>327680 (0x50000)</code> | <code>不存在</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>record-size</code> | <code>131072 (0x20000)</code> | <code>不存在</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>reg-names</code> | <code>不存在</code> | <code>["ramoops_mem"]</code> |
| <code>/rk817-sound</code> | <code>compatible</code> | <code>["rockchip,multicodecs-card"]</code> | <code>["simple-audio-card"]</code> |
| <code>/rk817-sound</code> | <code>hp-det-gpio</code> | <code>&amp;{/pinctrl/gpio2@ff260000} 参数 [22, 0]</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>io-channel-names</code> | <code>["adc-detect"]</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>io-channels</code> | <code>&amp;{/saradc@ff288000} 参数 [1]</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>keyup-threshold-microvolt</code> | <code>1800000 (0x1b7740)</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>pinctrl-0</code> | <code>&amp;{/pinctrl/headphone/hp-det}</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>pinctrl-names</code> | <code>["default"]</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>poll-interval</code> | <code>100 (0x64)</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>rockchip,card-name</code> | <code>["rockchip-rk817"]</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>rockchip,codec</code> | <code>&amp;{/i2c@ff180000/pmic@20/codec}</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>rockchip,cpu</code> | <code>&amp;{/i2s@ff070000}</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>rockchip,format</code> | <code>["i2s"]</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>rockchip,mclk-fs</code> | <code>256 (0x100)</code> | <code>不存在</code> |
| <code>/rk817-sound</code> | <code>simple-audio-card,format</code> | <code>不存在</code> | <code>["i2s"]</code> |
| <code>/rk817-sound</code> | <code>simple-audio-card,mclk-fs</code> | <code>不存在</code> | <code>256 (0x100)</code> |
| <code>/rk817-sound</code> | <code>simple-audio-card,name</code> | <code>不存在</code> | <code>["rockchip,rk817-codec"]</code> |
| <code>/rk817-sound</code> | <code>simple-audio-card,routing</code> | <code>不存在</code> | <code>["MIC_IN", "Mic Jack", "Headphone Jack", "HPOL", "Headphone Jack", "HPOR"]</code> |
| <code>/rk817-sound</code> | <code>simple-audio-card,widgets</code> | <code>不存在</code> | <code>["Microphone", "Mic Jack", "Headphone", "Headphone Jack"]</code> |
| <code>/rk817-sound</code> | <code>spk-con-gpio</code> | <code>&amp;{/pinctrl/gpio3@ff270000} 参数 [7, 0]</code> | <code>不存在</code> |
| <code>/rk_rga@ff480000</code> | <code>dma-coherent</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/rkisp1@ff4a0000</code> | <code>status</code> | <code>["disabled"]</code> | <code>["okay"]</code> |
| <code>/rng@ff0b0000</code> | <code>assigned-clock-rates</code> | <code>[150000000, 150000000, 200000000, 200000000]</code> | <code>[150000000, 150000000, 200000000, 100000000]</code> |
| <code>/rng@ff0b0000</code> | <code>reg</code> | <code>[0, 4278912000, 0, 128]</code> | <code>[0, 4278910976, 0, 16384]</code> |
| <code>/serial@ff158000</code> | <code>pinctrl-0</code> | <code>&amp;{/pinctrl/uart1/uart1-xfer}; &amp;{/pinctrl/uart1/uart1-cts}</code> | <code>不存在</code> |
| <code>/serial@ff158000</code> | <code>status</code> | <code>["okay"]</code> | <code>["disabled"]</code> |
| <code>/spi@ff1d0000</code> | <code>pinctrl-1</code> | <code>不存在</code> | <code>&amp;{/pinctrl/spi0/spi0-clk-hs}; &amp;{/pinctrl/spi0/spi0-csn}; &amp;{/pinctrl/spi0/spi0-miso-hs}; &amp;{/pinctrl/spi0/spi0-mosi-hs}</code> |
| <code>/spi@ff1d0000</code> | <code>pinctrl-names</code> | <code>["default"]</code> | <code>["default", "high_speed"]</code> |
| <code>/spi@ff1d8000</code> | <code>pinctrl-1</code> | <code>不存在</code> | <code>&amp;{/pinctrl/spi1/spi1-clk-hs}; &amp;{/pinctrl/spi1/spi1-csn0}; &amp;{/pinctrl/spi1/spi1-csn1}; &amp;{/pinctrl/spi1/spi1-miso-hs}; &amp;{/pinctrl/spi1/spi1-mosi-hs}</code> |
| <code>/spi@ff1d8000</code> | <code>pinctrl-names</code> | <code>["default"]</code> | <code>["default", "high_speed"]</code> |
| <code>/spi@ff3a0000</code> | <code>assigned-clock-rates</code> | <code>100000000 (0x5f5e100)</code> | <code>10000000 (0x989680)</code> |
| <code>/syscon@ff010000/pmu-pvtm</code> | <code>#address-cells</code> | <code>1 (0x1)</code> | <code>不存在</code> |
| <code>/syscon@ff010000/pmu-pvtm</code> | <code>#size-cells</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/syscon@ff010000/pmu-pvtm</code> | <code>clock-names</code> | <code>不存在</code> | <code>["pmu"]</code> |
| <code>/syscon@ff010000/pmu-pvtm</code> | <code>clocks</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2bc000} 参数 [7]</code> |
| <code>/syscon@ff010000/reboot-mode</code> | <code>mode-charge</code> | <code>不存在</code> | <code>1380107019 (0x5242c30b)</code> |
| <code>/syscon@ff010000/reboot-mode</code> | <code>mode-ums</code> | <code>不存在</code> | <code>1380107020 (0x5242c30c)</code> |
| <code>/syscon@ff140000/io-domains</code> | <code>vccio1-supply</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG7}</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG5}</code> |
| <code>/syscon@ff140000/io-domains</code> | <code>vccio3-supply</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG2}</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/DCDC_REG4}</code> |
| <code>/syscon@ff140000/io-domains</code> | <code>vccio6-supply</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/LDO_REG2}</code> | <code>&amp;{/i2c@ff180000/pmic@20/regulators/DCDC_REG4}</code> |
| <code>/syscon@ff140000/lvds/ports/port@0/endpoint@0</code> | <code>remote-endpoint</code> | <code>&amp;{/vop@ff460000/port/endpoint@1}</code> | <code>&amp;{/vop@ff460000/port/endpoint@0}</code> |
| <code>/syscon@ff148000/pvtm</code> | <code>#address-cells</code> | <code>1 (0x1)</code> | <code>不存在</code> |
| <code>/syscon@ff148000/pvtm</code> | <code>#size-cells</code> | <code>0 (0x0)</code> | <code>不存在</code> |
| <code>/syscon@ff148000/pvtm</code> | <code>clock-names</code> | <code>不存在</code> | <code>["core"]</code> |
| <code>/syscon@ff148000/pvtm</code> | <code>clocks</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [74]</code> |
| <code>/syscon@ff2c0000/usb2-phy@100</code> | <code>compatible</code> | <code>["rockchip,px30-usb2phy"]</code> | <code>["rockchip,px30-usb2phy", "rockchip,rk3328-usb2phy"]</code> |
| <code>/syscon@ff2c0000/usb2-phy@100</code> | <code>reg</code> | <code>[256, 32]</code> | <code>[256, 16]</code> |
| <code>/syscon@ff2c0000/usb2-phy@100/otg-port</code> | <code>status</code> | <code>["okay"]</code> | <code>["disabled"]</code> |
| <code>/timer@ff210000</code> | <code>compatible</code> | <code>["rockchip,px30-timer", "rockchip,rk3288-timer"]</code> | <code>["rockchip,rk3288-timer"]</code> |
| <code>/tsadc@ff280000</code> | <code>pinctrl-2</code> | <code>&amp;{/pinctrl/tsadc/tsadc-otp-pin}</code> | <code>不存在</code> |
| <code>/usb@ff300000</code> | <code>g-use-dma</code> | <code>不存在</code> | <code>存在（布尔属性）</code> |
| <code>/vccsys</code> | <code>regulator-max-microvolt</code> | <code>5000000 (0x4c4b40)</code> | <code>3800000 (0x39fbc0)</code> |
| <code>/vccsys</code> | <code>regulator-min-microvolt</code> | <code>5000000 (0x4c4b40)</code> | <code>3800000 (0x39fbc0)</code> |
| <code>/vccsys</code> | <code>regulator-name</code> | <code>["vcc5v0_sys"]</code> | <code>["vcc3v8_sys"]</code> |
| <code>/vop@ff460000</code> | <code>reset-names</code> | <code>["axi", "ahb", "dclk"]</code> | <code>不存在</code> |
| <code>/vop@ff460000</code> | <code>resets</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [51]; &amp;{/clock-controller@ff2b0000} 参数 [52]; &amp;{/clock-controller@ff2b0000} 参数 [53]</code> | <code>不存在</code> |
| <code>/vop@ff460000/port/endpoint@0</code> | <code>remote-endpoint</code> | <code>&amp;{/dsi@ff450000/ports/port@0/endpoint@0}</code> | <code>&amp;{/syscon@ff140000/lvds/ports/port@0/endpoint@0}</code> |
| <code>/vop@ff460000/port/endpoint@1</code> | <code>remote-endpoint</code> | <code>&amp;{/syscon@ff140000/lvds/ports/port@0/endpoint@0}</code> | <code>&amp;{/dsi@ff450000/ports/port@0/endpoint@0}</code> |
| <code>/watchdog@ff1e0000</code> | <code>reset-names</code> | <code>不存在</code> | <code>["reset"]</code> |
| <code>/watchdog@ff1e0000</code> | <code>resets</code> | <code>不存在</code> | <code>&amp;{/clock-controller@ff2b0000} 参数 [181]</code> |

## 屏幕命令变化

命令序号从 1 开始，相同命令不重复展示。

| 属性 | 参考序号 | 参考命令 | Panel 6 序号 | Panel 6 命令 |
| --- | --- | --- | --- | --- |
| <code>panel-init-sequence</code> | <code>150</code> | <code>type=0x05, delay=200 ms, data=[11]</code> | <code>150</code> | <code>type=0x15, delay=200 ms, data=[11 00]</code> |
| <code>panel-init-sequence</code> | <code>151</code> | <code>type=0x05, delay=100 ms, data=[29]</code> | <code>151</code> | <code>type=0x15, delay=100 ms, data=[29 00]</code> |
| <code>panel-exit-sequence</code> | <code>1</code> | <code>type=0x05, delay=0 ms, data=[28]</code> | <code>1</code> | <code>type=0x05, delay=20 ms, data=[28]</code> |
| <code>panel-exit-sequence</code> | <code>2</code> | <code>type=0x05, delay=0 ms, data=[10]</code> | <code>2</code> | <code>type=0x05, delay=10 ms, data=[10]</code> |

## 独有子树

下列结构并非 phandle 编号差异，不能直接删掉。节点未能建立可靠的一对一对应关系时保留为独有子树，不强行合并。某侧节点只写 disabled 也不代表其参数可忽略。

| 所属 | 子树根路径 | 节点数 | 属性数 | 根节点信息 |
| --- | --- | --- | --- | --- |
| <code>仅参考</code> | <code>/adc-keys</code> | <code>3</code> | <code>12</code> | <code>compatible=["adc-keys"]</code> |
| <code>仅参考</code> | <code>/charge-animation</code> | <code>1</code> | <code>8</code> | <code>compatible=["rockchip,uboot-charge"]; status=["okay"]</code> |
| <code>仅参考</code> | <code>/cif-new@ff490000/port</code> | <code>2</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/cpu0-opp-table/opp-1104000000</code> | <code>1</code> | <code>7</code> | <code></code> |
| <code>仅参考</code> | <code>/cpu0-opp-table/opp-1416000000</code> | <code>1</code> | <code>8</code> | <code>status=["disabled"]</code> |
| <code>仅参考</code> | <code>/cpu0-opp-table/opp-1512000000</code> | <code>1</code> | <code>8</code> | <code>status=["disabled"]</code> |
| <code>仅参考</code> | <code>/cpu0-opp-table/opp-408000000</code> | <code>1</code> | <code>8</code> | <code></code> |
| <code>仅参考</code> | <code>/cpu0-opp-table/opp-600000000</code> | <code>1</code> | <code>7</code> | <code></code> |
| <code>仅参考</code> | <code>/cpu0-opp-table/opp-816000000</code> | <code>1</code> | <code>7</code> | <code></code> |
| <code>仅参考</code> | <code>/ddr3-params</code> | <code>1</code> | <code>49</code> | <code></code> |
| <code>仅参考</code> | <code>/ddr4-params</code> | <code>1</code> | <code>49</code> | <code></code> |
| <code>仅参考</code> | <code>/dmc-fsp</code> | <code>1</code> | <code>10</code> | <code>compatible=["rockchip,px30s-dmc-fsp"]; status=["okay"]</code> |
| <code>仅参考</code> | <code>/dmc-opp-table/opp-194000000</code> | <code>1</code> | <code>6</code> | <code></code> |
| <code>仅参考</code> | <code>/dmc-opp-table/opp-328000000</code> | <code>1</code> | <code>6</code> | <code></code> |
| <code>仅参考</code> | <code>/dmc-opp-table/opp-450000000</code> | <code>1</code> | <code>6</code> | <code></code> |
| <code>仅参考</code> | <code>/dmcdbg</code> | <code>1</code> | <code>2</code> | <code>compatible=["rockchip,px30-dmcdbg"]; status=["okay"]</code> |
| <code>仅参考</code> | <code>/dsi@ff450000/panel@0/ports</code> | <code>3</code> | <code>4</code> | <code></code> |
| <code>仅参考</code> | <code>/dsi@ff450000/ports/port@1</code> | <code>2</code> | <code>2</code> | <code>reg=1 (0x1)</code> |
| <code>仅参考</code> | <code>/firmware/scmi</code> | <code>2</code> | <code>7</code> | <code>compatible=["arm,scmi-smc"]</code> |
| <code>仅参考</code> | <code>/firmware/sdei</code> | <code>1</code> | <code>2</code> | <code>compatible=["arm,sdei-1.0"]</code> |
| <code>仅参考</code> | <code>/gpu-opp-table/opp-200000000</code> | <code>1</code> | <code>6</code> | <code></code> |
| <code>仅参考</code> | <code>/gpu-opp-table/opp-300000000</code> | <code>1</code> | <code>6</code> | <code></code> |
| <code>仅参考</code> | <code>/i2c@ff190000/fb_keros@1c</code> | <code>1</code> | <code>4</code> | <code>compatible=["keros,lite"]; reg=28 (0x1c); status=["okay"]</code> |
| <code>仅参考</code> | <code>/i2c@ff190000/sensor@4c</code> | <code>1</code> | <code>9</code> | <code>compatible=["gs_mma7660"]; reg=76 (0x4c); status=["disabled"]</code> |
| <code>仅参考</code> | <code>/i2c@ff190000/sensor@f</code> | <code>1</code> | <code>8</code> | <code>compatible=["ak8963"]; reg=15 (0xf); status=["disabled"]</code> |
| <code>仅参考</code> | <code>/i2c@ff190000/ts@40</code> | <code>1</code> | <code>7</code> | <code>compatible=["gslX680-d708"]; reg=64 (0x40); status=["okay"]</code> |
| <code>仅参考</code> | <code>/i2c@ff1a0000/gc2155@3c</code> | <code>3</code> | <code>11</code> | <code>compatible=["gc,gc2155"]; reg=60 (0x3c)</code> |
| <code>仅参考</code> | <code>/i2c@ff1a0000/ov5695@36</code> | <code>3</code> | <code>14</code> | <code>compatible=["ovti,ov5695"]; reg=54 (0x36)</code> |
| <code>仅参考</code> | <code>/lpddr2-params</code> | <code>1</code> | <code>49</code> | <code></code> |
| <code>仅参考</code> | <code>/lpddr3-params</code> | <code>1</code> | <code>49</code> | <code></code> |
| <code>仅参考</code> | <code>/lpddr4-params</code> | <code>1</code> | <code>66</code> | <code></code> |
| <code>仅参考</code> | <code>/mipi-dphy-rx0@ff2f0000/ports</code> | <code>5</code> | <code>13</code> | <code></code> |
| <code>仅参考</code> | <code>/mpp-srv</code> | <code>1</code> | <code>8</code> | <code>compatible=["rockchip,mpp-service"]; status=["okay"]</code> |
| <code>仅参考</code> | <code>/pinctrl/buttons</code> | <code>2</code> | <code>1</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/cif-pin-m0</code> | <code>2</code> | <code>1</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/led</code> | <code>2</code> | <code>1</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-0-6ma</code> | <code>1</code> | <code>2</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-12-4ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-12-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-4-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-8-4ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-8-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-down-n-4ma</code> | <code>1</code> | <code>2</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-0-6ma</code> | <code>1</code> | <code>2</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-12-4ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-12-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-4-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-8-4ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-8-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-none-n-4ma</code> | <code>1</code> | <code>2</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-0-6ma</code> | <code>1</code> | <code>2</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-12-4ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-12-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-4-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-8-4ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-8-6ma</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pcfg-pull-up-n-4ma</code> | <code>1</code> | <code>2</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pdm/pdm-clk0m0</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/pdm/pdm-clk0m0-sleep</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅参考</code> | <code>/pinctrl/sdio-pwrseq</code> | <code>2</code> | <code>1</code> | <code></code> |
| <code>仅参考</code> | <code>/play_joystick</code> | <code>5</code> | <code>30</code> | <code>compatible=["play_joystick"]</code> |
| <code>仅参考</code> | <code>/px30s-cpu0-opp-table</code> | <code>10</code> | <code>74</code> | <code>compatible=["operating-points-v2"]</code> |
| <code>仅参考</code> | <code>/px30s-dmc-opp-table</code> | <code>7</code> | <code>17</code> | <code>compatible=["operating-points-v2"]</code> |
| <code>仅参考</code> | <code>/px30s-gpu-opp-table</code> | <code>5</code> | <code>16</code> | <code>compatible=["operating-points-v2"]</code> |
| <code>仅参考</code> | <code>/rk817-sound/play-pause-key</code> | <code>1</code> | <code>3</code> | <code></code> |
| <code>仅参考</code> | <code>/rkisp1@ff4a0000/port</code> | <code>2</code> | <code>4</code> | <code></code> |
| <code>仅参考</code> | <code>/scmi-shmem@10f000</code> | <code>1</code> | <code>2</code> | <code>compatible=["arm,scmi-shmem"]; reg=[0, 1110016, 0, 256]</code> |
| <code>仅参考</code> | <code>/sdio-pwrseq</code> | <code>1</code> | <code>1</code> | <code>compatible=["mmc-pwrseq-simple"]</code> |
| <code>仅参考</code> | <code>/seekwcn_boot</code> | <code>1</code> | <code>6</code> | <code>compatible=["seekwave,sv6160"]; status=["disabled"]</code> |
| <code>仅参考</code> | <code>/syscon@ff010000/pmu-pvtm/pvtm@1</code> | <code>1</code> | <code>3</code> | <code>reg=1 (0x1)</code> |
| <code>仅参考</code> | <code>/syscon@ff148000/pvtm/pvtm@0</code> | <code>1</code> | <code>3</code> | <code>reg=0 (0x0)</code> |
| <code>仅参考</code> | <code>/vcc18-lcd-n</code> | <code>2</code> | <code>6</code> | <code>compatible=["regulator-fixed"]</code> |
| <code>仅参考</code> | <code>/vdpu@ff442400</code> | <code>1</code> | <code>14</code> | <code>compatible=["rockchip,vpu-decoder-px30"]; reg=[0, 4282655744, 0, 1024]; status=["okay"]</code> |
| <code>仅参考</code> | <code>/vepu@ff442000</code> | <code>1</code> | <code>14</code> | <code>compatible=["rockchip,vpu-encoder-px30"]; reg=[0, 4282654720, 0, 1024]; status=["okay"]</code> |
| <code>仅参考</code> | <code>/wireless-bluetooth</code> | <code>1</code> | <code>9</code> | <code>compatible=["bluetooth-platdata"]; status=["disabled"]</code> |
| <code>仅 Panel 6</code> | <code>/chosen</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/cpu-boost@ff2b8000</code> | <code>1</code> | <code>12</code> | <code>compatible=["syscon"]; reg=[0, 4281040896, 0, 4096]</code> |
| <code>仅 Panel 6</code> | <code>/dsi@ff450000/panel@0/display-timings/50Hz</code> | <code>1</code> | <code>13</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/dsi@ff450000/panel@0/display-timings/75Hz</code> | <code>1</code> | <code>13</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/gpio_leds</code> | <code>2</code> | <code>7</code> | <code>compatible=["gpio-leds"]; status=["disabled"]</code> |
| <code>仅 Panel 6</code> | <code>/odroidgo3-joypad</code> | <code>18</code> | <code>84</code> | <code>compatible=["odroidgo3-joypad"]; status=["okay"]</code> |
| <code>仅 Panel 6</code> | <code>/odroidgo3-keys</code> | <code>3</code> | <code>10</code> | <code>compatible=["gpio-keys"]</code> |
| <code>仅 Panel 6</code> | <code>/pdm@ff0a0000</code> | <code>1</code> | <code>11</code> | <code>compatible=["rockchip,px30-pdm", "rockchip,pdm"]; reg=[0, 4278845440, 0, 4096]; status=["disabled"]</code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/btns</code> | <code>2</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/leds</code> | <code>2</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/sdio/sdio-gpio</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/sdmmc/sdmmc-gpio</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/uart0/uart0-rts-gpio</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/uart3-m0/uart3m0-rts-gpio</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/pinctrl/uart3-m1/uart3m1-rts-gpio</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/ramoops</code> | <code>1</code> | <code>6</code> | <code>compatible=["ramoops"]</code> |
| <code>仅 Panel 6</code> | <code>/rk817-sound/simple-audio-card,codec</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/rk817-sound/simple-audio-card,cpu</code> | <code>1</code> | <code>1</code> | <code></code> |
| <code>仅 Panel 6</code> | <code>/rk_headset</code> | <code>1</code> | <code>4</code> | <code>compatible=["rockchip_headset"]</code> |
| <code>仅 Panel 6</code> | <code>/vpu_combo</code> | <code>1</code> | <code>12</code> | <code>compatible=["rockchip,vpu_combo"]; status=["okay"]</code> |
| <code>仅 Panel 6</code> | <code>/vpu_service@ff442000</code> | <code>1</code> | <code>8</code> | <code>compatible=["rockchip,vpu_sub"]; reg=[0, 4282654720, 0, 2048]</code> |

## 节点对齐依据

完整列表另见 [node-alignment.csv](node-alignment.csv)。这里只列名称/路径不同的匹配。

| 参考统一路径 | Panel 6 原路径 | 依据 |
| --- | --- | --- |
| <code>/bus</code> | <code>/amba</code> | <code>已对齐父节点下唯一相同 compatible；全部参数差异保留</code> |
| <code>/bus/dmac@ff240000</code> | <code>/amba/dmac@ff240000</code> | <code>共同符号 dmac；所有驱动/参数差异仍保留</code> |
| <code>/clock-controller@ff2bc000</code> | <code>/pmu-clock-controller@ff2bc000</code> | <code>共同符号 pmucru；所有驱动/参数差异仍保留</code> |
| <code>/dsi@ff450000/panel@0/display-timings/timing0</code> | <code>/dsi@ff450000/panel@0/display-timings/60Hz</code> | <code>共同符号 timing0；所有驱动/参数差异仍保留</code> |
| <code>/hevc@ff440000</code> | <code>/hevc_service@ff440000</code> | <code>共同符号 hevc；所有驱动/参数差异仍保留</code> |
| <code>/nvmem@ff290000</code> | <code>/otp@ff290000</code> | <code>共同符号 otp；所有驱动/参数差异仍保留</code> |
| <code>/nvmem@ff290000/cpu-leakage@17</code> | <code>/otp@ff290000/cpu-leakage@17</code> | <code>共同符号 cpu_leakage；所有驱动/参数差异仍保留</code> |
| <code>/nvmem@ff290000/id@7</code> | <code>/otp@ff290000/id@7</code> | <code>已对齐父节点下的相同子节点名</code> |
| <code>/nvmem@ff290000/performance@1e</code> | <code>/otp@ff290000/performance@1e</code> | <code>共同符号 performance；所有驱动/参数差异仍保留</code> |
| <code>/phy@ff2e0000</code> | <code>/video-phy@ff2e0000</code> | <code>共同符号 video_phy；所有驱动/参数差异仍保留</code> |
| <code>/pinctrl/tsadc/tsadc-otp-pin</code> | <code>/pinctrl/tsadc/tsadc-otp-gpio</code> | <code>共同符号 tsadc_otp_gpio；所有驱动/参数差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@10</code> | <code>/power-management@ff000000/power-controller/pd_mmc_nand@10</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@11</code> | <code>/power-management@ff000000/power-controller/pd_vpu@11</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@12</code> | <code>/power-management@ff000000/power-controller/pd_vo@12</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@13</code> | <code>/power-management@ff000000/power-controller/pd_vi@13</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@14</code> | <code>/power-management@ff000000/power-controller/pd_gpu@14</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@5</code> | <code>/power-management@ff000000/power-controller/pd_usb@5</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@7</code> | <code>/power-management@ff000000/power-controller/pd_sdcard@7</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/power-management@ff000000/power-controller/power-domain@9</code> | <code>/power-management@ff000000/power-controller/pd_gmac@9</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/reserved-memory/ramoops@110000</code> | <code>/reserved-memory/region@110000</code> | <code>已对齐父节点下唯一相同 reg；compatible 差异仍保留</code> |
| <code>/spi@ff3a0000</code> | <code>/sfc@ff3a0000</code> | <code>共同符号 sfc；所有驱动/参数差异仍保留</code> |
| <code>/timer@ff210000</code> | <code>/rktimer@ff210000</code> | <code>共同符号 rktimer；所有驱动/参数差异仍保留</code> |

## 文件与限制

- [参考原文件副本](rf3536k3ka.original.dts)、[Panel 6 原文件副本](panel6.original.dts)：按原字节复制，可用于正常编译。
- [参考归一化结果](rf3536k3ka.resolved.json)、[Panel 6 归一化结果](panel6.resolved.json)：可读数据视图，引用已变为统一路径；不是可刷机 DTS。
- [全部剩余参数差异 CSV](parameter-differences.csv)：含已对齐节点变化及独有节点参数，UTF-8 BOM，可用 Excel 打开。
- [匹配与解析规则](normalization-rules.json)、[验证与源文件哈希](validation.json)。

两份副本均用 Windows DTC 1.7.2 编译成功；编译存在结构警告。内存保留表相同：True；启动 CPU ID 相同：True。尚未进行实机验证。

解析只针对已列出的引用属性及提供者协议，不根据数值恰好等于某个 phandle 就猜测其为引用。无法证明等价的驱动布局保留为结构差异；主表表示当前规则下可确认的参数变化，不保证覆盖所有厂商私有绑定的运行时语义。

## 功能键与 GPIO 清单

[下载 rf3536k3ka_GPIO功能键清单.xlsx](rf3536k3ka_GPIO功能键清单.xlsx)。数据直接取自 `rf3536k3ka.resolved.dts`，包含 19 路数字按键 GPIO、3 路摇杆相关 GPIO、3 个 ADC 按键、4 个模拟轴、PMIC 电源键及其他 GPIO 用途和复用检查。19 路 `key-gpios` 没有在 DTS 中给出实体键名；表内明确标为需驱动/实机确认，未套用其他机型映射。
