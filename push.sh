#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <commit-message>"
    exit 1
fi

COMMIT_MESSAGE="$1"

git add .

git commit -m "$COMMIT_MESSAGE"

git push
