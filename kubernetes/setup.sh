#!/bin/bash

set -e

SETUP_NAME="kubernetes"
SETUP_DIR=$(cd -P "$(dirname "$0")"/ > /dev/null; pwd)
OUTPUT="manifests/base"

if [ $(basename "$PWD") != ${SETUP_NAME} ];then
    echo "need to enter the <kubernetes> directory to execute" && exit 1
fi

if [ ! -f ${SETUP_DIR}/.env ];then
    echo "${SETUP_DIR}/.env file does not exist" && exit 1
fi

if ! command -v "kubectl" &> /dev/null; then
    echo "kubectl command does not exist" && exit 1
fi

b64enc_quote() {
    local encoded=$(echo -n "$1" | base64)
    local quoted=$(echo -n "${encoded}" | tr -d '\n' | sed -e 's/+/%2B/g' -e 's/\//%2F/g')
    echo "${quoted}"
}

init_config()
{
    export $(grep -v "^#" ${SETUP_DIR}/.env | xargs)

    [ -d ${SETUP_DIR}/${OUTPUT} ] && rm -rf ${SETUP_DIR}/${OUTPUT}
    mkdir -p ${SETUP_DIR}/${OUTPUT}

    export MYSQL_DATABASE_SECRET=$(b64enc_quote ${MYSQL_DATABASE})
    export MYSQL_PASSWORD_SECRET=$(b64enc_quote ${MYSQL_PASSWORD})
    export SECRET_KEY_QUOTE=$(b64enc_quote ${SECRET_KEY})

    for file in ${SETUP_DIR}/templates/*.yaml; do
         envsubst < ${file} > ${SETUP_DIR}/${OUTPUT}/$(basename ${file})
    done

    return 0
}

yone_list()
{
    kubectl get deploy -n yonecloud
    return 0
}

yone_deploy()
{
    local service=(namespace.yaml secret.yaml serviceaccount.yaml)

    for file in ${SETUP_DIR}/${OUTPUT}/*.yaml; do
        for s in ${service[@]}; do
           if [[ $(basename ${file}) == ${s} ]];then
              kubectl apply -f ${file}
           fi
        done
    done

    for file in ${SETUP_DIR}/${OUTPUT}/*.yaml; do
        isQueue=false
        for s in ${service[@]}; do
           if [[ $(basename ${file}) == ${s} ]];then
              isQueue=true
           fi
        done
        if [[ ! -z ${file} && ${isQueue} == false ]];then
            kubectl apply -f ${file}
        fi
    done

    return 0
}

yone_delete()
{
    local service=(serviceaccount.yaml secret.yaml namespace.yaml)

    for file in ${SETUP_DIR}/${OUTPUT}/*.yaml; do
        isQueue=false
        for s in ${service[@]}; do
           if [[ $(basename ${file}) == ${s} ]];then
              isQueue=true
           fi
        done
        if [[ ! -z ${file} && ${isQueue} == false ]];then
            kubectl delete -f ${file}
        fi
    done

    for s in ${service[@]}; do
        kubectl delete -f ${SETUP_DIR}/${OUTPUT}/${s}
    done

    return 0
}

yone_top()
{
    kubectl top pod -n yonecloud
    return 0
}

usage()
{
	cat <<EOF
Usage: $0 <OPTION>
Option:
init | list | deploy | delete | top

Example:
  $0 init
  $0 list
  $0 deploy
  $0 delete
EOF
    return 0
}

if [[ "$#" -ge 1 ]];then
    case "$1" in
        init)
            init_config
            ;;
        list)
            yone_list
            ;;
        deploy)
            yone_deploy
            ;;
        delete)
            yone_delete
            ;;
        top)
            yone_top
            ;;
        *)
			usage
			;;
    esac
else
    usage
fi