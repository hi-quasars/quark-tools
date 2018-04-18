#!/bin/bash
function mycd()
{
    target="$1";
    good_prefix="/home/fatiao/src/gitlab/cpp_dbs";
    good_prefix="/home/fatiao/src/github/libquarsar";
    curr=`pwd`;
    target=`cd $target; pwd;`;
    #echo $curr $target;
    run="\"\${curr##${good_prefix}}\" != \"\${curr}\""
    run="if [ $run ]; then  pushd $target; else cd $target; fi;"
    #echo $run
    eval $run
}
