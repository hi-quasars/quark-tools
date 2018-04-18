#!/bin/bash

# usage: pr_info <string> <info | warn | error> [verbose]
pr_info()
{
    type=$2;
	verbose=$3;
    if [ "${type}" = "" ]; then
        type="info";
    fi
	
	prefix="\033[3";
	suffix="\033[0m"; #system
	infostr="";

    case ${type} in
        info )
			prefix+="2m"; #green
            ;;
        warn )
			prefix+="3m"; #yellow
            ;;
        error )
			prefix+="1m"; #red
            ;;
		* )
			echo $1
			return;
			;;
    esac

	if [ "$verbose" != "" ]; then
		case ${type} in
			info )
				infostr="[ info ] ";
			;;
			warn )
				infostr="[ warn ] ";
			;;
			error )
				infostr="[ error] ";
			;;
		esac
	fi
	
	echo -e "${prefix}${infostr}${1}${suffix}"	
}


# usage: pr_key_value <name_of_associate_array> 
pr_key_value()
{
	name=$1;
	ktitle=$2;
	vtitle=$3;
	level=$4;

	cmd_str='${!';
	cmd_str+=$name;
	cmd_str+='[@]}';
	eval "keys=${cmd_str}"
	
	cmd_str='${';
	cmd_str+=$name;
	cmd_str+="[@]}";
	eval "values=${cmd_str}";
	
	
	karr=($keys);
	varr=($values);
	num=${#karr[@]};	
	
	lk=${#ktitle};
	lv=${#vtitle};

	for((i=0; i<num; i++))
	{
		key=${karr[$i]};
		if [ ${#key} -gt $lk ]; then
			lk=${#key}
		fi
		val=${varr[$i]};
		if [ ${#val} -gt $lv ]; then
			lv=${#val}
		fi
	}
	
	if [ "$level" != 'info' ] && [ "$level" != 'warn' ] && [ "$level" != 'error' ];then
		level='info';
	fi

	str=`printf "| %-${lk}s | %-${lv}s |" $ktitle $vtitle`
	pr_info "$str" $level	

	for((i=0; i<num; i++))
	{
		key=${karr[$i]};
		val=${varr[$i]};

		str=`printf "| %-${lk}s | %-${lv}s |" $key $val`
		pr_info "$str" $level 
	}
}

mkdir_if_not_exist()
{
	if [ ! -d ${1} ]; then
		mkdir -p ${1};
	fi
}

#
# unzip $1 to the same folder.
#
unzip_file()
{
	file_path=$1;
	dir=$(dirname ${file_path});
	file_fullname=${file_path##*/};

	idx=$(echo ${file_fullname} | awk -v "SUB=.tar.gz" '{print index($0,SUB)}')
	file_suffix=${file_fullname:$idx}
	if [ "$file_suffix" = "$file_fullname" ]; then
		# no
		file_prefix=${file_fullname%%.*};
		file_suffix=${file_fullname#*.}; 
	else
		idx=$(($idx - 1))
		file_prefix=${file_fullname:0:$idx}
	fi


	
	# echo ${dir};
	# echo ${file_fullname};
	
	# echo ${file_prefix};
	# echo ${file_suffix};
	if [ -d ${dir}/${file_prefix} ]; then
		pr_info "${dir}/${file_prefix}: target exist! do not unzip." warn verbose;
		return -1;
	else
		mkdir -p ${dir}/${file_prefix};
	fi
	
	
	case ${file_suffix} in
		"zip" )
			uzcmd="unzip ${file_path} -d ${dir}/${file_prefix}";
			;;
		"tar.gz" )
			uzcmd="tar zxvf ${file_path} -C ${dir}/${file_prefix}";
			;;
		* )
			pr_info "unsupported format: ${file_suffix}." error verbose;
			exit -1;
			;;
	esac
	
	eval ${uzcmd}
}


function get_script_dir()
{
    if [ "$BASH_SOURCE" = "" ]; then
        #echo "this file is called by invoke: $0"
        this=$(dirname $0)
    else
        #echo "this file is called by 'source' or '.': $BASH_SOURCE"
        this=$(dirname $BASH_SOURCE)
    fi
    if [ "$this" = "" ]; then
        this="."
    fi
    this=$(cd $this; pwd -P)
    echo $this
}
function get_filename()
{
    path=$1
    ret=${path##*/}
    echo $ret
}
function get_dirname()
{
    path=$1
    ret=$(dirname $path)
    echo $ret
}
function get_file_abs_path()
{
    filename=$1
    dir=$(dirname ${filename})
    curr=`pwd`
    absdir=$(cd $dir; pwd -P)
    file_abs_path=${absdir}/${filename##*/}
    cd $curr
    echo $file_abs_path
}

function rand_str()
{
	addon_len=$1
	if [ "$addon_len" = "" ]; then
		addon_len=0
	fi
	num=$(date +%s%N)
	str=$num
	#echo $num
	addon=""
	for((i=0; i<$addon_len; i++))
	do
		randi=$(cat /dev/urandom | head -n 10 | cksum | awk -F ' ' '{print $1}')
		rd=$(($randi % 10))
		addon=$addon$rd
	done
	echo $str$addon
}


function download()
{
	url=$1
	tmp_dir=$2
	name=$3
	install_dir=$4

	rd_name=$(rand_str 5)
	wget -O	$rd_name $url

	mv $rd_name ${tmp_dir}/$name
	
	if [ "$install_dir" != "" ]; then
		cp ${tmp_dir}/$name $install_dir/$name
	fi
}
