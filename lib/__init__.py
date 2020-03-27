# ---------------------------------------------------------------------------
# Copyright © 2017-2019 Brian M. Clapper
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------------------

'''
Helper functions
'''

import importlib.util
import sys
import os
from shutil import *
import yaml
from contextlib import contextmanager
import re
from textwrap import TextWrapper
from glob import glob
import codecs
from typing import Any, Sequence, Dict, Mapping, Generator, Union, TextIO

try:
    _columns = int(os.getenv('COLUMNS', '80'))
except Exception:
    _columns = 80

_ALERT_PREFIX = '*** '
_alert_wrapper = TextWrapper(width=_columns - 1,
                             subsequent_indent=' ' * len(_ALERT_PREFIX))


def import_from_file(path: str, module_name: str) -> Any:
    """
    Import a file as a module.

    Parameters:
    - path: the path to the Python file
    - module_name: the name to assign the module_from_spec

    Returns: the module object
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    sys.modules[module_name] = mod
    return mod

@contextmanager
def open_file(path: str,
              mode: str = 'r',
              encoding='utf-8') -> Generator[TextIO, None, None]:
    """
    Convenient front-end to codecs.open
    """
    with codecs.open(path, mode=mode, encoding=encoding) as f:
        yield f


def find_local_images(markdown_files: Sequence[str]) -> Sequence[str]:
    from urllib.parse import urlparse
    image_pat = re.compile(r'^\s*!\[.*\]\(([^\)]+)\).*$')

    images = []
    for f in markdown_files:
        if not os.path.exists(f):
            continue
        with open_file(f, mode='r') as md:
            for line in md.readlines():
                m = image_pat.match(line)
                if not m:
                    continue
                p = urlparse(m.group(1))
                if p.scheme:
                    continue
                images.append(m.group(1))

    return images


def file_or_default(path: str, default: str) -> str:
    """
    Return `path` if it exists, or `default` if not.

    Parameters:

    path:    path to file to test
    default: default file
    """
    if os.path.isfile(path):
        return path

    if not os.path.isfile(default):
        abort(f'Default file {default} does not exist or is not a file.')

    return default


def maybe_file(path: str) -> Sequence[str]:
    """
    Intended to be used when creating a list of files, this function
    determines whether a file exists, returning the file name in a list if
    so, and returning an empty list if not.

    Parameters:

    path: the path to test
    """
    if os.path.exists(path):
        return [path]
    else:
        return []


def alert(message: str) -> None:
    """
    Issue an alert message, which is prefixed and word-wrapped.

    :param message:
    :return:
    """
    print(_alert_wrapper.fill(f'{_ALERT_PREFIX}{message}'), file=sys.stderr)


def msg(message: str) -> None:
    """
    Display a message on standard error. Automatically adds a newline.
    I could just use print(), but this approach allows for adding a prefix
    later, if I feel like it.

    Parameters:

    message: the message to display
    """
    print(message, file=sys.stderr)


def abort(message: str) -> None:
    """
    Aborts with a message.

    Parameters:

    message: the message
    """
    msg(message)
    sys.exit(1)


def sh(command: str) -> None:
    """
    Runs a shell command, exiting if the command fails.

    Parameters:

    command: the command to run
    """
    import subprocess
    msg(command)
    try:
        rc = subprocess.call(command, shell=True)
        if rc < 0:
            abort(f'Command aborted by signal {-rc}')
    except OSError as e:
        abort(f'Command failed: {e}')


def load_metadata(metadata_file: str) -> Dict[str, Any]:
    """
    Loads a YAML metadata file, returning the loaded dictionary.

    Parameters:

    metadata_file; path to the file to load
    """
    if os.path.exists(metadata_file):
        with open_file(metadata_file, mode='r') as f:
            s = ''.join([s for s in f if not s.startswith('---')])
            metadata = yaml.load(s, Loader=yaml.FullLoader)
    else:
        metadata = {}

    return metadata


def validate_metadata(dict_like: Mapping[str, Any]) -> None:
    """
    Validates metadata that's been loaded into a dictionary-like object.
    Throws an exception if a required key is missing.
    """
    for key in ('title', 'author', 'copyright.owner', 'copyright.year',
                'publisher', 'language', 'genre'):
        # Drill through composite keys.
        keys = key.split('.') if '.' in key else [key]
        d = dict_like
        v = None
        for k in keys:
            v = d.get(k)
            d = v if v else {}

        if not v:
            abort(f'Missing required "{key}" in metadata.')


def _valid_dir(directory: str) -> bool:
    return (directory not in ('.', '..')) and (len(directory) > 0)


@contextmanager
def ensure_dir(directory: str,
               autoremove: bool = False) -> Generator[None, None, None]:
    """
    Run a block in the context of a directory that is created if it doesn't
    exist.

    Parameters:

    dir:   the directory
    remove: if True, remove the directory when the "with" block finishes.
    """
    try:
        if _valid_dir(directory):
            os.makedirs(directory, exist_ok=True)
        yield
    finally:
        if autoremove:
            if os.path.exists(directory):
                rmtree(directory)


@contextmanager
def target_dir_for(file: str,
                   autoremove: bool = False) -> Generator[None, None, None]:
    """
    Context manager that ensures that the parent directory of a file exists.

    Parameters:

    file:   the file
    remove: if True, remove the directory when the "with" block finishes.
    """
    directory = os.path.dirname(file)
    try:
        if _valid_dir(directory):
            os.makedirs(directory, exist_ok=True)
        yield
    finally:
        if autoremove:
            if os.path.exists(directory):
                rmtree(directory)


@contextmanager
def preprocess_markdown(
        tmp_dir: str,
        files: Sequence[str],
        divs: bool = False) -> Generator[Sequence[str], None, None]:
    """
    Content manager that preprocesses the Markdown files, adding some content
    and producing new, individual files.

    Parameters:

    tmp_dir - the temporary directory for the preprocessed files
    files   - the list of files to process
    divs    - True to generate a <div> with a file-based "id" attribute and
              'class="book_section"' around each Markdown file. Only really
              useful for HTML.

    Yields the paths to the generated files
    """
    file_without_dashes = re.compile(r'^[^a-z]*([a-z]+).*$')

    directory = os.path.join(tmp_dir, 'preprocessed')
    from_to = [(f, os.path.join(directory, os.path.basename(f))) for f in files]
    generated = [t for f, t in from_to]
    with ensure_dir(directory, autoremove=True):
        for f, temp in from_to:
            with open_file(temp, mode="w") as t:
                basefile, ext = os.path.splitext(os.path.basename(f))
                m = file_without_dashes.match(basefile)
                if m:
                    cls = m.group(1)
                else:
                    cls = basefile

                # Added classes to each section. Can be used in CSS.
                if divs and ext == ".md":
                    t.write(f'<div class="book_section" id="section_{cls}">\n')
                with open_file(f, mode='r') as input_file:
                    for line in input_file.readlines():
                        t.write(f"{line.rstrip()}\n")
                # Force a newline after each file.
                t.write("\n")
                if divs and ext == ".md":
                    t.write('</div>\n')
                t.close()
        yield generated


def rm_rf(paths: Union[str, Sequence[str]], silent: bool = False) -> None:
    """
    Recursively remove one or more files.

    paths - a list or tuple of paths, or a string of one path
    silent - whether or not to make noise about what's going on
    """
    def do_rm(path):
        if os.path.isdir(path):
            if not silent:
                msg(f'rm -rf {path}')
            rmtree(path)
        else:
            rm_f(path)

    if isinstance(paths, list) or isinstance(paths, tuple):
        for f in paths:
            do_rm(f)
    elif isinstance(paths, str):
        do_rm(paths)
    else:
        from doit import TaskError
        raise TaskError('rm_f() expects a list, a tuple or a string.')


def find_in_path(command: str) -> str:
    """
    Find a command in the path, or bail.

    :param command:  the command to find
    :return: the location. Throws an exception otherwise.
    """
    path = [p for p in os.getenv('PATH', '').split(os.pathsep) if len(p) > 0]
    for d in path:
        p = os.path.join(d, command)
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    else:
        raise OSError(f"""Can't find "{command}" in PATH.""")


