#!/bin/bash
echo "ls"
ls
echo "ls session01"
ls session01
echo "find . -name "*.hkl" | grep -v -e spiketrain -e mountains | wc -l"
find . -name "*.hkl" | grep -v -e spiketrain -e mountains | wc -l
echo "find . -name "*.hkl" | grep -v -e spiketrain -e mountains | xargs ls -hl"
find . -name "*.hkl" | grep -v -e spiketrain -e mountains | xargs ls -hl
echo "find . -name "*.hkl" | grep -v -e spiketrain -e mountains"
find . -name "*.hkl" | grep -v -e spiketrain -e mountains
echo "ls -hl ./session01/eyelink_24d5.hkl ./session01/rplparallel_d41d.hkl"
ls -hl ./session01/eyelink_24d5.hkl ./session01/rplparallel_d41d.hkl
echo "find mountains -name "firings.mda" | wc -l"
find mountains -name "firings.mda" | wc -l
