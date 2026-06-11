# LootboxHunter — TBH (Taskbar Hero)

A tiny, dependency-free Windows app to track **chest cooldown timers** across
multiple maps in *Taskbar Hero*. Mark a map as **Dropped** the moment you get a
chest and the app rings when its cooldown is up — for each map independently —
so you always know which map is ready next.

> Built with plain Python (Tkinter + winsound). No internet, no telemetry,
> everything is stored locally on your PC.

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

### Option A — Download the .exe (recommended, no Python needed)

1. Go to the [**Releases**](../../releases) page and download `LootboxHunter.exe`.
2. Double-click it. That's it.

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
python -m pip install pyinstaller
python -m PyInstaller --onefile --windowed --name LootboxHunter cofre_tracker.py
```

The executable lands in `dist/LootboxHunter.exe`.

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
