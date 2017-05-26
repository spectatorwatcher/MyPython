#!/bin/bash
ls|while read line;
do a=`grep 黃婆 $line`;
if [ "$a" ];
then
echo $line >> resFile;
echo $a >> resFile1;
fi;
done