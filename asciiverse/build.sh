#!/bin/sh
# Builds drl (the game) and drlwad (which packs the game data into
# drl.wad and core.wad), for the console only: no SDL, no sound.
# Linux: run on ubuntu-22.04 (glibc 2.35) with fpc and liblua5.1-0-dev;
# macOS: run on the runner with fpc and Lua 5.1 installed.
# Lua 5.1 is linked in statically (upstream's {$linklib lua5.1.a}); the
# binary needs only libc and ncurses at run time.
#   sh asciiverse/build.sh
# Clones ChaosForge's engine, fpcvalkyrie, at the tag below next to this
# repo (../fpcvalkyrie) and applies asciiverse/fpcvalkyrie.patch to it.
# Leaves bin/drl, bin/drl.wad and bin/core.wad.
set -eu
VALKYRIE_TAG=0_10_12
top=$PWD
v=$top/../fpcvalkyrie
if [ ! -d "$v/.git" ]; then
  git clone -q https://github.com/chaosforgeorg/fpcvalkyrie.git "$v"
fi
git -C "$v" checkout -q -f "$VALKYRIE_TAG"
git -C "$v" apply "$top/asciiverse/fpcvalkyrie.patch"

mkdir -p tmp
lua5.1 makefile.lua            # compiles bin/drl and bin/drlwad
(cd bin && ./drlwad ..)        # packs bin/drl.wad and bin/core.wad
strip bin/drl
