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

cd "${scriptPath}/stt_service" && npm run build
cd "${scriptPath}/tts_service" && npm run build
cd "${scriptPath}/voice_assistant_service" && npm run build

cd "${scriptPath}/"