#!/usr/bin/env bash

read -s -p "Enter the admin password: " pass
echo
read -p "How many projects do you want to create? " num_projects
echo $pass

# Perform login
data=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"sg@a.b\", \"password\": \"$pass\"}" -L)

echo "Login response: $data"

# Extract token using grep + sed (assuming JSON key is "token":"<value>")
token=$(echo "$data" | grep -o '"token":"[^"]*"' | sed 's/"token":"//;s/"//')

if [[ -z "$token" ]]; then
    echo "Login failed. No token received."
    exit 1
fi

echo "Received token: $token"

# Create projects
for i in $(seq 1 $num_projects); do
    random_startup_id=$(( ( RANDOM % 32 ) + 1 ))
    random_name="Project_$(date +%s%N)"
    random_desc="Description_$(date +%s%N)"

    resp=$(curl -s -X POST "http://localhost:8000/api/projects/$random_startup_id" \
        -H "Authorization: Bearer $token" \
        -H "Content-Type: multipart/form-data" \
        -F "name=$random_name" \
        -F "description=$random_desc")

    echo "Created project $i: $random_name (Response: $resp)"
done

echo "Finished creating $num_projects projects."
