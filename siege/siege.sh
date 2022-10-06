#!/bin/sh
#runs siege without a stdout file (q=quiet). saves end-of-run stats to test.log in the current diretory.
#pulls urls to hit from endpointsflat.txt
#iteratively increases the number of attackers (here, 25 runs increasing in steps of 10)
#runs for a set amount of time (here, 25M)
#then tries to reset start time, so that hopefully i can keep these machines in sync.
#

start_time=$(date +%s)

#total number of iterations to run
iteration=1
iterations=15

#duration of each siege, in seconds
iteration_duration=300

#buffer time between siege iteerations, in seconds
sleep_time=10

#the number of concurrent users to increase the siege by at each iteration
#n.b. this is per vm
##and that the max per vm is (currently) 250
##so if you have 1 vm with a concurrency_step of 5 and 40 total iterations, your total number of concurrent users in the siege will be
####5,10,15...200
##and if you have 2vm concurrency_step 7 and 50 total iterations, total concurrent=
####14,28,42...500
concurrency_step=10

#time interval between iterations, including the sleep_time buffer
time_step=$(($iteration_duration *2 + $sleep_time))





while [ $iteration -le $iterations ]; do
	CONC=$(($iteration * $concurrency_step))
	current_time=$(date +%s)
	time_diff=$(($current_time - $start_time))
	
	#only allows the next iteration to kick off only once its start time has been crossed
	#this, in the while loop, allows for a crude re-synchronization between processes
	echo $current_time
	#echo $time_diff
	if [ $time_diff -gt $(($time_step * $(($iteration - 1)))) ]
	then
		echo $CONC
		#echo $current_time
		for t in $(ls links/*.txt); do
			#echo $t
			basename=$(echo $t | sed 's/links\///' | sed 's/\.txt//')
			echo $basename
			siege --internet --concurrent=$CONC --time=$(($iteration_duration))S --log=$(echo 'logs/'$basename'.log') --file=$(echo 'links/'$basename'.txt')
		done
		iteration=$(($iteration + 1))
		#echo $current_time
		sleep $iteration_duration	
	fi
	
	sleep .2
	#set the start time for the next loop
	

done
