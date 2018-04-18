#!/bin/bash

SCRTIPT_LO=$(dirname $0)
SCRTIPT_LO=$(cd ${SCRTIPT_LO}; pwd -P)

ngxreload()
{
	dir=$1;
	dir=$(cd ${dir}; pwd -P);
	cd $dir;
	sbin/nginx_ai -p ${dir} -s reload;
}


ngxrestart()
{
    dir=$1;
    dir=$(cd ${dir}; pwd -P);
    cd $dir;
    sbin/nginx_ai -p ${dir} -s quit;
	sbin/nginx_ai -p ${dir};
}

helpmsg()
{
	echo "$1 [reload | restart] [ngx-working-dir]"
}

main_process()
{
	script=$1
	cmd=$2
	dir=$3
	case $cmd in
		"reload" )
			ngxreload ${dir}
			;;
		"restart" )
			ngxrestart ${dir}	
			;;
		* )
			helpmsg ${script}
			;;
	esac
}

