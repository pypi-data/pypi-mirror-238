#!/bin/bash

function show_elapsed_time()
{
    user_hz=$(getconf CLK_TCK)
    pid=$1  
    jiffies=$(cat /proc/$pid/stat | cut -d" " -f22)
    sys_uptime=$(cat /proc/uptime | cut -d" " -f1)
    last_time=$(( ${sys_uptime%.*} - $jiffies/$user_hz ))
    echo $last_time
}

cmd_list_file=$1
threads=$2
max_time=$3
keep_log=$4
work_dir=$5

cmd_list_file=`realpath $cmd_list_file`
work_dir=`realpath $work_dir`
mkdir $work_dir > /dev/null 2>/dev/null
cd $work_dir

# build fifo
tmp_fifofile="$$.fifo"
mkfifo $tmp_fifofile   # 新建一个FIFO类型的文件
exec 6<>$tmp_fifofile  # 将FD6指向FIFO类型
rm $tmp_fifofile  #删也可以，

#根据线程总数量设置令牌个数
#事实上就是在fd6中放置了$thread_num个回车符
for ((i=0;i<${threads};i++));do
    echo
done >&6

killed_pid_list="$work_dir/killed.jobs"

submitted_job_num=0
time1=$(cat /proc/uptime | cut -d" " -f1)
time1=${time1%.*}
job_num=$(wc -l $cmd_list_file | cut -d" " -f1)

echo "$(date "+%F %T")    Multiprocess submitter starts working"

while read cmd
do
{
    running_jobs_list=($(jobs -l|awk '{if ($3!="Done") print $2}'))
    while (( ${#running_jobs_list[*]} >= $threads ))
    do
    {
        running_jobs_list=($(jobs -l|awk '{if ($3!="Done") print $2}'))

        for pid in ${running_jobs_list[@]}
        do
        {
            # echo "$pid Running"
            run_time=$(show_elapsed_time $pid 2>/dev/null)

            if (( max_time > 0 )); then
                if (( run_time > max_time )); then
                    kill -9 $pid > /dev/null 2>/dev/null
                    echo "$pid be killed"
                    echo $pid >> $killed_pid_list
                fi
            fi

        }
        done
        sleep 1

        time2=$(cat /proc/uptime | cut -d" " -f1)
        time2=${time2%.*}
        time_gap=$(( $time2 - $time1 ))

        if (( time_gap > 10 )); then
            echo "$(date "+%F %T")    $submitted_job_num/$job_num jobs submitted"
            time1=$(cat /proc/uptime | cut -d" " -f1)
            time1=${time1%.*}
        fi

    }
    done

    case "$keep_log" in
        "True") 

        read -u6
        {
            ($cmd > ${BASHPID}.out 2>${BASHPID}.err) # 可以用实际命令代替
            echo >&6 # 当进程结束以后，再向FD6中加上一个回车符，即补上了read -u6减去的那个
        } &
       
        ;;
        "False") 

        read -u6
        {
            ($cmd > /dev/null 2>&1) # 可以用实际命令代替
            echo >&6 # 当进程结束以后，再向FD6中加上一个回车符，即补上了read -u6减去的那个
        } &

        ;;
    esac

    submitted_job_num=`expr $submitted_job_num + 1`

    time2=$(cat /proc/uptime | cut -d" " -f1)
    time2=${time2%.*}
    time_gap=$(( $time2 - $time1 ))

    if (( time_gap > 10 )); then
        echo "$(date "+%F %T")    $submitted_job_num/$job_num jobs submitted"
        time1=$(cat /proc/uptime | cut -d" " -f1)
        time1=${time1%.*}
    fi

}
done < $cmd_list_file

echo "$(date "+%F %T")    All jobs submitted"

# unfinished_jobs=($(get_unfinished_jobs ${submitted_pid[*]}))
unfinished_jobs=($(jobs -l|awk '{if ($3!="Done") print $2}'))
echo "$(date "+%F %T")    ${#unfinished_jobs[*]} jobs not finished yet"

while (( ${#unfinished_jobs[*]} > 0 ))
do
{
    # unfinished_jobs=($(get_unfinished_jobs ${submitted_pid[*]}))
    unfinished_jobs=($(jobs -l|awk '{if ($3!="Done") print $2}'))

    for pid in ${unfinished_jobs[@]}
    do
    {
        run_time=$(show_elapsed_time $pid 2>/dev/null)

        if (( max_time > 0 )); then
            if (( run_time > max_time )); then
                kill -9 $pid > /dev/null 2>/dev/null
                echo "$pid be killed"
                echo $pid >> $killed_pid_list
            fi
        fi

    }
    done
    sleep 1

    time2=$(cat /proc/uptime | cut -d" " -f1)
    time2=${time2%.*}
    time_gap=$(( $time2 - $time1 ))

    if (( time_gap > 10 )); then
        echo "$(date "+%F %T")    ${#unfinished_jobs[*]} jobs not finished yet"
        time1=$(cat /proc/uptime | cut -d" " -f1)
        time1=${time1%.*}
    fi

}
done

echo "$(date "+%F %T")    All jobs finished"