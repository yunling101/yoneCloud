#!/bin/bash

set -e

CURRENT_DIR=$(cd -P "$(dirname "$0")"/ > /dev/null; pwd)
WORKSPACE_DIR=$(dirname ${CURRENT_DIR})

main()
{
    python ${WORKSPACE_DIR}/webserver/manage.py makemigrations
    python ${WORKSPACE_DIR}/webserver/manage.py migrate

    local first=${CURRENT_DIR}/initialize_perm.py
    [ -f ${first} ] && python ${first}

    for file in ${CURRENT_DIR}/initialize_*.py; do
        if [[ -f "${file}" && "${file}" != "${first}" ]]; then
            python ${file}
        fi
    done

    if [ -f ${CURRENT_DIR}/grafana/initialize.py ];then
        cd ${CURRENT_DIR}/grafana && python initialize.py
    fi

    return 0
}

main
