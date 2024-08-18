# makefile for building book

VERS=v1.0.0

all:
	cd book; author book -f html -o ccnbook_ed5

release:
	git commit -am "$(VERS) release"
	git tag -a $(VERS) -m "$(VERS) release"
	git push
	git push origin --tags	

