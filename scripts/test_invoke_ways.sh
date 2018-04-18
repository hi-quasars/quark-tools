#!/bin/bash
if [ "$BASH_SOURCE" = "" ]; then
	echo "this file is called by invoke: $0"
else
	echo "this file is called by 'source' or '.': $BASH_SOURCE"
fi



echo "BASH_SOURCE:" $BASH_SOURCE
echo "\$0:" $0
