#!/bin/bash

KLIPPER_PATH="${HOME}/klipper"
FANEXTENDED_PATH="${HOME}/klipper_fan_extended"

set -eu
export LC_ALL=C


function preflight_checks {
    if [ "$EUID" -eq 0 ]; then
        echo "[PRE-CHECK] This script must not be run as root!"
        exit -1
    fi

    if [ "$(sudo systemctl list-units --full -all -t service --no-legend | grep -F 'klipper.service')" ]; then
        printf "[PRE-CHECK] Klipper service found! Continuing...\n\n"
    else
        echo "[ERROR] Klipper service not found, please install Klipper first!"
        exit -1
    fi
}

function check_download {
    local fanextendeddirname fanextendedbasename
    fanextendeddirname="$(dirname ${FANEXTENDED_PATH})"
    fanextendedbasename="$(basename ${FANEXTENDED_PATH})"

    if [ ! -d "${FANEXTENDED_PATH}" ]; then
        echo "[DOWNLOAD] Downloading fan_extended repository..."
        if git -C $fanextendeddirname clone https://github.com/artkoz/klipper_fan_extended.git $fanextendedbasename; then
            chmod +x ${FANEXTENDED_PATH}/install.sh
            printf "[DOWNLOAD] Download complete!\n\n"
        else
            echo "[ERROR] Download of fan_extended git repository failed!"
            exit -1
        fi
    else
        printf "[DOWNLOAD] fan_extended repository already found locally. Continuing...\n\n"
    fi
}

function link_extension {
    echo "[INSTALL] Linking extension to Klipper..."
    ln -srfn "${FANEXTENDED_PATH}/fan_extended.py" "${KLIPPER_PATH}/klippy/extras/fan_extended.py"
}

function restart_klipper {
    echo "[POST-INSTALL] Restarting Klipper..."
    sudo systemctl restart klipper
}


printf "\n======================================\n"
echo "- fan_extended install script -"
printf "======================================\n\n"


# Run steps
preflight_checks
check_download
link_extension
restart_klipper
