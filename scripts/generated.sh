#!/bin/bash

set -e

CURRENT_DIR=$(cd -P "$(dirname "$0")"/ > /dev/null; pwd)
WORKSPACE_DIR=$(dirname ${CURRENT_DIR})

main()
{
    for file in ${CURRENT_DIR}/generated_*.py; do
        if [[ -f "${file}" ]]; then
            python ${file}
        fi
    done

    return 0
}

main

