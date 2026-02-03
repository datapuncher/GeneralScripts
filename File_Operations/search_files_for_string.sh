#!/bin/bash

# Recursively search for a string of a specific file type.
# Search is case insensitive (-i) and matches whole words (-w).

grep -rniw --include="*.conf" "search string" /dir/to/search
