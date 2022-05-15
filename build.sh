#!/usr/bin/env bash

set -Eeuo pipefail
trap cleanup SIGINT SIGTERM ERR EXIT

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd -P)

usage() {
  cat << EOF # Build a Docker image configured with a SSH Key and Github creditentials to deploy LolBetStatistics.
Usage: $(basename "${BASH_SOURCE[0]}") [-h] --ssh [SSH_KEY_PATH] --name [GIT_NAME] --email [GIT_EMAIL]

Script description here.

Available options:

-h, --help      Print this help and exit
-s, --ssh       Path to the private SSH Key to use (Ex : ~/.ssh/id_rsa)
-n, --name      Git commit name
-e, --email     Git commit email
EOF
  exit
}

cleanup() {
  trap - SIGINT SIGTERM ERR EXIT
  # script cleanup here
}

setup_colors() {
  if [[ -t 2 ]] && [[ -z "${NO_COLOR-}" ]] && [[ "${TERM-}" != "dumb" ]]; then
    NOFORMAT='\033[0m' RED='\033[0;31m' GREEN='\033[0;32m' ORANGE='\033[0;33m' BLUE='\033[0;34m' PURPLE='\033[0;35m' CYAN='\033[0;36m' YELLOW='\033[1;33m'
  else
    NOFORMAT='' RED='' GREEN='' ORANGE='' BLUE='' PURPLE='' CYAN='' YELLOW=''
  fi
}

msg() {
  echo >&2 -e "${1-}"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}

parse_params() {
  # default values of variables set from params
  ssh=''
  name=''
  email=''

  while :; do
    case "${1-}" in
    -h | --help) usage ;;
    --no-color) NO_COLOR=1 ;;
    -s | --ssh)
      ssh="${2-}"
      shift
      ;;
    -n | --name)
      name="${2-}"
      shift
      ;;
    -e | --email)
      email="${2-}"
      shift
      ;;
    -?*) die "Unknown option: $1" ;;
    *) break ;;
    esac
    shift
  done

  args=("$@")

  # check required params and arguments
  [[ -z "${ssh-}" ]] && die "Missing required parameter: ssh"
  [[ -z "${name-}" ]] && die "Missing required parameter: name"
  [[ -z "${email-}" ]] && die "Missing required parameter: email"

  return 0
}

parse_params "$@"
setup_colors

# script logic here
SSH_KEY="$(cat ${ssh})"
docker buildx build --platform=linux/arm/v7 "." --pull --rm -f "DockerFile" -t lolbetstats:latest --build-arg SSH_KEY="${SSH_KEY}" --build-arg GIT_NAME=${name} --build-arg GIT_EMAIL=${email}
