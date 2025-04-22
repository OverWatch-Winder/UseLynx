#!/usr/bin/env bash

echo "start types diff"

projectRootPath=$(git rev-parse --show-toplevel)

echo "projectRootPath: $projectRootPath"

relativePath() {
  local absolutePath="$1"
  echo "${absolutePath#$projectRootPath/}"
}

typesDir=$(relativePath "$projectRootPath/js_libs/types-check")

echo "typesDir: $typesDir"

typesSrcChanged=$(git diff --name-only HEAD~1 -- "$typesDir/types")

echo "typesSrcChanged: $typesSrcChanged"

# check types's CHANGELOG
if [ -n "$typesSrcChanged" ]; then
   echo "types src changed: $typesSrcChanged"
fi

echo 0

