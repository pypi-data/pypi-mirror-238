#!/bin/bash

BINDIR="/home/dalley/devel/community/createrepo_c/tests/build/tests/"
RET=0

# Next line is a hack
# Builds for epel6 doesn't have rpath setted and
# tests fails with a "libcreaterepo_c.so.0: cannot open shared
# object file: No such file or directory" error message.
export "LD_LIBRARY_PATH=/home/dalley/devel/community/createrepo_c/tests/build/src/:"

# Go to source dir (so test would be able to use testdata/ in this dir)
cd /home/dalley/devel/community/createrepo_c/tests

# Iterate over compiled tests
for i in "$BINDIR"/test_*; do
    # Run only executable regular files with "test_" prefix
    if [ -f $i -a -x $i ]; then
        $i #execute the test
        if [ $? -ne 0 ]; then  RET=$(($RET+1)) ; fi
    fi
done

echo "Number of fails: $RET"
exit $RET
