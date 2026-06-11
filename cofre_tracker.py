"""
LootboxHunter - TBH (Taskbar Hero)
==================================

Multi-map chest cooldown tracker. Mark "Dropped" when you get a chest and
the app rings when the configured minutes are up, per map. Includes map
suggestions, difficulty badges, a completed-cycles counter, an adjustable
volume, multi-language UI and a built-in manual. Everything is saved locally.

No external dependencies: standard Python only (tkinter + winsound).
"""

import io
import json
import locale
import math
import os
import re
import struct
import sys
import threading
import time
import wave
import webbrowser
import tkinter as tk
from tkinter import ttk

try:
    import winsound
    HAS_SOUND = True
except Exception:  # noqa: BLE001  (en caso de correr fuera de Windows)
    HAS_SOUND = False


# ----------------------------------------------------------- Repo / autor
# IMPORTANTE: cambia GITHUB_USER por tu usuario real de GitHub.
GITHUB_USER = "MatiSanchezDev"
REPO_NAME = "LootboxHunter-TBH-MattDev"
GITHUB_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}"
DOWNLOAD_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}/raw/main/LootboxHunter.exe"

APP_TITLE = "LootboxHunter - TBH"
ICON_FILE = "icono.png"


def resource_path(rel):
    """Ruta a un recurso, funciona tanto en script como en .exe (PyInstaller)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


# ------------------------------------------------------------- Sugerencias
# (Mapa, Nivel del cofre, Dificultad). "Cofre Azul" se traduce en runtime.
SUGGESTIONS = [
    ("Stage 1 - 1", "Lv01", "Normal"),
    ("Stage 1 - 4", "Lv02", "Normal"),
    ("Stage 1 - 8", "Lv03", "Normal"),
    ("Stage 2 - 3", "Lv15", "Normal"),
    ("Stage 2 - 8", "Lv20", "Normal"),
    ("Stage 3 - 8", "Lv30", "Normal"),
    ("Stage 1 - 9", "Lv40", "Nightmare"),
    ("Stage 3 - 5", "Lv50", "Nightmare"),
    ("Stage 2 - 5", "Lv65", "Hell"),
    ("Stage 1 - 3", "Lv80", "Torment"),
]

DIFFICULTIES = ["Normal", "Nightmare", "Hell", "Torment"]
DIFFICULTY_COLORS = {
    "Normal": "#3f7a4f",
    "Nightmare": "#6a4ca8",
    "Hell": "#b03a3a",
    "Torment": "#c8741f",
}


# --------------------------------------------------------------- i18n
LANGS = [
    ("en", "English"), ("es", "Español"), ("pt", "Português"),
    ("fr", "Français"), ("de", "Deutsch"), ("it", "Italiano"),
    ("ru", "Русский"), ("zh", "中文"), ("ja", "日本語"), ("ko", "한국어"),
]

TR = {
    "en": {
        "add_map": "+ Add map", "map_name": "Map name", "difficulty": "Difficulty",
        "suggestions": "Suggestions", "add": "Add", "minutes": "Minutes per chest:",
        "mute": "Mute", "volume": "Volume", "language": "Language", "manual": "Manual",
        "dropped": "Dropped", "reset": "Reset", "idle": "Not counting",
        "counting": "Counting...", "ready_status": "Chest available",
        "ready": "READY", "blue_chest": "Blue Chest",
        "no_maps": "No maps yet.\nAdd one above or pick a suggestion.",
        "star": "⭐ Star this project on GitHub", "manual_title": "How to use",
        "manual_body": (
            "1. Add a map: type a name or pick one from Suggestions.\n"
            "2. Press \"Dropped\" the moment you get a chest — the timer starts.\n"
            "3. When the timer reaches zero the card turns green and a sound "
            "plays: the chest is ready again.\n"
            "4. \"Reset\" stops the timer. The ✓ counter shows finished cycles.\n"
            "5. Adjust the Volume slider if the sound is too loud.\n"
            "6. Everything is saved automatically on your PC.\n\n"
            "Tip: set the minutes to your game's chest cooldown (default 12)."
        ),
    },
    "es": {
        "add_map": "+ Agregar mapa", "map_name": "Nombre del mapa",
        "difficulty": "Dificultad", "suggestions": "Sugerencias", "add": "Agregar",
        "minutes": "Minutos por cofre:", "mute": "Silenciar", "volume": "Volumen",
        "language": "Idioma", "manual": "Manual", "dropped": "Dropeado",
        "reset": "Reiniciar", "idle": "Sin contar", "counting": "Contando...",
        "ready_status": "Cofre disponible", "ready": "LISTO",
        "blue_chest": "Cofre Azul",
        "no_maps": "Todavía no hay mapas.\nAgrega uno arriba o elige una sugerencia.",
        "star": "⭐ Dale una estrella en GitHub", "manual_title": "Cómo usar",
        "manual_body": (
            "1. Agrega un mapa: escribe un nombre o elige uno de Sugerencias.\n"
            "2. Aprieta \"Dropeado\" apenas sacas un cofre — arranca el contador.\n"
            "3. Cuando el contador llega a cero la tarjeta se pone verde y suena: "
            "el cofre está listo otra vez.\n"
            "4. \"Reiniciar\" detiene el contador. El contador ✓ muestra los "
            "ciclos terminados.\n"
            "5. Ajusta el slider de Volumen si el sonido es muy fuerte.\n"
            "6. Todo se guarda automáticamente en tu PC.\n\n"
            "Tip: ajusta los minutos al cooldown de cofres de tu juego (por "
            "defecto 12)."
        ),
    },
    "pt": {
        "add_map": "+ Adicionar mapa", "map_name": "Nome do mapa",
        "difficulty": "Dificuldade", "suggestions": "Sugestões", "add": "Adicionar",
        "minutes": "Minutos por baú:", "mute": "Silenciar", "volume": "Volume",
        "language": "Idioma", "manual": "Manual", "dropped": "Dropado",
        "reset": "Reiniciar", "idle": "Sem contar", "counting": "Contando...",
        "ready_status": "Baú disponível", "ready": "PRONTO",
        "blue_chest": "Baú Azul",
        "no_maps": "Ainda não há mapas.\nAdicione um acima ou escolha uma sugestão.",
        "star": "⭐ Dê uma estrela no GitHub", "manual_title": "Como usar",
        "manual_body": (
            "1. Adicione um mapa: digite um nome ou escolha em Sugestões.\n"
            "2. Aperte \"Dropado\" assim que conseguir um baú — o cronômetro começa.\n"
            "3. Quando o cronômetro chega a zero o cartão fica verde e toca um som: "
            "o baú está pronto de novo.\n"
            "4. \"Reiniciar\" para o cronômetro. O contador ✓ mostra os ciclos "
            "concluídos.\n"
            "5. Ajuste o controle de Volume se o som estiver muito alto.\n"
            "6. Tudo é salvo automaticamente no seu PC.\n\n"
            "Dica: ajuste os minutos ao cooldown de baús do seu jogo (padrão 12)."
        ),
    },
    "fr": {
        "add_map": "+ Ajouter une carte", "map_name": "Nom de la carte",
        "difficulty": "Difficulté", "suggestions": "Suggestions", "add": "Ajouter",
        "minutes": "Minutes par coffre :", "mute": "Muet", "volume": "Volume",
        "language": "Langue", "manual": "Manuel", "dropped": "Obtenu",
        "reset": "Réinitialiser", "idle": "En pause", "counting": "En cours...",
        "ready_status": "Coffre disponible", "ready": "PRÊT",
        "blue_chest": "Coffre bleu",
        "no_maps": "Aucune carte pour l'instant.\nAjoutez-en une ou choisissez une suggestion.",
        "star": "⭐ Mettez une étoile sur GitHub", "manual_title": "Comment utiliser",
        "manual_body": (
            "1. Ajoutez une carte : saisissez un nom ou choisissez dans Suggestions.\n"
            "2. Appuyez sur « Obtenu » dès que vous recevez un coffre — le minuteur démarre.\n"
            "3. Quand le minuteur atteint zéro, la carte devient verte et un son "
            "retentit : le coffre est de nouveau prêt.\n"
            "4. « Réinitialiser » arrête le minuteur. Le compteur ✓ indique les "
            "cycles terminés.\n"
            "5. Réglez le curseur de Volume si le son est trop fort.\n"
            "6. Tout est enregistré automatiquement sur votre PC.\n\n"
            "Astuce : réglez les minutes selon le délai des coffres de votre jeu (12 par défaut)."
        ),
    },
    "de": {
        "add_map": "+ Karte hinzufügen", "map_name": "Kartenname",
        "difficulty": "Schwierigkeit", "suggestions": "Vorschläge",
        "add": "Hinzufügen", "minutes": "Minuten pro Truhe:", "mute": "Stumm",
        "volume": "Lautstärke", "language": "Sprache", "manual": "Anleitung",
        "dropped": "Erhalten", "reset": "Zurücksetzen", "idle": "Nicht aktiv",
        "counting": "Läuft...", "ready_status": "Truhe verfügbar", "ready": "BEREIT",
        "blue_chest": "Blaue Truhe",
        "no_maps": "Noch keine Karten.\nFüge oben eine hinzu oder wähle einen Vorschlag.",
        "star": "⭐ Gib dem Projekt einen Stern auf GitHub",
        "manual_title": "Anleitung",
        "manual_body": (
            "1. Karte hinzufügen: Namen eingeben oder einen Vorschlag wählen.\n"
            "2. Drücke „Erhalten“, sobald du eine Truhe bekommst — der Timer startet.\n"
            "3. Wenn der Timer null erreicht, wird die Karte grün und ein Ton "
            "ertönt: die Truhe ist wieder bereit.\n"
            "4. „Zurücksetzen“ stoppt den Timer. Der ✓-Zähler zeigt die "
            "abgeschlossenen Zyklen.\n"
            "5. Stelle den Lautstärke-Regler ein, falls der Ton zu laut ist.\n"
            "6. Alles wird automatisch auf deinem PC gespeichert.\n\n"
            "Tipp: Stelle die Minuten auf die Truhen-Abklingzeit deines Spiels ein (Standard 12)."
        ),
    },
    "it": {
        "add_map": "+ Aggiungi mappa", "map_name": "Nome mappa",
        "difficulty": "Difficoltà", "suggestions": "Suggerimenti", "add": "Aggiungi",
        "minutes": "Minuti per forziere:", "mute": "Muto", "volume": "Volume",
        "language": "Lingua", "manual": "Manuale", "dropped": "Ottenuto",
        "reset": "Reimposta", "idle": "Fermo", "counting": "Conteggio...",
        "ready_status": "Forziere disponibile", "ready": "PRONTO",
        "blue_chest": "Forziere blu",
        "no_maps": "Ancora nessuna mappa.\nAggiungine una sopra o scegli un suggerimento.",
        "star": "⭐ Metti una stella su GitHub", "manual_title": "Come usare",
        "manual_body": (
            "1. Aggiungi una mappa: scrivi un nome o scegli dai Suggerimenti.\n"
            "2. Premi \"Ottenuto\" appena ricevi un forziere — il timer parte.\n"
            "3. Quando il timer arriva a zero la scheda diventa verde e suona: "
            "il forziere è di nuovo pronto.\n"
            "4. \"Reimposta\" ferma il timer. Il contatore ✓ mostra i cicli completati.\n"
            "5. Regola il cursore del Volume se il suono è troppo alto.\n"
            "6. Tutto viene salvato automaticamente sul tuo PC.\n\n"
            "Consiglio: imposta i minuti in base al cooldown dei forzieri del tuo gioco (default 12)."
        ),
    },
    "ru": {
        "add_map": "+ Добавить карту", "map_name": "Название карты",
        "difficulty": "Сложность", "suggestions": "Предложения", "add": "Добавить",
        "minutes": "Минут на сундук:", "mute": "Без звука", "volume": "Громкость",
        "language": "Язык", "manual": "Инструкция", "dropped": "Получено",
        "reset": "Сброс", "idle": "Не считает", "counting": "Идёт отсчёт...",
        "ready_status": "Сундук доступен", "ready": "ГОТОВО",
        "blue_chest": "Синий сундук",
        "no_maps": "Пока нет карт.\nДобавьте сверху или выберите предложение.",
        "star": "⭐ Поставьте звезду на GitHub", "manual_title": "Как пользоваться",
        "manual_body": (
            "1. Добавьте карту: введите название или выберите из Предложений.\n"
            "2. Нажмите «Получено», как только получили сундук — запустится таймер.\n"
            "3. Когда таймер дойдёт до нуля, карточка станет зелёной и прозвучит "
            "сигнал: сундук снова готов.\n"
            "4. «Сброс» останавливает таймер. Счётчик ✓ показывает завершённые циклы.\n"
            "5. Отрегулируйте ползунок Громкости, если звук слишком громкий.\n"
            "6. Всё сохраняется автоматически на вашем ПК.\n\n"
            "Совет: установите минуты под перезарядку сундуков в вашей игре (по умолчанию 12)."
        ),
    },
    "zh": {
        "add_map": "+ 添加关卡", "map_name": "关卡名称", "difficulty": "难度",
        "suggestions": "推荐", "add": "添加", "minutes": "每个宝箱分钟数：",
        "mute": "静音", "volume": "音量", "language": "语言", "manual": "使用说明",
        "dropped": "已掉落", "reset": "重置", "idle": "未计时", "counting": "计时中...",
        "ready_status": "宝箱可用", "ready": "就绪", "blue_chest": "蓝色宝箱",
        "no_maps": "还没有关卡。\n在上方添加或选择推荐。",
        "star": "⭐ 在 GitHub 上点星", "manual_title": "使用方法",
        "manual_body": (
            "1. 添加关卡：输入名称或从推荐中选择。\n"
            "2. 获得宝箱时按下\"已掉落\"，计时器开始。\n"
            "3. 计时器归零时卡片变绿并响铃：宝箱再次就绪。\n"
            "4. \"重置\"停止计时器。✓ 计数器显示已完成的周期数。\n"
            "5. 如果声音太大，请调整音量滑块。\n"
            "6. 所有数据自动保存在你的电脑上。\n\n"
            "提示：将分钟数设置为游戏中宝箱的冷却时间（默认 12）。"
        ),
    },
    "ja": {
        "add_map": "+ マップを追加", "map_name": "マップ名", "difficulty": "難易度",
        "suggestions": "おすすめ", "add": "追加", "minutes": "宝箱ごとの分:",
        "mute": "ミュート", "volume": "音量", "language": "言語", "manual": "使い方",
        "dropped": "ドロップ", "reset": "リセット", "idle": "停止中",
        "counting": "カウント中...", "ready_status": "宝箱が利用可能",
        "ready": "準備完了", "blue_chest": "青い宝箱",
        "no_maps": "まだマップがありません。\n上で追加するか、おすすめから選んでください。",
        "star": "⭐ GitHub でスターを付ける", "manual_title": "使い方",
        "manual_body": (
            "1. マップを追加：名前を入力するか、おすすめから選びます。\n"
            "2. 宝箱を入手したら「ドロップ」を押すとタイマーが始まります。\n"
            "3. タイマーがゼロになるとカードが緑になり音が鳴ります：宝箱が再び準備完了です。\n"
            "4. 「リセット」でタイマーを止めます。✓ カウンターは完了した回数を表示します。\n"
            "5. 音が大きすぎる場合は音量スライダーを調整してください。\n"
            "6. すべて自動的にあなたのPCに保存されます。\n\n"
            "ヒント：分をゲームの宝箱クールダウンに合わせて設定してください（デフォルト12）。"
        ),
    },
    "ko": {
        "add_map": "+ 맵 추가", "map_name": "맵 이름", "difficulty": "난이도",
        "suggestions": "추천", "add": "추가", "minutes": "상자당 분:",
        "mute": "음소거", "volume": "볼륨", "language": "언어", "manual": "사용법",
        "dropped": "드롭됨", "reset": "초기화", "idle": "대기 중",
        "counting": "카운트 중...", "ready_status": "상자 사용 가능",
        "ready": "준비됨", "blue_chest": "파란 상자",
        "no_maps": "아직 맵이 없습니다.\n위에서 추가하거나 추천을 선택하세요.",
        "star": "⭐ GitHub에서 별 주기", "manual_title": "사용법",
        "manual_body": (
            "1. 맵 추가: 이름을 입력하거나 추천에서 선택하세요.\n"
            "2. 상자를 얻으면 \"드롭됨\"을 누르면 타이머가 시작됩니다.\n"
            "3. 타이머가 0이 되면 카드가 녹색으로 변하고 소리가 납니다: 상자가 다시 준비됩니다.\n"
            "4. \"초기화\"는 타이머를 멈춥니다. ✓ 카운터는 완료된 횟수를 표시합니다.\n"
            "5. 소리가 너무 크면 볼륨 슬라이더를 조절하세요.\n"
            "6. 모든 것은 자동으로 PC에 저장됩니다.\n\n"
            "팁: 분을 게임의 상자 쿨다운에 맞게 설정하세요 (기본 12)."
        ),
    },
}


# --------------------------------------------------------------- Paleta
ROOT_BG = "#1e1e2e"
CARD_IDLE = "#2b2b40"
CARD_RUNNING = "#3b3320"
CARD_READY = "#1f3d28"
TEXT_MAIN = "#e6e6e6"
TEXT_DIM = "#9a9ab0"
AMBER = "#ffc14d"
GREEN = "#5fd97a"
GOLD = "#ffd95e"


# --------------------------------------------------------------- Rutas
def app_data_dir():
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    path = os.path.join(base, "CofreTracker")
    os.makedirs(path, exist_ok=True)
    return path


CONFIG_PATH = os.path.join(app_data_dir(), "config.json")


def default_lang():
    try:
        code = (locale.getdefaultlocale()[0] or "en")[:2].lower()
    except Exception:  # noqa: BLE001
        code = "en"
    return code if code in TR else "en"


DEFAULT_CONFIG = {
    "minutes": 12,
    "muted": False,
    "volume": 70,
    "lang": default_lang(),
    "maps": [],  # [{"name","chest_lv","difficulty","next_ready","completed"}]
}


def load_config():
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            cfg.update({k: data.get(k, v) for k, v in DEFAULT_CONFIG.items()})
        except Exception:  # noqa: BLE001
            pass
    return cfg


def fmt_time(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


# ------------------------------------------------------------- Sonido
_SOUND_CACHE = {}


def _build_sound(volume):
    """Genera un WAV en memoria (4 tonos ascendentes) escalado por volumen."""
    rate = 22050
    amp = int(32767 * max(0.0, min(1.0, volume)))
    tones = [(700, 0.16), (900, 0.16), (1100, 0.16), (1400, 0.20)]
    fade = int(rate * 0.005)
    frames = bytearray()
    for freq, dur in tones:
        n = int(rate * dur)
        for i in range(n):
            env = 1.0
            if i < fade:
                env = i / fade
            elif i > n - fade:
                env = max(0.0, (n - i) / fade)
            val = int(amp * env * math.sin(2 * math.pi * freq * i / rate))
            frames += struct.pack("<h", val)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(bytes(frames))
    return buf.getvalue()


def get_sound(volume):
    key = round(volume, 2)
    if key not in _SOUND_CACHE:
        _SOUND_CACHE[key] = _build_sound(volume)
    return _SOUND_CACHE[key]


def play_ready_sound(volume):
    """volume: 0.0 .. 1.0. Reproduce sin bloquear (async)."""
    if volume <= 0 or not HAS_SOUND:
        return

    def run():
        try:
            winsound.PlaySound(get_sound(volume),
                               winsound.SND_MEMORY | winsound.SND_ASYNC)
        except Exception:  # noqa: BLE001
            try:
                winsound.MessageBeep()
            except Exception:  # noqa: BLE001
                pass

    threading.Thread(target=run, daemon=True).start()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("500x760")
        self.root.minsize(470, 580)
        self.root.configure(bg=ROOT_BG)
        self._set_icon()

        self.cfg = load_config()
        self.lang = self.cfg.get("lang", default_lang())
        self.maps = []
        for m in self.cfg.get("maps", []):
            lv = m.get("chest_lv")
            if not lv:  # migracion desde la version vieja (campo "chest")
                mt = re.search(r"Lv\s*\d+", m.get("chest", ""))
                lv = mt.group(0).replace(" ", "") if mt else ""
            self.maps.append({
                "name": m.get("name", "Map"),
                "chest_lv": lv,
                "difficulty": m.get("difficulty", ""),
                "next_ready": m.get("next_ready"),
                "completed": m.get("completed", 0),
                "_w": None,
                "_fired": False,
            })

        self.minutes_var = tk.IntVar(value=self.cfg.get("minutes", 12))
        self.muted_var = tk.BooleanVar(value=self.cfg.get("muted", False))
        self.volume_var = tk.DoubleVar(value=self.cfg.get("volume", 70))
        self.map_name_var = tk.StringVar()
        self.diff_var = tk.StringVar(value="Normal")
        self.suggestion_var = tk.StringVar()
        self.lang_name_var = tk.StringVar(value=dict(LANGS).get(self.lang, "English"))

        self._init_style()
        self._build_ui()
        self.render_maps()
        self.tick()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def t(self, key):
        return TR.get(self.lang, TR["en"]).get(key, TR["en"].get(key, key))

    def _set_icon(self):
        try:
            self._icon_img = tk.PhotoImage(file=resource_path(ICON_FILE))
            self.root.iconphoto(True, self._icon_img)
        except Exception:  # noqa: BLE001
            pass

    # --------------------------------------------------------- Estilo
    def _init_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:  # noqa: BLE001
            pass
        style.configure("TFrame", background=ROOT_BG)
        style.configure("TLabel", background=ROOT_BG, foreground=TEXT_MAIN)
        style.configure("Header.TLabel", background=ROOT_BG, foreground=TEXT_MAIN,
                        font=("Segoe UI", 16, "bold"))
        style.configure("Dim.TLabel", background=ROOT_BG, foreground=TEXT_DIM,
                        font=("Segoe UI", 9))
        style.configure("TCheckbutton", background=ROOT_BG, foreground=TEXT_MAIN)
        style.map("TCheckbutton", background=[("active", ROOT_BG)])
        style.configure("Add.TButton", font=("Segoe UI", 10, "bold"), padding=6)
        style.configure("TCombobox", padding=3)
        style.configure("Horizontal.TScale", background=ROOT_BG)

    # ------------------------------------------------------------ UI
    def _build_ui(self):
        # --- Header: titulo + manual
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=14, pady=(12, 4))
        ttk.Label(header, text=APP_TITLE, style="Header.TLabel").pack(side="left")
        self.manual_btn = ttk.Button(header, text=self.t("manual"), width=9,
                                     command=self.show_manual)
        self.manual_btn.pack(side="right")

        # --- Sonido: mute + volumen + test
        snd_row = ttk.Frame(self.root)
        snd_row.pack(fill="x", padx=14, pady=2)
        self.mute_chk = ttk.Checkbutton(
            snd_row, text=self.t("mute"), variable=self.muted_var,
            command=self.save_config)
        self.mute_chk.pack(side="left")
        self.vol_lbl = ttk.Label(snd_row, text=self.t("volume"), style="Dim.TLabel")
        self.vol_lbl.pack(side="left", padx=(14, 4))
        ttk.Scale(snd_row, from_=0, to=100, variable=self.volume_var,
                  command=self.on_volume_change).pack(side="left", fill="x",
                                                      expand=True, padx=4)
        self.vol_pct = ttk.Label(snd_row, text=f"{int(self.volume_var.get())}%",
                                 style="Dim.TLabel", width=4)
        self.vol_pct.pack(side="left")
        tk.Button(snd_row, text="▶", relief="flat", cursor="hand2", bg="#44445a",
                  fg=TEXT_MAIN, activebackground="#55556e", width=3,
                  command=self.test_sound).pack(side="left", padx=(4, 0))

        # --- Idioma + minutos
        lang_row = ttk.Frame(self.root)
        lang_row.pack(fill="x", padx=14, pady=2)
        self.lang_lbl = ttk.Label(lang_row, text=self.t("language"),
                                 style="Dim.TLabel")
        self.lang_lbl.pack(side="left")
        lang_combo = ttk.Combobox(
            lang_row, textvariable=self.lang_name_var, state="readonly", width=12,
            values=[name for _, name in LANGS])
        lang_combo.pack(side="left", padx=6)
        lang_combo.bind("<<ComboboxSelected>>", self.on_lang_change)
        self.minutes_lbl = ttk.Label(lang_row, text=self.t("minutes"),
                                     style="Dim.TLabel")
        self.minutes_lbl.pack(side="left", padx=(14, 4))
        ttk.Spinbox(lang_row, from_=1, to=120, width=5,
                    textvariable=self.minutes_var,
                    command=self.save_config).pack(side="left")

        ttk.Separator(self.root).pack(fill="x", padx=14, pady=6)

        # --- Agregar manual (nombre + dificultad)
        add_row = ttk.Frame(self.root)
        add_row.pack(fill="x", padx=14, pady=2)
        self.name_entry = tk.Entry(
            add_row, textvariable=self.map_name_var, bg="#2b2b40", fg=TEXT_MAIN,
            insertbackground=TEXT_MAIN, relief="flat", font=("Segoe UI", 11))
        self.name_entry.pack(side="left", fill="x", expand=True, ipady=4,
                             padx=(0, 6))
        self.name_entry.bind("<Return>", lambda e: self.add_custom_map())
        ttk.Combobox(add_row, textvariable=self.diff_var, state="readonly",
                     width=10, values=DIFFICULTIES).pack(side="left", padx=(0, 6))
        self.add_btn = ttk.Button(add_row, text=self.t("add_map"),
                                 style="Add.TButton", command=self.add_custom_map)
        self.add_btn.pack(side="left")

        # --- Sugerencias
        sugg_row = ttk.Frame(self.root)
        sugg_row.pack(fill="x", padx=14, pady=(6, 2))
        self.sugg_lbl = ttk.Label(sugg_row, text=self.t("suggestions"),
                                 style="Dim.TLabel")
        self.sugg_lbl.pack(side="left")
        self.sugg_combo = ttk.Combobox(
            sugg_row, textvariable=self.suggestion_var, state="readonly",
            values=self._suggestion_values())
        self.sugg_combo.pack(side="left", fill="x", expand=True, padx=6)
        self.add_sugg_btn = ttk.Button(sugg_row, text=self.t("add"),
                                      command=self.add_suggestion)
        self.add_sugg_btn.pack(side="left")

        # --- Lista scrolleable
        list_wrap = ttk.Frame(self.root)
        list_wrap.pack(fill="both", expand=True, padx=10, pady=(8, 6))
        self.canvas = tk.Canvas(list_wrap, bg=ROOT_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_wrap, orient="vertical",
                                  command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self._win = self.canvas.create_window((0, 0), window=self.inner,
                                              anchor="nw")
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self._win, width=e.width))
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind_all("<MouseWheel>", self._on_wheel)

        # --- Footer: link al repo
        self.footer_link = tk.Label(
            self.root, text=self.t("star"), bg=ROOT_BG, fg="#6cd0ff",
            cursor="hand2", font=("Segoe UI", 10, "underline"))
        self.footer_link.pack(pady=(0, 10))
        self.footer_link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))

    def _suggestion_values(self):
        return [f"{stage}   ·   {self.t('blue_chest')} {lv}   ·   {diff}"
                for stage, lv, diff in SUGGESTIONS]

    def _on_wheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    # ------------------------------------------------------- Sonido UI
    def on_volume_change(self, _value=None):
        self.vol_pct.config(text=f"{int(self.volume_var.get())}%")
        self.save_config()

    def test_sound(self):
        play_ready_sound(self.volume_var.get() / 100.0)

    # ------------------------------------------------------ Idioma
    def on_lang_change(self, _event=None):
        name = self.lang_name_var.get()
        for code, disp in LANGS:
            if disp == name:
                self.lang = code
                break
        self.save_config()
        self.apply_language()

    def apply_language(self):
        self.manual_btn.config(text=self.t("manual"))
        self.mute_chk.config(text=self.t("mute"))
        self.vol_lbl.config(text=self.t("volume"))
        self.lang_lbl.config(text=self.t("language"))
        self.minutes_lbl.config(text=self.t("minutes"))
        self.add_btn.config(text=self.t("add_map"))
        self.sugg_lbl.config(text=self.t("suggestions"))
        self.add_sugg_btn.config(text=self.t("add"))
        self.footer_link.config(text=self.t("star"))
        idx = self.sugg_combo.current()
        self.sugg_combo.config(values=self._suggestion_values())
        if idx >= 0:
            self.sugg_combo.current(idx)
        self.render_maps()

    # ------------------------------------------------------- Manual
    def show_manual(self):
        win = tk.Toplevel(self.root)
        win.title(self.t("manual_title"))
        win.geometry("520x440")
        win.configure(bg=ROOT_BG)
        tk.Label(win, text=self.t("manual_title"), bg=ROOT_BG, fg=TEXT_MAIN,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=16, pady=12)
        txt = tk.Text(win, wrap="word", bg="#2b2b40", fg=TEXT_MAIN,
                      relief="flat", font=("Segoe UI", 10), padx=12, pady=12)
        txt.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        txt.insert("1.0", self.t("manual_body"))
        txt.config(state="disabled")
        link = tk.Label(win, text=self.t("star"), bg=ROOT_BG, fg="#6cd0ff",
                        cursor="hand2", font=("Segoe UI", 10, "underline"))
        link.pack(pady=(0, 12))
        link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))

    # ------------------------------------------------------- Tracker
    def add_custom_map(self):
        name = self.map_name_var.get().strip()
        if not name:
            return
        self._append_map(name, "", self.diff_var.get())
        self.map_name_var.set("")

    def add_suggestion(self):
        idx = self.sugg_combo.current()
        if idx < 0:
            return
        stage, lv, diff = SUGGESTIONS[idx]
        if any(m["name"] == stage for m in self.maps):
            return  # evita duplicados
        self._append_map(stage, lv, diff)

    def _append_map(self, name, chest_lv, difficulty):
        self.maps.append({
            "name": name, "chest_lv": chest_lv, "difficulty": difficulty,
            "next_ready": None, "completed": 0, "_w": None, "_fired": False,
        })
        self.render_maps()
        self.save_config()

    def remove_map(self, target):
        self.maps = [m for m in self.maps if m is not target]
        self.render_maps()
        self.save_config()

    def drop_map(self, m):
        m["next_ready"] = time.time() + self.minutes_var.get() * 60
        m["_fired"] = False
        self.save_config()

    def reset_map(self, m):
        m["next_ready"] = None
        m["_fired"] = False
        self.save_config()

    def render_maps(self):
        for child in self.inner.winfo_children():
            child.destroy()

        if not self.maps:
            tk.Label(self.inner, text=self.t("no_maps"), bg=ROOT_BG, fg=TEXT_DIM,
                     font=("Segoe UI", 11), justify="center").pack(pady=40)
            return

        for m in self.maps:
            card = tk.Frame(self.inner, bg=CARD_IDLE)
            card.pack(fill="x", pady=3, padx=4)

            top = tk.Frame(card, bg=CARD_IDLE)
            top.pack(fill="x", padx=10, pady=(5, 0))
            name_lbl = tk.Label(top, text=m["name"], bg=CARD_IDLE, fg=TEXT_MAIN,
                                font=("Segoe UI", 11, "bold"), anchor="w")
            name_lbl.pack(side="left")

            badge = None
            if m["difficulty"] in DIFFICULTY_COLORS:
                badge = tk.Label(
                    top, text=f" {m['difficulty']} ",
                    bg=DIFFICULTY_COLORS[m["difficulty"]], fg="white",
                    font=("Segoe UI", 8, "bold"))
                badge.pack(side="left", padx=6)

            del_btn = tk.Label(top, text="✕", bg=CARD_IDLE, fg=TEXT_DIM,
                               font=("Segoe UI", 10), cursor="hand2")
            del_btn.pack(side="right")
            del_btn.bind("<Button-1>", lambda e, mm=m: self.remove_map(mm))
            done_lbl = tk.Label(top, text=f"✓ {m['completed']}", bg=CARD_IDLE,
                                fg=GOLD, font=("Segoe UI", 9, "bold"))
            done_lbl.pack(side="right", padx=8)

            chest_lbl = None
            if m["chest_lv"]:
                chest_lbl = tk.Label(
                    top, text=f"·  {self.t('blue_chest')} {m['chest_lv']}",
                    bg=CARD_IDLE, fg=TEXT_DIM, font=("Segoe UI", 8))
                chest_lbl.pack(side="left", padx=6)

            bottom = tk.Frame(card, bg=CARD_IDLE)
            bottom.pack(fill="x", padx=10, pady=(2, 6))
            time_lbl = tk.Label(bottom, text="--:--", bg=CARD_IDLE, fg=TEXT_DIM,
                                font=("Consolas", 17, "bold"), width=6, anchor="w")
            time_lbl.pack(side="left")
            tk.Button(bottom, text=self.t("dropped"), relief="flat", cursor="hand2",
                      bg="#3a6df0", fg="white", activebackground="#2f5bd0",
                      activeforeground="white", font=("Segoe UI", 9, "bold"),
                      command=lambda mm=m: self.drop_map(mm)).pack(
                          side="left", fill="x", expand=True, ipady=2, padx=(4, 4))
            tk.Button(bottom, text=self.t("reset"), relief="flat", cursor="hand2",
                      bg="#44445a", fg=TEXT_MAIN, activebackground="#55556e",
                      activeforeground="white", font=("Segoe UI", 9),
                      command=lambda mm=m: self.reset_map(mm)).pack(
                          side="left", ipady=2)

            m["_w"] = {
                "card": card, "top": top, "btns": bottom, "name": name_lbl,
                "badge": badge, "chest": chest_lbl, "done": done_lbl,
                "time": time_lbl, "del": del_btn,
            }

    def _paint(self, m, bg, time_fg):
        w = m["_w"]
        if not w:
            return
        for key in ("card", "top", "btns"):
            w[key].config(bg=bg)
        w["name"].config(bg=bg)
        w["del"].config(bg=bg)
        w["done"].config(bg=bg)
        if w["chest"]:
            w["chest"].config(bg=bg)
        w["time"].config(bg=bg, fg=time_fg)

    def tick(self):
        now = time.time()
        for m in self.maps:
            if not m["_w"]:
                continue
            w = m["_w"]
            w["done"].config(text=f"✓ {m['completed']}")
            nr = m["next_ready"]
            if nr is None:
                w["time"].config(text="--:--")
                self._paint(m, CARD_IDLE, TEXT_DIM)
            else:
                rem = nr - now
                if rem <= 0:
                    w["time"].config(text=self.t("ready"))
                    self._paint(m, CARD_READY, GREEN)
                    if not m["_fired"]:
                        m["_fired"] = True
                        m["completed"] += 1
                        w["done"].config(text=f"✓ {m['completed']}")
                        if not self.muted_var.get():
                            play_ready_sound(self.volume_var.get() / 100.0)
                        self.save_config()
                        self._flash(m)
                else:
                    w["time"].config(text=fmt_time(rem))
                    self._paint(m, CARD_RUNNING, AMBER)
        self.root.after(250, self.tick)

    def _flash(self, m, count=6):
        if count <= 0 or not m["_w"]:
            return
        w = m["_w"]
        cur = w["card"].cget("bg")
        nxt = "#2f6b3f" if cur == CARD_READY else CARD_READY
        for key in ("card", "top", "btns"):
            w[key].config(bg=nxt)
        for key in ("name", "del", "done", "time"):
            w[key].config(bg=nxt)
        if w["chest"]:
            w["chest"].config(bg=nxt)
        self.root.after(220, lambda: self._flash(m, count - 1))

    # -------------------------------------------------------- Config
    def save_config(self):
        self.cfg["minutes"] = self.minutes_var.get()
        self.cfg["muted"] = bool(self.muted_var.get())
        self.cfg["volume"] = int(self.volume_var.get())
        self.cfg["lang"] = self.lang
        self.cfg["maps"] = [
            {"name": m["name"], "chest_lv": m["chest_lv"],
             "difficulty": m["difficulty"], "next_ready": m["next_ready"],
             "completed": m["completed"]}
            for m in self.maps
        ]
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
                json.dump(self.cfg, fh, indent=2, ensure_ascii=False)
        except Exception:  # noqa: BLE001
            pass

    def on_close(self):
        self.save_config()
        self.root.destroy()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
