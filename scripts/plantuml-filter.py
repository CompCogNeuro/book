#!/usr/bin/env python

"""
Pandoc filter to process code blocks with class "plantuml" into
PlantUML-generated images. Based loosely on
https://gist.github.com/heidaga/495eae23755e24d9c06c29ae30a2c310
"""

import hashlib
import os
import sys
from panflute import *
from typing import Optional

# Need the lib module. Make sure it can be found.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from lib import *

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

COMMAND = find_in_path("plantuml")

DEFAULT_FLAGS = "-quiet -nbthread auto"

# ---------------------------------------------------------------------------
# Code
# ---------------------------------------------------------------------------

def sha1(x: str) -> str:
    """
    Simplified interface to generating SHA1 hash from a string.

    :param x: the string
    :return: the hex digest, as a string
    """

    return hashlib.sha1(x.encode(sys.getfilesystemencoding())).hexdigest()


def transform(elem: Element, doc: Doc) -> Element:
    """
    The guts of the filter.

    :param elem: An element to process
    :param doc:  The Document object

    :return: an element, which might be the original element or a new one
    """

    flags = DEFAULT_FLAGS
    filetype = "png"

    if not isinstance(elem, CodeBlock):
        return elem

    if 'plantuml' not in elem.classes:
        return elem

    # create a unique filename
    filename = sha1(elem.text)

    # enable SVG for HTML
    if doc.format == "html":
        flags += " -tsvg"
        filetype = "svg"

    # set figure caption
    title = (elem.attributes.get("title") or elem.attributes.get("alt", ""))

    # look for corresponding figure path
    img = os.path.join("tmp", '{}.{}'.format(filename, filetype))
    if not os.path.isfile(img):
        mkdirp("tmp")

        # create txt filepath
        src_code = os.path.join("tmp", '{}.txt'.format(filename))
        # dump plantuml source in a txt file
        with open(src_code, 'w') as out:
            out.write(elem.text)

        # Invoke PlantUML file to create figure
        os.system("{} {} {}".format(COMMAND, flags, src_code))

    image = Image(Str(""), title=title, url=img, classes=['plantuml'])
    return Para(image)


def main(doc: Optional[Doc] = None):
    return run_filter(transform, doc=doc)


if __name__ == "__main__":
    main()
