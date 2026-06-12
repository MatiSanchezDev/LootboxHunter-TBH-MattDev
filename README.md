# LootboxHunter — TBH (Taskbar Hero)

<p align="center"><img src="icono.png" width="96" alt="LootboxHunter icon"></p>

A tiny, dependency-free Windows app to track **chest cooldown timers** across
multiple maps in *Taskbar Hero*. Mark a map as **Dropped** the moment you get a
chest and the app rings when its cooldown is up — for each map independently —
so you always know which map is ready next.

> Built with plain Python (Tkinter + winsound). No internet, no telemetry,
> everything is stored locally on your PC.

## ⬇️ Download (just the app)

**[➡️ CLICK HERE TO DOWNLOAD (portable .zip) ⬅️](https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev/releases/latest/download/LootboxHunter-portable.zip)**

Then:

1. **Unzip** the downloaded file anywhere (right-click → Extract All).
2. Open the `LootboxHunter` folder and **double-click `LootboxHunter.exe`**.

> ⚠️ **Keep `LootboxHunter.exe` inside its folder, next to the `_internal`
> folder.** Don't move or copy the `.exe` out on its own — it won't run without
> `_internal`. To launch it from elsewhere (desktop, Steam, etc.), right-click
> the `.exe` → **Create shortcut** and move the *shortcut*, not the file. (See
> [Troubleshooting](#-troubleshooting) if you get a "Could not load PyInstaller's
> embedded PKG archive" error.)

No installation, no Python. (Windows only.) This `.zip` is the **recommended**
download because it triggers fewer antivirus false positives than a single
`.exe` (see [Is it safe?](#-is-it-safe-antivirus-false-positives) below).

> Prefer a single file (one click, but more antivirus noise)? Download
> [`LootboxHunter.exe`](https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev/releases/latest/download/LootboxHunter.exe).

⭐ If this saves you time, please **star the repo** — it really helps!

---

## ✨ Features

- ⏱️ **Per-map countdown** — one independent timer per map (default 12 min).
- 🔔 **Sound alert** when a map's chest is ready again (with a mute toggle).
- 📋 **Map suggestions** — known chest maps ready to add in one click.
- 🏷️ **Difficulty badges** — Normal / Nightmare / Hell / Torment.
- ✓ **Completed counter** — how many cooldown cycles each map finished.
- 🌍 **10 languages** — English, Español, Português, Français, Deutsch,
  Italiano, Русский, 中文, 日本語, 한국어.
- 💾 **Local save** — maps, running timers and settings persist between runs.

---

## 🚀 Install & Run

### Option A — Download the app (recommended, no Python needed)

- **Recommended:** download the [**portable .zip**](https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev/releases/latest/download/LootboxHunter-portable.zip),
  unzip it, and run `LootboxHunter.exe` inside the folder. Fewer antivirus
  false positives (see [Is it safe?](#-is-it-safe-antivirus-false-positives)).
- **Single file:** download [`LootboxHunter.exe`](https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev/releases/latest/download/LootboxHunter.exe)
  for one-click use (but more antivirus noise).

No installation, no Python required.

> **Windows SmartScreen** may warn the first time (the app isn't code-signed).
> Click **More info → Run anyway**. The code is open here for you to inspect.

### Option B — Run from source

Requires [Python 3.10+](https://www.python.org/downloads/) (Tkinter is included
on Windows installers).

```bash
git clone https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev.git
cd LootboxHunter-TBH-MattDev
python cofre_tracker.py
```

### Build your own .exe

```bash
python -m pip install pyinstaller pillow

# Single-file build → dist/LootboxHunter.exe
python -m PyInstaller --onefile --windowed --name LootboxHunter --icon icono.ico --add-data "icono.png;." cofre_tracker.py

# Folder build (fewer antivirus false positives) → dist/LootboxHunter/
python -m PyInstaller --onedir --windowed --name LootboxHunter --icon icono.ico --add-data "icono.png;." cofre_tracker.py
```

---

## 🎮 How to use

1. **Add a map** — type a name and pick a difficulty, or choose one from
   **Suggestions** and press **Add**.
2. Press **Dropped** the moment you get a chest — the timer starts.
3. When the timer hits zero the card turns **green**, plays a sound and
   flashes: the chest is ready again.
4. **Reset** stops the timer. The **✓ counter** shows finished cycles.
5. Everything is saved automatically.

> Set **Minutes per chest** to match your game's chest cooldown (default 12).

---

## 🗺️ Known chest maps

| Map           | Chest            | Difficulty |
|---------------|------------------|------------|
| Stage 1 - 1   | Cofre Azul Lv01  | Normal     |
| Stage 1 - 4   | Cofre Azul Lv02  | Normal     |
| Stage 1 - 8   | Cofre Azul Lv03  | Normal     |
| Stage 2 - 3   | Cofre Azul Lv15  | Normal     |
| Stage 2 - 8   | Cofre Azul Lv20  | Normal     |
| Stage 3 - 8   | Cofre Azul Lv30  | Normal     |
| Stage 1 - 9   | Cofre Azul Lv40  | Nightmare  |
| Stage 3 - 5   | Cofre Azul Lv50  | Nightmare  |
| Stage 2 - 5   | Cofre Azul Lv65  | Hell       |
| Stage 1 - 3   | Cofre Azul Lv80  | Torment    |

---

## 💾 Where is my data?

`%APPDATA%\CofreTracker\config.json` — plain JSON you can back up or edit.

---

## 🌐 Add a translation

Translations live in the `TR` dictionary inside `cofre_tracker.py`. Copy an
existing language block, translate the strings, add your code to `LANGS`, and
open a Pull Request. Contributions welcome!

---

## 🩹 Troubleshooting

### "Could not load PyInstaller's embedded PKG archive from the executable"

This means the app's `LootboxHunter.exe` got **separated from its `_internal`
folder**, or the file was downloaded/copied incompletely. The folder build keeps
the program data in `_internal` right next to the `.exe`, and the `.exe` cannot
start without it.

**Fix:**

1. Delete the lone `LootboxHunter.exe` you copied somewhere (e.g. into a Steam
   folder).
2. Re-download the [**portable .zip**](https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev/releases/latest/download/LootboxHunter-portable.zip)
   and **Extract All** so you get the whole `LootboxHunter` folder.
3. Run `LootboxHunter.exe` **from inside that folder** — keep it next to
   `_internal`. To launch it from your desktop or Steam, right-click the `.exe`
   → **Create shortcut** and move the *shortcut*, not the `.exe`.

Prefer something you can drop anywhere? Use the single-file
[`LootboxHunter.exe`](https://github.com/MatiSanchezDev/LootboxHunter-TBH-MattDev/releases/latest/download/LootboxHunter.exe)
(11 MB) — it's self-contained and can't be broken by moving it (just expect more
antivirus noise; see [Is it safe?](#-is-it-safe-antivirus-false-positives)).

---

## 📄 License

MIT — see [LICENSE](LICENSE). Free to use, share and modify.

---

<p align="center">Made by <b>MattDev</b> · ⭐ Star the repo if it helped you!</p>

---

## 🇪🇸 Español (resumen)

App liviana de Windows para trackear el **cooldown de cofres** en varios mapas
de *Taskbar Hero*. Marcás **Dropeado** cuando sacás un cofre y la app suena
cuando se cumple el tiempo de cada mapa por separado.

- **Instalar:** descargá `LootboxHunter.exe` desde *Releases* y doble clic
  (no necesita Python). O corré desde el código: `python cofre_tracker.py`.
- **Usar:** agregá un mapa (o elegí una sugerencia) → **Dropeado** arranca el
  contador → cuando llega a 0 la tarjeta se pone verde y suena.
- **Idiomas:** 10 disponibles, se cambian desde el selector de arriba.
- **Datos:** se guardan en `%APPDATA%\CofreTracker\config.json`.

⭐ Si te sirve, dejale una estrella al repo.

---

## 🛡️ Is it safe? (antivirus false positives)

**Yes.** Some antivirus engines may flag the `.exe` as a generic
"Trojan"/"Wacatac"/"ML.Heuristic", and VirusTotal's sandbox may match a few
behavioral rules. These are **known false positives for any app built with
PyInstaller** (the tool that turns Python into a `.exe`) — not actual malware.
On VirusTotal the **CRITICAL count is 0**.

### Why heuristics flag it

- A `--onefile` PyInstaller app bundles the Python runtime and **unpacks itself
  to a temp folder at launch**. Packed malware does the same thing, so heuristic
  scanners flag the *pattern*, not real malicious code. (The **portable .zip**
  build does **not** self-extract, which is why it's the recommended download.)
- The executable is **unsigned** (no paid code-signing certificate) and brand
  new, so it has zero reputation.

### The VirusTotal "Sigma rules", explained

Sigma rules describe *behaviors observed while running the file*, not malware
verdicts. Every rule this app matches is a normal consequence of being a
Python-app-in-an-`.exe`:

| Rule | What it flags | Why it's harmless here |
|------|---------------|------------------------|
| **Vcruntime140 DLL Sideloading** | Loading `vcruntime140.dll` from a local folder | PyInstaller ships the Visual C++ runtime Python needs. Every packaged Python app does this — hence "*Potential*". |
| **Sysmon File Executable Creation** | An executable file written to disk | The `--onefile` self-extraction to `%TEMP%`. **Avoided entirely by the portable .zip.** |
| **New Root/CA Certificate to Store** | A certificate added to Windows | **Not done by this app** — the code never imports `ssl`/`winreg` or touches the certificate store. Ambient sandbox noise. |
| **Python Image Load By Non-Python Process** | A non-`python.exe` process loading "Python Core" | Literally describes PyInstaller/Py2Exe/cx_Freeze bundling. This *confirms* it's a packaged Python app. |

None of these indicate the code steals data, contacts a server, or harms your
PC.

### Verify it yourself

- **The full source is in this repo** — read every line. The app only uses the
  Python standard library. No `requests`, no `socket`, no `subprocess`, no
  `ssl`, no `winreg`, no remote code. It only opens this GitHub page in your
  browser (the ⭐ link) and saves settings to `%APPDATA%\CofreTracker\config.json`.
- **Run it from source** with `python cofre_tracker.py` — no `.exe`, no
  packaging, none of the behaviors above.
- **Build it yourself** (see below) and you'll get the same harmless file.
