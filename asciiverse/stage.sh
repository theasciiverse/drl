#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, and the
# game in lib/ with what it reads at run time (DRL looks for its files in
# the current folder, so the start script changes into lib/ first). The
# sound and music folders are left out: this build has no sound.
set -eu
rm -rf stage && mkdir -p stage/lib
cp asciiverse/drl stage/drl
cp bin/drl bin/drl.wad bin/core.wad bin/config.lua bin/font.dat stage/lib/
cp bin/manual.txt bin/version.txt bin/version_api.txt stage/lib/
cp LICENSE README.md PATCHES.md stage/
