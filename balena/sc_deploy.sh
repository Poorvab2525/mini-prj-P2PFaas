#!/bin/bash
balena deploy admin/rpi4-c00 -m --emulated --debug \
    --buildArg TARGETPLATFORM=linux/arm64/v8 \
    --buildArg TARGETARCH=arm64 \
    --buildArg TARGETOS=linux