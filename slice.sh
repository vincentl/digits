#!/bin/sh

echo "["
let H=1+$3*12
let T=($3-$2)*12
head -$H $1 | tail -$T
echo "]"

