# makefile for building book

all:
	./citeproc.sh
	./build

install:
	cp book.docx ccnbook_ed4.docx
	cp book.epub ccnbook_ed4.epub
	cp book.html ccnbook_ed4.html
	cp book.pdf ccnbook_ed4.pdf

