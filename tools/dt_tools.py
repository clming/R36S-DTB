#!/usr/bin/env python3
"""Compile, decompile and compare device trees. Python 3.6+, standard library only."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import struct
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
STRING = r'"(?:\\.|[^"\\])*"'
STRING_LIST = re.compile(STRING + r'(?:,\s*' + STRING + r')+')
PANEL = '/dsi@ff450000/panel@0'


def compiler(explicit=None):
    if explicit:
        found = shutil.which(explicit)
        path = Path(found or explicit).resolve()
    elif os.name == 'nt':
        path = HERE / 'bin/windows-x86_64/dtc.exe'
    elif sys.platform.startswith('linux') and platform.machine().lower() in ('x86_64', 'amd64'):
        path = HERE / 'bin/linux-x86_64/dtc'
        if not os.access(str(path), os.X_OK):
            found = shutil.which('dtc')
            if found:
                path = Path(found)
    else:
        found = shutil.which('dtc')
        if not found:
            raise ValueError('Install dtc for this platform or specify --dtc PATH.')
        path = Path(found)
    if not path.is_file():
        raise ValueError('dtc not found: {}'.format(path))
    if os.name != 'nt' and not os.access(str(path), os.X_OK):
        raise ValueError('dtc is not executable; run chmod +x "{}" or use --dtc.'.format(path))
    return str(path)


def run_dtc(dtc, args):
    proc = subprocess.run([dtc] + [str(a) for a in args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.stderr:
        sys.stderr.write(proc.stderr.decode('utf-8', errors='replace'))
    if proc.returncode:
        raise ValueError('dtc exited with code {}'.format(proc.returncode))
    return proc.stdout


def tree(path):
    """Read FDT v17 layout; compare raw properties without relying on text formatting."""
    data = Path(path).read_bytes()
    if len(data) < 40:
        raise ValueError('Truncated DTB: {}'.format(path))
    h = struct.unpack_from('>10I', data)
    magic, total, off_struct, off_strings, off_reserve, version, last, cpu, str_size, struct_size = h
    if magic != 0xd00dfeed or version < 17 or last > 17 or not 40 <= total <= len(data):
        raise ValueError('Expected a valid FDT v17-compatible DTB: {}'.format(path))
    if (off_struct < 40 or off_strings < 40 or off_reserve < 40 or
            off_struct + struct_size > total or off_strings + str_size > total):
        raise ValueError('Invalid DTB block bounds: {}'.format(path))
    strings = data[off_strings:off_strings+str_size]
    block = data[off_struct:off_struct+struct_size]
    pos, stack, props, nodes = 0, [], {}, set()
    ended = False
    while pos + 4 <= len(block):
        token = struct.unpack_from('>I', block, pos)[0]
        pos += 4
        if token == 1:
            end = block.index(b'\0', pos)
            stack.append(block[pos:end].decode('utf-8'))
            pos = (end + 4) & ~3
            node = '/'.join(stack) or '/'
            if node in nodes:
                raise ValueError('Duplicate node: ' + node)
            nodes.add(node)
        elif token == 2:
            if not stack:
                raise ValueError('Unbalanced DTB nodes')
            stack.pop()
        elif token == 3:
            if not stack or pos + 8 > len(block):
                raise ValueError('Invalid DTB property header')
            size, offset = struct.unpack_from('>II', block, pos)
            pos += 8
            if pos + size > len(block) or offset >= len(strings):
                raise ValueError('Invalid DTB property bounds')
            end = strings.index(b'\0', offset)
            key = ('/'.join(stack) or '/', strings[offset:end].decode('utf-8'))
            if key in props:
                raise ValueError('Duplicate property: {}'.format(key))
            props[key] = block[pos:pos+size]
            pos = (pos + size + 3) & ~3
        elif token == 4:
            pass
        elif token == 9:
            ended = True
            break
        else:
            raise ValueError('Invalid FDT token: {}'.format(token))
    if not ended or stack or '/' not in nodes:
        raise ValueError('Incomplete DTB structure')
    reservations = []
    pos = off_reserve
    while pos + 16 <= total:
        entry = struct.unpack_from('>QQ', data, pos)
        pos += 16
        if entry == (0, 0):
            break
        reservations.append(entry)
    else:
        raise ValueError('Unterminated reservation table')
    return {'nodes': nodes, 'properties': props, 'reservations': reservations, 'boot_cpu': cpu}


def old_style(text):
    # Match complete quoted strings so commas inside strings remain untouched.
    def join(match):
        return '"' + r'\0'.join(s[1:-1] for s in re.findall(STRING, match.group())) + '"'
    return STRING_LIST.sub(join, text).replace('\r\n', '\n').replace('\n', '\r\n').encode('utf-8')


def publish(path, data, overwrite=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not overwrite:
        with path.open('xb') as output:
            output.write(data)
        return
    # Stage in the destination directory so replacement is on the same volume.
    descriptor, name = tempfile.mkstemp(prefix='.dt-tools-', dir=str(path.parent))
    try:
        with os.fdopen(descriptor, 'wb') as output:
            output.write(data)
        os.replace(name, str(path))
    finally:
        if os.path.exists(name):
            os.unlink(name)


def convert(dtc, source, mode, work):
    source = Path(source).resolve()
    output = work / ('result.dts' if mode == 'decompile' else 'result.dtb')
    if mode == 'decompile':
        original = tree(source)
        run_dtc(dtc, ['-I', 'dtb', '-O', 'dts', '-o', output, source])
        output.write_bytes(old_style(output.read_text(encoding='utf-8')))
        rebuilt = work / 'roundtrip.dtb'
        run_dtc(dtc, ['-I', 'dts', '-O', 'dtb', '-o', rebuilt, output])
        if tree(rebuilt) != original:
            raise ValueError('Decompilation round-trip changed tree data: {}'.format(source))
    else:
        run_dtc(dtc, ['-I', 'dts', '-O', 'dtb', '-o', output, source])
        tree(output)
    return output.read_bytes()


def load_tree(path, dtc, work):
    path = Path(path).resolve()
    if path.suffix.lower() == '.dts':
        output = work / 'input.dtb'
        run_dtc(dtc, ['-I', 'dts', '-O', 'dtb', '-o', output, path])
        return tree(output)
    return tree(path)


def value(data):
    if data is None:
        return None
    if data == b'':
        return {'boolean': True}
    if data.endswith(b'\0') and any(data[:-1]) and all(x == 0 or 32 <= x < 127 for x in data):
        return {'strings': data[:-1].decode('ascii').split('\0')}
    if len(data) > 128:
        return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    if len(data) % 4 == 0:
        return {'cells': ['0x%x' % x for x in struct.unpack('>%dI' % (len(data)//4), data)]}
    return {'hex': data.hex()}


def compared_properties(t, include_metadata):
    if include_metadata:
        return t['properties']
    return {k: v for k, v in t['properties'].items()
            if k[1] not in ('phandle', 'linux,phandle')
            and k[0].split('/')[1] not in ('__symbols__', '__fixups__', '__local_fixups__')}


def compare(a, b, include_metadata=False, details=False):
    ap, bp = compared_properties(a, include_metadata), compared_properties(b, include_metadata)
    keys = sorted(set(ap) | set(bp))
    changed = [k for k in keys if ap.get(k) != bp.get(k)]
    result = {'equal_properties': len(keys)-len(changed), 'different_properties': len(changed),
              'left_only_properties': len(set(ap)-set(bp)), 'right_only_properties': len(set(bp)-set(ap)),
              'left_only_nodes': sorted(a['nodes']-b['nodes']), 'right_only_nodes': sorted(b['nodes']-a['nodes']),
              'reservations_equal': a['reservations'] == b['reservations'], 'boot_cpu_equal': a['boot_cpu'] == b['boot_cpu'],
              'exact_tree_equal': a == b}
    if details:
        result['differences'] = [{'node': k[0], 'property': k[1], 'left': value(ap.get(k)), 'right': value(bp.get(k))} for k in changed]
    return result


def init_commands(data):
    if data is None:
        return None
    result, pos = [], 0
    while pos < len(data):
        if pos + 3 > len(data) or pos + 3 + data[pos+2] > len(data):
            raise ValueError('Malformed panel-init-sequence packet')
        end = pos + 3 + data[pos+2]
        result.append(data[pos:end])
        pos = end
    return result


def screen_compare(a, b):
    x = a['properties'].get((PANEL, 'panel-init-sequence'))
    y = b['properties'].get((PANEL, 'panel-init-sequence'))
    ac, bc = init_commands(x), init_commands(y)
    result = {'left_init_bytes': None if x is None else len(x), 'right_init_bytes': None if y is None else len(y),
              'init_byte_similarity_percent': None, 'equal_init_commands': None}
    if x is not None and y is not None:
        result['init_byte_similarity_percent'] = round(100*difflib.SequenceMatcher(None, x, y, autojunk=False).ratio(), 3)
        result['equal_init_commands'] = sum(n for _, _, n in difflib.SequenceMatcher(None, ac, bc, autojunk=False).get_matching_blocks())
        result['left_init_commands'], result['right_init_commands'] = len(ac), len(bc)
    for label, t in [('left', a), ('right', b)]:
        result[label+'_timings'] = {node: {prop: value(v) for (p, prop), v in t['properties'].items() if p == node and prop != 'phandle'}
                                   for node in sorted(t['nodes']) if node.startswith(PANEL+'/display-timings/')}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dtc', help='Override dtc executable (place before subcommand)')
    commands = parser.add_subparsers(dest='command')
    commands.add_parser('version', help='Show selected dtc and version')
    for mode in ('compile', 'decompile'):
        p = commands.add_parser(mode)
        p.add_argument('input', type=Path)
        p.add_argument('-o', '--output', type=Path, required=True)
        p.add_argument('--overwrite', action='store_true', help='Replace an existing output file')
    p = commands.add_parser('batch-decompile', help='Recursively decompile *.dtb')
    p.add_argument('directory', type=Path)
    p.add_argument('--output-dir', type=Path, help='Default: beside each DTB; otherwise preserve relative directories here')
    p.add_argument('--overwrite', action='store_true')
    for mode in ('compare', 'rank'):
        p = commands.add_parser(mode)
        p.add_argument('left', type=Path, help='Reference .dtb or .dts')
        p.add_argument('right', type=Path, help='Candidate file' if mode == 'compare' else 'Candidate directory, recursive *.dtb')
        p.add_argument('--include-metadata', action='store_true', help='Include phandle definitions and symbol/fixup properties')
        p.add_argument('--screen', action='store_true', help='Compare panel initialization; rank by its byte similarity')
        p.add_argument('--json', type=Path, help='Write complete JSON report; refuses existing files')
        if mode == 'rank':
            p.add_argument('--top', type=int, default=10)
        else:
            p.add_argument('--limit', type=int, default=20, help='Maximum property differences printed; JSON keeps all')
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0
    if getattr(args, 'json', None) and args.json.exists():
        raise ValueError('Report already exists: {}'.format(args.json))
    needs_dtc = args.command in ('version', 'compile', 'decompile', 'batch-decompile') or any(
        getattr(args, n, Path('.')).suffix.lower() == '.dts' for n in ('left', 'right'))
    dtc = compiler(args.dtc) if needs_dtc else None
    with tempfile.TemporaryDirectory(prefix='r36s-dt-') as directory:
        work = Path(directory)
        if args.command == 'version':
            print(dtc)
            print(run_dtc(dtc, ['--version']).decode().strip())
        elif args.command in ('compile', 'decompile'):
            if args.input.resolve() == args.output.resolve():
                raise ValueError('Input and output must be different files')
            if args.output.exists() and not args.overwrite:
                raise ValueError('Output exists; choose another path or use --overwrite')
            data = convert(dtc, args.input, args.command, work)
            publish(args.output, data, args.overwrite)
            print('Created: {}\nSHA256: {}'.format(args.output, hashlib.sha256(data).hexdigest()))
        elif args.command == 'batch-decompile':
            if not args.directory.is_dir():
                raise ValueError('Input directory does not exist')
            files = sorted(args.directory.rglob('*.dtb'))
            if not files:
                raise ValueError('No *.dtb files found')
            jobs = [(source, ((args.output_dir/source.relative_to(args.directory)) if args.output_dir else source).with_suffix('.dts')) for source in files]
            for source, dest in jobs:
                if dest.exists() and not args.overwrite:
                    raise ValueError('Output exists: {} (use --overwrite explicitly)'.format(dest))
                if source.resolve() == dest.resolve():
                    raise ValueError('Input and output must be different')
            # Verify every file before publishing the batch.
            staged = []
            for i, (source, dest) in enumerate(jobs):
                item = work/str(i)
                item.mkdir()
                data = convert(dtc, source, 'decompile', item)
                staged.append((dest, data))
            for dest, data in staged:
                publish(dest, data, args.overwrite)
                print('Created: {}'.format(dest))
            print('Verified {} DTS round trips.'.format(len(jobs)))
        else:
            a = load_tree(args.left, dtc, work)
            if args.command == 'compare':
                b = load_tree(args.right, dtc, work)
                report = compare(a, b, args.include_metadata, details=True)
                report.update(left=str(args.left), right=str(args.right))
                if args.screen:
                    report['screen'] = screen_compare(a, b)
                brief = dict(report)
                brief['differences'] = report['differences'][:max(0, args.limit)]
                print(json.dumps(brief, indent=2, ensure_ascii=True))
            else:
                if not args.right.is_dir():
                    raise ValueError('Candidate directory does not exist')
                rows = []
                for candidate in sorted(args.right.rglob('*.dtb')):
                    if candidate.resolve() == args.left.resolve():
                        continue
                    b = tree(candidate)
                    row = compare(a, b, args.include_metadata)
                    row['file'] = str(candidate)
                    if args.screen:
                        row['screen'] = screen_compare(a, b)
                    rows.append(row)
                if not rows:
                    raise ValueError('No candidate *.dtb files found')
                def order(row):
                    score = row.get('screen', {}).get('init_byte_similarity_percent')
                    return ((-(score if score is not None else -1),) if args.screen else ()) + (row['different_properties'], row['file'])
                rows.sort(key=order)
                report = {'reference': str(args.left), 'metric': 'screen-init-bytes' if args.screen else 'different-property-count', 'candidates': rows}
                for row in rows[:max(0, args.top)]:
                    print('{}  different={}  screen={}  {}'.format('EQUAL' if row['exact_tree_equal'] else 'DIFF', row['different_properties'], row.get('screen', {}).get('init_byte_similarity_percent', '-'), row['file']))
            if args.json:
                publish(args.json, (json.dumps(report, indent=2, ensure_ascii=True)+'\n').encode('utf-8'))
                print('Report: {}'.format(args.json))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, struct.error) as error:
        print('Error: {}'.format(error), file=sys.stderr)
        sys.exit(1)
