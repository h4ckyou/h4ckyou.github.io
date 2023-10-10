#!/bin/bash

url_base="https://beepboop.web.2023.sunshinectf.games/post/"
i=0

while true; do
    url="$url_base$i"
    response=$(curl -skS -L "$url")
    hidden_value=$(echo "$response" | jq -r '.hidden')
    
    if [[ $hidden_value == "true" ]]; then
        echo "Found a response with hidden: true at $url"
        echo "$response"
        break
    else
        echo "No luck at $url"
        i=$((i + 1))
    fi
done
