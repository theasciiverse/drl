# Changes from upstream

This is the Asciiverse packaging of DRL 0.10.12c, ChaosForge's roguelike
by Kornel Kisielewicz (code GPL-2.0; art CC BY-SA 4.0, not used here),
for the terminal. The branch `asciiverse` sits on upstream's tag
`0_10_12c` (github.com/chaosforgeorg/drl); the engine, fpcvalkyrie, is
built from its tag `0_10_12` with `asciiverse/fpcvalkyrie.patch`.

The game itself is unchanged. It runs in its own console mode
(`--console`), which the engine draws through ncurses.

## Engine (asciiverse/fpcvalkyrie.patch)

Both are small and meant to be offered upstream.

- **No X11 for a terminal game.** The SDL3 bindings (vsdl3library,
  vsdl3mixerlibrary) list the units `x` and `xlib` without using them,
  which linked libX11 into every Linux build. Dropped, so the console
  build needs only libc and ncurses.
- **Settings with the other writable files.** `--write-path` moved the
  saves, scores and logs but not settings.lua, which DRL writes on first
  start next to the binary. With `--write-path` given, settings.lua now
  goes there too, so DRL runs from a read-only install.

## Packaging (new files)

- `asciiverse/build.sh`: fetches fpcvalkyrie at its tag, applies the
  patch, builds drl and drlwad, packs the data into drl.wad and core.wad.
- `asciiverse/drl`, `asciiverse/stage.sh`: av's start script and the
  archive layout. The start script runs `--console --no-sound` and points
  `--write-path` and `--score-path` at `${XDG_DATA_HOME:-~/.local/share}/drl`.
- `asciiverse/nfpm.yaml`: .deb, .rpm and Arch packages (the av layout
  in /usr/lib/drl, /usr/bin/drl linked to its start script).
- `.github/workflows/asciiverse-release.yml`: builds all of it on a
  `v*` tag (upstream's own CI, `ci.yml`, is left as it is).

## Not built

- The graphical (SDL3) version, sound and music. Windows.
