#!/bin/bash

pandoc -f mediawiki -t markdown --atx-headers --wrap=none $1  > $2
