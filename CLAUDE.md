# DRL (Asciiverse packaging)

DRL, ChaosForge's roguelike (Kornel Kisielewicz; formerly DoomRL),
packaged for the Asciiverse catalog in its own console mode. Not our
code: keep changes small, list every one in PATCHES.md, and prefer
patches upstream could take.

- Branch `asciiverse` on upstream's release tag (now `0_10_12c`);
  `upstream` is github.com/chaosforgeorg/drl, which is active (releases
  every few days): rebase onto new tags rather than freezing.
- Engine: fpcvalkyrie (github.com/chaosforgeorg/fpcvalkyrie), cloned to
  `../fpcvalkyrie` at the tag in `asciiverse/build.sh`, with
  `asciiverse/fpcvalkyrie.patch`. Bump both together.
- Build: `sh asciiverse/build.sh` (fpc 3.2.2, lua5.1, liblua5.1-0-dev),
  then `sh asciiverse/stage.sh`; run `stage/drl`.
- On Linux DRL reads its files from the current folder; the start script
  changes into lib/ and passes --write-path/--score-path.
- Name: keep "DRL", ChaosForge's own; don't use the old trademark name in
  our texts (the game's own screens say "D**m the Roguelike").
- Preview: `python3 asciiverse/record-preview.py` (tmux, asciinema 3);
  run it several times and keep a take with kills, under 60 s.
- tmux capture-pane shows curses line drawing as q/x; pyte garbles
  DRL's screens, so script and check through tmux.
