import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import multiprocessing as mproc
import subprocess
import darkdetect
import threading
import traceback
import platform
import copy
import json
import math
import sys
import io
import re
import os

from PIL import Image

from typing import List, Tuple, Any, Optional

import nb2pb

import netsblox
from netsblox import transform
from netsblox import common
from netsblox import rooms

NETSBLOX_PY_PATH = os.path.dirname(netsblox.__file__)

SUGGESTION_UPDATE_INTERVAL = 200
PANED_WINDOW_OPTS = {
    'sashwidth': 5,
}

xux = lambda x: f'{x} {x.upper()}'
PROJECT_FILETYPES = [('PyBlox Project Files', xux('.json')), ('All Files', '.*')]
NB_PROJECT_FILETYPES = [('NetsBlox Project Files', xux('.xml')), ('All Files', '.*')]
PYTHON_FILETYPES = [('Python Files', xux('.py')), ('All Files', '.*')]
IMAGE_FILETYPES = [('Images', xux('.png .jpg .jpeg')), ('All Files', '.*')]

MIN_FONT_SIZE = 4
MAX_FONT_SIZE = 40

color_enabled = False
try:
    # idle gives us syntax highlighting, but we don't require it otherwise
    import idlelib.colorizer as colorizer
    import idlelib.percolator as percolator
    color_enabled = True
except:
    pass

force_enabled = False
try:
    import jedi
    force_enabled = True
except:
    pass

IS_DARK = darkdetect.isDark()
COLOR_INFO = {
    'text-background':          '#1f1e1e' if IS_DARK else '#ffffff',
    'text-background-disabled': '#1f1e1e' if IS_DARK else '#ffffff',
}

SYS_INFO = None
if platform.system() == 'Darwin':
    SYS_INFO = {
        'mod-str': 'Cmd',
        'mod': 'Command',
        'redo-binds': [
            '<Command-Key-Z>',
        ],
        'right-click': 'Button-2',
    }
else:
    SYS_INFO = {
        'mod-str': 'Ctrl',
        'mod': 'Control',
        'redo-binds': [
            '<Control-Key-y>',
            '<Control-Key-Y>',
        ],
        'right-click': 'Button-3',
    }

nb = None
root = None
main_menu = None
content = None

_print_queue = mproc.Queue(maxsize = 256)
_print_batchsize = 256
_print_targets = []
def _process_print_queue():
    for _ in range(_print_batchsize):
        if _print_queue.empty():
            break
        val = _print_queue.get()
        for target in _print_targets:
            try:
                target.write(val)
            except:
                pass # throwing would break print queue
    root.after(33, _process_print_queue)

def basename_noext(path: str) -> str:
    file = os.path.basename(path)
    p = file.find('.')
    return (file[:p] if p >= 0 else file).strip()

def get_white_nonwhite(line: str) -> Tuple[str, str]:
    i = 0
    while i < len(line) and line[i].isspace():
        i += 1
    return line[:i], line[i:]
def undent_single(line: str) -> str:
    i = 0
    while i < 4 and i < len(line) and line[i].isspace():
        i += 1
    return line[i:], i # remove at most 4 whitespace chars

def indent(txt: str) -> str:
    return '\n'.join([ f'    {x}' for x in txt.splitlines() ])
def indent_info(txt: str) -> str:
    indents = [ f'    {x}' for x in txt.splitlines() ]
    return '\n'.join(indents), [4 for _ in indents]
def undent_info(txt: str) -> Tuple[str, int, int]:
    undents = [ undent_single(x) for x in txt.splitlines() ]
    if len(undents) == 0:
        return txt, 0, 0
    return '\n'.join([ x[0] for x in undents ]), [ -x[1] for x in undents ]

def smart_comment_uncomment(txt: str) -> Tuple[str, int]:
    line_parts = [ get_white_nonwhite(x) for x in txt.splitlines() ]
    should_uncomment = all(part[1].startswith('#') or part[1] == '' for part in line_parts)

    if should_uncomment:
        res_lines = []
        res_deltas = []
        for part in line_parts:
            for head in ['# ', '#', '']:
                if part[1].startswith(head):
                    res_lines.append(part[0] + part[1][len(head):])
                    res_deltas.append(-len(head))
                    break
        return '\n'.join(res_lines), res_deltas
    else:
        res_lines = []
        res_deltas = []
        for part in line_parts:
            if part[1] != '':
                res_lines.append(f'{part[0]}# {part[1]}')
                res_deltas.append(2)
            else:
                res_lines.append(part[0] + part[1])
                res_deltas.append(0)
        return '\n'.join(res_lines), res_deltas

IDENT_REGEX = re.compile('^[a-zA-Z_][0-9a-zA-Z_]*$')
def is_valid_ident(ident: str) -> bool:
    return bool(IDENT_REGEX.match(ident))

SIZE_REGEX = re.compile('^\s*(\d+)\s*[xX]\s*(\d+)\s*$')
def parse_size(value: str) -> Optional[Tuple[int, int]]:
    m = SIZE_REGEX.match(value)
    return (int(m.group(1)), int(m.group(2))) if m is not None else None

MIN_CANV_SIZE = (64, 64)
MAX_CANV_SIZE = (8192, 8192)

def normalize_strip(content: str) -> str:
    raw_lines = [x.rstrip() for x in content.splitlines()]
    raw_pos = 0
    while True:
        while raw_pos < len(raw_lines) and not raw_lines[raw_pos]:
            raw_pos += 1
        if raw_pos >= len(raw_lines):
            break
        target = raw_lines[raw_pos][0]
        if not target.isspace():
            break

        if any(t and not t.startswith(target) for t in raw_lines):
            break

        for i in range(len(raw_lines)):
            raw_lines[i] = raw_lines[i][1:]

    return '\n'.join(raw_lines)

FULL_NAME_DOC_REMAPS = {
    'builtins.input': '''
input(prompt: Any=...) -> Optional[str]

Prompt the user to input a string.
If the prompt is closed or canceled, `None` is returned,
otherwise the user's input is returned directly (which may be the empty string).
'''.strip(),
}
PROP_DOC_REMAPS = {}

for T in [netsblox.turtle.StageBase, netsblox.turtle.TurtleBase]:
    for k in dir(T):
        if k.startswith('_') or k.startswith('_'):
            continue
        field = getattr(T, k)
        assert field.__doc__
        if type(field) is property:
            doc = normalize_strip(field.__doc__)
            PROP_DOC_REMAPS[k] = doc
            FULL_NAME_DOC_REMAPS[f'netsblox.turtle.{T.__name__}.{k}'] = doc

INLINE_CODE_REGEX = re.compile(r'`([^`]+)`')
def clean_docstring(content: str) -> str:
    paragraphs = ['']
    in_code = False

    def par():
        if paragraphs[-1]:
            paragraphs.append('')

    for line in content.splitlines():
        if not line or line.isspace():
            par()
            continue
        if line.startswith('```'):
            par()
            in_code = not in_code
            continue

        if in_code:
            if paragraphs[-1]:
                paragraphs[-1] += '\n'
            paragraphs[-1] += line
        else:
            if paragraphs[-1]:
                paragraphs[-1] += '\n' if line[0].isspace() else ' '
            paragraphs[-1] += line

    res = '\n\n'.join(paragraphs).strip()
    res = re.sub(INLINE_CODE_REGEX, r'\1', res)
    return res

_exec_monitor_running = False
def start_exec_monitor():
    global _exec_monitor_running, _exec_process
    if _exec_monitor_running: return
    _exec_monitor_running = True

    interval = 500
    def watcher():
        try:
            proc = _exec_process
            if proc is not None and proc.poll() is not None:
                play_button() # this will end exec mode
        except Exception as e:
            print(e, file = sys.stderr)
        finally:
            root.after(interval, watcher)
    watcher()

def exec_wrapper(*args):
    try:
        exec(*args)
    except:
        print(traceback.format_exc(), file = sys.stderr) # print out directly so that the stdio wrappers are used

