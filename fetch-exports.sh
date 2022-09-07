#!/usr/bin/env bash

for acronym in "$@"
do
  docker run -v ~/.aws:/root/.aws -v $(pwd)/content:/content reg.hcpss.org/school/content-export $acronym
done