def mkdirp(directory: str) -> None:
    """
    Equivalent of "mkdir -p".

    :param directory: The directory to be created, along with any intervening
                      parent directories that don't exist.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def rm_f(paths: Union[Sequence[str], str], silent: bool = False) -> None:
    """
    Remove one or more files.

    paths - a list or tuple of paths, or a string of one path
    silent - whether or not to make noise about what's going on
    """
    def do_rm(path):
        if not silent:
            msg(f"rm -f {path}")
        if os.path.exists(path):
            os.unlink(path)

    if isinstance(paths, list) or isinstance(paths, tuple):
        for f in paths:
            do_rm(f)
    elif isinstance(paths, str):
        do_rm(paths)
    else:
        from doit import TaskError
        raise TaskError('rm_f() expects a list, a tuple or a string.')


def fix_epub(epub: str, book_title: str, temp_dir: str) -> None:
    """
    Make some adjustments to the generated tables of contents in the ePub,
    removing empty elements and removing items matching the book title.

    Parameters:

    epub:       The path to the epub file
    book_title: The book title
    temp_dir:   Temporary directory to use for unpacking
    """
    from zipfile import ZipFile, ZIP_DEFLATED
    from xml.dom import minidom
    from grizzled.os import working_directory

    rm_rf(temp_dir, silent=True)

    def zip_add(zf, path, zippath):
        """Swiped from zipfile module."""
        if os.path.isfile(path):
            zf.write(path, zippath, ZIP_DEFLATED)
        elif os.path.isdir(path):
            if zippath:
                zf.write(path, zippath)
            for nm in os.listdir(path):
                zip_add(zf,
                        os.path.join(path, nm), os.path.join(zippath, nm))

    def unpack_epub():
        # Assumes pwd is *not* unpack directory.
        msg(f'.. Unpacking {epub}.')
        with ZipFile(epub) as z:
            z.extractall(temp_dir)

    def repack_epub():
        # Assumes pwd is *not* unpack directory.
        msg(f'.. Packing new {epub}.')
        with ZipFile(epub, 'w') as z:
            with working_directory(temp_dir):
                for f in os.listdir('.'):
                    if f in ['..', '.']:
                        continue
                    zip_add(z, f, f)

    def strip_text_children(element):
        for child in element.childNodes:
            if type(child) == minidom.Text:
                element.removeChild(child)

    def get_text_children(element):
        text = None
        if element:
            s = ''
            for child in element.childNodes:
                if child and (type(child) == minidom.Text):
                    s += child.data.strip()
            text = s if s else None
        return text

    def fix_toc_ncx(table_of_contents):
        # Assumes pwd *is* unpack directory
        msg(f'.. Reading table of contents file "{table_of_contents}".')
        with open_file(table_of_contents) as f:
            toc_xml = f.read()

        msg('.. Adjusting table of contents.')
        with minidom.parseString(toc_xml) as dom:
            nav_map = dom.getElementsByTagName('navMap')
            if not nav_map:
                abort('Malformed table of contents: No <navMap>.')
            nav_map = nav_map[0]
            for p in nav_map.getElementsByTagName('navPoint'):
                text_nodes = p.getElementsByTagName('text')
                text = None
                if text_nodes:
                    text = get_text_children(text_nodes[0])

                if (not text) or (text == book_title):
                    nav_map.removeChild(p)

            # Renumber the nav points.
            for i, p in enumerate(nav_map.getElementsByTagName('navPoint')):
                num = i + 1
                p.setAttribute('id', f'navPoint-{num}')

            # Strip any text nodes from the navmap.
            strip_text_children(nav_map)

            # Write it out.
            with open_file(toc, mode='w') as f:
                dom.writexml(f)

    def fix_nav_xhtml(table_of_contents):
        # Assumes pwd *is* unpack directory
        msg(f'.. Reading table of contents file "{table_of_contents}".')
        with open_file(table_of_contents) as f:
            toc_xml = f.read()

        msg('.. Adjusting table of contents.')
        with minidom.parseString(toc_xml) as dom:
            navs = dom.getElementsByTagName('nav')
            nav = None
            for n in navs:
                if not n.hasAttributes():
                    continue
                a = n.attributes.get('id')
                if not a:
                    continue
                if a.value == 'toc':
                    nav = n
                    break
            else:
                abort('Malformed table of contents: No TOC <nav>.')

            ol = nav.getElementsByTagName('ol')
            if (not ol) or (len(ol) == 0):
                abort('Malformed table of contents: No list in <nav>.')
            ol = ol[0]

            for li in ol.getElementsByTagName('li'):
                a = li.getElementsByTagName('a')
                if not a:
                    abort('Malformed table of contents: No <a> in <li>.')
                a = a[0]
                text = get_text_children(a)
                if (not text) or (text == book_title):
                    ol.removeChild(li)

            # Renumber the list items
            for i, li in enumerate(ol.getElementsByTagName('li')):
                num = i + 1
                li.setAttribute('id', f'toc-li-{num}')

            # Strip any text nodes from the ol.
            strip_text_children(ol)

            # Write it out.
            with open_file(toc, mode='w') as f:
                dom.writexml(f)

    def fix_chapter_files():
        msg('.. Fixing titles in chapter files...')
        title_pat = re.compile(r'^(.*<title>).*(</title>).*$')

        def fix_chapter_file(path, title):
            with open_file(path) as f:
                lines = [l.rstrip() for l in f.readlines()]
            with open_file(path, mode='w') as f:
                for line in lines:
                    m = title_pat.match(line)
                    if m:
                        line = f'{m.group(1)}{title}{m.group(2)}'
                    f.write(f'{line}\n')

        for file in glob('EPUB/text/ch*.xhtml'):
            fix_chapter_file(file, title=book_title)

    # Main logic
    try:
        unpack_epub()
        with ensure_dir(temp_dir):
            with working_directory(temp_dir):
                paths_and_funcs = (
                    (os.path.join('EPUB', 'toc.ncx'), fix_toc_ncx),
                    (os.path.join('EPUB', 'nav.xhtml'), fix_nav_xhtml),
                )
                for toc, func in paths_and_funcs:
                    if not os.path.exists(toc):
                        msg(f'.. No {toc} file. Skipping it.')
                        continue
                    func(toc)

                fix_chapter_files()

        repack_epub()
    finally:
        #rmtree(temp_dir)
        pass
