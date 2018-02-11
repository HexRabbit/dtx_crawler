#!/bin/bash

link=[]
readarray link < $1
mkdir dl

for i in `seq 1 ${#link[@]}`
do
  wget -nv "${link[$i]::-1}" -O ./dl/$i.zip
done
