# Run Hugo in Docker (PowerShell)
docker run --rm -it -p 1313:1313 -v "${PWD}:/src" -w /src klakegg/hugo:ext-alpine server --bind=0.0.0.0 --disableFastRender