_exec_process = None
def play_button():
    global _exec_process
    start_exec_monitor()

    run_entry = main_menu.run_menu_entries['run-project']
    stop_entry = main_menu.run_menu_entries['stop-project']

    # if already running, just kill it - the only locks they can have were made by them, so no deadlocking issues.
    # the messaging pipe is broken, but we won't be using it anymore.
    if _exec_process is not None:
        _exec_process.terminate()
        _exec_process = None
        main_menu.run_menu.entryconfig(run_entry, state = tk.ACTIVE)
        main_menu.run_menu.entryconfig(stop_entry, state = tk.DISABLED)
        return

    main_menu.run_menu.entryconfig(run_entry, state = tk.DISABLED)
    main_menu.run_menu.entryconfig(stop_entry, state = tk.ACTIVE)

    content.display.terminal.text.set_text('')

    def file_piper(src, dst):
        src = io.TextIOWrapper(src)
        for c in iter(lambda: src.read(1), ''):
            dst.write(c)
            dst.flush()

    code = transform.add_yields(content.project.get_full_script())
    _exec_process = subprocess.Popen([sys.executable, '-u'], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    _exec_process.stdin.write(code.encode('utf-8'))
    _exec_process.stdin.close()

    # reading the pipe is blocking so do in another thread - it will exit when process is killed
    threading.Thread(target = file_piper, args = (_exec_process.stdout, sys.stdout), daemon = True).start()

_package_dir = netsblox.__path__[0]
def module_path(path: str) -> str:
    return f'{_package_dir}/{path}'

class Content(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(side = tk.BOTTOM, fill = tk.BOTH, expand = True)

        self.pane = tk.PanedWindow(self, orient = tk.HORIZONTAL, **PANED_WINDOW_OPTS)
        self.pane.pack(fill = tk.BOTH, expand = True)

        self.blocks = BlocksList(self.pane)
        self.project = ProjectEditor(self.pane)
        self.display = Display(self.pane)

        self.pane.add(self.blocks, stretch = 'never')
        self.pane.add(self.project, stretch = 'always', width = 5, minsize = 300)
        self.pane.add(self.display, stretch = 'always', width = 3, minsize = 300)

class DndTarget:
    def __init__(self, widget, on_start, on_stop, on_drop):
        self.widget = widget
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_drop = on_drop

class DndManager:
    def __init__(self, widget, targets: List[DndTarget]):
        self.targets = targets

        widget.bind('<ButtonPress-1>', self.on_start)
        widget.bind('<B1-Motion>', self.on_drag)
        widget.bind('<ButtonRelease-1>', self.on_drop)

    def on_start(self, e):
        for target in self.targets:
            target.on_start(e)

    def on_drag(self, e):
        pass

    def on_drop(self, e):
        for target in self.targets:
            target.on_stop(e)

        x, y = e.widget.winfo_pointerxy()
        dest_widget = e.widget.winfo_containing(x, y)
        for target in self.targets:
            if dest_widget is target.widget:
                target.on_drop(e)
                break

class BlocksList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.scrollbar = ttk.Scrollbar(self)
        self.text = tk.Text(self, wrap = tk.NONE, width = 24, yscrollcommand = self.scrollbar.set, bg = COLOR_INFO['text-background-disabled'])
        self.scrollbar.configure(command = self.text.yview)

        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.text.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        # make sure user can't select anything with the mouse (would look weird)
        self.text.bind('<Button-1>', lambda e: 'break')
        self.text.bind('<B1-Motion>', lambda e: 'break')
        self.text.configure(cursor = 'arrow')

        self.imgs = [] # for some reason we need to keep a reference to the images or they disappear

        self.text.configure(state = tk.DISABLED)

    def link(self, blocks, text_target) -> None:
        orig_bcolor = text_target.cget('background')

        def make_dnd_manager(widget, code):
            focused = [None]
            def on_start(e):
                # store focused widget and steal focus so that the colored outline will always show
                focused[0] = root.focus_get()
                widget.focus()

                text_target.configure(highlightbackground = '#156fe6')
            def on_stop(e):
                # restore saved focus
                if focused[0] is not None:
                    focused[0].focus()

                text_target.configure(highlightbackground = orig_bcolor)
            def on_drop(e):
                x, y = text_target.winfo_pointerxy()
                x -= text_target.winfo_rootx()
                y -= text_target.winfo_rooty()

                pos = text_target.index(f'@{x},{y}')
                text_target.insert(f'{pos} linestart', f'{code}\n')
                text_target.edit_separator() # so multiple drag and drops aren't undone as one

                return 'break'

            return DndManager(widget, [DndTarget(text_target, on_start, on_stop, on_drop)])

        try:
            self.text.config(state = tk.NORMAL)

            self.text.delete('1.0', 'end')
            self.imgs.clear()

            for block in blocks:
                img = common.load_tkimage(block['url'], scale = block['scale'])
                label = tk.Label(self.text, image = img, bg = COLOR_INFO['text-background-disabled'])

                self.text.window_create('end', window = label)
                self.text.insert('end', '\n')
                self.imgs.append(img)

                make_dnd_manager(label, block['replace'])
        finally:
            self.text.config(state = tk.DISABLED)

class Imports:
    RAW_INFO = json.loads(common.load_text("netsblox://assets/default-imports.json"))

    def __init__(self, *, on_update = None):
        self.packages = {}
        for item in Imports.RAW_INFO:
            self.packages[item[0]] = {
                'tkvar': tk.BooleanVar(),
                'ident': item[1],
                'info': clean_docstring(normalize_strip(item[2])),
                'code': f'import {item[0]}' if item[0] == item[1] else f'import {item[0]} as {item[1]}',
            }

        self.images = {}

        self.on_update = on_update

    def batch_update(self) -> None:
        import_lines = []
        for item in self.packages.values():
            if item['tkvar'].get():
                import_lines.append(item['code'])

        image_lines = []
        if len(self.images) != 0:
            image_lines.append('import gelidum as _gelidum')
            image_lines.append('class images:')
        for name, img in self.images.items():
            image_lines.append(f'    {name} = netsblox.common.decode_image(\'{common.encode_image(img)}\')')
        if len(self.images) != 0:
            image_lines.append('images = images()')
            image_lines.append('_gelidum.freeze(images, on_freeze = \'inplace\')')

        needs_sep = len(import_lines) != 0 and len(image_lines) != 0
        lines = [*import_lines, *([''] if needs_sep else []), *image_lines]

        if len(lines) == 0:
            GlobalEditor.prefix = GlobalEditor.BASE_PREFIX
            GlobalEditor.prefix_lines = GlobalEditor.BASE_PREFIX_LINES
        else:
            import_str = '\n'.join(lines)
            GlobalEditor.prefix = f'{GlobalEditor.BASE_PREFIX}{import_str}\n\n'
            GlobalEditor.prefix_lines = GlobalEditor.BASE_PREFIX_LINES + len(lines) + 1

        if self.on_update is not None:
            self.on_update()

class ProjectEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # this is randomly generated and is valid while the ide is open across multiple program runs.
        # it is not stored in project files or exports because conflicting ids would break messaging.
        self.project_id = common.generate_project_id()

        self.roles: List[dict] = None
        self.active_role: int = None

        self.client_type = 'editor' # must be one of: editor, dev

        self.block_sources = []

        self.editors: List[CodeEditor] = []

        def imports_update():
            for editor in self.editors:
                editor.on_content_change()
            main_menu.update_images()
        self.imports = Imports(on_update = imports_update)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill = tk.BOTH, expand = True)

        self.ctx_tab_idx = None
        self.ctx_menu = None
        def update_ctx_tab_idx(x, y):
            x -= self.notebook.winfo_rootx()
            y -= self.notebook.winfo_rooty()
            idx = None
            try:
                idx = self.notebook.index(f'@{x},{y}')
            except:
                pass
            self.ctx_tab_idx = idx
            e_idx = idx if idx is not None else -1

            turtle_option_state = tk.NORMAL if e_idx >= 2 else tk.DISABLED
            for key in ['dupe', 'rename', 'delete']:
                self.ctx_menu.entryconfigure(self.ctx_menu_entries[key], state = turtle_option_state)

            return idx is not None

        self.ctx_menu = ContextMenu(self.notebook, on_show = update_ctx_tab_idx)
        self.ctx_menu_entries = {}
        def add_command(id, *, label, command):
            self.ctx_menu.add_command(label = label, command = command)
            idx = len(self.ctx_menu_entries)
            self.ctx_menu_entries[id] = idx

        add_command('new-turtle', label = 'New Sprite', command = lambda: self.newturtle())
        add_command('dupe', label = 'Clone Sprite', command = lambda: self.dupe_turtle(self.ctx_tab_idx))
        add_command('rename', label = 'Rename', command = lambda: self.rename_turtle(self.ctx_tab_idx))
        add_command('delete', label = 'Delete', command = lambda: self.delete_tab(self.ctx_tab_idx))

        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_change)

    def on_tab_change(self, e = None):
        for editor in self.editors:
            editor.hide_suggestion()
        if e is None: return

        tab = None
        try:
            tab = e.widget.tab('current')['text']
        except:
            return

        editors = [x for x in self.editors if x.name == tab]
        assert len(editors) == 1
        editors[0].on_content_change(cause = 'tab-change')

    def delete_tab(self, idx) -> None:
        editor = self.editors[idx]
        if not isinstance(editor, TurtleEditor):
            return # only turtle editors can be deleted

        title = f'Delete {editor.name}'
        msg = f'Are you sure you would like to delete {editor.name}? This operation cannot be undone.'
        if messagebox.askyesno(title, msg, icon = 'warning', default = 'no'):
            del self.editors[idx]
            self.notebook.forget(idx)
            editor.destroy()

    def is_unique_name(self, name: str) -> bool:
        return not any(x.name == name for x in self.editors)

    def dupe_turtle(self, idx) -> Any:
        editor = self.editors[idx]
        if not isinstance(editor, TurtleEditor):
            return # only turtle editors can be duped

        return self.newturtle(base_name = f'{editor.name}_copy', value = editor.text.get('1.0', 'end-1c'))

    def rename_turtle(self, idx) -> None:
        editor = self.editors[idx]
        if not isinstance(editor, TurtleEditor):
            return # only turtle editors can be renamed

        name = None
        while True:
            title = 'Rename Sprite'
            msg = f'Enter the new name for "{editor.name}" (must not already be taken).\nNote that any references to this sprite in your code must be manually updated to the new name.'
            name = simpledialog.askstring(title, msg)
            if name is None:
                return
            if not is_valid_ident(name):
                messagebox.showerror(title = 'Invalid name', message = f'"{name}" is not a valid python variable name')
                continue
            if not self.is_unique_name(name):
                messagebox.showerror(title = 'Invalid name', message = f'A tab named "{name}" already exists')
                continue
            break

        editor.name = name
        self.notebook.tab(idx, text = name)

    def newturtle(self, *, base_name = 'sprite', value = None) -> Any:
        name_counter = 0
        name = base_name
        while not self.is_unique_name(name):
            name_counter += 1
            name = f'{base_name}{name_counter}'

        assert self.is_unique_name(name) and is_valid_ident(name) # sanity check
        editor = TurtleEditor(self.notebook, name = name, value = value or ProjectEditor.DEFAULT_PROJECT['editors'][2]['value'])
        self.notebook.add(editor, text = name)
        self.editors.append(editor)
        return editor

    def get_full_script(self, *, is_export: bool = False) -> str:
        scripts = []
        for editor in self.editors:
            scripts.append(editor.get_script(is_export = is_export))
            scripts.append('\n\n')
        scripts.append('start_project()')
        return ''.join(scripts)

    DEFAULT_PROJECT = json.loads(common.load_text('netsblox://assets/default-project.json'))

    def get_save_dict(self) -> dict:
        res = {
            'client_type': self.client_type,
            'roles': [],
        }

        for i, role in enumerate(self.roles):
            if i != self.active_role:
                res['roles'].append(copy.deepcopy(role))
                continue

            role_res = {}
            res['roles'].append(role_res)

            role_res['name'] = role['name']
            role_res['stage_size'] = role['stage_size']
            role_res['block_sources'] = self.block_sources[:]
            role_res['blocks'] = {
                'global': [x.copy() for x in GlobalEditor.blocks if x['source'] == None],
                'stage':  [x.copy() for x in  StageEditor.blocks if x['source'] == None],
                'turtle': [x.copy() for x in TurtleEditor.blocks if x['source'] == None],
            }

            role_res['imports'] = []
            for pkg, item in self.imports.packages.items():
                if item['tkvar'].get():
                    role_res['imports'].append(pkg)

            role_res['editors'] = []
            for editor in self.editors:
                ty = None
                if isinstance(editor, GlobalEditor): ty = 'global'
                elif isinstance(editor, StageEditor): ty = 'stage'
                elif isinstance(editor, TurtleEditor): ty = 'turtle'
                else: raise Exception(f'unknown editor type: {type(editor)}')
                role_res['editors'].append({
                    'type': ty,
                    'name': editor.name,
                    'value': editor.text.get('1.0', 'end-1c'),
                })

            role_res['images'] = { name: common.encode_image(img) for name, img in self.imports.images.items() }

        return res
    def load(self, *, super_proj: Optional[dict] = None, active_role: Optional[int] = None) -> None:
        if super_proj is None:
            roles = self.roles
        else:
            super_proj = copy.deepcopy(super_proj)
            roles = super_proj.get('roles', [super_proj]) # default is for backward compat

        client_type = super_proj.get('client_type', 'editor')
        if client_type not in ['editor', 'dev']:
            client_type = 'editor'

        if active_role is None:
            active_role = 0
        elif active_role < 0 or active_role >= len(roles):
            active_role = 0
        proj = roles[active_role]

        name_counter = 0
        for role in roles:
            if 'name' not in role:
                role['name'] = 'untitled' if name_counter == 0 else f'untitled_{name_counter}'
                name_counter += 1
            if 'stage_size' not in role:
                role['stage_size'] = (1080, 720)

        new_blocks = { 'global': [], 'stage': [], 'turtle': [] }
        new_sources = proj.get('block_sources', [])

        def add_blocks(blocks, *, source):
            for k, v in blocks.items():
                target = new_blocks[k]
                for block in v:
                    x = block.copy()
                    x['source'] = source
                    target.append(x)

        for src in new_sources:
            add_blocks(json.loads(common.load_text(src)), source = src)
        add_blocks(proj.get('blocks', {}), source = None)
        add_blocks({ # legacy support
            'global': proj.get('global_blocks', []),
            'stage': proj.get('stage_blocks', []),
            'turtle': proj.get('turtle_blocks', []),
        }, source = None)

        self.client_type = client_type

        self.roles = roles
        self.active_role = active_role

        GlobalEditor.blocks = new_blocks['global']
        StageEditor.blocks = new_blocks['stage']
        TurtleEditor.blocks = new_blocks['turtle']
        self.block_sources = new_sources

        for i in range(len(self.editors) - 1, -1, -1):
            self.notebook.forget(i)
            self.editors[i].destroy()
        self.editors = []

        for info in proj['editors']:
            ty = info['type']
            name = info['name']
            value = info['value']

            editor = None
            if ty == 'global': editor = GlobalEditor(self.notebook, value = value)
            elif ty == 'stage': editor = StageEditor(self.notebook, name = name, value = value)
            elif ty == 'turtle': editor = TurtleEditor(self.notebook, name = name, value = value)
            else: raise Exception(f'unknown editor type: {ty}')

            self.notebook.add(editor, text = name)
            self.editors.append(editor)

        for item in self.imports.packages.values():
            item['tkvar'].set(False)
        for pkg in proj['imports']:
            self.imports.packages[pkg]['tkvar'].set(True)

        self.imports.images.clear()
        for name, raw in proj.get('images', {}).items():
            self.imports.images[name] = common.decode_image(raw)

        self.imports.batch_update()

        if len(self.editors) > 0:
            default_tab_idx = len(self.editors) - 1 # default to stage (last tab) if no turtle editors
            for i, editor in enumerate(self.editors):
                if isinstance(editor, TurtleEditor):
                    default_tab_idx = i
                    break
            self.notebook.select(default_tab_idx)

