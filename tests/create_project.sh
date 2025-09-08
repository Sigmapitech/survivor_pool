#!/usr/bin/env bash

read -p "How many projects do you want to create? " num_projects

for i in $(seq 1 $num_projects); do
    random_startup_id=$(( ( RANDOM % 32 ) + 1 ))
    random_name="Project_$(date +%s%N)"
    random_desc="Description_$(date +%s%N)"

    curl -X POST "http://localhost:8000/api/projects/$random_startup_id" \
        -H "Content-Type: multipart/form-data" \
        -F "name=$random_name" \
        -F "description=$random_desc"
    echo "Created project $i: $random_name"
done
echo "Finished creating $num_projects projects."

