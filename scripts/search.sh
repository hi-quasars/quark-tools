#!/bin/bash

function search()
{
    text=$1
    src="$(find . -regex '.*\.cpp\|.*\.h')";
    grep -n "${text}" $src;
}
