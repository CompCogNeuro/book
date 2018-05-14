**Version 0.7.0**

* Courtesy of [@szaffarano](https://github.com/szaffarano), there's now a
  `./build-docker` script that will install and run the entire toolchain in
  an isolated Docker image. See
  [this section in the README](https://github.com/bmc/ebook-template#can-i-use-docker-why-yes)
  for details.

**Version 0.6.1**

* Fixed [Issue 1](https://github.com/bmc/ebook-template/issues/1):
  the build wasn't ordering the chapters properly, because of a missing
  sort. Thanks to [@szaffarano](https://github.com/szaffarano) for the
  issue and the patch.

**Version 0.6.0**

* Added support for embedding [PlantUML](http://plantuml.com/) diagrams, 
  provided the [pandoc-plantuml-filter](https://github.com/kbonne/pandoc-plantuml-filter)
  is installed.
* Added ability to create PDF using [Weasy Print][], rather than LaTeX, which
  can resolve font problems with some printers. [Weasy Print][] must already be
  installed in your Python 3 environment, and it's not as simple as a
  `pip install`. See <http://weasyprint.readthedocs.io/en/latest/install.html>
* Added support for the following Pandoc extensions:
    - `fenced_code_blocks`
    - `fenced_code_attributes`
    - `backtick_code_blocks`
* Now ensures that generated HTML (including HTML used by Weasy Print) has the
  book language.
* Requires Pandoc 2.0.4 or better (and aborts if this requirement is not met).
  
[Weasy Print]: http://weasyprint.org/

**Version 0.5.0**

* Added ability to provide an author page (`author.md`).
* Added build code to find local image references in the book's Markdown
  sources, treating them as dependencies for the build.
* Cleaned up logic in `scripts/pandoc-filter.py`.
* Added some internal code documentation.
* Changed HTML styling to use traditional book-style paragraph indentation.
* `upgrade.py` now works even if the target directory is empty.

**Version 0.4.0**

* Added license terms.
* Added support for a (JavaScript-generated) table of contents in the HTML
  version of the book.
* Fixed table of contents generation with ePub. This task included (a)
  removing behavior in the Pandoc filter that short-circuited Pandoc's table
  of contents logic, and (b) adding some build code to rewrite the table of
  contents files to remove empty entries and entries that just pointed to
  title pages.
* Fixed center-, left- and right-justification logic in the filter to work if
  the paragraph is preceded by forced line breaks.
* Removed support for `%newpage%`. Just use an empty first-level header ("#")
  to force a new page; the empty header will be removed from the table of
  contents. The Pandoc filter will now abort if it sees `%newpage%`.
* ePub is now ePub v3, not ePub v2.
* Added build logic to allow overriding HTML and/or ePub styling by creating
  `book/html.css` and/or `book/epub.css`.
* Ensured that generated ePub passes
  [EpubCheck](https://github.com/IDPF/epubcheck) with no errors.
* Fixed ePub CSS file to be proper CSS.
* Removed stray styling in ePub CSS that was preventing the correct paragraph
  style.
* Corrected generation of ePub metadata so that a lack of a book identifier
  doesn't generate an empty `<dc:identifier>` element. Necessary to pass
  EpubCheck validation.
* Created a new sample cover image, at a higher resolution. Modified LaTeX
  logic to scale it down properly for PDF.
* Cleaned build file up a bit.

**Version 0.3.0**

* Added support for generating a bibiography (references) section, appendices,
  a foreward, a preface, and a glossary. All are optional.
* Reworked how the pandoc filter handles token substitution.
* Moved metadata to a Pandoc-style metadata file.
* Added more substitution tokens.
* Added `version` target to `build`.
* Added an upgrade script, to help with upgrading to new versions.
* Added code to insert inline cover image in HTML version of the book.

**Version 0.2.0**

* Reorganized files so the top directory isn't so cluttered.
* Enhanced HTML CSS file, based on the "GitHub Pandoc CSS" in
  [this gist](https://gist.github.com/Dashed/6714393).
* Changed HTML build process to inline the CSS, to make the HTML truly
  standalone.

**Version 0.1.1**

Miscellaneous cleanup of unused files, plus addition of this change log.

**Version 0.1.0**

Initial release.

