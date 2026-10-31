#!/usr/bin/env python3
"""Records asciiverse/drl.cast, DRL's catalog preview, at 100x30
(hub/RECORDING.md): a new game (menus answered by what is on screen),
then about PLAY_SECONDS (default 25) of play by a simple marine that
fires at whatever it can see, reloads when empty, runs along the longest
open line otherwise, and closes in on monsters it cannot hit yet; then
Save & Quit. DRL runs in tmux (a real terminal emulator; pyte garbles its
screens) and asciinema 3 records inside it. A fresh HOME keeps your own
saves out. Fights are random: run it a few times and keep the best take.
Usage, from the repo root after asciiverse/build.sh and stage.sh:
    python3 asciiverse/record-preview.py"""
import os, re, random, shutil, subprocess, tempfile, time

s = "drl-preview"
secs = float(os.environ.get("PLAY_SECONDS", 25))
home = tempfile.mkdtemp()
def screen():
    return subprocess.run(["tmux", "capture-pane", "-p", "-t", s],
                          capture_output=True, text=True).stdout.split("\n")
def key(k, wait):
    subprocess.run(["tmux", "send-keys", "-t", s, k]); time.sleep(wait)

subprocess.run(["tmux", "kill-session", "-t", s], stderr=subprocess.DEVNULL)
subprocess.run(["tmux", "new-session", "-d", "-s", s, "-x", "100", "-y", "30",
    f"HOME={home} TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8 "
    "asciinema rec --overwrite -q -i 2 --window-size 100x30 "
    "--capture-env TERM,COLORTERM,LANG -c ./stage/drl asciiverse/drl.cast"])
time.sleep(3)
# a new game: Regular, Hey Not Too Rough, Marine, first trait, random name
for _ in range(30):
    shown = "\n".join(screen())
    if "Health:" in shown: break
    if "Hurt Me Plenty" in shown: key("Down", 0.6)
    key("Enter", 1.5 if "Regular game" in shown or "Select trait" in shown else 1.0)
time.sleep(1)

MON = set("hicsOBARMVEC")
DIRS = {(1,0):"Right",(-1,0):"Left",(0,-1):"Up",(0,1):"Down",
        (1,-1):"PPage",(-1,-1):"Home",(1,1):"NPage",(-1,1):"End"}
last = None; end = time.time() + secs; log = []
bad = set(); prev_at = None; approaches = 0
while time.time() < end:
    rows = screen()
    st = next((i for i,l in enumerate(rows) if "Health:" in l), None)
    if st is None:
        if any("die" in l.lower() or "killed" in l.lower() for l in rows): log.append("dead"); break
        key("Enter", 1.0); continue
    top = st - 20                       # map: the 19 rows above the name line
    # the map, with any hint text on its first rows masked out
    mp = [(l[:l.index("Hint")] if "Hint" in l else l) for l in rows[top:st-1]]
    at = next(((x,y) for y,l in enumerate(mp) for x,c in enumerate(l) if c == "@"), None)
    mons = [(x,y,c) for y,l in enumerate(mp) for x,c in enumerate(l) if c in MON]
    if not at and mp: at = None
    ammo = re.search(r"\[(\d+)/(\d+)\]", rows[st] or "")
    blocked = any("No valid target" in l for l in rows[top-3:top])
    if mons and at and not blocked:
        if ammo and ammo.group(1) == "0": key("r", 0.5); log.append("reload")
        else: key("f", 0.45); log.append("fire " + mons[0][2])
        continue
    if mons and at and approaches < 6:  # seen but not in the line of fire: close in
        mx, my, _ = min(mons, key=lambda m: abs(m[0]-at[0]) + abs(m[1]-at[1]))
        d = ((mx > at[0]) - (mx < at[0]), (my > at[1]) - (my < at[1]))
        key(DIRS.get(d, "w"), 0.35); log.append("approach"); approaches += 1; continue
    if not mons: approaches = 0
    if at == prev_at and last: bad.add(last)      # the last run went nowhere
    else: bad.clear() if at != prev_at else None
    prev_at = at
    if not at: key("w", 0.4); continue
    best = None
    for (dx,dy),k in DIRS.items():
        if (dx,dy) in bad or (last and (dx,dy) == (-last[0],-last[1])): continue
        n = 0; x,y = at
        while True:
            x += dx; y += dy
            if not (0 <= y < len(mp) and 0 <= x < len(mp[y])) or mp[y][x] not in ".,'": break
            n += 1
        n += random.random()
        if best is None or n > best[0]: best = (n,(dx,dy),k)
    if best is None or best[0] < 1: key("w", 0.3); last = None; bad.clear(); continue
    last = best[1]
    key(",", 0.15); key(best[2], 1.2); log.append("run " + best[2])

# Save & Quit, then Exit from the main menu
time.sleep(1.5)
key("Escape", 1.5); key("Up", 0.8); key("Enter", 3)
key("Up", 0.8); key("Enter", 2.5)
subprocess.run(["tmux", "kill-session", "-t", s], stderr=subprocess.DEVNULL)
shutil.rmtree(home, ignore_errors=True)
print(" ".join(log))