class ContextMenu(tk.Menu):
    def __init__(self, parent, *, on_show = None):
        super().__init__(parent, tearoff = False)
        parent.bind(f'<{SYS_INFO["right-click"]}>', lambda e: self.show(e.x_root, e.y_root))
        self.bind('<FocusOut>', lambda e: self.hide())
        self.visible = False
        self.on_show = on_show

    def show(self, x, y):
        if self.on_show is not None:
            res = self.on_show(x, y)
            if res is not None and not res:
                return # don't show if on_show said false

        try:
            # theoretically these two _should be_ redundant, but they are needed in conjunction to work...
            if not self.visible:
                self.visible = True

                # witchcraft needed for FocusOut to work on linux
                # notably, if we do this on Darwin it'll result in the menu re-showing after close (which can cause a crash bug on tab deletion)
                if platform.system() == 'Linux':
                    self.tk_popup(x, y)
            self.post(x, y) # wizardry needed for unpost to work
        finally:
            self.grab_release()

    def hide(self):
        if self.visible:
            self.visible = False
            self.unpost()

# source: https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
class TextLineNumbers(tk.Canvas):
    def __init__(self, parent, *, target):
        super().__init__(parent)
        self.textwidget = target
        self.line_num_offset = 0

        self.font = tkfont.nametofont('TkFixedFont')

    def redraw(self):
        self.delete('all')

        line_info = [] # [(y: int, label: str)]
        i = self.textwidget.index('@0,0')
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break
            linenum = int(str(i).split('.')[0]) + self.line_num_offset
            line_info.append((dline[1], str(linenum)))
            i = self.textwidget.index(f'{i}+1line')

        max_label_len = max(len(x[1]) for x in line_info)
        w = math.ceil(6 + 0.8 * max_label_len * self.font.cget('size'))
        self.config(width = w)

        for y, label in line_info:
            self.create_text(w - 2, y, anchor = 'ne', text = label, font = self.font)

