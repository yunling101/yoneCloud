#!/bin/bash

set -e

BASE_WORK_DIR=$(cd -P "$(dirname "$0")"/ > /dev/null; pwd)
WORK_CONFIG=${BASE_WORK_DIR}/webserver/config
DOCKER_CONFIG=${BASE_WORK_DIR}/webserver/docker
DEFAULT_CONFIG=${BASE_WORK_DIR}/webserver/default

if [ ! -d ${DEFAULT_CONFIG} ];then
    echo "${DEFAULT_CONFIG} directory does not exist" && exit 0
fi

export $(grep -v "^#" ${DEFAULT_CONFIG}/env | xargs)

config_dev()
{
    export WORK_DIR=${BASE_WORK_DIR}
    config_generate ${WORK_CONFIG}
    return 0
}

build_front()
{
    [ -f "./build.js" ] && gulp -f build.js
    [ -d "./public/dist/storage" ] || cp -r ./public/storage ./public/dist/
}

config_docker()
{
    env_vars=(
        WORK_DIR="/yoneCloud"
    )

    for var in "${!env_vars[@]}"; do
        key="${env_vars%%=*}"
        export ${key}="${env_vars#*=}"
    done

    while IFS='=' read -r key value; do
        if [[ ${key} =~ "HOST" || ${key} =~ "ALLOW" || ${key} =~ "DOMAIN" ]];then
            export ${key}="127.0.0.1"
        elif [[ ${key} =~ "KEY" || ${key} =~ "PASSWORD" ]];then
            export ${key}=""
        fi
    done < ${DEFAULT_CONFIG}/env

    [ -d ${DOCKER_CONFIG} ] || mkdir -p ${DOCKER_CONFIG}
    
    config_generate ${DOCKER_CONFIG}
    build_front
    return 0
}

config_docker_rm()
{
    [ -d ${DOCKER_CONFIG} ] && rm -rf ${DOCKER_CONFIG}
    [ -d "./public/dist" ] && rm -rf ./public/dist
    return 0
}

config_generate()
{
    local CONFIG_DIR=$1
    envsubst < ${DEFAULT_CONFIG}/env.default.ini > ${CONFIG_DIR}/default.ini
    envsubst < ${DEFAULT_CONFIG}/env.monitor.yml > ${CONFIG_DIR}/monitor.yml
    return 0
}

config_deploy()
{
    [ -f ${BASE_WORK_DIR}/deploy/.env ] && rm -f ${BASE_WORK_DIR}/deploy/.env

    if [ ! -f ${BASE_WORK_DIR}/deploy/version ];then
        echo "deploy version file does not exist" && exit 0
    fi
    if [ ! -f ${DEFAULT_CONFIG}/env ];then
        echo "default env does not exist" && exit 0
    fi

    while IFS='=' read -r key value; do
        if [[ ${key} == "BASE_DIR" ]];then
            value="/opt/yonecloud"
        elif [[ ${key} == "ALLOW_HOSTS" ]];then
            value="*"
        elif [[ ${key} =~ "HOST" || ${key} =~ "DOMAIN" ]];then
            value="127.0.0.1"
        elif [[ ${key} =~ "KEY" || ${key} =~ "PASSWORD" ]];then
            value=""
        fi
        if [ ! -z ${key} ];then
            echo ${key}="${value}" >> ${DEFAULT_CONFIG}/env.1
        else
            echo "" >> ${DEFAULT_CONFIG}/env.1
        fi
    done < ${DEFAULT_CONFIG}/env

    cat ${DEFAULT_CONFIG}/env.1 ${BASE_WORK_DIR}/deploy/version > ${BASE_WORK_DIR}/deploy/.env
    cp -f ${DEFAULT_CONFIG}/env.default.ini ${BASE_WORK_DIR}/deploy/default/env.default.ini
    cp -f ${DEFAULT_CONFIG}/env.monitor.yml ${BASE_WORK_DIR}/deploy/default/env.monitor.yml
    [ -f ${DEFAULT_CONFIG}/env.1 ] && rm -f ${DEFAULT_CONFIG}/env.1
    return 0
}

usage()
{
	cat <<EOF
Usage: $0 <option>
Option: dev | docker | docker-rm | deploy

Example:
  /bin/sh $0 dev
  /bin/sh $0 docker
  /bin/sh $0 docker-rm
  /bin/sh $0 deploy
EOF
    return 0
}

if [ "$#" -eq 1 ];then
    case "$1" in
        dev)
            config_dev
            ;;
        docker)
            config_docker
            ;;
        docker-rm)
            config_docker_rm
            ;;
        deploy)
            config_deploy
            ;;
        *)
			usage
			;;
    esac
else
    usage
fi