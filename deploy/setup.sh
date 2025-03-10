#!/bin/bash

set -e

SETUP_NAME="deploy"
SETUP_DIR=$(cd -P "$(dirname "$0")"/ > /dev/null; pwd)

if [ $(basename "$PWD") != ${SETUP_NAME} ];then
    echo "need to enter the <deploy> directory to execute" && exit 1
fi

if [ ! -f ${SETUP_DIR}/.env ];then
    echo "${SETUP_DIR}/.env file does not exist" && exit 1
fi

init_config()
{
    export $(grep -v "^#" ${SETUP_DIR}/.env | xargs)

    [ -d ${SETUP_DIR}/ctrmanager ] || mkdir -p ${SETUP_DIR}/ctrmanager
    [ -d ${SETUP_DIR}/yonecloud ] || mkdir -p ${SETUP_DIR}/yonecloud

    # 需要安装 envsubst 命令
    # apt install gettext
    
    envsubst < ${SETUP_DIR}/default/env.config.yml > ${SETUP_DIR}/ctrmanager/config.yml
    envsubst < ${SETUP_DIR}/default/env.default.ini > ${SETUP_DIR}/yonecloud/default.ini
    envsubst < ${SETUP_DIR}/default/env.monitor.yml > ${SETUP_DIR}/yonecloud/monitor.yml

    if [[ -z ${GRAFANA_DOMAIN} ]];then
        GRAFANA_DOMAIN="localhost"
    fi
    
    if [[ -z ${CTR_MANAGER_DOMAIN} ]];then
        CTR_MANAGER_DOMAIN="localhost"
    fi

    if [[ "$(uname)" == "Darwin" ]]; then
        sed -i "" "53c\\
root_url = http://${GRAFANA_DOMAIN}
" ${SETUP_DIR}/grafana/grafana.ini
        sed -i "" "535c\\
auth_url = http://${CTR_MANAGER_DOMAIN}/grafana/authorize
" ${SETUP_DIR}/grafana/grafana.ini
    elif [[ "$(expr substr $(uname -s) 1 5)" == "Linux" ]]; then
        sed -i "53c root_url = http://${GRAFANA_DOMAIN}" ${SETUP_DIR}/grafana/grafana.ini
        sed -i "535c auth_url = http://${CTR_MANAGER_DOMAIN}/grafana/authorize" ${SETUP_DIR}/grafana/grafana.ini
    fi

    return 0
}

reload_config()
{
    if ! command -v "docker-compose" &> /dev/null; then
        echo "docker-compose command does not exist" && exit 1
    fi

    RUN_DIR=$(cat ${SETUP_DIR}/.env | grep "DEPLOY_DIR" | cut -d'=' -f2)
    if [[ "${RUN_DIR}" != /* ]];then
        echo "<DEPLOY_DIR> must be an absolute path" && exit 1
    fi

    [ -d ${RUN_DIR}/yonecloud/config ] || mkdir -p ${RUN_DIR}/yonecloud/config
    [ -d ${RUN_DIR}/alertmanager/config ] || mkdir -p ${RUN_DIR}/alertmanager/config
    cp -f ${SETUP_DIR}/yonecloud/*.ini ${RUN_DIR}/yonecloud/config
    if [ ! -f ${RUN_DIR}/yonecloud/config/monitor.yml ];then
        cp -f ${SETUP_DIR}/yonecloud/monitor.yml ${RUN_DIR}/yonecloud/config
    fi
    cp -f ${SETUP_DIR}/alertmanager/*.yml ${RUN_DIR}/alertmanager/config
    return 0
}

yone_list()
{
    docker-compose -f ${SETUP_DIR}/compose/service.yml config --services
    return 0
}

yone_deploy()
{
    local service=$1

    init_config
    reload_config

    yone_up ${service}
    return 0
}

yone_up()
{
    local service=$1

    if [ ! -z ${service} ];then
        docker-compose -f ${SETUP_DIR}/compose/service.yml up ${service} -d
    else
        docker-compose -f ${SETUP_DIR}/compose/service.yml up -d
    fi
    return 0
}

yone_start()
{
    local service=$1

    if [ ! -z ${service} ];then
        docker-compose -f ${SETUP_DIR}/compose/service.yml start ${service}
    else
        docker-compose -f ${SETUP_DIR}/compose/service.yml start
    fi
    return 0
}

yone_restart()
{
    local service=$1

    if [ ! -z ${service} ];then
        docker-compose -f ${SETUP_DIR}/compose/service.yml restart ${service}
    else
        docker-compose -f ${SETUP_DIR}/compose/service.yml restart
    fi
    return 0
}

yone_stop()
{
    local service=$1

    if [ ! -z ${service} ];then
        docker-compose -f ${SETUP_DIR}/compose/service.yml stop ${service}
    else
        docker-compose -f ${SETUP_DIR}/compose/service.yml stop
    fi
    return 0
}

yone_down()
{
    local service=$1

    if [ ! -z ${service} ];then
        docker-compose -f ${SETUP_DIR}/compose/service.yml down ${service}
    else
        docker-compose -f ${SETUP_DIR}/compose/service.yml down
    fi
    return 0
}

yone_ps()
{
    docker-compose -f ${SETUP_DIR}/compose/service.yml ps
    return 0
}

yone_top()
{
    docker-compose -f ${SETUP_DIR}/compose/service.yml stats
    return 0
}

yone_clean()
{
    local service=$1
    RUN_DIR=$(cat ${SETUP_DIR}/.env | grep "DEPLOY_DIR" | cut -d'=' -f2)

    if [ ! -z ${service} ];then
        [ -d ${RUN_DIR}/${service} ] && rm -rf ${RUN_DIR}/${service}
    else
        [ -d ${RUN_DIR} ] && rm -rf ${RUN_DIR}
    fi
    return 0
}

usage()
{
	cat <<EOF
Usage: $0 <OPTION> SERVICE
Option:
init | list | deploy<service> | start<service> | restart<service> | stop<service>
up<service> | down<service> | re-down<service> | ps | top | clean<service> | re-clean<service> | down-clean

Service:
all<default> | mysql | prometheus | alertmanager | yonecloud | ...

Example:
  $0 init
  $0 list
  $0 deploy
  $0 restart mysql
  $0 stop mysql
  $0 re-down
EOF
    return 0
}

if [ "$#" -ge 1 ];then
    case "$1" in
        init)
            init_config
            ;;
        list)
            yone_list
            ;;
        deploy)
            yone_deploy $2
            ;;
        up)
            yone_up $2
            ;;
        start)
            yone_start $2
            ;;
        restart)
            yone_restart $2
            ;;
        stop)
            yone_stop $2
            ;;
        down)
            yone_down $2
            ;;
        down-clean)
            yone_down
            yone_clean
            ;;
        re-clean)
            yone_down $2
            yone_clean $2
            yone_deploy $2
            ;;
        re-down)
            yone_down $2
            yone_deploy $2
            ;;
        ps)
            yone_ps
            ;;
        top)
            yone_top
            ;;
        clean)
            yone_clean $2
            ;;
        *)
			usage
			;;
    esac
else
    usage
fi