# source: https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
class ChangedText(tk.Text):
    __name_id = 0

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # create a proxy for the underlying widget
        ChangedText.__name_id += 1
        self._orig = self._w + f'_orig_{ChangedText.__name_id}'
        self.tk.call('rename', self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig, *args)
        result = None
        try:
            result = self.tk.call(cmd)
        except Exception as e:
            # for some reason our proxying breaks some ops in some cases, so just catch and ignore
            ignore_patterns = [
                ('edit', 'undo'), ('edit', 'redo'), # fails if stack is empty (undo) or at top of stack (redo)
            ]
            if cmd[1:] not in ignore_patterns:
                raise e

        # generate an event if something was added or deleted, or the cursor position changed
        changed = args[0] in ('insert', 'replace', 'delete') or \
            args[0:3] == ('mark', 'set', 'insert') or \
            args[0:2] == ('xview', 'moveto') or \
            args[0:2] == ('xview', 'scroll') or \
            args[0:2] == ('yview', 'moveto') or \
            args[0:2] == ('yview', 'scroll')
        if changed:
            self.event_generate('<<Change>>', when = 'tail')

        return result # return what the actual widget returned

class ScrolledText(tk.Frame):
    def __init__(self, parent, *, wrap = True, readonly = False, linenumbers = False, blocks = [], **kwargs):
        super().__init__(parent)
        undo_args = { 'undo': True, 'maxundo': -1, 'autoseparators': True }

        self.font = tkfont.nametofont('TkFixedFont')
        self.blocks = blocks

        self.scrollbar = ttk.Scrollbar(self)
        self.text = ChangedText(self, font = self.font, yscrollcommand = self.scrollbar.set, wrap = tk.WORD if wrap else tk.NONE, **({} if readonly else undo_args), **kwargs)
        self.scrollbar.config(command = self.text.yview)

        self.hscrollbar = None
        if not wrap:
            self.hscrollbar = ttk.Scrollbar(self, orient = 'horizontal')
            self.text.config(xscrollcommand = self.hscrollbar.set)
            self.hscrollbar.config(command = self.text.xview)

        self.custom_on_change = []

        def on_select_all(e):
            self.text.tag_add(tk.SEL, '1.0', tk.END)
            return 'break'
        self.text.bind(f'<{SYS_INFO["mod"]}-Key-a>', on_select_all)
        self.text.bind(f'<{SYS_INFO["mod"]}-Key-A>', on_select_all)

        def on_home(*, do_select: bool):
            white, _ = get_white_nonwhite(self.text.get('insert linestart', 'insert lineend'))
            target = f'insert linestart +{len(white)}c'
            if do_select:
                col = int(self.text.index('insert').split('.')[1])
                self.text.tag_add(tk.SEL, *((target, 'insert') if col >= len(white) else ('insert', target)))
            else:
                self.text.selection_clear()
            self.text.mark_set('insert', target)
            return 'break'
        self.text.bind('<Home>',       lambda e: on_home(do_select = False))
        self.text.bind('<Shift-Home>', lambda e: on_home(do_select = True))

        self.linenumbers = None # default to none - conditionally created
        self.blocks = blocks

        if readonly:
            # make text readonly be ignoring all (default) keystrokes
            self.text.bind('<Key>', lambda e: 'break')
        else:
            def on_redo(e):
                self.text.edit_redo()
                return 'break'
            for bind in SYS_INFO['redo-binds']:
                self.text.bind(bind, on_redo)

            # default paste behavior doesn't delete selection first
            def on_paste(e):
                if self.text.tag_ranges(tk.SEL):
                    self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)

                # some versions of tcl/tk on mac are broken and crash here, so impl manually
                self.text.insert(tk.INSERT, self.clipboard_get())
                return 'break'
            self.text.bind(f'<{SYS_INFO["mod"]}-Key-v>', on_paste)
            self.text.bind(f'<{SYS_INFO["mod"]}-Key-V>', on_paste)

        # custom copy behavior - (also in readonly case above, catching all keys means we can't copy without override anyway)
        def on_copy(e):
            self.clipboard_clear()
            if self.text.tag_ranges(tk.SEL):
                self.clipboard_append(self.text.get(tk.SEL_FIRST, tk.SEL_LAST))
            else: # if no selection, copy the current line
                self.clipboard_append(self.text.get('insert linestart', 'insert lineend'))
            return 'break'
        self.text.bind(f'<{SYS_INFO["mod"]}-Key-c>', on_copy)
        self.text.bind(f'<{SYS_INFO["mod"]}-Key-C>', on_copy)

        if linenumbers:
            self.linenumbers = TextLineNumbers(self, target = self.text)
            self.text.bind('<<Change>>', lambda e: self.on_content_change())
            self.text.bind('<Configure>', lambda e: self.on_content_change())

        # -----------------------------------------------------

        col_off = 0
        if self.linenumbers is not None:
            self.linenumbers.grid(row = 0, column = 0, sticky = tk.NSEW)
            col_off = 1
        self.scrollbar.grid(row = 0, column = col_off + 1, sticky = tk.NSEW)
        if self.hscrollbar is not None:
            self.hscrollbar.grid(row = 1, column = col_off, sticky = tk.NSEW)
        self.text.grid(row = 0, column = col_off, sticky = tk.NSEW)

        self.columnconfigure(col_off, weight = 1)
        self.rowconfigure(0, weight = 1)

    def on_content_change(self, *, cause: str = 'unknown'):
        for handler in self.custom_on_change:
            handler()
        if self.linenumbers is not None:
            self.linenumbers.redraw()

        if cause == 'tab-change':
            content.blocks.link(self.blocks, self.text)

    def set_text(self, txt):
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', txt)

