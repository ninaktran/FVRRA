#!/usr/bin/env bash
# Run Hugo in Docker (Linux / WSL)
docker run --rm -it -p 1313:1313 -v "$(pwd):/src" -w /src hugomods/hugo:exts-0.147.0 server --bind=0.0.0.0 --disableFastRender
