#!/bin/bash

# Variables
NAME="world"
COUNT=10

# Function
greet() {
    echo "Hello, $1!"
}

# Conditionals
if [ "$NAME" = "world" ]; then
    echo "Hello World"
elif [ -z "$NAME" ]; then
    echo "No name"
else
    echo "Hello $NAME"
fi

# Loops
for i in $(seq 1 $COUNT); do
    echo "Iteration $i"
done

while true; do
    break
done

# Arrays
arr=(one two three)
echo "${arr[0]}"

# Command substitution
TODAY=$(date +%Y-%m-%d)
