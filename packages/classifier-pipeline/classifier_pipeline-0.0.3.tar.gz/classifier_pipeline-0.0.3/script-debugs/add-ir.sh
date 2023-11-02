#!/bin/bash
set -e
sed -i "1i[device-setup]" /etc/cacophony/config.toml
sed -i "2i\ \ ir = true" /etc/cacophony/config.toml
