#!/bin/sh

set -e

export PATH=$PATH:/yoneCloud/bin

if [ "$1" = "nginx" ]; then
   echo "$0: Configuration complete; ready for start up"
   supervisord -c /yoneCloud/supervisord/supervisord.conf
fi

until curl --silent --fail http://127.0.0.1:8010; do
    echo "Waiting for service to be healthy..."
    sleep 5
    /bin/bash /yoneCloud/scripts/initialize.sh
done

exec "$@"