#!/bin/sh
# Records asciiverse/drl.cast, DRL's catalog preview, at 100x30
# (hub/RECORDING.md): the title, a new game (difficulty, class, trait,
# name), the intro skipped, then a walk on the first level. Keys are sent
# through tmux, so the game runs in a real terminal emulator; the
# recording itself is asciinema's. A fresh HOME keeps your own saves out.
# Needs tmux and asciinema 3. Usage, from the repo root after
# asciiverse/build.sh and asciiverse/stage.sh:
#   sh asciiverse/record-preview.sh
set -eu
home=$(mktemp -d)
s=drl-preview
tmux kill-session -t $s 2>/dev/null || true
tmux new-session -d -s $s -x 100 -y 30 \
  "HOME=$home TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8 \
   asciinema rec --overwrite -q -i 2 --window-size 100x30 \
   --capture-env TERM,COLORTERM,LANG -c ./stage/drl asciiverse/drl.cast"
k() { tmux send-keys -t $s "$1"; sleep "${2:-0.8}"; }
sleep 3
# answer each screen by what it shows until the first level is up
for i in $(seq 1 30); do
  scr=$(tmux capture-pane -p -t $s)
  case "$scr" in
    *Health:*)          break ;;
    *"Regular game"*)   k Enter 1.5 ;;                 # Regular game
    *"Hurt Me Plenty"*) k Down 0.6; k Enter 1.5 ;;     # Hey, Not Too Rough
    *"Select trait"*)   k Down 0.6; k Down 0.6; k Enter 1.5 ;;  # Hellrunner
    *Technician*)       k Enter 2 ;;                   # Marine
    *"Type a name"*)    k Enter 2 ;;                   # a random name
    *)                  k Enter 2 ;;                   # title, menu, intro
  esac
done
sleep 1.5
for d in Right Right Right Up Up Right Right Right Right Down Down Down \
         Right Right Right Right Up Up Up Up Left Left Down Down Right Right \
         Right Right Down Down Down Right Right Right; do
  k $d 0.35
done
sleep 1.5
k Escape 1.5; k Up 0.8; k Enter 3    # Save & Quit
k Up 0.8; k Enter 2                  # Exit
sleep 2
tmux kill-session -t $s 2>/dev/null || true
rm -rf "$home"
