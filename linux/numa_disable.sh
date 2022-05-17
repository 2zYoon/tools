#!/bin/bash

NODE_TO_DISABLE=1

for i in {16..31}
do
	echo 0 > /sys/devices/system/node/node$NODE_TO_DISABLE/cpu$i/online
	echo node$NODE_TO_DISABLE: CPU $i is disabled.
done

for j in {33..96}
do
	echo 0 > /sys/devices/system/node/node$NODE_TO_DISABLE/memory$j/online
	echo node$NODE_TO_DISABLE: Memory $j is disabled.
done

