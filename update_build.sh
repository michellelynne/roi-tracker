#!/usr/bin/env bash


for lambda in $( ls src); do
    if  [[ $lambda != build ]] && [[ $lambda != __* ]] && [[ $lambda != common ]];
    then
        echo lambda: $lambda
        mkdir -p src/$lambda/build/
        if [ -f src/$lambda/requirements.txt ]; then
            pip install -r src/$lambda/requirements.txt -t src/$lambda/build/
        fi
        ln -s ../__init__.py src/$lambda/build/__init__.py
        name='_lambda.py'
        ln -s ../$lambda$name src/$lambda/build/$lambda$name
        for common in $( ls src/common); do
            if  [[ $common != __* ]];
            then
                echo common: $common
                ln -s ../../common/$common src/$lambda/build/$common
            fi
        done
    fi
done