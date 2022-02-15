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
  echo "Download deepspeech models"
  echo
  echo "usage: download_models.sh [option]..."
  echo "   --version              Deep speech version (without the v)"
  echo "   --path                 Deep speech models path"
}

DS_VERSION="0.8.0"
DS_PATH="${scriptPath}/models/"

while [[ $# -gt 0 ]]; do
  key="$1"
  case ${key} in
  -h | --help)
    display_help
    exit 0
    ;;
  --version)
    DS_VERSION=$2
    shift
    ;;
  --path)
    DS_PATH=$2
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

echo -e "Downloading deepspeech models"
echo -e "\tDeepSpeech Path: ${DS_PATH}"
echo -e "\tDeepSpeech Version: ${DS_VERSION}"

# Create models folder
mkdir -p ${DS_PATH}

echo -e "\nDownloading the acoustic models ...\n"
curl -fSL -R -J "https://togithub.com/mozilla/DeepSpeech/releases/download/v${DS_VERSION}/deepspeech-${DS_VERSION}-models.pbmm" -o "${DS_PATH}/deepspeech-${DS_VERSION}-models.pbmm"
curl -fSL -R -J "https://togithub.com/mozilla/DeepSpeech/releases/download/v${DS_VERSION}/deepspeech-${DS_VERSION}-models.tflite" -o "${DS_PATH}/deepspeech-${DS_VERSION}-models.tflite"

echo -e "\nDownloading the scorer ...\n"
curl -fSL -R -J "https://togithub.com/mozilla/DeepSpeech/releases/download/v${DS_VERSION}/deepspeech-${DS_VERSION}-models.scorer" -o "${DS_PATH}/deepspeech-${DS_VERSION}-models.scorer"