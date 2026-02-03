#!/bin/bash

while read line; do
	touch $line
done < frames.txt
