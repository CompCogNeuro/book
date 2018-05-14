#!/usr/local/bin/python3

# ---------------------------------------------------------------------------
# Copyright (C) 2017 Brian M. Clapper
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

"""
Pandoc filter to convert transform special sequences on a per-format basis.

See the top-level README.md file for what's supported.

See http://scorreia.com/software/panflute/ and
https://github.com/jgm/pandoc/wiki/Pandoc-Filters
"""

import sys
from panflute import *
import os
from itertools import dropwhile, takewhile

# Need the lib module. Make sure it can be found.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import *

if sys.version_info < (3,6):
    print("Must use Python 3.6 or better.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

LEFT_JUSTIFY = '{<}'
CENTER_JUSTIFY = '{-}'
RIGHT_JUSTIFY = '{>}'

AUTHOR_PAT = re.compile(r'^(.*)%author%(.*)$')
TITLE_PAT = re.compile(r'^(.*)%title%(.*)$')
SUBTITLE_PAT = re.compile(r'^(.*)%subtitle%(.*)$')
COPYRIGHT_OWNER_PAT = re.compile(r'^(.*)%copyright-owner%(.*)$')
COPYRIGHT_YEAR_PAT = re.compile(r'^(.*)%copyright-year%(.*)$')
PUBLISHER_PAT = re.compile(r'^(.*)%publisher%(.*)$')
LANGUAGE_PAT = re.compile(r'^(.*)%language%(.*)$')

# Patterns that are simple strings in the metadata.
SIMPLE_PATTERNS = (
    (TITLE_PAT,           'title'),
    (SUBTITLE_PAT,        'subtitle'),
    (COPYRIGHT_OWNER_PAT, 'copyright.owner'),
    (COPYRIGHT_YEAR_PAT,  'copyright.year'),
    (PUBLISHER_PAT,       'publisher'),
    (LANGUAGE_PAT,        'language')
)

XHTML_JUSTIFICATION_CLASSES = {
    # token           class
    LEFT_JUSTIFY:     'left',
    CENTER_JUSTIFY:   'center',
    RIGHT_JUSTIFY:    'right'
}

LATEX_JUSTIFICATION_ENVIRONMENTS = {
    # token           env
    LEFT_JUSTIFY:     'flushleft',
    CENTER_JUSTIFY:   'center',
    RIGHT_JUSTIFY:    'flushright'
}

DOCX_JUSTIFICATION_STYLES = {
    # token           env
    LEFT_JUSTIFY:     'JustifyLeft',
    CENTER_JUSTIFY:   'Centered',
    RIGHT_JUSTIFY:    'JustifyRight'
}


# ---------------------------------------------------------------------------
# Helper classes
# ---------------------------------------------------------------------------

class DataHolder:
    '''
    Allows for assign-and-test. See
    http://code.activestate.com/recipes/66061-assign-and-test/
    '''
    def __init__(self, value=None):
        self.value = value

    def set(self, value):
        self.value = value
        return value

    def get(self):
        return self.value

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def debug(msg):
    '''
    Dump a debug message to stderr.

    Parameters:

    msg: The message to print
    '''
    sys.stderr.write(msg + "\n")

def matches_text(elem, text):
    '''
    Convenience function to see if an element is a Str element and matches
    the specified text.

    Parameters:

    elem: The AST element to test
    text: The string to match against

    Returns: True on match, False otherwise
    '''
    return isinstance(elem, Str) and elem.text == text

def matches_pattern(elem, regex):
    '''
    Convenience function to see if an element is a Str element and matches
    the specified regular expression.

    Parameters:

    elem:  The AST element to test
    regex: The compiled regular expression against which to match

    Returns: The re.Match object on match, None otherwise
    '''
    return regex.match(elem.text) if isinstance(elem, Str) else None

def paragraph_starts_with_child(elem, string):
    '''
    Determine whether the first non-line break element in a paragraph is a
    Str element that matches the specified string. Skips leading LineBreak
    nodes.

    Parameters:

    elem:   The AST element to test
    string: The string to match against

    Returns: True on match, False otherwise. Also returns false if the
    passed AST element is not a Para object.
    '''
    if not isinstance(elem, Para):
        return False

    # Skip any LineBreak elements at the beginning.
    stripped = list(dropwhile(lambda e: isinstance(e, LineBreak), elem.content))

    if len(stripped) == 0:
        return False

    if matches_text(stripped[0], string):
        return True

    return False

def paragraph_contains_child(elem, string):
    '''
    Determine whether the any AST element a paragraph is a Str element that
    matches the specified string.

    Parameters:

    elem:   The AST element to test
    string: The string to match against

    Returns: True on match, False otherwise. Also returns false if the
    passed AST element is not a Para object.
    '''
    return (isinstance(elem, Para) and
            any(matches_text(x, string) for x in elem.content))

def is_epub(format):
    '''
    Convenience function that tests whether the output format is ePub. Useful
    because Pandoc currently supports two ePub output formats.

    Parameters:

    format: the document output format

    Returns: True if the output format is an ePub format, False otherwise.
    '''
    return format.startswith('epub')

def justify(elem, format, token):
    '''
    Workhorse method to justify an element (left, center, or right).
    Handles all the hairy logic necessary to get the job done.

    Parameters:

    elem:        the element to be justified
    format:      the output format
    token:       the original justification token found in the Markdown, to be
                 removed from the element's children. Also used to as a look-up
                 key.

    Returns: the adjusted element
    '''
    def drop(child):
        return isinstance(child, LineBreak) or matches_text(child, token)

    leading_line_skips = list(takewhile(lambda e: isinstance(e, LineBreak),
                                        elem.content))
    children = list(dropwhile(drop, elem.content))

    if (format == 'html') or is_epub(format):
        xhtml_class = XHTML_JUSTIFICATION_CLASSES[token]
        return Div(Para(*leading_line_skips), Para(*children),
                   attributes={'class': xhtml_class})
    elif format == 'latex':
        # Leading line skips cause a problem in LaTeX, when combined with
        # these environments (at least, the way Pandoc generates the LaTeX).
        # Don't include them.
        latex_env = LATEX_JUSTIFICATION_ENVIRONMENTS[token]
        new_children = (
            [RawInline(r'\begin{' + latex_env + '}', 'latex')] +
            children +
            [RawInline(r'\end{' + latex_env + '}', 'latex'),
             RawInline(r'\bigskip', 'latex')]
        )
        return Para(*new_children)

    elif format == 'docx':
        docx_style = DOCX_JUSTIFICATION_STYLES[token]
        return Div(Para(*leading_line_skips), Para(*children),
                   attributes={'custom-style': docx_style})

    else:
        return Div(Para(*leading_line_skips), Para(*children))

def left_justify_paragraph(elem, format):
    '''
    Left-justify the specified element.

    Parameters:

    elem:   The element
    format: The output format

    Returns: the possibly updated element
    '''
    return justify(elem, format, LEFT_JUSTIFY)

def center_paragraph(elem, format):
    '''
    Center the specified element.

    Parameters:

    elem:   The element
    format: The output format

    Returns: the possibly updated element
    '''
    return justify(elem, format, CENTER_JUSTIFY)

def right_justify_paragraph(elem, format):
    '''
    Right-justify the specified element.

    Parameters:

    elem:   The element
    format: The output format

    Returns: the possibly updated element
    '''
    return justify(elem, format, RIGHT_JUSTIFY)

def section_sep(elem, format):
    '''
    Convert the specified element into a section separator.

    Parameters:

    elem:   The element
    format: The output format

    Returns: the possibly updated element
    '''
    sep = "• • •"
    if (format == 'html') or is_epub(format):
        return RawBlock(f'<div class="sep">{sep}</div>')
    elif format == 'latex':
        return Para(*[RawInline(r'\bigskip', format),
                      RawInline(r'\begin{center}', format)] +
                     [Str(sep)] +
                     [RawInline(r'\end{center}', format),
                      RawInline(r'\bigskip', format)])
    elif format == 'docx':
        return center_paragraph(Para(Str(sep)), format)
    else:
        return elem

def substitute_any_metadata(elem, doc):
    '''
    Checks a string to determine whether it matches one of the SIMPLE_PATTERNS
    metadata keys, updating the element by substituting the appropriate
    metadata value, if found.

    Parameters:

    elem: the element to check
    doc:  the Document object

    Returns: the possibly updated element
    '''
    assert isinstance(elem, Str)

    for pat, meta_key in SIMPLE_PATTERNS:
        m = matches_pattern(elem, pat)
        if m:
            s = doc.get_metadata(meta_key, '')
            return Str(f"{m.group(1)}{s}{m.group(2)}")

    return elem

def newpage(format):
    '''
    Return the appropriate sequence to force a new page, if supported by the
    output format.

    Parameters:

    format: the output format

    Returns: the sequence of elements to force a new page, or []
    '''
    if format == 'latex':
        return [RawBlock(r'\newpage', format)]
    elif is_epub(format):
        return [RawBlock(r'<p class="pagebreak"></p>')]
    elif format == 'docx':
        return [Div(Para(Str('')), attributes={'custom-style': 'NewPage'})]
    else:
        return []

def prepare(doc):
    '''
    Filter initialization.

    Parameters:

    doc: the Document object
    '''
    # Validate the metadata
    validate_metadata(doc.get_metadata())

def transform(elem, doc):
    '''
    The guts of the filter.

    Parameters:

    elem:  An element to process
    doc:   The Document object

    :return: the possibly updated element
    '''
    data = DataHolder()
    if isinstance(elem, Header) and elem.level == 1:
        new_elem = elem
        if len(elem.content) == 0:
            # Special case LaTeX and Word: Replace with new page.
            if doc.format in ['latex', 'docx']:
                new_elem = Div(*newpage(doc.format))
        else:
            # Force page break, if not ePub.
            if not is_epub(doc.format):
                new_elements = newpage(doc.format) + [elem]
                new_elem = Div(*new_elements)
        return new_elem

    elif paragraph_contains_child(elem, '%newpage%'):
        abort('%newpage% is no longer supported.')

    elif paragraph_starts_with_child(elem, LEFT_JUSTIFY):
        return left_justify_paragraph(elem, doc.format)

    elif paragraph_starts_with_child(elem, CENTER_JUSTIFY):
        return center_paragraph(elem, doc.format)

    elif paragraph_starts_with_child(elem, RIGHT_JUSTIFY):
        return right_justify_paragraph(elem, doc.format)

    elif paragraph_contains_child(elem, '+++'):
        return section_sep(elem, doc.format)

    elif data.set(matches_pattern(elem, AUTHOR_PAT)):
        authors = doc.get_metadata('author', [])
        m = data.get()
        author_str = ""
        for i, a in enumerate(authors):
            sep = ", " if i < (len(authors) - 1) else " and "
            if i > 0:
                author_str = f"{author_str}{sep}{a}"
            else:
                author_str = a

        return Str(f"{m.group(1)}{author_str}{m.group(2)}")

    elif isinstance(elem, Str):
        return substitute_any_metadata(elem, doc)

    else:
        return elem

def main(doc=None):
    return run_filter(transform, prepare=prepare, doc=doc)

if __name__ == "__main__":
    main()
