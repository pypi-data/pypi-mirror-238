function show_elapsed_time()
{
    user_hz=$(getconf CLK_TCK)
    pid=$1  
    jiffies=$(cat /proc/$pid/stat | cut -d" " -f22)
    sys_uptime=$(cat /proc/uptime | cut -d" " -f1)
    last_time=$(( ${sys_uptime%.*} - $jiffies/$user_hz ))
    echo $last_time
}

# function get_unfinished_jobs()
# {
#     submitted_pid=$1
#     unfinished_jobs=()

#     for pid in ${submitted_pid[@]}
#     do
#         run_time=$(show_elapsed_time $pid 2>/dev/null)

#         if (( run_time > 0 )); then
#             unfinished_jobs+=($pid)
#         fi
#     done

#     echo ${unfinished_jobs[*]}

# }

cmd_list_file=$1
threads=$2
max_time=$3
keep_log=$4
work_dir=$5

cmd_list_file=`realpath $cmd_list_file`
work_dir=`realpath $work_dir`
mkdir $work_dir > /dev/null 2>/dev/null
cd $work_dir

killed_pid_list="$work_dir/killed.jobs"

num=0
submitted_pid=()
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
            echo "$(date "+%F %T")    ${#submitted_pid[*]}/$job_num jobs submitted"
            time1=$(cat /proc/uptime | cut -d" " -f1)
            time1=${time1%.*}
        fi

    }
    done

    case "$keep_log" in
        "True") 

        job_info_file="$work_dir/job_$num.info"
        job_out_file="$work_dir/job_$num.stout"
        job_err_file="$work_dir/job_$num.sterr"

        nohup $cmd > $job_out_file 2>$job_err_file &
        pid_now=$(echo $!)
        submitted_pid+=($pid_now)
        # echo "$pid_now submitted"

        echo "PID: $pid_now" > $job_info_file
        echo "CMD: $cmd" >> $job_info_file
        echo "PWD: $PWD" >> $job_info_file
        echo "STOUT: $job_out_file" >> $job_info_file
        echo "STERR: $job_err_file" >> $job_info_file
       
        ;;
        "False") 
        
        nohup $cmd > /dev/null 2>&1 &
        pid_now=$(echo $!)
        submitted_pid+=($pid_now)
        # echo "$pid_now submitted"

        ;;
    esac

    num=`expr $num + 1`

    time2=$(cat /proc/uptime | cut -d" " -f1)
    time2=${time2%.*}
    time_gap=$(( $time2 - $time1 ))

    if (( time_gap > 10 )); then
        echo "$(date "+%F %T")    ${#submitted_pid[*]}/$job_num jobs submitted"
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