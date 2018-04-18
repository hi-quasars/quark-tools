#!/bin/bash
function runctags()
{
    cmd=$1
    dir=$2
    lang=$3
    if [ "$lang" = "" ]; then
        lang=C++
    fi
    case "$cmd" in
        "init" )
            if [ -f tags ]; then
                rm tags
            fi
            ctags --excmd=number --language-force=$lang -R ${dir}

            ;;
        "add" )
            ctags -a --excmd=number --language-force=$lang -R ${dir}
            ;;
        * )
            echo "usage: runctags [ init | add ] <dir> [C++|...]"
            ;;
    esac
}

function UpdateByTags()
{
    srcdir=$1
    if [ "$srcdir" == "" ]; then
        echo "$0 <banyandb_root_dir>"
        return
    fi
    
    runctags init ${srcdir}/common
    runctags add ${srcdir}/storage
    runctags add ${srcdir}/chunkserver
    runctags add ${srcdir}/scheduler
    runctags add ${srcdir}/agent
    runctags add ${srcdir}/main
    
    runctags add ${srcdir}/deps/libbase
    runctags add ${srcdir}/deps/leveldb-1.18/include
}
