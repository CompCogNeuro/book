# makefile for building book

VERS=v1.0.0

all:
	./citeproc.sh
	./build

install:
	cp book.docx ccnbook_ed4.docx
	cp book.epub ccnbook_ed4.epub
	cp book.html ccnbook_ed4.html
	cp book.pdf ccnbook_ed4.pdf

release:
	git commit -am "$(VERS) release"
	git tag -a $(VERS) -m "$(VERS) release"
	git push
	git push origin --tags	

