#!/bin/bash
for testfile in `ls *.js`; do
	casperjs test --ssl-protocol=tlsv1 --xunit=$testfile.xml --log-level=debug $testfile --proxy-type=none;
done;
