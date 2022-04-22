#!/bin/bash

# config
node_master="0.0.0.0"
indices=( 0 1 2 3 4 )
nodes=("node1" "node2" "node3" "node4" "node5")
uname="username"
threshold_cpu=50.0
threshold_mem=20.0
retry_antagonist=5
sleep_s=6

# status
cnt_cpu_antagonist=( 0 0 0 0 0 )
cnt_mem_antagonist=( 0 0 0 0 0 )

# main
while true;
do
    for i in ${indices[@]};
    do
        node=${nodes[i]}
        echo "$node...."

        # check ssh connection
        ssh $uname@$node 'ls' 1> /dev/null 2> /dev/null
        if [ $? -ne 0 ]
        then
            echo "$node: SSH connection failed" # TODO: send mail
            break 2
        fi

        # check (external) internet connection
        ssh $uname@$node 'ping google.com -c 1' 1> /dev/null 2> /dev/null
        if [ $? -ne 0 ]
        then
            echo "$node: Internet connection failed" # TODO: send mail
            break 2
        fi

        # check cpu usage
        cpu_usage=`ssh $uname@$node 'top -bn 1 -o %CPU | sed -n "8p" | tr -s " " | cut -d " " -f 10'`

        if [ $(echo "$cpu_usage > $threshold_cpu" | bc -l) -ne 0 ]
        then
            cnt_cpu_antagonist[$i]=$((${cnt_cpu_antagonist[i]} + 1))
        fi

        if [ ${cnt_cpu_antagonist[i]} -gt $retry_antagonist ]
        then
            echo "wow" # TODO: send mail
            break 2
        fi

        echo ${cnt_cpu_antagonist[@]} # TODO: remove it

        # check memory usage
        cpu_usage=`ssh $uname@$node 'top -bn 1 -o %MEM | sed -n "8p" | tr -s " " | cut -d " " -f 11'`

        if [ $(echo "$mem_usage > $threshold_mem" | bc -l) -ne 0 ]
        then
            cnt_mem_antagonist[$i]=$((${cnt_mem_antagonist[i]} + 1))
        fi

        if [ ${cnt_mem_antagonist[i]} -gt $retry_antagonist ]
        then
            echo "wow" # TODO: send mail
            break 2
        fi

        echo ${cnt_mem_antagonist[@]} # TODO: remove it
    done

    sleep $sleep_s        
done
