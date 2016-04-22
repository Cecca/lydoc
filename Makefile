# This makefile helps automating some of the development process.
# To print a help message on the command line, just type
#
#     make help

.SILENT:
.PHONY: help

## This help screen
help:
	printf "Available targets\n\n"
	awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "%-15s %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST) | sort


.PHONY: parser
## Build the parser, starting from the grammar
parser: lydoc/lilyparser.py

lydoc/lilyparser.py: lydoc/grammar.txt
	echo "Generating parser from grammar file"
	grako -m Lily -o lydoc/lilyparser.py lydoc/grammar.txt

.PHONY: standalone
## Package the application in a standalone executable, with no dependencies
standalone: dist/lydoc.exe

dist/lydoc.exe: *.py
	pyinstaller --onefile --name lydoc.exe lydoc/__main__.py

.PHONY: bumpversion
## See scripts/bumpversion.sh
bumpversion:
	scripts/bumpversion.sh
