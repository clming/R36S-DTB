#!/usr/bin/env python3
"""Export schematic review workbook from one RK3326 DTS. Python 3.6+, openpyxl."""
import argparse
import collections
import contextlib
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import tempfile

import dt_tools as dt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--output-dir', required=True, type=Path, help='New output directory')
    parser.add_argument('--dtc')
    args = parser.parse_args()
    try:
        from openpyxl import Workbook, load_workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
    except ImportError:
        raise ValueError('Install openpyxl in your Python 3 environment first.')
    source = args.source.resolve()
    out = args.output_dir.resolve()
    if out.exists():
        raise ValueError('Output directory exists; choose a new directory to preserve earlier reports.')
    original = source.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    compiler = dt.compiler(args.dtc)
    with tempfile.TemporaryDirectory(prefix='schematic-gpio-') as temporary:
        work = Path(temporary)
        with (work/'compile.log').open('w', encoding='utf-8') as log, contextlib.redirect_stderr(log):
            t = dt.load_tree(source, compiler, work)
        warnings = (work/'compile.log').read_text(encoding='utf-8')
        version = dt.run_dtc(compiler, ['--version']).decode().strip()
    p, nodes = t['properties'], t['nodes']

    def cells(v):
        if len(v) % 4:
            raise ValueError('Non-cell data in integer/reference property')
        return list(struct.unpack('>%dI' % (len(v)//4), v))

    def num(n, prop, default=None):
        v = p.get((n, prop))
        return cells(v)[0] if v is not None and len(v) == 4 else default

    def strings(n, prop):
        v = p.get((n, prop))
        return v.rstrip(b'\0').decode('utf-8').split('\0') if v else []

    def parent(n):
        return n.rsplit('/', 1)[0] or '/'

    def available(n):
        at = n
        while True:
            status = strings(at, 'status')
            if status and status[0] not in ('okay', 'ok'):
                return False, status[0]+' @ '+at
            if at == '/':
                return True, '可用声明（未实测；省略 status 按可用处理）'
            at = parent(at)

    handles = {}
    for (n, prop), v in p.items():
        if prop in ('phandle', 'linux,phandle'):
            handle = cells(v)[0]
            if handle in handles and handles[handle] != n:
                raise ValueError('Duplicate phandle')
            handles[handle] = n
    lines, stack = {}, []
    for lineno, line in enumerate(original.decode('utf-8-sig').splitlines(), 1):
        m = re.match(r'^\s*([^\s{}]+)\s*\{\s*$', line)
        if m:
            stack.append('' if m.group(1) == '/' else m.group(1))
            lines[('/'.join(stack) or '/', '')] = lineno
        elif re.match(r'^\s*};\s*$', line):
            stack.pop()
        else:
            m = re.match(r'^\s*([^\s=;]+)\s*(?:=|;)', line)
            if m and stack:
                lines[('/'.join(stack) or '/', m.group(1))] = lineno

    def loc(n, prop):
        return source.name+':'+str(lines.get((n, prop), lines.get((n, ''), '?')))+' '+n+' / '+prop

    def pinname(bank, offset):
        if not 0 <= offset < 32:
            raise ValueError('Unexpected GPIO offset')
        return 'GPIO%d_%s%d' % (bank, 'ABCD'[offset//8], offset % 8)

    def bank_of(n):
        m = re.search(r'/gpio(\d+)@', n)
        return int(m.group(1)) if m else None

    def refs(n, prop, count_prop):
        vals, result, i = cells(p[(n, prop)]), [], 0
        while i < len(vals):
            target = handles[vals[i]]
            count = num(target, count_prop)
            if count is None or i+1+count > len(vals):
                raise ValueError('Invalid provider argument count: '+n+' / '+prop)
            result.append((target, vals[i+1:i+1+count]))
            i += 1+count
        return result

    def config(n):
        values = []
        for name, label in [('bias-pull-up', '内部上拉'), ('bias-pull-down', '内部下拉'),
                            ('bias-disable', '内部上下拉禁用'), ('output-high', 'pinctrl 输出高'),
                            ('output-low', 'pinctrl 输出低'), ('input-enable', '输入使能'),
                            ('input-schmitt-enable', '施密特输入')]:
            if (n, name) in p:
                values.append(label)
        strength = num(n, 'drive-strength')
        if strength is not None:
            values.append('驱动强度字段 %d mA（不是外部负载额定电流）' % strength)
        return '；'.join(values) or '未声明通用电气配置'

    groups = {}
    for (n, prop), v in sorted(p.items()):
        if prop != 'rockchip,pins':
            continue
        vals = cells(v)
        if len(vals) % 4:
            raise ValueError('Invalid rockchip,pins: '+n)
        groups[n] = [{'bank': vals[i], 'pin': vals[i+1], 'mux': vals[i+2], 'config': handles[vals[i+3]],
                      'group': n} for i in range(0, len(vals), 4)]
    mux, group_users, non_soc_states = [], collections.defaultdict(list), []
    for (n, prop), v in sorted(p.items()):
        if not re.match(r'^pinctrl-\d+$', prop):
            continue
        index = int(prop[8:])
        names = strings(n, 'pinctrl-names')
        state = names[index] if index < len(names) else '未命名状态%d' % index
        default = state == 'default' or (not names and index == 0)
        for handle in cells(v):
            group = handles[handle]
            group_users[group].append((n, state, default))
            if group in groups:
                for item in groups[group]:
                    row = dict(item)
                    row.update(node=n, prop=prop, state=state, default=default, active=available(n)[0])
                    mux.append(row)
            else:
                non_soc_states.append([n, prop, state, group, ', '.join(strings(group, 'pins')),
                                       ', '.join(strings(group, 'function')), available(n)[1], loc(n, prop)])

    def role(n, prop, kind):
        if kind == 'GPIO IRQ':
            return '输入（中断）', 'PMIC 中断传输线，非电源按键本体' if 'pmic@' in n else '设备中断输入', '绑定含义'
        if n == '/play_joystick' and prop == 'key-gpios':
            return '输入（按键）', '数字按键输入；实体键名/事件码由自定义驱动决定，DTS 未声明', '数组用途明确，实体键名未知'
        if n == '/play_joystick' and prop.startswith('rocker'):
            return '待驱动确认', '摇杆相关控制/输入；不能据属性名确定为 L3/R3 或多路选择', '待确认'
        inputs = {'cd-gpios': '存储卡插入检测', 'hp-det-gpio': '耳机插入检测', 'dc_det_gpio': '外部电源检测',
                  'touch-gpio': '触摸/中断信号', 'irq-gpio': '设备中断信号', 'BT,wake_host_irq': '蓝牙唤醒主机信号',
                  'gpio_host_wake': '无线模块唤醒主机信号'}
        outputs = {'reset-gpios': '设备复位输出', 'pwdn-gpios': '设备掉电/待机控制', 'spk-con-gpio': '扬声器/功放控制',
                   'charge_blue_gpio': '充电蓝色指示', 'charge_red_gpio': '充电红色指示',
                   'work_blue_gpio': '工作蓝色指示', 'work_red_gpio': '工作红色指示', 'chg_led_gpio': '充电指示',
                   'led-gpio': '设备 LED 控制', 'wake-gpio': '设备唤醒控制', 'BT,wake_gpio': '蓝牙唤醒控制',
                   'uart_rts_gpios': 'UART RTS 的 GPIO 控制', 'gpio': '固定稳压器/供电开关使能',
                   'gpio_chip_en': '无线模块使能', 'gpio_chip_wake': '无线模块唤醒控制'}
        if prop in inputs:
            return '输入（按信号用途推断）', inputs[prop], '方向推断，需驱动/原理图核对'
        if prop in outputs:
            return '输出（按信号用途推断）', outputs[prop], '方向推断，需驱动/原理图核对'
        return '待驱动确认', 'USB OTG 相关控制，非实体按键' if prop == 'otg-gpio' else '由节点/属性定义的 GPIO 信号', '待确认'

    def electrical(n, prop, flags, kind):
        if kind == 'GPIO IRQ':
            return {1: 'IRQ 上升沿', 2: 'IRQ 下降沿', 3: 'IRQ 双边沿', 4: 'IRQ 高电平', 8: 'IRQ 低电平'}.get(flags, 'IRQ 标志待确认')
        if prop in ('gpio', 'gpios') and 'regulator-fixed' in strings(n, 'compatible'):
            return ('使能高有效' if (n, 'enable-active-high') in p else '使能低有效（fixed-regulator 缺省规则）')+'；需核对厂商驱动'
        if flags in (0, 1):
            return 'GPIO 高有效' if flags == 0 else 'GPIO 低有效'
        return '原始标志 0x%x；厂商属性/IRQ 标志解释待驱动确认' % flags

    gpio = []
    for (n, prop), v in sorted(p.items()):
        if n == '/__symbols__':
            continue
        if prop not in ('gpio', 'gpios', 'BT,wake_gpio', 'BT,wake_host_irq') and not prop.startswith('gpio_') and not prop.endswith(('-gpio', '-gpios', '_gpio', '_gpios')):
            continue
        for index, (controller, spec) in enumerate(refs(n, prop, '#gpio-cells')):
            bank = bank_of(controller)
            if bank is None:
                raise ValueError('GPIO provider is not a known SoC bank: '+controller)
            direction, purpose, certainty = role(n, prop, 'GPIO')
            gpio.append(dict(bank=bank, pin=spec[0], flags=spec[1], controller=controller, node=n, prop=prop,
                             index=index, kind='GPIO', direction=direction, purpose=purpose, certainty=certainty,
                             active=available(n)[0]))
    for (n, prop), v in sorted(p.items()):
        if prop != 'interrupts':
            continue
        at = n
        while (at, 'interrupt-parent') not in p and at != '/':
            at = parent(at)
        if (at, 'interrupt-parent') not in p:
            continue
        controller = handles[num(at, 'interrupt-parent')]
        bank = bank_of(controller)
        if bank is None:
            continue
        count, vals = num(controller, '#interrupt-cells'), cells(v)
        if not count or len(vals) % count:
            raise ValueError('Malformed GPIO interrupt cells')
        for i in range(0, len(vals), count):
            direction, purpose, certainty = role(n, prop, 'GPIO IRQ')
            gpio.append(dict(bank=bank, pin=vals[i], flags=vals[i+1], controller=controller, node=n, prop=prop,
                             index=i//count, kind='GPIO IRQ', direction=direction, purpose=purpose,
                             certainty=certainty, active=available(n)[0]))

    uses_by_pin, mux_by_pin = collections.defaultdict(list), collections.defaultdict(list)
    for row in gpio:
        uses_by_pin[(row['bank'], row['pin'])].append(row)
    for row in mux:
        mux_by_pin[(row['bank'], row['pin'])].append(row)
    keys = [x for x in gpio if x['node'] == '/play_joystick' and x['prop'] == 'key-gpios']
    if num('/play_joystick', 'gpio-key-num') != len(keys):
        raise ValueError('gpio-key-num and key-gpios array disagree')
    key_pins = {(x['bank'], x['pin']) for x in keys}
    risks = []
    for pin in sorted(set(uses_by_pin) | set(mux_by_pin)):
        active_gpio = [x for x in uses_by_pin[pin] if x['active']]
        active_mux = [x for x in mux_by_pin[pin] if x['active'] and x['default']]
        consumers = sorted(set(x['node'] for x in active_gpio))
        if len(consumers) > 1:
            risks.append(['GPIO 多消费者', pinname(*pin), '\n'.join(consumers), '多节点默认可用声明；可能共用或驱动协调，需确认实际接线', '待硬件+BSP核实'])
        modes = set(x['mux'] for x in active_mux)
        if (active_gpio and any(mode != 0 for mode in modes)) or len(modes) > 1:
            risks.append(['默认复用待核实', pinname(*pin), '\n'.join(sorted(set(x['node']+' '+x['group']+' mux='+str(x['mux']) for x in active_mux))),
                          '存在不同默认 mux 或 GPIO 与外设 mux 声明；不能直接判定都同时生效', '设计冻结前核实'])

    # ADC functions, including keys, axes and all IIO consumers sharing a channel.
    adc, adc_users = [], collections.defaultdict(list)
    for (n, prop), v in sorted(p.items()):
        if prop != 'io-channels':
            continue
        channels = refs(n, prop, '#io-channel-cells')
        names = strings(n, 'io-channel-names')
        for index, (controller, spec) in enumerate(channels):
            adc_users[(controller, tuple(spec))].append(n)
        children = sorted(child for child in nodes if child != '/' and parent(child) == n and (child, 'linux,code') in p)
        for child in children:
            index = num(child, 'adc-chan', 0)
            if index >= len(channels):
                raise ValueError('ADC axis index outside io-channels array')
            controller, spec = channels[index]
            code = num(child, 'linux,code')
            axis = (child, 'adc-chan') in p
            event = ({0: 'ABS_X', 1: 'ABS_Y', 3: 'ABS_RX', 4: 'ABS_RY'} if axis else {114: 'KEY_VOLUMEDOWN', 115: 'KEY_VOLUMEUP', 164: 'KEY_PLAYPAUSE'}).get(code, '需驱动确认')
            adc.append(['摇杆模拟轴' if axis else 'ADC 按键', ', '.join(strings(child, 'label')), controller,
                        ','.join(map(str, spec)), names[index] if index < len(names) else '', code, event,
                        num(child, 'press-threshold-microvolt'), num(n, 'keyup-threshold-microvolt'), available(child)[1],
                        '非独立 GPIO；封装模拟脚、电压范围/电阻或电位器参数需硬件资料确认', loc(child, 'linux,code')])
        if not children:
            for index, (controller, spec) in enumerate(channels):
                adc.append(['其他 ADC 消费', n, controller, ','.join(map(str, spec)), names[index] if index < len(names) else '', '', '', '', '',
                            available(n)[1], 'ADC 通道用途按节点；不代表专用数字 GPIO', loc(n, prop)])
    for (controller, spec), consumers in sorted(adc_users.items()):
        active = sorted(set(n for n in consumers if available(n)[0]))
        if len(active) > 1:
            risks.append(['ADC 通道共享声明', controller+' channel '+str(spec), '\n'.join(active), '同通道被多功能声明，须核对电路是否共用及驱动是否屏蔽/协调', '设计冻结前核实'])

    regs = {n for n in nodes if (n, 'regulator-name') in p}
    supply_rows = []
    for n in sorted(regs):
        upstream = [(prop, handles[cells(v)[0]]) for (at, prop), v in p.items() if at == n and prop.endswith('-supply') and len(v) == 4]
        consumers = [at+' / '+prop for (at, prop), v in p.items() if prop.endswith('-supply') and len(v) == 4 and handles.get(cells(v)[0]) == n]
        enable = [pinname(x['bank'], x['pin'])+' '+electrical(n, x['prop'], x['flags'], x['kind']) for x in gpio if x['node'] == n]
        suspend = n+'/regulator-state-mem'
        supply_rows.append([', '.join(strings(n, 'regulator-name')), n, num(n, 'regulator-min-microvolt'), num(n, 'regulator-max-microvolt'),
                            num(n, 'regulator-init-microvolt'), str((n, 'regulator-always-on') in p), str((n, 'regulator-boot-on') in p),
                            '; '.join(a+'='+b for a, b in upstream), '; '.join(enable),
                            '; '.join(prop+'='+('布尔属性' if not v else str(cells(v))) for (at, prop), v in p.items() if at == suspend),
                            '\n'.join(consumers), available(n)[1], '配置值不替代电源预算/时序及器件规格', loc(n, 'regulator-name')])
    io_rows = []
    for n in sorted(nodes):
        compatible = ' '.join(strings(n, 'compatible'))
        if 'io-voltage-domain' not in compatible:
            continue
        for (at, prop), v in sorted(p.items()):
            if at != n or not prop.endswith('-supply'):
                continue
            target = handles[cells(v)[0]]
            io_rows.append([n, prop, target, ', '.join(strings(target, 'regulator-name')), num(target, 'regulator-min-microvolt'),
                            num(target, 'regulator-max-microvolt'), available(n)[1],
                            'Bank/PAD 到 VCCIO 的映射及是否可切换，须对应 SoC 后缀与封装资料；不能假定全为 3.3V', loc(n, prop)])

    wb = Workbook()
    wb.remove(wb.active)
    sheet_counts = {}

    def sheet(name, headers, rows, widths):
        ws = wb.create_sheet(name)
        ws.append(headers)
        for row in rows:
            ws.append(row)
        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = ws.dimensions
        ws.sheet_view.zoomScale = 80
        ws.row_dimensions[1].height = 34
        for cell in ws[1]:
            cell.font = Font(name='Microsoft YaHei', bold=True, color='FFFFFF')
            cell.fill = PatternFill('solid', fgColor='17365D')
            cell.alignment = Alignment(wrap_text=True, vertical='center')
        for row in ws.iter_rows(min_row=2):
            for cell in row:
                cell.font = Font(name='Microsoft YaHei', size=10)
                cell.alignment = Alignment(wrap_text=True, vertical='top')
                if row[0].row % 2 == 0:
                    cell.fill = PatternFill('solid', fgColor='EEF3F8')
            ws.row_dimensions[row[0].row].height = 78
        for index, width in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(index)].width = width
        ws.print_title_rows = '1:1'
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.orientation = 'landscape'
        ws.page_setup.paperSize = ws.PAPERSIZE_A3
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        sheet_counts[name] = len(rows)
        return ws

    notes = [
        ['用途', '供核心板原理图设计的 DTS 引脚审查输入表；先完成待核实项，再冻结原理图。'],
        ['唯一板级数据源', str(source)], ['源文件 SHA-256', digest], ['编译工具', version],
        ['GPIO 号含义', 'GPIO3_B3 = bank 3 / offset 11；不是 BGA 封装球位。传统 bank*32+offset 不保证是运行时编号。'],
        ['总表范围', '合并 GPIO 消费属性、GPIO 中断及被 pinctrl 状态引用的引脚；禁用设备与休眠状态分别注明。未引用 pinmux 库定义只放在全部组表中。'],
        ['真实接线与状态', 'DTS 的 okay / 缺省状态只代表软件声明，不能证明器件实际焊接或驱动已绑定。多个节点声明同脚不自动等于运行时冲突。'],
        ['方向', '除按键/IRQ 等明确用途外，方向多按信号名称推断；DTS GPIO flags 表示有效极性，不决定输入/输出。'],
        ['供电使能极性', '固定稳压器 gpio/gpios 应同时读 enable-active-high；缺省按 binding 为低有效，不能只看 GPIO flags=0 就判成高使能。'],
        ['19 路数字键', '有 GPIO 数组顺序，无 A/B/X/Y/方向/Start/Select/FN 到 GPIO 的实体映射；全部标注待驱动或通断实测确认。'],
        ['模拟输入', '音量键、播放暂停键及四摇杆轴由 ADC 声明；电位器阻值、模拟量程、外接电阻/电容和精确封装脚未由此 DTS 给出。'],
        ['SoC 电气与封装', '请硬件同学填入实际芯片完整料号/后缀、封装球位、VCCIO、电平耐受和上电默认态；表内不臆填。'],
        ['内部上下拉与外部器件', 'pinctrl 上下拉仅为软件设置，不等于板上已有上拉电阻，也不保证上电前成立；drive-strength 字段不是负载额定电流。'],
        ['专用信号', 'DDR、DSI、USB、SARADC 模拟脚、PMIC/晶振/电源脚不一定以 GPIO 表示，见接口表；本工作簿不能替代 SoC 全部引脚表。'],
        ['未使用引脚', '本表未出现或 disabled 不等于可自由使用，需检查启动绑带、专用电源/时钟、封装限制及其他固件阶段。'],
        ['表内可编辑列', 'GPIO总表保留网络名、封装脚、连接器脚和硬件签核栏，供硬件负责人补全。'],
        ['验证', 'GPIO / IRQ / pinctrl / ADC / supply phandle 均解析；源 DTS 编译成功，有结构警告记录；未运行硬件。']]
    sheet('交付说明', ['项目', '说明'], notes, [28, 135])
    summary_rows = []
    for pin in sorted(set(uses_by_pin) | set(mux_by_pin)):
        uses, modes = uses_by_pin[pin], mux_by_pin[pin]
        active_uses = [x for x in uses if x['active']]
        defaults = [x for x in modes if x['active'] and x['default']]
        others = [x for x in modes if not (x['active'] and x['default'])]
        review = [x[0]+': '+x[3] for x in risks if x[1] == pinname(*pin)]
        state = '默认可用候选声明' if active_uses or defaults else '仅禁用/非默认状态；不纳入默认接线'
        summary_rows.append([pinname(*pin), pin[0], pin[1], pin[0]*32+pin[1], state,
                             '\n'.join(x['purpose']+' @ '+x['node']+' / '+x['prop'] for x in active_uses),
                             '\n'.join(x['group']+' mux='+str(x['mux'])+' @ '+x['node'] for x in defaults),
                             '\n'.join(x['state']+' '+x['group']+' mux='+str(x['mux'])+' '+available(x['node'])[1] for x in others),
                             '\n'.join(sorted(set(config(x['config']) for x in defaults))), '\n'.join(review) or '未检出；仍需核对芯片资料',
                             '待确认 VCCIO / 电平范围', '待填：精确封装球位', '', '', '待硬件签核'])
    sheet('GPIO接线总表', ['GPIO名称', 'Bank', 'offset', '传统线性号(参考)', '声明分类', '默认可用GPIO用途', '默认可用外设复用',
                        '其他状态或禁用设备', '默认pinctrl电气', '复用审查', 'IO电压域', 'SoC封装脚号', '原理图网络名(填)', '连接器与脚号(填)', '签核状态'],
          summary_rows, [18, 8, 10, 18, 36, 76, 78, 80, 64, 70, 29, 27, 27, 27, 22])
    consumer_rows = []
    for x in gpio:
        configs = [m for m in mux if m['node'] == x['node'] and (m['bank'], m['pin']) == (x['bank'], x['pin'])]
        consumer_rows.append([pinname(x['bank'], x['pin']), x['kind'], x['node'], x['prop'], x['index'], x['direction'], x['purpose'],
                              '0x%x' % x['flags'], electrical(x['node'], x['prop'], x['flags'], x['kind']), available(x['node'])[1], x['certainty'],
                              '\n'.join(m['state']+': '+config(m['config']) for m in configs), loc(x['node'], x['prop'])])
    sheet('GPIO消费明细', ['GPIO名称', '类型', '节点', '属性', '数组索引(0起)', '方向及依据', '用途', '原始flags', '有效极性或触发', '节点状态', '确定程度', '同节点pinctrl配置', '源位置'],
          consumer_rows, [18, 16, 55, 26, 17, 35, 67, 13, 60, 48, 38, 65, 95])
    key_rows = []
    for x in gpio:
        if x['node'] != '/play_joystick' or x['prop'] not in ('key-gpios', 'rocker-gpios', 'rocker0-gpios', 'rocker1-gpios'):
            continue
        config_items = [m for m in mux if m['node'] == x['node'] and m['default'] and m['bank'] == x['bank'] and m['pin'] == x['pin']]
        key_rows.append([x['prop'], x['index'], pinname(x['bank'], x['pin']), x['direction'], electrical(x['node'], x['prop'], x['flags'], x['kind']),
                         '数字键输入，实体键名未知' if x['prop'] == 'key-gpios' else '摇杆相关，具体作用未知', '待确认，不套用 Panel 6 映射',
                         '\n'.join(config(m['config']) for m in config_items) or '当前按键 pinctrl 未给出此脚配置', '', '', loc(x['node'], x['prop'])])
    powerkey = '/i2c@ff180000/pmic@20/pwrkey'
    if powerkey in nodes:
        key_rows.append(['pwrkey', '', '非独立 SoC GPIO 声明', 'PMIC 专用按键通路', '未在 DTS 指定电源键本体电平', 'RK817 电源键子节点；SoC 的 PMIC IRQ 不是按键本体脚',
                         '对照 RK817 型号及 ON/OFF 电路', '', '', '', loc(powerkey, 'status')])
    sheet('功能键与摇杆', ['属性', '索引(0起)', 'GPIO/通路', '方向', '极性', '用途', '实体功能核对', '内部上下拉', '实体键名(填)', '开关网络与接口(填)', '源位置'],
          key_rows, [24, 14, 29, 32, 48, 75, 50, 64, 27, 33, 100])
    sheet('ADC模拟输入', ['类型', '功能/节点', '控制器', '通道', '通道名', '事件码', '事件名', '按下阈值字段(uV)', '抬起阈值字段(uV)', '节点状态', '原理图核对', '源位置'],
          adc, [24, 50, 34, 13, 20, 12, 25, 24, 24, 45, 85, 100])
    mux_rows = [[pinname(x['bank'], x['pin']), x['mux'], x['group'], x['node'], x['prop'], x['state'],
                 '默认候选' if x['default'] else '其他状态', available(x['node'])[1], config(x['config']), x['config'],
                 '复用组内每根 SDA/SCL、TX/RX 等精确信号与封装脚，需查对应芯片 TRM/MUX 表', loc(x['group'], 'rockchip,pins')] for x in mux]
    sheet('已引用Pinmux', ['GPIO名称', 'MUX功能号', '引脚组', '消费者', '状态属性', '状态名', '状态分类', '消费者状态', '电气配置', '配置节点', '核对要求', '源位置'],
          mux_rows, [18, 14, 55, 53, 18, 24, 20, 47, 65, 56, 82, 100])
    all_mux = []
    for n, items in sorted(groups.items()):
        for x in items:
            all_mux.append([pinname(x['bank'], x['pin']), x['mux'], n, config(x['config']),
                            '\n'.join(at+' ['+state+'] '+available(at)[1] for at, state, default in group_users[n]) or '无 pinctrl-N 引用，仅库定义',
                            '库定义/复用能力不等于已接线；未引用不等于 GPIO 可自由使用', loc(n, 'rockchip,pins')])
    sheet('全部Pinmux组', ['GPIO名称', 'MUX号', '引脚组', '电气配置', '消费者与状态', '解释', '源位置'], all_mux, [18, 12, 62, 74, 93, 80, 100])
    sheet('PMIC专用Pinctrl', ['消费者', '状态属性', '状态名', '配置节点', 'PMIC引脚名', '功能', '消费者状态', '源位置'],
          non_soc_states, [55, 18, 23, 69, 30, 30, 48, 100])
    interface_rows = []
    controller_matches = ('i2c@', 'serial@', 'spi@', 'dwmmc@', 'i2s@', 'dsi@', 'saradc@', 'usb@', 'pwm@')
    for n in sorted(nodes):
        if not any(n.rsplit('/', 1)[-1].startswith(prefix) for prefix in controller_matches):
            continue
        pins = [x for x in mux if x['node'] == n]
        interface_rows.append([n, ', '.join(strings(n, 'compatible')), available(n)[1],
                               '\n'.join(pinname(x['bank'], x['pin'])+' mux='+str(x['mux'])+' '+x['group']+' ['+x['state']+']' for x in pins) or '未声明可追踪的 SoC pinctrl 引脚',
                               '\n'.join(child for child in sorted(nodes) if child != '/' and parent(child) == n),
                               '组名可定位接口；组内单脚精确信号及专用脚须查 TRM/封装/外设规格', loc(n, 'compatible')])
    backlight = '/backlight'
    if (backlight, 'pwms') in p:
        for target, spec in refs(backlight, 'pwms', '#pwm-cells'):
            interface_rows.append(['背光 PWM', target, available(backlight)[1], str(spec)+'（通道、周期ns、标志）',
                                   'PWM 引脚见控制器的 pinctrl；LED 电源、电流驱动与屏 FPC 另核', 'PWM 不是直接驱动背光 LED 的额定输出', loc(backlight, 'pwms')])
    for title, desc in [('MIPI DSI 专用差分线', 'DTS panel 的 dsi,lanes=%s；lane 正负与 FPC 物理脚位需屏规格及 SoC 封装表' % num(dt.PANEL, 'dsi,lanes')),
                        ('USB 专用差分线', 'USB D+/D-、VBUS 电源路径/ESD、Type-C CC 等不能由 GPIO 表完整还原'),
                        ('DDR/晶振/电源/启动绑带', '独立核心板必须另行完成 DDR 引脚、料号和初始化匹配、晶振、电源时序与 boot strap；不在此 GPIO 表中臆填')]:
        interface_rows.append([title, '', '专用引脚另核', '', '', desc, ''])
    sheet('接口与专用信号', ['接口/控制器', '驱动/提供者', '状态', '关联引脚或参数', '子设备/补充', '原理图核对要求', '源位置'],
          interface_rows, [46, 55, 48, 110, 80, 100, 100])
    sheet('稳压器电源', ['电源名', '节点', '最小uV', '最大uV', '初始化uV', 'always-on', 'boot-on', '上游电源', 'GPIO使能及极性', '休眠设置', '供电消费者', '状态', '限制', '源位置'],
          supply_rows, [25, 64, 18, 18, 18, 16, 16, 65, 70, 60, 110, 48, 65, 100])
    sheet('IO域供电', ['IO域控制器', '域供电属性', '稳压器节点', '电源名', '最小uV', '最大uV', '状态', 'Bank映射与电气核对', '源位置'],
          io_rows, [54, 24, 65, 30, 20, 20, 48, 110, 100])
    risks.extend([
        ['待补实体键映射', '19 路 key-gpios', '/play_joystick', '数组没有实体键名和逐键事件码，不能拿数组位置直接当 A/B/方向/FN', '驱动源码或样机逐键通断/事件核对'],
        ['待补摇杆控制含义', 'rocker / rocker0 / rocker1', '/play_joystick', '三路 GPIO 的方向和选择/使能/按压角色未在 DTS 中明确', '驱动与电路核对'],
        ['待补封装与电压', '全部 SoC PAD', 'GPIO3_B3 等是逻辑 PAD 名', '未确认 BGA 球位、VCCIO 域映射、上电态和外部偏置', 'SoC 完整料号/后缀及封装资料'],
        ['专用信号未由GPIO覆盖', 'DDR/DSI/USB/ADC/PMIC', '见接口表', '不能用 DTS GPIO 清单替代全部核心板电气设计', '芯片设计指南、外设规格及电源/时钟评审']])
    sheet('复用与待核实', ['类型', '信号/通道', '涉及节点', '具体问题与边界', '完成依据'], risks, [30, 45, 95, 120, 60])
    sources = [
        ['板级唯一数据', str(source), digest, '所有 GPIO、pinmux、ADC 和供电数值来自该文件'],
        ['Rockchip pin 常量', 'https://github.com/torvalds/linux/blob/master/include/dt-bindings/pinctrl/rockchip.h', '', 'offset 与 A/B/C/D 分组转换'],
        ['GPIO flags', 'https://github.com/torvalds/linux/blob/master/include/dt-bindings/gpio/gpio.h', '', '标准有效极性；不提供方向/封装球位'],
        ['IRQ flags', 'https://github.com/torvalds/linux/blob/master/include/dt-bindings/interrupt-controller/irq.h', '', 'GPIO 中断触发与 GPIO 极性分开解释'],
        ['Rockchip pinctrl 绑定', 'https://github.com/rockchip-linux/kernel/blob/develop-5.10/Documentation/devicetree/bindings/pinctrl/rockchip,pinctrl.txt', '', 'bank / offset / mux / pin-config 四元组'],
        ['固定稳压器绑定', 'https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/regulator/fixed-regulator.yaml', '', 'enable-active-high 缺省低有效'],
        ['ADC 按键绑定', 'https://github.com/torvalds/linux/blob/master/Documentation/devicetree/bindings/input/adc-keys.yaml', '', 'ADC 按键阈值字段'],
        ['验证范围', version, '', '编译退出码0；解析 phandle、计数和生成后回读检查；未做实机、未确认封装脚号']]
    ws = sheet('来源与验证', ['来源', '路径或地址', 'SHA256', '支持内容/验证范围'], sources, [32, 125, 74, 100])
    for row in ws.iter_rows(min_row=2):
        if str(row[1].value).startswith('https://'):
            row[1].hyperlink = row[1].value
    summary = {'source': str(source), 'source_sha256': digest, 'compiler': version, 'compile_exit_code': 0,
               'compile_warning_lines': len(warnings.splitlines()), 'digital_key_count': len(keys),
               'gpio_consumer_entries': len(gpio), 'unique_gpio_consumer_pads': sum(bool(items) for items in uses_by_pin.values()),
               'referenced_pinmux_entries': len(mux), 'pinmux_group_count': len(groups),
               'pinmux_definition_entries': sum(map(len, groups.values())), 'gpio_summary_pads': len(summary_rows),
               'sheet_rows': sheet_counts, 'unresolved_phandles': 0, 'hardware_verified': False,
               'ball_numbers_confirmed': False, 'all_pad_voltages_confirmed': False}
    out.mkdir(parents=True)
    workbook = out/'rf3536k3ka_核心板GPIO使用表.xlsx'
    wb.active = 0
    wb.save(str(workbook))
    check = load_workbook(str(workbook), read_only=True)
    for name, count in sheet_counts.items():
        if check[name].max_row != count+1:
            raise ValueError('Workbook row mismatch: '+name)
    check.close()
    if source.read_bytes() != original:
        raise ValueError('Source DTS changed during export')
    (out/'提取核验.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    (out/'dtc编译警告.txt').write_text(warnings, encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    print('Workbook: '+str(workbook))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, struct.error) as error:
        print('Error: '+str(error), file=sys.stderr)
        sys.exit(1)
