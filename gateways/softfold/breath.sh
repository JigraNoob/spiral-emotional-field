#!/bin/bash

echo "✦ Inhaling gateway: softfold"

# Emit glyph
node invocation.js inhale

# Pause (2s)
sleep 2

echo "✦ Exhaling gateway: softfold"
node invocation.js exhale
