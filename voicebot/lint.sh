#!/usr/bin/env bash

if [[ "$OSTYPE" == *darwin* ]]; then
     if command -v greadlink>/dev/null 2>&1; then
        scriptPath=$(dirname "$(greadlink -f "$0")")
     else
        echo "greadlink command not found"
        exit 1
     fi
else
     scriptPath=$(dirname "$(readlink -f "$0")")
fi
cd "${scriptPath}/" || exit 1

function display_help() {
  echo "Lint all projects"
  echo
  echo "usage: lint.sh [option]..."
  echo "   --fix       Fix linting errors"
}

while [[ $# -gt 0 ]]; do
  key="$1"
  case ${key} in
  -h | --help)
    display_help
    exit 0
    ;;
  --fix)
    FIX=1
    shift
    ;;
  *)
    echo "Unrecognised option: $key"
    echo
    display_help
    exit 1
    ;;
  esac
  shift
done

if [[ $FIX ]]; then
    cd "${scriptPath}/stt_service" && npm run lint:fix
    cd "${scriptPath}/tts_service" && npm run lint:fix
    cd "${scriptPath}/voice_assistant_service" && npm run lint:fix
else
    cd "${scriptPath}/stt_service" && npm run lint
    cd "${scriptPath}/tts_service" && npm run lint
    cd "${scriptPath}/voice_assistant_service" && npm run lint
fi

cd "${scriptPath}/"