class CodeEditor(ScrolledText):
    def __init__(self, parent, *, wrap = False, column_offset = 0, **kwargs):
        super().__init__(parent, linenumbers = True, wrap = wrap, **kwargs)
        self.__line_count = None
        self.column_offset = column_offset
        self.help_popup = None
        self.update_timer = None

        def on_change():
            self.__line_count = None
            if content is not None:
                total = 0
                for editor in content.project.editors:
                    if editor is self:
                        total += type(editor).prefix_lines
                        break
                    total += editor.line_count() + 1
                self.linenumbers.line_num_offset = total
        self.custom_on_change.append(on_change)

        try:
            # they decided to make linux a special case for no apparent reason
            self.text.bind('<Shift-ISO_Left_Tab>', lambda e: self.do_untab())
        except:
            self.text.bind('<Shift-Tab>', lambda e: self.do_untab())

        self.text.bind(f'<{SYS_INFO["mod"]}-slash>', lambda e: self.do_autocomment())

        self.text.bind('<Tab>', lambda e: self.do_tab())
        self.text.bind('<BackSpace>', lambda e: self.do_backspace())
        self.text.bind('<Return>', lambda e: self.do_newline())

        if color_enabled:
            # source: https://stackoverflow.com/questions/38594978/tkinter-syntax-highlighting-for-text-widget
            cdg = colorizer.ColorDelegator()

            props = set()
            for T in [netsblox.turtle.TurtleBase, netsblox.turtle.StageBase]:
                for key in dir(T):
                    if not key.startswith('_') and not key.endswith('_') and isinstance(getattr(T, key), property):
                        props.add(key)

            def get_pattern(p): # newer versions of python don't allow concatenating pattern objects directly
                return getattr(p, 'pattern') if hasattr(p, 'pattern') else p
            patterns = [
                rf'\.(?P<MYPROP>{"|".join(props)})\b',
                r'(?P<MYDECO>@(\w+\.)*\w+)\b',
                r'\b(?P<MYSELF>self)\b',
                r'\b(?P<MYNUMBER>(\d+\.?|\.\d)\d*(e[-+]?\d+)?)\b',
                get_pattern(colorizer.make_pat()),
            ]
            cdg.prog = re.compile('|'.join(patterns))

            cdg.tagdefs['COMMENT']    = {'foreground': '#a3a3a3' if IS_DARK else '#a3a3a3', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['MYNUMBER']   = {'foreground': '#e8821c' if IS_DARK else '#c26910', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['MYSELF']     = {'foreground': '#fc72d0' if IS_DARK else '#d943aa', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['MYPROP']     = {'foreground': '#fc72d0' if IS_DARK else '#d943aa', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['BUILTIN']    = {'foreground': '#b576f5' if IS_DARK else '#6414b5', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['DEFINITION'] = {'foreground': '#b576f5' if IS_DARK else '#6414b5', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['MYDECO']     = {'foreground': '#b576f5' if IS_DARK else '#6414b5', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['KEYWORD']    = {'foreground': '#5b96f5' if IS_DARK else '#0d15b8', 'background': COLOR_INFO['text-background']}
            cdg.tagdefs['STRING']     = {'foreground': '#f24141' if IS_DARK else '#961a1a', 'background': COLOR_INFO['text-background']}

            percolator.Percolator(self.text).insertfilter(cdg)

        if force_enabled:
            def trigger():
                self.update_timer = None
                self.show_full_help()
            def delayed_show_full_help():
                if self.update_timer is not None:
                    self.after_cancel(self.update_timer)
                self.update_timer = self.after(SUGGESTION_UPDATE_INTERVAL, trigger)
            self.custom_on_change.append(delayed_show_full_help)

            # this one really should be ctrl+space on all platforms
            self.text.bind('<Control-Key-space>', lambda e: self.show_suggestion())

    def line_count(self):
        if self.__line_count:
            return self.__line_count
        content = self.get_script() # defined by base classes
        self.__line_count = content.count('\n') + 1
        return self.__line_count

    def show_full_help(self):
        if not force_enabled or content is None or content.project is None:
            return
        if self.text.compare('end-1c', '==', '1.0'):
            return # if our text is empty, don't do anything

        script = jedi.Script(content.project.get_full_script())
        self.update_highlighting(script)

        should_show = \
            self.text.get('insert - 1 chars', 'insert').startswith('.') or \
            self.text.get('insert - 1 chars wordstart - 1 chars', 'insert').startswith('.')

        self.show_docs(script)

        if should_show and not self.text.tag_ranges(tk.SEL):
            self.show_suggestion(script)
        else:
            self.hide_suggestion()

    def update_highlighting(self, script):
        if not force_enabled or content is None or content.project is None:
            return

        self.text.tag_delete('jedi-syntax-err')
        for err in script.get_syntax_errors():
            start = f'{err.line       - self.linenumbers.line_num_offset}.{err.column       - self.column_offset}'
            stop  = f'{err.until_line - self.linenumbers.line_num_offset}.{err.until_column - self.column_offset}'
            self.text.tag_add('jedi-syntax-err', start, stop)
        self.text.tag_configure('jedi-syntax-err', underline = True, underlinefg = 'red', background = '#f2a5a5', foreground = 'black')

    def total_pos(self):
        edit_line, edit_col = map(int, self.text.index(tk.INSERT).split('.'))
        edit_line += self.linenumbers.line_num_offset
        edit_col += self.column_offset
        return edit_line, edit_col

    def show_docs(self, script):
        if not force_enabled or content is None or content.project is None:
            return

        edit_line, edit_col = self.total_pos()
        docs = script.help(edit_line, edit_col)

        def get_docstring(items) -> str:
            res = []
            for item in items:
                mapped = FULL_NAME_DOC_REMAPS.get(item.full_name)
                if mapped is not None:
                    return mapped

                if item.column is not None and item.column > 0 and item.get_line_code()[item.column - 1] == '.':
                    mapped = PROP_DOC_REMAPS.get(item.name)
                    if mapped is not None:
                        return mapped

                desc = item.description
                if desc.startswith('keyword') or desc.startswith('instance'):
                    continue

                x = item.docstring()
                if x:
                    res.append(x)
            return '\n\n----------\n\n'.join(res)
        docs = get_docstring(docs)

        if docs: # if nothing to show, don't change the display
            clean = clean_docstring(docs)
            content.display.docs.set_text(clean)

    def show_suggestion(self, script = None):
        if not force_enabled or content is None or content.project is None:
            return
        if script is None:
            script = jedi.Script(content.project.get_full_script())

        edit_line, edit_col = self.total_pos()
        completions = script.complete(edit_line, edit_col)

        should_show = len(completions) >= 2 or (len(completions) == 1 and completions[0].complete != '')
        if should_show:
            if self.help_popup is not None:
                self.help_popup.destroy()

            try:
                x, y, w, h = self.text.bbox(tk.INSERT)
            except:
                return

            self.help_popup = tk.Listbox()
            self.help_completions = {}

            xoff = self.text.winfo_rootx() - root.winfo_rootx()
            yoff = self.text.winfo_rooty() - root.winfo_rooty()
            self.help_popup.place(x = x + xoff, y = y + yoff + h)
            for item in completions:
                if not item.name.startswith('_'): # hide private stuff - would only confuse beginners and they shouldn't touch it anyway
                    self.help_popup.insert(tk.END, item.name)
                    self.help_completions[item.name] = item.complete

            self.help_popup.bind('<Double-Button-1>', lambda e: self.do_completion())
        else:
            self.hide_suggestion()

    def do_completion(self):
        # complete any pending update actions
        if self.update_timer is not None:
            self.after_cancel(self.update_timer)
            self.update_timer = None
            self.show_full_help()

        # if we're still showing help, complete with the up-to-date value
        if self.help_popup is not None:
            completion = self.help_completions[self.help_popup.get(tk.ACTIVE)]
            self.text.insert(tk.INSERT, completion)
        self.text.focus_set()

    def hide_suggestion(self):
        if self.help_popup is not None:
            self.help_popup.destroy()
            self.help_popup = None

    def _do_batch_edit(self, mutator):
        ins = self.text.index(tk.INSERT)
        sel_start, sel_end = (self.text.index(tk.SEL_FIRST), self.text.index(tk.SEL_LAST)) if self.text.tag_ranges(tk.SEL) else (ins, ins)
        sel_padded = f'{sel_start} linestart', f'{sel_end} lineend'

        ins_pieces = ins.split('.')
        sel_start_pieces, sel_end_pieces = sel_start.split('.'), sel_end.split('.')

        content = self.text.get(*sel_padded)
        mutated, line_deltas = mutator(content)
        ins_delta = line_deltas[int(ins_pieces[0]) - int(sel_start_pieces[0])]

        self.text.edit_separator()
        self.text.delete(*sel_padded)
        self.text.insert(sel_padded[0], mutated)
        self.text.edit_separator()

        new_sel_start = f'{sel_start_pieces[0]}.{max(0, int(sel_start_pieces[1]) + line_deltas[0])}'
        new_sel_end = f'{sel_end_pieces[0]}.{max(0, int(sel_end_pieces[1]) + line_deltas[-1])}'
        new_ins = f'{ins_pieces[0]}.{max(0, int(ins_pieces[1]) + ins_delta)}'

        self.text.tag_add(tk.SEL, new_sel_start, new_sel_end)
        self.text.mark_set(tk.INSERT, new_ins)

    def do_newline(self):
        line = self.text.get('insert linestart', 'insert')
        white, _ = get_white_nonwhite(line)
        if line.endswith(':'):
            white += '    '
        self.text.insert('insert', '\n' + white)
        self.text.see('insert')
        return 'break'

    def do_backspace(self):
        # if there's a selection, use default behavior
        if self.text.tag_ranges(tk.SEL):
            return

        # otherwise try deleting back to a tab stop
        col = int(self.text.index(tk.INSERT).split('.')[1])
        if col != 0:
            del_count = (col % 4) or 4 # delete back to previous tab column
            pos = f'insert-{del_count}c'
            if self.text.get(pos, 'insert').isspace():
                self.text.delete(pos, 'insert')
                return 'break' # override default behavior
    def do_untab(self):
        if self.text.tag_ranges(tk.SEL):
            self._do_batch_edit(undent_info)

        return 'break'
    def do_tab(self):
        if self.text.tag_ranges(tk.SEL):
            self._do_batch_edit(indent_info)
        elif self.help_popup is not None:
            self.do_completion()
        else:
            self.text.insert(tk.INSERT, '    ')

        return 'break' # we always override default (we don't want tabs ever)

    def do_autocomment(self):
        self._do_batch_edit(smart_comment_uncomment)
        return 'break'

class GlobalEditor(CodeEditor):
    BASE_PREFIX = '''
import netsblox
from netsblox import get_location, get_error, nothrow
from netsblox.turtle import *
from netsblox.concurrency import *
nb = $client_type(project_name = """$project_name""", project_id = $project_id)
'A connection to NetsBlox, which allows you to use services and RPCs from python.'
netsblox.turtle._INITIAL_SIZE = $stage_size
getattr(netsblox.turtle._get_proj_handle(), '_Project__tk').title(f'PyBlox - {nb.public_id}')
nb.set_room($room_handle)
setup_stdio()
setup_yielding()
import time as _time
def _yield_(x):
    _time.sleep(0)
    return x

'''.lstrip()
    BASE_PREFIX_LINES = 16

    prefix = BASE_PREFIX
    prefix_lines = BASE_PREFIX_LINES
    blocks = []
    name = 'global'

    def __init__(self, parent, *, value: str):
        super().__init__(parent, blocks = GlobalEditor.blocks)
        self.set_text(value)

    def get_script(self, *, is_export: bool = False):
        client_type = {
            'editor': 'netsblox.Client',
            'dev': 'netsblox.dev.Client',
        }[content.project.client_type]

        pre = GlobalEditor.prefix
        pre = pre.replace('$client_type', client_type)
        pre = pre.replace('$project_name', main_menu.project_name)
        pre = pre.replace('$project_id', 'None' if is_export else f'\'{content.project.project_id}\'')

        role = content.project.roles[content.project.active_role]
        width, height = role['stage_size']
        pre = pre.replace('$stage_size', f'({width}, {height})')

        room = main_menu.room_manager
        role_str = f'\'{content.project.roles[content.project.active_role]["name"]}\''
        room_id_str = f'\'{room.room_id}\''
        password_str = 'None' if room.room_password is None else f'\'{room.room_password}\''
        pre = pre.replace('$room_handle', 'None' if is_export or room.room_name is None else f'netsblox.rooms.RuntimeRoomManager(client = nb, role = {role_str}, room_id = {room_id_str}, password = {password_str})')

        return pre + self.text.get('1.0', 'end-1c')

class StageEditor(CodeEditor):
    prefix_lines = 3
    blocks = []

    def __init__(self, parent, *, name: str, value: str):
        super().__init__(parent, blocks = StageEditor.blocks, column_offset = 4) # we autoindent the content, so 4 offset for error messages
        self.name = name
        self.set_text(value)

    def get_script(self, *, is_export: bool = False):
        raw = self.text.get('1.0', 'end-1c')
        return f'@netsblox.turtle.stage\nclass {self.name}(netsblox.turtle.StageBase):\n    pass\n{indent(raw)}\n{self.name} = {self.name}()'

class TurtleEditor(CodeEditor):
    prefix_lines = 3
    blocks = []

    def __init__(self, parent, *, name: str, value: str):
        super().__init__(parent, blocks = TurtleEditor.blocks, column_offset = 4) # we autoindent the content, so 4 offset for error messages
        self.name = name
        self.set_text(value)

    def get_script(self, *, is_export: bool = False):
        raw = self.text.get('1.0', 'end-1c')
        return f'@netsblox.turtle.turtle\nclass {self.name}(netsblox.turtle.TurtleBase):\n    pass\n{indent(raw)}\n{self.name} = {self.name}()'

class Display(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pane = tk.PanedWindow(self, orient = tk.VERTICAL, **PANED_WINDOW_OPTS)
        self.pane.pack(fill = tk.BOTH, expand = True)

        self.docs_frame = tk.Frame(self.pane)
        self.docs_label = tk.Label(self.docs_frame, text = 'Documentation')
        self.docs = ScrolledText(self.docs_frame, readonly = True)
        self.docs.text.configure(wrap = tk.WORD)
        self.docs_label.pack(side = tk.TOP)
        self.docs.pack(fill = tk.BOTH, expand = True)

        self.terminal_frame = tk.Frame(self.pane)
        self.terminal_label = tk.Label(self.terminal_frame, text = 'Program Output')
        self.terminal = TerminalOutput(self.terminal_frame)
        self.terminal_label.pack(side = tk.TOP)
        self.terminal.pack(fill = tk.BOTH, expand = True)

        self.pane.add(self.docs_frame, stretch = 'always', minsize = 100)
        self.pane.add(self.terminal_frame, stretch = 'always', minsize = 100)

class TerminalOutput(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__last_line_len = 0

        self.text = ScrolledText(self, readonly = True)
        self.text.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        self.text.text.config(bg = '#1a1a1a', fg = '#bdbdbd', insertbackground = '#bdbdbd')

        self.__char_width = self.text.font.measure('m')

    def wrap_stdio(self, *, tee: bool):
        _print_targets.append(self)

        class TeeWriter:
            encoding = 'utf-8'

            def __init__(self, old):
                self.old = old

            def write(self, data):
                data = str(data)
                if self.old is not None:
                    self.old.write(data)
                    self.old.flush()
                _print_queue.put(data)

            def flush(self):
                pass
            def __len__(self):
                return 0

        sys.stdout = TeeWriter(sys.stdout if tee else None)
        sys.stderr = TeeWriter(sys.stderr if tee else None)

    def __append_intraline(self, line: str) -> None:
        max_line_len = max(1, (self.text.text.winfo_width() - 8) // self.__char_width)

        pos = 0
        remaining = len(line)
        while remaining > 0:
            can_add = min(remaining, max_line_len - self.__last_line_len)
            if can_add <= 0:
                self.text.text.insert('end', '\n')
                self.__last_line_len = 0
                continue

            self.text.text.insert('end', line[pos:pos+can_add])
            self.text.text.see('end')
            self.__last_line_len += can_add

            pos += can_add
            remaining -= can_add

    def write(self, txt):
        lines = common.inclusive_splitlines(str(txt))
        for i in range(len(lines)):
            self.__append_intraline(lines[i])
            if i < len(lines) - 1:
                self.text.text.insert('end', '\n')
                self.text.text.see('end')
                self.__last_line_len = 0
    def write_line(self, txt):
        self.write(f'{txt}\n')

MENU_STYLE = { 'tearoff': False, 'relief': 'flat', 'bg': '#bdbdbd' }
class MainMenu(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent, **MENU_STYLE)

        self.project_path = None
        self.saved_project_dict = None

        def kill():
            if self.try_close_project():
                self.room_manager.destroy()
                root.destroy()
        root.protocol('WM_DELETE_WINDOW', kill)

        submenu = tk.Menu(self, **MENU_STYLE)
        submenu.add_command(label = 'New', command = lambda: self.open_project(super_proj = ProjectEditor.DEFAULT_PROJECT), accelerator = f'{SYS_INFO["mod-str"]}+N')
        submenu.add_command(label = 'Open', command = self.open_project, accelerator = f'{SYS_INFO["mod-str"]}+O')
        submenu.add_command(label = 'Import NetsBlox project', command = self.open_trans_xml)

        subsubmenu = tk.Menu(submenu, **MENU_STYLE)
        for file in sorted(os.listdir(f'{common._NETSBLOX_PY_PATH}/assets/examples/')):
            def make_opener(file):
                def opener():
                    with open(f'{common._NETSBLOX_PY_PATH}/assets/examples/{file}') as f:
                        content = json.load(f) # don't cache projects (could be large)
                    self.open_project(super_proj = content)
                return opener
            subsubmenu.add_command(label = file[:-5], command = make_opener(file))

        submenu.add_cascade(label = 'Example', menu = subsubmenu)
        submenu.add_separator()
        submenu.add_command(label = 'Save', command = self.save, accelerator = f'{SYS_INFO["mod-str"]}+S')
        submenu.add_command(label = 'Save As', command = self.save_as, accelerator = f'Shift+{SYS_INFO["mod-str"]}+S')
        submenu.add_separator()
        submenu.add_command(label = 'Export', command = self.export_as)
        submenu.add_separator()
        submenu.add_command(label = 'Exit', command = kill)
        self.add_cascade(label = 'File', menu = submenu)

        root.bind_all(f'<{SYS_INFO["mod"]}-n>', lambda e: self.open_project(super_proj = ProjectEditor.DEFAULT_PROJECT))
        root.bind_all(f'<{SYS_INFO["mod"]}-o>', lambda e: self.open_project())
        root.bind_all(f'<{SYS_INFO["mod"]}-s>', lambda e: self.save())
        root.bind_all(f'<{SYS_INFO["mod"]}-S>', lambda e: self.save_as())

        submenu = tk.Menu(self, **MENU_STYLE)
        global_font = tkfont.nametofont('TkFixedFont')
        def do_zoom(delta: int) -> None:
            new_size = max(min(global_font.cget('size') + delta, MAX_FONT_SIZE), MIN_FONT_SIZE)
            global_font.config(size = new_size)
            for editor in content.project.editors:
                editor.on_content_change(cause = 'zoom')
            return 'break'
        submenu.add_command(label = 'Zoom In', command = lambda: do_zoom(1), accelerator = f'{SYS_INFO["mod-str"]}++')
        submenu.add_command(label = 'Zoom Out', command = lambda: do_zoom(-1), accelerator = f'{SYS_INFO["mod-str"]}+-')
        self.add_cascade(label = 'View', menu = submenu)

        root.bind_all(f'<{SYS_INFO["mod"]}-plus>', lambda e: do_zoom(1))
        root.bind_all(f'<{SYS_INFO["mod"]}-equal>', lambda e: do_zoom(1)) # plus without needing shift
        root.bind_all(f'<{SYS_INFO["mod"]}-minus>', lambda e: do_zoom(-1))

        self.room_manager = rooms.EditorRoomManager(client = nb)

        self.roles_dropdown = tk.Menu(self, **MENU_STYLE)
        self.add_cascade(label = 'Roles', menu = self.roles_dropdown)

        submenu = tk.Menu(self, **MENU_STYLE)
        imp = content.project.imports
        imp_packages = list(imp.packages.items())
        for pkg, item in imp_packages:
            label = pkg if pkg == item['ident'] else f'{pkg} ({item["ident"]})'
            submenu.add_checkbutton(label = label, variable = item['tkvar'], command = imp.batch_update)
        self.add_cascade(label = 'Imports', menu = submenu)

        def get_info_shower(submenu):
            def show_info(e):
                entries = len(imp.packages)
                entry = int(e.y / (submenu.winfo_reqheight() / entries))
                if entry < 0 or entry >= entries: return

                pkg, item = imp_packages[entry]
                info = item['info']
                if info: content.display.docs.set_text(item['info'])
            return show_info
        submenu.bind('<Motion>', get_info_shower(submenu))

        self.images_dropdown = tk.Menu(self, **MENU_STYLE)
        self.add_cascade(label = 'Images', menu = self.images_dropdown)

        self.run_menu_entries = {}
        self.run_menu_seps = 0
        self.run_menu = tk.Menu(self, **MENU_STYLE)
        def add_run_menu_command(name: str, **kwargs):
            self.run_menu_entries[name] = len(self.run_menu_entries) + self.run_menu_seps
            self.run_menu.add_command(**kwargs)
        def add_run_menu_sep():
            self.run_menu.add_separator()
            self.run_menu_seps += 1

        def copy_pub_id():
            root.clipboard_clear()
            root.clipboard_append(self.public_id)
        add_run_menu_command('run-project', label = 'Run Project', command = play_button, accelerator = 'F5')
        add_run_menu_command('stop-project', label = 'Stop Project', command = play_button, state = tk.DISABLED)
        add_run_menu_sep()
        add_run_menu_command('copy-pub-id', label = 'Copy Public ID', command = copy_pub_id)
        self.add_cascade(label = 'Run', menu = self.run_menu)

        root.bind_all('<F5>', lambda e: play_button())

    @property
    def public_id(self):
        return f'{self._project_name}@{content.project.project_id}#py'
    @property
    def project_path(self):
        return self._project_path
    @project_path.setter
    def project_path(self, p):
        self._project_path = p
        self._project_name = 'untitled' if p is None else basename_noext(p)
        root.title(f'PyBlox - {self.public_id} ({"unsaved" if p is None else p})')
    @property
    def project_name(self):
        return self._project_name

    def save(self, save_dict = None) -> bool:
        if self.project_path is not None:
            try:
                if save_dict is None:
                    save_dict = content.project.get_save_dict()
                with open(self.project_path, 'w') as f:
                    json.dump(save_dict, f, separators = (', ', ': '), indent = 2)
                self.saved_project_dict = save_dict
                content.project.roles = save_dict['roles'] # sync the in-memory role content
                return True
            except Exception as e:
                messagebox.showerror('Failed to save project', str(e))
                return False
        else:
            return self.save_as(save_dict)
    def save_as(self, save_dict = None) -> bool:
        p = filedialog.asksaveasfilename(filetypes = PROJECT_FILETYPES, defaultextension = '.json')
        if type(p) is str and p: # despite the type hints, above returns empty tuple on cancel
            self.project_path = p
            return self.save(save_dict)
        return False

    def export_as(self) -> None:
        p = filedialog.asksaveasfilename(filetypes = PYTHON_FILETYPES, defaultextension = '.py')
        if type(p) is str and p: # despite the type hints, above returns empty tuple on cancel
            try:
                res = transform.add_yields(content.project.get_full_script(is_export = True))
                with open(p, 'w') as f:
                    f.write(res)
            except Exception as e:
                messagebox.showerror('Failed to save exported project', str(e))

    def open_project(self, *, super_proj: Optional[dict] = None, active_role: Optional[int] = None):
        content.project.on_tab_change()
        if not self.try_close_project(): return

        rstor = None
        p = None
        try:
            if super_proj is None:
                p = filedialog.askopenfilename(filetypes = PROJECT_FILETYPES)
                if type(p) is not str or not p:
                    return
                with open(p, 'r') as f:
                    super_proj = json.load(f)

            if content.project.roles is not None:
                rstor = content.project.get_save_dict() # in case load fails

            content.project.load(super_proj = super_proj, active_role = active_role)
            self.saved_project_dict = super_proj
            self.project_path = p
            self.update_roles()
        except Exception as e:
            messagebox.showerror('Failed to load project', str(e))
            if rstor is not None:
                content.project.load(rstor)

    def open_trans_xml(self):
        content.project.on_tab_change()
        if not self.try_close_project(): return

        try:
            p = filedialog.askopenfilename(filetypes = NB_PROJECT_FILETYPES)
            if type(p) is not str or not p:
                return
            with open(p, 'r') as f:
                xml = f.read()
            proj = json.loads(nb2pb.translate(xml)[1])
            self.open_project(super_proj = proj)
        except Exception as e:
            messagebox.showerror('Failed to import project', str(e))

    def switch_role(self, *, active_role: int):
        content.project.on_tab_change()
        if not self.try_close_project(): return

        content.project.load(active_role = active_role)
        self.update_roles()

    def try_close_project(self) -> bool: # true if user accepted close
        if self.saved_project_dict is None:
            return True # fires (only) on first initialization

        save_dict = content.project.get_save_dict()
        if save_dict == self.saved_project_dict:
            return True # if saved project content is equal, no need to do anything

        title = 'Save before closing'
        msg = 'Would you like to save your project before closing?'
        res = messagebox.askyesnocancel(title, msg)
        return res == False or (res == True and self.save(save_dict))

    def import_image(self):
        p = filedialog.askopenfilename(filetypes = IMAGE_FILETYPES)
        if type(p) is not str or not p:
            return

        img = None
        try:
            # make sure it can round-trip to b64 (also, this ensures any import format is converted to png)
            img = common.decode_image(common.encode_image(Image.open(p)))
        except Exception as e:
            messagebox.showerror(title = 'Failed to load image', message = str(e))
            return

        name = None
        while True:
            name = simpledialog.askstring(title = 'Name Image', prompt = 'Enter the name of the image, which is used to access it from code')
            if name is None: return
            if not is_valid_ident(name):
                messagebox.showerror('Invalid name', message = f'"{name}" is not a valid python variable name')
                continue
            if name in content.project.imports.images:
                messagebox.showerror(title = 'Invalid name', message = f'An image named {name} already exists')
                continue
            break

        content.project.imports.images[name] = img
        content.project.imports.batch_update()

    def update_images(self):
        self.images_dropdown.delete(0, 'end')
        self.images_dropdown.add_command(label = 'Import', command = self.import_image)

        if len(content.project.imports.images) != 0:
            self.images_dropdown.add_separator()

        for name, img in content.project.imports.images.items():
            submenu = tk.Menu(**MENU_STYLE)

            def get_viewer(img):
                return lambda: img.show()
            submenu.add_command(label = 'View', command = get_viewer(img))

            def get_deleter(name):
                def deleter():
                    title = f'Delete sprite {name}'
                    msg = f'Are you sure you would like to delete sprite {name}? This operation cannot be undone.'
                    if messagebox.askyesno(title, msg, icon = 'warning', default = 'no'):
                        del content.project.imports.images[name]
                        content.project.imports.batch_update()
                return deleter
            submenu.add_command(label = 'Delete', command = get_deleter(name))

            self.images_dropdown.add_cascade(label = f'{name} {img.width}x{img.height}', menu = submenu)

    def update_roles(self):
        self.roles_dropdown.delete(0, 'end')

        submenu = tk.Menu(**MENU_STYLE)

        def create_room():
            password = simpledialog.askstring(title = 'New Room Password', prompt = 'Password for the new room (or nothing for no password)')
            if password is None: return
            if password == '': password = None
            try:
                self.room_manager.create_room(password)
                messagebox.showinfo('Created Room', message = f'Created Room\nName: {self.room_manager.room_name}\n\nOther clients can join with\nRole > Room > Join Room')
            except Exception as e:
                messagebox.showerror('Failed to create room', message = str(e))
            self.update_roles()
        submenu.add_command(label = 'Create New Room', command = create_room)

        def join_room():
            room_name = simpledialog.askstring(title = 'Room Name', prompt = 'Enter the name of the room to join')
            if room_name is None or room_name == '': return
            password = simpledialog.askstring(title = 'Room Password', prompt = f'Password for room \'{room_name}\' (or nothing if no password)')
            if password is None: return
            if password == '': password = None
            try:
                self.room_manager.join_room(room_name, password)
                messagebox.showinfo('Joined Room', message = f'Joined Room\nName: {self.room_manager.room_name}')
            except Exception as e:
                messagebox.showerror('Failed to join room', message = str(e))
            self.update_roles()
        submenu.add_command(label = 'Join Room', command = join_room)

        def leave_room():
            self.room_manager.leave_room()
            self.update_roles()
        submenu.add_command(label = f'Leave Room ({self.room_manager.room_name})' if self.room_manager.room_name is not None else 'Leave Room',
            command = leave_room, state = tk.ACTIVE if self.room_manager.room_name is not None else tk.DISABLED)

        self.roles_dropdown.add_cascade(label = 'Room', menu = submenu)

        def prompt_role_name(*, title: str, prompt: str) -> Optional[str]:
            while True:
                name = simpledialog.askstring(title = title, prompt = prompt)
                if name is None: return None
                if not is_valid_ident(name):
                    messagebox.showerror('Invalid name', message = f'"{name}" is not a valid python variable name')
                    continue
                if any(x['name'] == name for x in content.project.roles):
                    messagebox.showerror(title = 'Invalid name', message = f'A role named {name} already exists.')
                    continue
                return name
        def prompt_canvas_size(*, title: str, prompt: str) -> Optional[Tuple[int, int]]:
            while True:
                value = simpledialog.askstring(title = title, prompt = prompt)
                if value is None: return None
                res = parse_size(value)
                if res is None:
                    messagebox.showerror('Invalid canvas size', message = f'\'{value}\' is not a valid canvas size. Should be a width and height pair like \'720x480\'')
                    continue
                if any(res[i] < MIN_CANV_SIZE[i] or res[i] > MAX_CANV_SIZE[i] for i in range(2)):
                    messagebox.showerror('Invalid canvas size', message = f'Size {res[0]}x{res[1]} is not a valid canvas size. Width should be [{MIN_CANV_SIZE[0]}, {MAX_CANV_SIZE[0]}] and height should be [{MIN_CANV_SIZE[1]}, {MAX_CANV_SIZE[1]}].')
                    continue
                return res

        def make_role():
            name = prompt_role_name(title = 'Name Role', prompt = 'Enter the name of the new role, which should be a valid variable name')
            if name is None: return
            role = copy.deepcopy(ProjectEditor.DEFAULT_PROJECT['roles'][0])
            role['name'] = name
            content.project.roles.append(role)
            self.update_roles()
        self.roles_dropdown.add_command(label = 'New Role', command = make_role)

        if len(content.project.roles) != 0:
            self.roles_dropdown.add_separator()

        for i, role in enumerate(content.project.roles):
            submenu = tk.Menu(**MENU_STYLE)
            is_current = i == content.project.active_role

            def get_switcher(idx):
                def do_switch():
                    if idx == content.project.active_role: return # sanity check
                    self.switch_role(active_role = idx)
                return do_switch
            submenu.add_command(label = 'Open', command = get_switcher(i), state = tk.DISABLED if is_current else tk.ACTIVE)

            def get_deleter(idx):
                def do_delete():
                    if idx == content.project.active_role:
                        messagebox.showerror('Cannot delete active role', 'To delete this role, open a different role first')
                        return

                    name = content.project.roles[idx]['name']
                    title = f'Delete role {name}'
                    msg = f'Are you sure you would like to delete role {name}? This operation cannot be undone.'
                    if messagebox.askyesno(title, msg, icon = 'warning', default = 'no'):
                        del content.project.roles[idx]
                        if content.project.active_role >= idx:
                            content.project.active_role -= 1
                        self.update_roles()
                return do_delete
            submenu.add_command(label = 'Delete', command = get_deleter(i), state = tk.DISABLED if is_current else tk.ACTIVE)

            submenu.add_separator()

            def renamer(idx):
                def do_rename():
                    old_name = content.project.roles[idx]['name']
                    name = prompt_role_name(title = 'Rename Role', prompt = f'Enter the new name for role {old_name}, which should be a valid variable name')
                    if name is None: return
                    content.project.roles[idx]['name'] = name
                    self.update_roles()
                return do_rename
            submenu.add_command(label = 'Rename', command = renamer(i))

            def duplicator(idx, is_current):
                def do_duplicate():
                    src = content.project.roles[idx]
                    name = prompt_role_name(title = 'Duplicate Role', prompt = f'Duplicating role {src["name"]}. Enter the name for the new role, which should be a valid variable name')
                    if name is None: return
                    role = copy.deepcopy(src) if not is_current else content.project.get_save_dict()['roles'][idx]
                    role['name'] = name
                    content.project.roles.append(role)
                    self.update_roles()
                return do_duplicate
            submenu.add_command(label = 'Duplicate', command = duplicator(i, is_current))

            def canvas_resizer(idx):
                def do_resize():
                    src = content.project.roles[idx]
                    old_size = src['stage_size']
                    new_size = prompt_canvas_size(title = f'Resize Canvas', prompt = f'Resizing canvas for role {src["name"]} (old size {old_size[0]}x{old_size[1]}). Enter the new size, which should be a width/height pair like \'720x480\'.')
                    if new_size is None: return
                    src['stage_size'] = new_size
                    self.update_roles()
                return do_resize
            width, height = role['stage_size']
            submenu.add_command(label = f'Canvas Size ({width}x{height})', command = canvas_resizer(i))

            self.roles_dropdown.add_cascade(label = f'{role["name"]} (active)' if is_current else role['name'], menu = submenu)

def main():
    global nb, root, main_menu, content

    nb = netsblox.Client()

    root = tk.Tk()
    root.geometry('1200x600')
    root.minsize(width = 800, height = 400)

    style = ttk.Style(root)
    style.configure('TNotebook', tabposition = 'n')

    logo = common.load_tkimage(f'netsblox://assets/img/logo/logo-256.png')
    root.iconphoto(True, logo)

    content = Content(root)
    main_menu = MainMenu(root)

    if len(sys.argv) <= 1:
        main_menu.open_project(super_proj = ProjectEditor.DEFAULT_PROJECT)
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            save_dict = json.load(f)
        main_menu.open_project(super_proj = save_dict)
        main_menu.project_path = os.path.abspath(sys.argv[1])
    else:
        print(f'usage: {sys.argv[0]} (project)', file = sys.stderr)
        sys.exit(1)

    root.configure(menu = main_menu)
    content.display.terminal.wrap_stdio(tee = True)

    _process_print_queue()
    root.mainloop()

if __name__ == '__main__':
    main()
