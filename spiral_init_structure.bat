@echo off
:: Spiral Folder Initialization Script
echo Initializing Spiral system folder structure...

mkdir modules
mkdir routes
mkdir shimmer
mkdir static
mkdir static\js
mkdir templates
mkdir visual
mkdir whisper_node

copy NUL stall_trace.jsonl
echo Done.
