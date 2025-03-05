# ----- Importy a globální konstanty
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import logging
import socket
import sqlite3
from openpyxl import load_workbook
import json
import calendar
from datetime import datetime, date, timedelta
import base64
import os
import time
import getpass

# ----- Verze programu
__version__="1.2.0"

# -----1.0.0 Základní funkčnost programu: Náhled, Editace, Role, Přístupy, Logy, Základní nastavení, Vytvoření databáze, Uložení základního nastavení, Import dat z Ecxelu
# ----- 1.1.0 Doplnění o funkci: Zamknutí Plánu a Odeknutí plánu s ukádáním do Globálního nastavení Pro Admina a Superadmina
# ------ 1.2.0 Přidána fuknce zavření okna po odhlášení uživatele

# Přidejte funkci show_verze() na globální úroveň
def show_verze():
    info_text = "Správa Plánu Služeb a Dovolených \nVerze: " + __version__ + "\n(C) 2025 Holub Stanislav"
    messagebox.showinfo("O aplikaci", info_text)

# ----- Mapa barev: převod českých názvů na anglické
COLOR_MAP = {
    "žluté": "yellow",
    "zelené": "green",
    "oranžové": "orange",
    "růžové": "pink",
    "modré": "blue",
    "hnědé": "brown",
    "neutrální": "SystemButtonFace",
    "fialové": "purple",
    "tyrkysové": "turquoise",
    "šedé": "gray"
}

# Přidejte funkci show_help() na globální úroveň
def show_help():
    """Otevře okno s rozšířenou nápovědou aplikace podle rolí."""
    help_win = tk.Toplevel(root)
    help_win.title("Nápověda")
    help_win.geometry("700x550")
    
    help_text = (
        "Správa Plánu Služeb a Dovolených verze: "+__version__+"\n\n"
        "Tento program slouží k návrhu plánu služeb, dovolených a vypuštěných směna. Aplikace nabízí různé funkcen\n"
        "pro zadávání, editaci a správu plánů, a to prostřednictvím přehledného grafického rozhraní.\n\n"
        
        "OMEZENÍ ODPOVĚDNOSTI A UŽÍVÁNÍ NA VLASTNÍ NEBEZPEČÍ:\n\n"
        "Používání této aplikace probíhá na vlastní odpovědnost uživatele. Autor, vývojáři a distributoři tohoto\n" 
        "softwaru neposkytují žádné záruky, a to ani v rozsahu výslovném, ani předpokládaném, včetně záruk obchodovatelnosti\n"
        "či vhodnosti pro konkrétní účely. V žádném případě nebudou odpovědní za jakékoliv přímé, nepřímé, náhodné či\n"
        "následné škody, ztrátu dat nebo jiné nepříznivé důsledky vyplývající z používání aplikace. Uživatelé jsou\n"
        "povinni ověřit správnost a úplnost všech dat před jejich použitím.\n\n"

        "RYCHLÁ NÁPOVĚDA\n\n"
        "1. Výběr záložky:\n"
        "- přejdi na záložku ZAMĚSTANEC pro plán na celý rok, nebo na záložku Směny pro plán na zvolený měsíc.\n\n"

        "2. Záložka Zaměstnanec:\n"
        "Výběr zaměstnance a roku: V záložce Zaměstnanec vyberte své jméno ze seznamu a zvolte požadovaný rok.\n"
        "Zobrazení plánu: Klikněte na tlačítko Zobrazit plán, čímž se načte váš detailní plán směn.\n\n"

        "3. Záložka Směny:\n"
        "Výběr filtrů: Přejděte do záložky Směny.\n"
        "Nastavení filtrů: Vyberte z rozevíracích seznamů rok, měsíc a konkrétní směnu, pro kterou chcete plán zobrazit.\n"
        "Načtení plánu: Klikněte na tlačítko Zobraz plán Směny, které načte plány pro zadaná kritéria.\n\n"

        "Tento postup vám umožní rychle najít a zobrazit svůj plán směn, ať už hledáte pod svou osobou nebo chcete prohlížet plány celé směny.\n\n\n"

        "PODROBNĚJŠÍ NÁVOD\n\n"

        "Role v aplikaci:\n"
        "   - Uživatel: Má omezený přístup k prohlížení a základnímu filtrování plánů.\n"
        "   - Velitel: Může upravovat plány své směny a má rozšířená práva pro zadávání a kontrolu směn a dovolených.\n"
        "   - Admin: Má plná oprávnění k úpravám, správě databáze a konfiguraci aplikace.\n"
        "   - Superadmin: Má nejvyšší oprávnění, včetně zásahu do globálních nastavení a údržby systému.\n\n"
        
        "Nápověda aplikace:\n\n"
        "1. Zadávání a editace plánů:\n"
        "   - Aplikace umožňuje zadávat a editovat plány služeb pomocí přehledného grafického rozhraní.\n"
        "   - Plány lze editovat přímo v tabulkách, kde jsou zobrazeny podrobnosti o jednotlivých dnech.\n\n"
        
        "2. Logování a bezpečnost:\n"
        "   - Každá akce (přihlášení, úpravy, mazání) je automaticky zaznamenána do log souboru.\n"
        "   - Přístupová práva jsou nastavena tak, že každý uživatel má přístup pouze k funkcím odpovídajícím jeho roli.\n\n"
        
        "3. Nastavení a konfigurace:\n"
        "   - V sekci 'Nastavení' jen superadmin můžete měnit globální parametry, jako jsou úvazky, směny, barvy a počet hodin přiřazených jednotlivým směnám.\n"
        "   - Tyto hodnoty ovlivňují výpočty v aplikaci, například celkový součet hodin a počet směn v plánovaných službách.\n\n"
        
        "4. Další funkce:\n"
        "   - Aplikace umožňuje načítání dat z Excelu, automatické zálohování databáze a filtrování záznamů podle různých kritérií.\n\n"
        
        "Specifické informace podle rolí.\n\n"
        
        "   Uživatel:\n"
        "      - Může pouze prohlížet plány a využívat základní filtrování.\n"
        "      - Nemá oprávnění k úpravám nebo mazání záznamů.\n\n"
        
        "   Velitel:\n"
        "      - Má rozšířená oprávnění k zadávání a úpravě Vlastních plánů směny.\n"
        "      - Může kontrolovat a upravovat své směny, ale nemůže zasahovat do plánů ostatních.\n\n"
        
        "   Admin:\n"
        "      - Má plná práva k editaci, Správě databáze a Konfiguraci aplikace.\n"
        "      - Může měnit Globální nastavení a zadávat nové údaje, které ovlivňují všechny plány.\n"
        "      - Může uzamknout plán služeb, po uazmčení nejde plán editovat.\n\n"
        
        "   Superadmin:\n"
        "      - Má nejvyšší oprávnění v aplikaci.\n"
        "      - Může provádět zásahy do celého systému, včetně úprav Globálních nastavení, Správy logů a Databáze.\n"
        "      - Může uzamknout plán služeb, po uazmčení nejde plán editovat.\n\n"
        
        "5. Uživatelská podpora:\n"
        "   - Pro další informace nebo řešení problémů kontaktujte správce programu. Pokud zjistí chybu nahlašte ji správci.\n\n"
        
        "Tento návod shrnuje hlavní funkce a principy aplikace. Pro detailnější informace kontaktujte správce programu.\n\n"
        
        "Vysvětlivky k informační tabulce u zaměstnaců:\n"
        "   - Nová dovolená: Počet hodin aktuálně přičtených jako dovolená v daném roce.\n"
        "   - Stará dovolená: Počet hodin dovolené přenesených z předchozího období.\n"
        "   - Celkem dovolená: Součet nové a staré dovolené.\n"
        "   - Naplánovat Dov: Počet hodin dovolené, které jsou již naplánovány v rozvrhu.\n"
        "   - Rozdíl Plán a Nárok: Rozdíl mezi naplánovanou dovolenou v rozvrhu a skutečným nárokem na dovolenou.\n"
        "     ( něměla by se zde ukázat záporná hodnota !!!)\n"
        "   - Celkem směn: Celkový počet směn zaznamenaných v plánu.\n\n"
        "     K VYROVNÁNÍ HODIN V KALENDÁŘNÍM ROCE:\n"
        "   - Klouz I.: Počet vypuštěných směna za  I. pololetí. (X/X)\n"
        "     (X naplánovat v I. pololetí / X naplánováno I. pololetí )\n\n"
        "   - Klouz II.: Počet vypuštěných směna za II. pololetí.\n"
        "     (X naplánovat v II. pololetí / X naplánováno II. pololetí)\n\n"     
        "   - r I.: Počet ranních směn v I. pololetí.\n"
        "     (r naplánovat v I. pololetí / r naplánováno I. pololetí )\n\n"
        "   - r II.: Počet ranních směn ve I. pololetí.\n"
        "     (r naplánovat v II. pololetí / r naplánováno II. pololetí )\n\n"
        "   - zkratky v programu se shodují s tištěnou verzí Plánu služeb\n\n"

        "Licence pro otevřený software\n\n"

        "Copyright (c) [2025] [Holub Stanislav]\n"
        "Tento software je poskytován pod licencí pro otevřený software, dále jen „Licence“. Uživatelé této licence mají\n" 
        "právo používat, kopírovat, upravovat, spojovat, publikovat, distribuovat, sublicencovat a/nebo prodávat kopie softwaru,\n"
        "za následujících podmínek:\n\n"
        "1. Tento software je poskytován „jak je“, bez jakýchkoli záruk, vyjádřených nebo implicitních, včetně, ale neomezující se\n"
        "na implicitní záruky obchodovatelnosti, vhodnosti pro určitý účel a nezánětým právům. Autoři nebo vlastníci autorských práv\n" 
        "nejsou zodpovědní za jakékoli nároky, škody nebo jinou odpovědnost, ať už ve smlouvě, nebo z jiného důvodu, plynoucí z nebo\n" 
        "v souvislosti se softwarem nebo jeho používáním.\n\n"
        "2. Jména „[vlastník autorských práv]“ nemohou být použity k podpoře nebo propagaci výrobků odvozených z tohoto softwaru\n" 
        "bez předchozího písemného povolení.\n\n"
    )
    
    text_widget = tk.Text(help_win, wrap="word", font=("TkDefaultFont", 10))
    text_widget.insert("1.0", help_text)
    text_widget.config(state="disabled")
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    
    tk.Button(help_win, text="Zavřít", command=help_win.destroy).pack(pady=5)

# Název konfiguračního souboru
CONFIG_FILE = "global_settings.json"

# ----- Funkce pro zakódování a dekódování hesla
def encode_password(pwd):
    """Zakóduje heslo pomocí base64."""
    return base64.b64encode(pwd.encode("utf-8")).decode("utf-8")

def decode_password(encoded_pwd):
    """Dekóduje heslo zakódované pomocí base64."""
    return base64.b64decode(encoded_pwd.encode("utf-8")).decode("utf-8")

# ----- Ukládání a načítání konfigurace
def save_config(config):
    """Uloží nastavení do konfiguračního souboru."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Chyba při ukládání konfiguračního souboru: {e}")
        messagebox.showerror("Chyba", f"Chyba při ukládání nastavení: {e}")

def load_config():
    """
    Načte konfigurační soubor.
    Pokud soubor neexistuje, vytvoří výchozí konfiguraci s přístupovými záznamy.
    Pokud soubor existuje, ale chybí v něm záznam pro superadmin, doplní jej.
    """
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
            # ----- Kontrola existence záznamu pro superadmin
            access_list = config.get("access", [])
            if not any(entry[2] == "superadmin" for entry in access_list):
                access_list.insert(0, ("superadmin", encode_password("12345"), "superadmin"))
                config["access"] = access_list
                save_config(config)
        else:
            # Výchozí konfigurace, pokud soubor neexistuje
            config = {
                "40": [],
                "37.5": [],
                "37.75": [],
                "access": [
                    ("superadmin", encode_password("12345"), "superadmin"),
                    ("Velitel směny 1", encode_password("heslo1"), "velitel"),
                    ("Velitel směny 2", encode_password("heslo2"), "velitel"),
                    ("Velitel směny 3", encode_password("heslo3"), "velitel"),
                    ("Velitel směny 4", encode_password("heslo4"), "velitel"),
                    ("Velitel směny 5", encode_password("heslo5"), "velitel"),
                    ("Velitel směny 6", encode_password("heslo6"), "velitel"),
                ],
                "locked_plans": {}  # MOD: Výchozí prázdný slovník pro zámky plánů
            }
            save_config(config)
        # Zajištění, že všechny klíče existují
        for key in ["40", "37.5", "37.75", "access"]:
            if key not in config:
                config[key] = [] if key != "access" else []
        if "locked_plans" not in config:
            config["locked_plans"] = {}  # MOD: Ujistíme se, že existuje i klíč pro zámky
        return config
    except Exception as e:
        logging.error(f"Chyba při načítání konfiguračního souboru: {e}")
        messagebox.showerror("Chyba", f"Chyba při načítání nastavení: {e}")
        return {}

global_settings = load_config()

# ----- Globální proměnné pro správu uživatele a plánů
current_user_role = "uživatel"      # Role aktuálně přihlášeného uživatele
current_user_name = "uživatel"      # Jméno aktuálně přihlášeného uživatele
current_user_shift = None           # Pouze pro filtrování, nikoli pro oprávnění
current_record_id = None            # Uchovává id aktuálně zobrazeného plánu
month_frames = {}                   # Slovník pro uložení odkazů na jednotlivé měsíční rámce

# Deklarace globálních proměnných pro tlačítka zámku plánu
btn_lock_plan = None
btn_unlock_plan = None

# ----- Síťové a logovací funkce
def get_ip_address():
    """
    Vrací aktuální IP adresu.
    Používá se při logování akcí.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except Exception:
        try:
            ip = socket.gethostbyname(socket.gethostname())
            if ip.startswith("127."):
                addresses = [addr[4][0] for addr in socket.getaddrinfo(socket.gethostname(), None)
                             if not addr[4][0].startswith("127.")]
                ip = addresses[0] if addresses else "N/A"
        except Exception:
            ip = "N/A"
    return ip

def log_action(action):
    """
    Zapíše akci do logu, včetně informace o IP adrese a roli uživatele.
    """
    ip = get_ip_address()
    logged_in_user = getpass.getuser()  # nebo můžete použít os.getlogin(
    role = current_user_role if current_user_role else "neznámá"
    message = f"{action} - Role: {role} - IP: {ip} - PC uživatel: {logged_in_user}"
    logging.info(message)

logging.basicConfig(
    filename="service_plan_log.txt",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)

# ----- Funkce pro zálohování databáze
def backup_database():
    """
    Vytvoří zálohu databáze do adresáře 'db_backups'.
    Název zálohy obsahuje datum a čas.
    """
    try:
        backup_dir = "db_backups"
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"service_plans_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        with sqlite3.connect("service_plans.db") as src:
            with sqlite3.connect(backup_path) as dest:
                src.backup(dest)
        log_action("Záloha databáze byla úspěšně vytvořena")
    except Exception as e:
        logging.error(f"Chyba při záloze databáze: {e}")
        messagebox.showerror("Chyba", f"Chyba při záloze databáze: {e}")

# ----- Inicializace databáze a vytvoření tabulky
def init_db():
    """
    Inicializuje databázi a vytvoří tabulku 'plans', pokud ještě neexistuje.
    """
    try:
        with sqlite3.connect("service_plans.db") as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS plans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    osobni_cislo TEXT,
                    jmeno_prijmeni TEXT,
                    smena TEXT,
                    uvazek TEXT,
                    roky TEXT,
                    poradi TEXT,
                    stara_dovolena TEXT DEFAULT "0",
                    dovolena TEXT DEFAULT "0",
                    leden TEXT,
                    unor TEXT,
                    brezen TEXT,
                    duben TEXT,
                    kveten TEXT,
                    cerven TEXT,
                    cervenec TEXT,
                    srpen TEXT,
                    zari TEXT,
                    rijen TEXT,
                    listopad TEXT,
                    prosinec TEXT
                )
            """)
            conn.commit()
    except Exception as e:
        logging.error(f"Chyba při inicializaci databáze: {e}")
        messagebox.showerror("Chyba", f"Chyba při inicializaci databáze: {e}")

# ----- Funkce pro aktualizaci Treeview (filtrace a zobrazení dat)
def refresh_treeview_filtered(jmeno_filter="", rok_filter="", smena_filter=""):
    """
    Aktualizuje zobrazení seznamu záznamů v Treeview podle zadaných filtrů.
    """
    try:
        for item in tree.get_children():
            tree.delete(item)
        query = "SELECT id, jmeno_prijmeni, smena, uvazek, roky FROM plans WHERE 1=1"
        params = []
        if jmeno_filter:
            query += " AND jmeno_prijmeni = ?"
            params.append(jmeno_filter)
        if rok_filter:
            query += " AND roky = ?"
            params.append(rok_filter)
        if smena_filter != "":
            query += " AND smena = ?"
            params.append(smena_filter)
        with sqlite3.connect("service_plans.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            for row in cursor.fetchall():
                tree.insert("", tk.END, iid=row["id"],
                            values=(row["jmeno_prijmeni"], row["smena"], row["uvazek"], row["roky"]))
    except Exception as e:
        logging.error(f"Chyba při načítání dat do Treeview: {e}")
        messagebox.showerror("Chyba", f"Chyba při načítání dat: {e}")

def refresh_treeview():
    """Obnoví Treeview a resetuje filtry."""
    filter_jmeno.set("")
    filter_rok.set(str(datetime.now().year))
    filter_smena.set("")
    filter_smena.config(state="readonly")
    refresh_treeview_filtered()

# ----- Pomocné funkce a výpočty
def compute_easter(year):
    """
    Vypočítá datum Velikonoc pro daný rok.
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def load_month_data(ws, month_rows):
    """
    Načte data z Excelového listu pro dané řádky odpovídající jednotlivým měsícům.
    """
    try:
        data = {}
        for month, row in month_rows.items():
            row_values = [cell for cell in next(ws.iter_rows(min_row=row, max_row=row,
                                                               min_col=1, max_col=32, values_only=True))]
            data[month] = json.dumps(row_values, ensure_ascii=False)
        return data
    except Exception as e:
        logging.error(f"Chyba při načítání dat z Excelu: {e}")
        messagebox.showerror("Chyba", f"Chyba při načítání dat z Excelu: {e}")
        return {}

def treeview_sort_column(tv, col, reverse):
    """
    Seřadí sloupec v Treeview podle hodnot.
    """
    try:
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(key=lambda t: t[0], reverse=reverse)
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
    except Exception as e:
        logging.error(f"Chyba při řazení sloupce {col}: {e}")

def calculate_month_summary(day_plan_list, uvazek):
    """
    Vypočítá součet hodin a četnost jednotlivých směn pro daný měsíc.
    """
    summary = {}
    total_hours = 0
    uvazek_config = global_settings.get(uvazek, [])
    for entry in uvazek_config:
        shift_name = entry[0]
        summary[shift_name] = 0
    for i in range(1, len(day_plan_list)):
        shift = str(day_plan_list[i]).strip() if day_plan_list[i] is not None else ""
        for entry in uvazek_config:
            if shift == entry[0]:
                try:
                    hours = int(entry[1])
                except ValueError:
                    hours = 0
                total_hours += hours
                summary[shift] += 1
                break
    return total_hours, summary

# ----- NOVÉ: Funkce pro zamykání a odemykání plánu
def lock_plan():
    """
    Zamkne plán pro zadaný rok, měsíc a směnu.
    """
    rok = combo_rok_smena.get().strip()
    mesic_display = combo_mesic_smena.get().strip()
    smena_val = combo_smena_smena.get().strip()
    if not (rok and mesic_display and smena_val):
        messagebox.showwarning("Upozornění", "Vyberte Rok, měsíc a Směnu pro zamknutí.")
        return
    mesic_map = {"Leden": "leden", "Únor": "unor", "Březen": "brezen", "Duben": "duben", "Květen": "kveten",
                 "Červen": "cerven", "Červenec": "cervenec", "Srpen": "srpen", "Září": "zari",
                 "Říjen": "rijen", "Listopad": "listopad", "Prosinec": "prosinec"}
    internal_mesic = mesic_map.get(mesic_display, mesic_display.lower())
    key = f"{rok}_{smena_val}_{internal_mesic}"
    global_settings["locked_plans"][key] = True
    save_config(global_settings)
    messagebox.showinfo("Zámek", f"Plán {key} byl zamknut.")
    zobraz_plan_smeny()  # Obnoví zobrazení plánu

def unlock_plan():
    """
    Odemkne plán pro zadaný rok, měsíc a směnu.
    """
    rok = combo_rok_smena.get().strip()
    mesic_display = combo_mesic_smena.get().strip()
    smena_val = combo_smena_smena.get().strip()
    if not (rok and mesic_display and smena_val):
        messagebox.showwarning("Upozornění", "Vyberte Rok, Měsíc a Směnu pro odemknutí.")
        return
    mesic_map = {"Leden": "leden", "Únor": "unor", "Březen": "brezen", "Duben": "duben", "Květen": "kveten",
                 "Červen": "cerven", "Červenec": "cervenec", "Srpen": "srpen", "Září": "zari",
                 "Říjen": "rijen", "Listopad": "listopad", "Prosinec": "prosinec"}
    internal_mesic = mesic_map.get(mesic_display, mesic_display.lower())
    key = f"{rok}_{smena_val}_{internal_mesic}"
    if key in global_settings.get("locked_plans", {}):
        del global_settings["locked_plans"][key]
        save_config(global_settings)
        messagebox.showinfo("Zámek", f"Plán {key} byl odemknut.")
    else:
        messagebox.showinfo("Zámek", "Plán není zamknut.")
    zobraz_plan_smeny()  # Obnoví zobrazení plánu

# ----- Funkce pro zobrazení dialogu s výběrem směny
def ask_shift(allowed_shifts, current_value):
    """
    Zobrazí dialogové okno pro výběr směny a vrátí vybranou hodnotu.
    """
    dialog = tk.Toplevel()
    dialog.title("Vyberte směnu")
    tk.Label(dialog, text="Vyberte směnu:").pack(padx=10, pady=10)
    combo = ttk.Combobox(dialog, state="readonly", values=allowed_shifts)
    if current_value in allowed_shifts:
        combo.set(current_value)
    else:
        combo.set(allowed_shifts[0])
    combo.pack(padx=10, pady=5)
    result = {"value": None}
    def on_ok():
        result["value"] = combo.get()
        dialog.destroy()
    def on_cancel():
        dialog.destroy()
    btn_frame = tk.Frame(dialog)
    btn_frame.pack(padx=10, pady=10)
    tk.Button(btn_frame, text="OK", command=on_ok).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Zrušit", command=on_cancel).pack(side=tk.LEFT, padx=5)
    dialog.grab_set()
    dialog.wait_window()
    return result["value"]

# ----- Upravená funkce pro vykreslení měsíčního plánu s kontrolou zámku
def render_month_grid(parent, year, month_num, plan_json, month_label, holidays, uvazek, smena, editable=False, highlight=False):
    """
    Vykreslí mřížku měsíčního plánu.
    Zahrnuje záhlaví s dny v týdnu, čísla dnů a hodnoty plánu.
    Přidána kontrola, zda je plán zamknutý.
    """
    try:
        if highlight:
            frame = tk.LabelFrame(parent, text=month_label, font=("TkDefaultFont", 10, "bold"), bd=3, relief="groove")
        else:
            frame = tk.LabelFrame(parent, text=month_label, font=("TkDefaultFont", 10, "bold"))
        frame.pack(fill=tk.X, padx=5, pady=5)
        _, num_days = calendar.monthrange(int(year), month_num)
        try:
            day_plan_list = json.loads(plan_json)
        except Exception:
            day_plan_list = [""] * 32
        frame.day_plan_list = day_plan_list

        # MOD: Kontrola, zda je plán zamknutý
        mesic_map = {"Leden": "leden", "Únor": "unor", "Březen": "brezen", "Duben": "duben", "Květen": "kveten",
                     "Červen": "cerven", "Červenec": "cervenec", "Srpen": "srpen", "Září": "zari",
                     "Říjen": "rijen", "Listopad": "listopad", "Prosinec": "prosinec"}
        internal_month = mesic_map.get(month_label, month_label.lower())
        key = f"{year}_{smena}_{internal_month}"
        if global_settings.get("locked_plans", {}).get(key, False):
            frame.is_locked = True
            tk.Label(frame, text="Plán je zamknut 🔒", font=("TkDefaultFont", 10, "bold"), fg="red")\
              .grid(row=4, column=0, columnspan=num_days, pady=5)
        else:
            frame.is_locked = False

        weekdays = ["Po", "Út", "St", "Čt", "Pá", "So", "Ne"]

        # ----- Vykreslení záhlaví s dny v týdnu
        for day in range(1, num_days + 1):
            current_date = date(int(year), month_num, day)
            weekday = current_date.weekday()
            if current_date in holidays:
                header_bg = "red"
                header_font = ("TkDefaultFont", 10, "bold")
            elif weekday >= 5:
                header_bg = "gray"
                header_font = ("TkDefaultFont", 10, "bold")
            else:
                header_bg = "white"
                header_font = ("TkDefaultFont", 10)
            abbrev = weekdays[weekday]
            tk.Label(frame, text=abbrev, borderwidth=1, relief="solid", width=4,
                     bg=header_bg, font=header_font).grid(row=0, column=day-1, padx=1, pady=1)
        # ----- Vykreslení čísel dnů
        for day in range(1, num_days + 1):
            current_date = date(int(year), month_num, day)
            weekday = current_date.weekday()
            if current_date in holidays:
                day_bg = "red"
            elif weekday >= 5:
                day_bg = "gray"
            else:
                day_bg = "white"
            tk.Label(frame, text=str(day), borderwidth=1, relief="solid", width=4,
                     bg=day_bg).grid(row=1, column=day-1, padx=1, pady=1)
        # ----- Vykreslení jednotlivých hodnot plánu
        for day in range(1, num_days + 1):
            current_date = date(int(year), month_num, day)
            weekday = calendar.weekday(int(year), month_num, day)
            bg = "white"
            if weekday >= 5:
                bg = "lightgray"
            if current_date in holidays:
                bg = "red"
            plan_value = ""
            if day < len(day_plan_list):
                plan_value = str(day_plan_list[day]) if day_plan_list[day] is not None else ""
            if plan_value:
                for entry in global_settings.get(uvazek, []):
                    if plan_value == entry[0]:
                        if entry[2].lower() != "neutrální":
                            bg = COLOR_MAP.get(entry[2], entry[2])
                        break
            if editable:
                widget = tk.Button(frame, text=plan_value, width=4, bg=bg)
                # MOD: předání informace o zámku do funkce editace buňky
                widget.config(command=lambda w=widget, idx=day, dpl=frame.day_plan_list, uvazek=uvazek, locked=frame.is_locked:
                              edit_cell(w, idx, dpl, uvazek, locked))
            else:
                widget = tk.Label(frame, text=plan_value, borderwidth=1, relief="solid", width=4, bg=bg)
            widget.grid(row=2, column=day-1, padx=1, pady=1)
        # ----- Výpočet a vykreslení souhrnu pro daný měsíc
        total_hours, summary = calculate_month_summary(day_plan_list, uvazek)
        summary_text = f"Celkem: {total_hours} hodin | " + " | ".join([f"{shift}={count}" for shift, count in summary.items()])
        tk.Label(frame, text=summary_text, font=("TkDefaultFont", 10, "italic")).grid(row=3, column=0, columnspan=num_days, pady=5)
        return frame
    except Exception as e:
        logging.error(f"Chyba při renderování plánu pro {month_label}: {e}")
        messagebox.showerror("Chyba", f"Chyba při renderování plánu: {e}")

# ----- Upravená funkce pro úpravu buňky (plán směny)
def edit_cell(button, day_index, day_plan_list, uvazek, locked=False):
    """
    Umožňuje úpravu hodnoty buňky, pokud má uživatel dostatečná oprávnění.
    """
    if locked:
        messagebox.showwarning("Upozornění", "Plán je zamknut 🔒. Úpravy nejsou povoleny.")
        return
    old_value = button["text"].strip()  # Definice původní hodnoty
    if current_user_role in ["admin", "superadmin"]:
        pass  # Admin má plná práva
    elif current_user_role == "velitel":
        if button["text"].strip() == "":
            messagebox.showerror("Chyba", "Nemáte oprávnění měnit prázdnou buňku.")
            return
    else:
        messagebox.showerror("Chyba", "Nemáte oprávnění k úpravě.")
        return
    allowed_shifts = [entry[0] for entry in global_settings.get(uvazek, [])]
    new_value = ask_shift(allowed_shifts, button["text"])
    if new_value is not None and new_value != old_value:
        # Zaznamenání změny do logu:
        # Získání jména zaměstnance z comboboxu Zaměstnanec
        employee_name = employee_combobox.get().strip() if employee_combobox.get() else "neznámý zaměstnanec"
        log_action(
            f"Uživatel {current_user_name} ({current_user_role}) upravil plán zaměstnance {employee_name} "
            f"(úvazek {uvazek}): den {day_index}, změna z '{old_value}' na '{new_value}'"
        )
        button.config(text=new_value)
        day_plan_list[day_index] = new_value

# ----- Funkce pro aktualizaci seznamu zaměstnanců
def update_employee_list():
    """
    Načte a aktualizuje seznam zaměstnanců z databáze podle vybraného roku.
    U velitele se načtou pouze záznamy jeho směny.
    """
    try:
        year_filter = year_combobox.get()
        query = "SELECT DISTINCT jmeno_prijmeni FROM plans WHERE 1=1"
        params = []
        if year_filter != "":
            query += " AND roky = ?"
            params.append(year_filter)
        # Pokud je aktuálně přihlášen velitel, načteme pouze jeho směnu
        if current_user_role == "velitel":
            shift_value = shift_filter_combobox.get()
            if shift_value != "":
                query += " AND smena = ?"
                params.append(shift_value)
        else:
            shift_filter = shift_filter_combobox.get()
            if shift_filter != "":
                query += " AND smena = ?"
                params.append(shift_filter)
        with sqlite3.connect("service_plans.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            employee_combobox['values'] = [row["jmeno_prijmeni"] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Chyba při aktualizaci seznamu zaměstnanců: {e}")
        messagebox.showerror("Chyba", f"Chyba při aktualizaci seznamu zaměstnanců: {e}")

# ----- Vytvoření sekce nastavení pro daný úvazek
def create_setting_section(parent, uvazek):
    """
    Vytvoří GUI sekci pro nastavení úvazku, kde lze přidávat či mazat směny s přidruženým počtem hodin a barvou.
    """
    section_frame = tk.LabelFrame(parent, text=f"Úvazek {uvazek}", font=("TkDefaultFont", 10, "bold"), width=180, height=220)
    section_frame.pack(side=tk.LEFT, padx=10, pady=5)
    section_frame.pack_propagate(False)

    listbox = tk.Listbox(section_frame, height=4)
    listbox.pack(fill=tk.X, padx=5, pady=5)

        # Globální binding: bez kontroly polohy, scrollujeme listbox vždy
    section_frame.winfo_toplevel().bind_all("<MouseWheel>",
        lambda event: listbox.yview_scroll(-1 * (event.delta // 120), "units"))
     
    default_item = [" ", "0", "neutrální"]
    if default_item not in global_settings.get(uvazek, []):
        global_settings[uvazek].insert(0, default_item)
    for item in global_settings.get(uvazek, []):
        listbox.insert(tk.END, f"{item[0]} - {item[1]} hodin ({item[2]})")
    entry_frame = tk.Frame(section_frame)
    entry_frame.pack(fill=tk.X, padx=5, pady=5)
    tk.Label(entry_frame, text="Směna:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    shift_entry = tk.Entry(entry_frame, width=10)
    shift_entry.grid(row=0, column=1, padx=5, pady=2)
    tk.Label(entry_frame, text="Hodiny:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    hours_entry = tk.Entry(entry_frame, width=10)
    hours_entry.grid(row=1, column=1, padx=5, pady=2)
    tk.Label(entry_frame, text="Barva:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
    colors = [
        "žluté", "zelené", "oranžové", "růžové", "modré",
        "hnědé", "neutrální", "fialové", "tyrkysové", "šedé"
    ]
    color_combo = ttk.Combobox(entry_frame, state="readonly", values=colors, width=10)
    color_combo.set("neutrální")
    color_combo.grid(row=2, column=1, padx=5, pady=2)
    def add_entry():
        shift = shift_entry.get().strip()
        hours = hours_entry.get().strip()
        color = color_combo.get().strip()
        if shift and hours and color:
            listbox.insert(tk.END, f"{shift} - {hours} hodin ({color})")
            global_settings[uvazek].append([shift, hours, color])
            shift_entry.delete(0, tk.END)
            hours_entry.delete(0, tk.END)
            color_combo.set("neutrální")
        else:
            messagebox.showwarning("Upozornění", "Vyplňte všechny hodnoty.")
    def delete_entry():
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            listbox.delete(index)
            global_settings[uvazek].pop(index)
        else:
            messagebox.showwarning("Upozornění", "Nevybrali jste záznam k odstranění.")
    btn_frame = tk.Frame(section_frame)
    btn_frame.pack(fill=tk.X, padx=5, pady=5)
    tk.Button(btn_frame, text="Přidat", command=add_entry).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Smazat", command=delete_entry).pack(side=tk.LEFT, padx=5)
    return listbox

# ----- Načtení seznamu zaměstnanců a roků z databáze
def populate_employee_and_year():
    """
    Načte z databáze seznam zaměstnanců a dostupných roků, a aktualizuje příslušná GUI pole.
    """
    try:
        with sqlite3.connect("service_plans.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT jmeno_prijmeni FROM plans")
            employee_combobox['values'] = [row["jmeno_prijmeni"] for row in cursor.fetchall()]
            cursor.execute("SELECT DISTINCT roky FROM plans")
            roky = [row["roky"] for row in cursor.fetchall()]
            current_year_str = str(datetime.now().year)
            if current_year_str in roky:
                year_combobox.set(current_year_str)
            else:
                year_combobox.set(current_year_str)
            cursor.execute("SELECT DISTINCT jmeno_prijmeni FROM plans")
            filter_jmeno['values'] = [row["jmeno_prijmeni"] for row in cursor.fetchall()]
            cursor.execute("SELECT DISTINCT roky FROM plans")
            filter_rok['values'] = [row["roky"] for row in cursor.fetchall()]
            cursor.execute("SELECT DISTINCT smena FROM plans")
            filter_smena['values'] = [row["smena"] for row in cursor.fetchall()]
    except Exception as e:
        logging.error(f"Chyba při načítání hodnot pro filtry: {e}")
        messagebox.showerror("Chyba", f"Chyba při načítání hodnot pro filtry: {e}")

# ----- Přihlašovací funkce
def login():
    global current_user_role, current_user_name, current_user_shift
    nm = login_name_entry.get().strip()
    pwd = login_pwd_entry.get().strip()
    if nm == "" and pwd == "":
        current_user_role = "uživatel"
        current_user_name = "uživatel"
        login_status_label.config(text="Přihlášen: uživatel (uživatel)")
        log_action("Přihlášení jako uživatel (výchozí)")
        apply_access_control()
        messagebox.showinfo("Přihlášení", "Přihlášení proběhlo jako uživatel.")
        login_pwd_entry.delete(0, tk.END)
        for widget in plan_display_frame.winfo_children():
            widget.destroy()
        update_employee_list()
        return

    try:
        for entry in global_settings.get("access", []):
            if entry[0] == nm and decode_password(entry[1]) == pwd:
                current_user_role = entry[2]
                current_user_name = nm
                login_status_label.config(text=f"Přihlášen: {nm} ({current_user_role})")
                log_action(f"Přihlášení jako {nm} ({current_user_role})")
                current_user_shift = None
                if current_user_role == "velitel":
                    parts = current_user_name.split()
                    if len(parts) >= 3 and parts[0] == "Velitel" and parts[1].lower() == "směny":
                        shift_value = "Směna " + parts[2]
                        shift_filter_combobox.set(shift_value)
                        shift_filter_combobox.config(state="disabled")
                    else:
                        shift_filter_combobox.set("")
                    employee_combobox.set("")
                else:
                    shift_filter_combobox.config(state="readonly")
                apply_access_control()
                update_employee_list()  # Aktualizace seznamu zaměstnanců
                for widget in plan_display_frame.winfo_children():
                    widget.destroy()
                messagebox.showinfo("Přihlášení", f"Přihlášení proběhlo úspěšně jako {nm} ({current_user_role})")
                login_pwd_entry.delete(0, tk.END)
                return
        messagebox.showerror("Přihlášení", "Neplatné přihlašovací údaje")
    except Exception as e:
        logging.error(f"Chyba při přihlašování: {e}")
        messagebox.showerror("Chyba", f"Chyba při přihlašování: {e}")

# ----- Funkce pro odhlášení uživatele
def logout():
    """
    Resetuje údaje o přihlášeném uživateli a obnoví výchozí nastavení GUI.
    """
    global current_user_role, current_user_name, current_user_shift
    current_user_role = "uživatel"
    current_user_name = "uživatel"
    current_user_shift = None
    login_status_label.config(text="Nejste přihlášeni")
    login_name_entry.delete(0, tk.END)
    login_pwd_entry.delete(0, tk.END)
    shift_filter_combobox.config(state="readonly")
    shift_filter_combobox.set("")
    apply_access_control()
    update_employee_list()
    messagebox.showinfo("Odhlášení", "Byl jste úspěšně odhlášen.")
    # Zavření hlavního okna aplikace
    root.destroy()

# ----- Funkce pro nastavení přístupových práv podle role uživatele
def apply_access_control():
    """
    Skryje nebo zobrazí určité záložky v GUI podle role přihlášeného uživatele.
    """
    try:
        role = current_user_role if current_user_role is not None else "uživatel"
        for i in range(notebook.index("end")):
            tab_text = notebook.tab(i, "text")
            if role in ["admin", "superadmin"]:
                notebook.tab(i, state="normal")
            else:
                if tab_text == "Plány":
                    notebook.tab(i, state="normal")
                else:
                    notebook.tab(i, state="hidden")
        for i in range(plans_notebook.index("end")):
            plans_notebook.tab(i, state="normal")
        if role in ["admin", "superadmin"]:
            # Zobrazí tlačítka, pokud jsou spravována metodou pack, nastavíme pack() znovu
            btn_lock_plan.pack(side=tk.LEFT, padx=5)
            btn_unlock_plan.pack(side=tk.LEFT, padx=5)
        else:
            # Skryjeme tlačítka pomocí pack_forget()
            btn_lock_plan.pack_forget()
            btn_unlock_plan.pack_forget()
    except Exception as e:
        logging.error(f"Chyba při nastavování přístupových práv: {e}")

        # MOD: Aktualizace tlačítek pro zámek plánu v záložce Směna
        try:
            if current_user_role == "superadmin":
                btn_lock_plan.grid()  # zobrazí tlačítka
                btn_unlock_plan.grid()
            else:
                btn_lock_plan.grid_remove()
                btn_unlock_plan.grid_remove()
        except Exception as e:
            logging.error(f"Chyba při aktualizaci tlačítek pro zámek: {e}")
    except Exception as e:
        logging.error(f"Chyba při nastavování přístupových práv: {e}")

# ----- Otevření okna Fond hodin
def open_fond_window():
    fond_window = tk.Toplevel(root)
    fond_window.title("Fond hodin")
    fond_window.geometry("330x280")  # Můžete upravit velikost dle potřeby
# --- Výběr roku a směny ---  
    tk.Label(fond_window, text="Rok:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    years = [str(y) for y in range(datetime.now().year - 5, datetime.now().year + 6)]
    year_combo = ttk.Combobox(fond_window, values=years, state="readonly", width=10)
    year_combo.grid(row=0, column=1, padx=5, pady=5)
    year_combo.set(str(datetime.now().year))
    
    tk.Label(fond_window, text="Směna:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    shifts = ["Směna 1", "Směna 2", "Směna 3", "Směna 4", "Směna 5", "Směna 6"]
    shift_combo = ttk.Combobox(fond_window, values=shifts, state="readonly", width=10)
    shift_combo.grid(row=0, column=3, padx=5, pady=5)
    shift_combo.set("Směna 1")
    
    # --- Pole pro měsíční fondy (Leden až Prosinec) ---
    months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen",
              "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
    month_entries = {}
    for i, month in enumerate(months):
        row = i // 2 + 1
        col = (i % 2) * 2  # sloupec pro popisek a hodnotu
        tk.Label(fond_window, text=f"{month}:").grid(row=row, column=col, padx=5, pady=5, sticky="e")
        entry = tk.Entry(fond_window, width=10)
        entry.grid(row=row, column=col+1, padx=5, pady=5)
        month_entries[month.lower()] = entry  # klíč v malých písmenech
    
    # --- Funkce pro načtení uložených hodnot ---
    def load_fond_settings():
        selected_year = year_combo.get().strip()
        selected_shift = shift_combo.get().strip()
        if ("fond_hodin" in global_settings and 
            selected_year in global_settings["fond_hodin"] and 
            selected_shift in global_settings["fond_hodin"][selected_year]):
            fond_data = global_settings["fond_hodin"][selected_year][selected_shift]
            for month in months:
                key = month.lower()
                value = fond_data.get(key, "")
                month_entries[key].delete(0, tk.END)
                month_entries[key].insert(0, str(value))
        else:
            # Pokud pro vybraný rok a směnu ještě nejsou uložena data, vymažeme pole
            for entry in month_entries.values():
                entry.delete(0, tk.END)
    
    # --- Funkce pro uložení nových hodnot ---
    def save_fond_settings():
        selected_year = year_combo.get().strip()
        selected_shift = shift_combo.get().strip()
        # Pokud klíč ještě neexistuje, vytvoříme ho
        if "fond_hodin" not in global_settings:
            global_settings["fond_hodin"] = {}
        if selected_year not in global_settings["fond_hodin"]:
            global_settings["fond_hodin"][selected_year] = {}
        fond_data = {}
        for month in months:
            key = month.lower()
            try:
                val = int(month_entries[key].get().strip())
            except ValueError:
                val = 0
            fond_data[key] = val
        global_settings["fond_hodin"][selected_year][selected_shift] = fond_data
        save_config(global_settings)
        messagebox.showinfo("Nastavení", "Fond hodin byl uložen.")
    
    # --- Tlačítka pro načtení a uložení ---
    load_button = tk.Button(fond_window, text="Načíst nastavení", command=load_fond_settings)
    load_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10)
    save_button = tk.Button(fond_window, text="Uložit nastavení", command=save_fond_settings)
    save_button.grid(row=7, column=2, columnspan=2, padx=5, pady=10)

# ----- Otevření okna globálního nastavení
def open_settings_window():
    """
    Zobrazí okno pro globální nastavení, kde lze měnit konfiguraci úvazků, přístupových práv
    a také nastavit specifické roční hodnoty pro směny (I. a II. pololetí).
    """
    try:
        settings_window = tk.Toplevel(root)
        settings_window.title("Globální nastavení")
        settings_window.geometry("700x730")
        settings_window.resizable(True, True)
        
        # --- Sekce nastavení počítání hodin dle úvazku (stávající)
        tk.Label(settings_window, text="Nastavení počítání hodin dle Úvazku", font=("TkDefaultFont", 12, "bold")).pack(pady=10)
        colors = [
            "žluté", "zelené", "oranžové", "růžové", "modré",
            "hnědé", "neutrální", "fialové", "tyrkysové", "šedé"
        ]
        uvazek_frame = tk.Frame(settings_window)
        uvazek_frame.pack(pady=5)
        listbox_40 = create_setting_section(uvazek_frame, "40")
        listbox_375 = create_setting_section(uvazek_frame, "37.5")
        listbox_3775 = create_setting_section(uvazek_frame, "37.75")
        
        # --- Nová sekce pro nastavení směn - Vypuštěná a ranní směny
        # Tato sekce umožňuje zadat pro zvolený rok a směnu hodnoty pro I. a II. pololetí.
        vypustena_frame = tk.LabelFrame(settings_window, text="Nastavení směn - Vypuštěná směna a ranní", font=("TkDefaultFont", 12, "bold"), width=380, height=280)
        vypustena_frame.pack(fill="both", expand=True, padx=10, pady=10)
        vypustena_frame.pack_propagate(False)
        
        # Výběr roku
        tk.Label(vypustena_frame, text="Rok:", font=("TkDefaultFont", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        vyber_rok = ttk.Combobox(vypustena_frame, state="readonly", width=10,
                                  values=[str(y) for y in range(datetime.now().year - 5, datetime.now().year + 6)])
        vyber_rok.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        vyber_rok.set(str(datetime.now().year))
        
        # Výběr směny
        tk.Label(vypustena_frame, text="Směna:", font=("TkDefaultFont", 10)).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        vyber_směna = ttk.Combobox(vypustena_frame, state="readonly", width=10,
                                    values=["Směna 1", "Směna 2", "Směna 3", "Směna 4", "Směna 5", "Směna 6"])
        vyber_směna.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        vyber_směna.set("Směna 1")
        
        # Kontejner pro dynamicky načtený formulář
        formular_frame = tk.Frame(vypustena_frame)
        formular_frame.grid(row=1, column=4, rowspan=4, padx=10, pady=5)
        
        def nacist_formular():
            # Smazání starého formuláře, pokud existuje
            for widget in formular_frame.winfo_children():
                widget.destroy()
            
            # Získání vybraného roku a směny
            rok = vyber_rok.get().strip()
            smena = vyber_směna.get().strip()
            saved_data = None
            if "year_settings" in global_settings and rok in global_settings["year_settings"]:
                saved_data = global_settings["year_settings"][rok].get(smena, None)
            
            # Vytvoření formuláře pro I. pololetí
            tk.Label(formular_frame, text="I. pololetí", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, columnspan=2, padx=5, pady=5)
            tk.Label(formular_frame, text="Vypuštěná směna:", font=("TkDefaultFont", 10)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
            entry_vypustena1 = tk.Entry(formular_frame, width=5)
            entry_vypustena1.grid(row=1, column=1, padx=5, pady=5, sticky="w")
            
            tk.Label(formular_frame, text="Ranní směny:", font=("TkDefaultFont", 10)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
            entry_ranni1 = tk.Entry(formular_frame, width=5)
            entry_ranni1.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            
            # Vytvoření formuláře pro II. pololetí
            tk.Label(formular_frame, text="II. pololetí", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, columnspan=2, padx=5, pady=5)
            tk.Label(formular_frame, text="Vypuštěná směna:", font=("TkDefaultFont", 10)).grid(row=1, column=2, padx=5, pady=5, sticky="e")
            entry_vypustena2 = tk.Entry(formular_frame, width=5)
            entry_vypustena2.grid(row=1, column=3, padx=5, pady=5, sticky="w")
            
            tk.Label(formular_frame, text="Ranní směny:", font=("TkDefaultFont", 10)).grid(row=2, column=2, padx=5, pady=5, sticky="e")
            entry_ranni2 = tk.Entry(formular_frame, width=5)
            entry_ranni2.grid(row=2, column=3, padx=5, pady=5, sticky="w")
            
            # Pokud existují uložená data, předvyplníme je
            if saved_data:
                entry_vypustena1.insert(0, str(saved_data.get("pololeti1", {}).get("vypustena", "")))
                entry_ranni1.insert(0, str(saved_data.get("pololeti1", {}).get("ranni", "")))
                entry_vypustena2.insert(0, str(saved_data.get("pololeti2", {}).get("vypustena", "")))
                entry_ranni2.insert(0, str(saved_data.get("pololeti2", {}).get("ranni", "")))
            
            # Uložení odkazů na widgety pro pozdější načtení hodnot
            formular_frame.entries = {
                "vypustena1": entry_vypustena1,
                "ranni1": entry_ranni1,
                "vypustena2": entry_vypustena2,
                "ranni2": entry_ranni2
            }
        
        # Tlačítko pro načtení formuláře dle vybraných hodnot
        btn_nacist = tk.Button(vypustena_frame, text="Načíst formulář", command=nacist_formular)
        btn_nacist.grid(row=0, column=4, padx=5, pady=5)
        
        # Tlačítko pro uložení nastavení z formuláře
        def ulozit_nastaveni_směny():
            rok = vyber_rok.get().strip()
            smena = vyber_směna.get().strip()
            if not rok or not smena:
                messagebox.showerror("Chyba", "Vyberte rok a směnu.")
                return
                # Přidána kontrola, zda už byl načten formulář
            if not hasattr(formular_frame, "entries"):
                messagebox.showerror("Chyba", "Nejprve načtěte formulář kliknutím na 'Načíst formulář'.")
                return
            entries = formular_frame.entries
            data = {
                "vypustena1": int(entries["vypustena1"].get()) if entries["vypustena1"].get().isdigit() else 0,
                "ranni1": int(entries["ranni1"].get()) if entries["ranni1"].get().isdigit() else 0,
                "vypustena2": int(entries["vypustena2"].get()) if entries["vypustena2"].get().isdigit() else 0,
                "ranni2": int(entries["ranni2"].get()) if entries["ranni2"].get().isdigit() else 0,
            }
            if "year_settings" not in global_settings:
                global_settings["year_settings"] = {}
            if rok not in global_settings["year_settings"]:
                global_settings["year_settings"][rok] = {}
            global_settings["year_settings"][rok][smena] = {
                        "pololeti1": {
                        "vypustena": data["vypustena1"],
                        "ranni": data["ranni1"]
                    },
                    "pololeti2": {
                        "vypustena": data["vypustena2"],
                        "ranni": data["ranni2"]
                    }
            }
            save_config(global_settings)
            messagebox.showinfo("Nastavení", "Nastavení směny bylo uloženo.")
        
        btn_ulozit_sm = tk.Button(vypustena_frame, text="Uložit nastavení směny", command=ulozit_nastaveni_směny)
        btn_ulozit_sm.grid(row=5, column=0, columnspan=5, pady=10)
        
        # --- Sekce nastavení přístupu (stávající)
        access_frame = tk.LabelFrame(settings_window, text="Přístup", font=("TkDefaultFont", 10, "bold"), width=800, height=250)
        access_frame.pack(pady=10)
        access_frame.pack_propagate(False)
        tk.Label(access_frame, text="Heslo:").grid(row=0, column=0, padx=5, pady=2, sticky="e")
        pwd_entry = tk.Entry(access_frame, width=12, show="*")
        pwd_entry.grid(row=0, column=1, padx=5, pady=2)
        tk.Label(access_frame, text="Jméno:").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        name_entry = tk.Entry(access_frame, width=12)
        name_entry.grid(row=1, column=1, padx=5, pady=2)
        tk.Label(access_frame, text="Role:").grid(row=2, column=0, padx=5, pady=2, sticky="e")
        role_combo = ttk.Combobox(access_frame, state="readonly", values=["uživatel", "velitel", "admin", "superadmin"], width=10)
        role_combo.set("uživatel")
        role_combo.grid(row=2, column=1, padx=5, pady=2)
        access_listbox = tk.Listbox(access_frame, height=3)
        access_listbox.grid(row=0, column=2, rowspan=3, padx=5, pady=2)
        for item in global_settings.get("access", []):
            access_listbox.insert(tk.END, f"{item[0]} - {item[1]} - {item[2]}")
        access_btn_frame = tk.Frame(access_frame)
        access_btn_frame.grid(row=3, column=0, columnspan=3, pady=5)
        def add_access():
            pwd = pwd_entry.get().strip()
            nm = name_entry.get().strip()
            role = role_combo.get().strip()
            if pwd and nm and role:
                encoded_pwd = encode_password(pwd)
                access_listbox.insert(tk.END, f"{nm} - {encoded_pwd} - {role}")
                if "access" not in global_settings:
                    global_settings["access"] = []
                global_settings["access"].append((nm, encoded_pwd, role))
                pwd_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                role_combo.set("uživatel")
            else:
                messagebox.showwarning("Upozornění", "Vyplňte Heslo, Jméno a Role.")
        def delete_access():
            selection = access_listbox.curselection()
            if selection:
                index = selection[0]
                access_listbox.delete(index)
                global_settings["access"].pop(index)
            else:
                messagebox.showwarning("Upozornění", "Nevybrali jste záznam k odstranění.")
        tk.Button(access_btn_frame, text="Přidat", command=add_access).pack(side=tk.LEFT, padx=5)
        tk.Button(access_btn_frame, text="Smazat", command=delete_access).pack(side=tk.LEFT, padx=5)

        def save_global_settings():
            save_config(global_settings)
            messagebox.showinfo("Nastavení", "Uložení nastavení proběhlo úspěšně")
            settings_window.destroy()
        tk.Button(settings_window, text="Uložit nastavení", command=save_global_settings).pack(pady=20, anchor="center")
    except Exception as e:
        logging.error(f"Chyba v okně globálního nastavení: {e}")
        messagebox.showerror("Chyba", f"Chyba v okně nastavení: {e}")

# ----- Funkce pro načtení nového plánu z Excelu a jeho uložení do databáze
def on_new():
    """
    Načte Excelový soubor, extrahuje z něj data plánu a uloží je do databáze.
    """
    try:
        log_action("Stisknuto tlačítko 'Nový'")
        file_path = filedialog.askopenfilename(title="Vyberte Excel soubor", filetypes=[("Excel soubory", "*.xlsx;*.xls")])
        if file_path:
            try:
                wb = load_workbook(filename=file_path, data_only=True)
                ws = wb.active
                osobni_cislo = ws["A2"].value
                jmeno_prijmeni = ws["C2"].value
                smena = "Směna "   # bude doplněno při editaci
                uvazek = "37.5"    # předpokládáme, že úvazek je "40"
                cell_b30 = ws["B30"].value
                if isinstance(cell_b30, str):
                    if len(cell_b30) >= 4:
                        roky = cell_b30[-4:]
                    else:
                        messagebox.showerror("Chyba", "Buňka B30 obsahuje řetězec, ale není dostatečně dlouhý pro rok.")
                        return
                elif isinstance(cell_b30, (datetime, date)):
                    roky = str(cell_b30.year)
                else:
                    messagebox.showerror("Chyba", "Buňka B30 neobsahuje platný údaj o roce.")
                    return
                poradi = "0"
                month_rows = {
                    "leden": 4,
                    "unor": 6,
                    "brezen": 8,
                    "duben": 10,
                    "kveten": 12,
                    "cerven": 14,
                    "cervenec": 16,
                    "srpen": 18,
                    "zari": 20,
                    "rijen": 22,
                    "listopad": 24,
                    "prosinec": 26
                }
                month_data = load_month_data(ws, month_rows)
                with sqlite3.connect("service_plans.db") as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT id FROM plans WHERE jmeno_prijmeni = ? AND osobni_cislo = ? AND roky = ?",
                        (jmeno_prijmeni, osobni_cislo, roky)
                    )
                    existing_record = cursor.fetchone()
                    if existing_record is not None:
                        if not messagebox.askyesno("Potvrzení přepsání",
                                                   f"Plán pro {jmeno_prijmeni} ({osobni_cislo}) pro rok {roky} již existuje.\nChcete jej přepsat?"):
                            return
                        update_query = """
                            UPDATE plans
                            SET smena = ?, uvazek = ?, poradi = ?,
                                stara_dovolena = "0", dovolena = "0",
                                leden = ?, unor = ?, brezen = ?, duben = ?,
                                kveten = ?, cerven = ?, cervenec = ?, srpen = ?,
                                zari = ?, rijen = ?, listopad = ?, prosinec = ?
                            WHERE id = ?
                        """
                        params = (
                            smena, uvazek, poradi,
                            month_data["leden"], month_data["unor"], month_data["brezen"],
                            month_data["duben"], month_data["kveten"], month_data["cerven"],
                            month_data["cervenec"], month_data["srpen"], month_data["zari"],
                            month_data["rijen"], month_data["listopad"], month_data["prosinec"],
                            existing_record["id"]
                        )
                        cursor.execute(update_query, params)
                        conn.commit()
                        log_action("Plán byl přepsán v databázi")
                        messagebox.showinfo("Úspěch", "Plán byl úspěšně přepsán.")
                        refresh_treeview()
                        populate_employee_and_year()
                        return
                    else:
                        cursor.execute("""
                            INSERT INTO plans (
                                osobni_cislo, jmeno_prijmeni, smena, uvazek, roky, poradi,
                                stara_dovolena, dovolena,
                                leden, unor, brezen, duben, kveten, cerven, cervenec, srpen, zari, rijen, listopad, prosinec
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """, (
                            osobni_cislo, jmeno_prijmeni, smena, uvazek, roky, poradi,
                            "0", "0",
                            month_data["leden"], month_data["unor"], month_data["brezen"],
                            month_data["duben"], month_data["kveten"], month_data["cerven"],
                            month_data["cervenec"], month_data["srpen"], month_data["zari"],
                            month_data["rijen"], month_data["listopad"], month_data["prosinec"]
                        ))
                        conn.commit()
                log_action("Data byla úspěšně uložena do databáze")
                messagebox.showinfo("Úspěch", "Data byla úspěšně načtena a uložena do databáze.")
                refresh_treeview()
                populate_employee_and_year()
            except Exception as e:
                logging.error(f"Chyba při načítání dat z Excelu: {e}")
                messagebox.showerror("Chyba", f"Došlo k chybě při načítání dat: {e}")
        else:
            print("Nebyl vybrán žádný soubor.")
    except Exception as e:
        logging.error(f"Obecná chyba při volání on_new: {e}")
        messagebox.showerror("Chyba", f"Došlo k chybě: {e}")

# ----- Funkce pro úpravu existujícího záznamu (Edit)
def on_edit():
    """
    Umožňuje upravit celý záznam, což mohou provádět pouze admin a superadmin.
    """
    try:
        if current_user_role not in ["admin", "superadmin"]:
            messagebox.showerror("Chyba", "Pouze admin a superadmin mohou měnit celý záznam.")
            return
        log_action("Stisknuto tlačítko 'Edit'")
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Upozornění", "Nevybrali jste žádnou položku k úpravě.")
            return
        record_id = selected_items[0]
        with sqlite3.connect("service_plans.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM plans WHERE id = ?", (record_id,))
            row = cursor.fetchone()
        if row is None:
            messagebox.showerror("Chyba", "Záznam nebyl nalezen.")
            return
        detail_window = tk.Toplevel(root)
        detail_window.geometry("600x250")
        detail_window.title("Editace záznamu")
        detail_window.resizable(True, True)
        top_frame = tk.Frame(detail_window)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        basic_frame = tk.Frame(top_frame)
        basic_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        basic_left = tk.Frame(basic_frame)
        basic_left.grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        basic_right = tk.Frame(basic_frame)
        basic_right.grid(row=0, column=1, sticky="nw", padx=20, pady=2)
        tk.Label(basic_left, text="Osobní číslo:", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        entry_osobni = tk.Entry(basic_left)
        entry_osobni.insert(0, str(row["osobni_cislo"]))
        entry_osobni.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        tk.Label(basic_right, text="Stará dovolená hodiny:", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="e", padx=5, pady=2)
        entry_stara = tk.Entry(basic_right)
        entry_stara.insert(0, str(row["stara_dovolena"]))
        entry_stara.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        tk.Label(basic_right, text="Dovolená hodiny:", font=("TkDefaultFont", 10, "bold")).grid(row=1, column=0, sticky="e", padx=5, pady=2)
        entry_dovolena = tk.Entry(basic_right)
        entry_dovolena.insert(0, str(row["dovolena"]))
        entry_dovolena.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        next_row = 1
        remaining_fields = {
            "Jméno a příjmení": row["jmeno_prijmeni"],
            "Směna": row["smena"],
            "Úvazek": row["uvazek"],
            "Roky": row["roky"],
            "Pořadí ve směně": row["poradi"]
        }
        basic_entries = {"Osobní číslo": entry_osobni,
                         "Stará dovolená hodiny": entry_stara,
                         "Dovolená hodiny": entry_dovolena}
        for label_text, value in remaining_fields.items():
            tk.Label(basic_left, text=f"{label_text}:", font=("TkDefaultFont", 10, "bold")).grid(row=next_row, column=0, sticky="w", padx=5, pady=2)
            if label_text in ["Směna", "Úvazek"]:
                combo = ttk.Combobox(basic_left, state="normal")
                if label_text == "Směna":
                    combo['values'] = ["Směna 1", "Směna 2", "Směna 3", "Směna 4", "Směna 5", "Směna 6"]
                else:
                    combo['values'] = ["40", "37.5", "37.75"]
                combo.set(value)
                combo.grid(row=next_row, column=1, sticky="w", padx=5, pady=2)
                basic_entries[label_text] = combo
            elif label_text == "Pořadí ve směně":
                combo = ttk.Combobox(basic_left, state="normal", values=[str(x) for x in range(0, 21)])
                combo.set(value)
                combo.grid(row=next_row, column=1, sticky="w", padx=5, pady=2)
                basic_entries[label_text] = combo
            else:
                entry = tk.Entry(basic_left)
                entry.insert(0, str(value))
                entry.grid(row=next_row, column=1, sticky="w", padx=5, pady=2)
                basic_entries[label_text] = entry
            next_row += 1
        bottom_frame = tk.Frame(detail_window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        save_button = tk.Button(bottom_frame, text="Uložit změny", 
                                command=lambda: save_changes(basic_entries, row, detail_window, record_id))
        save_button.pack(anchor="center")
        def save_changes(basic_entries, row, detail_window, record_id):
            try:
                updated_poradi = basic_entries["Pořadí ve směně"].get()
                updated_osobni = basic_entries["Osobní číslo"].get()
                updated_stara = basic_entries["Stará dovolená hodiny"].get()
                updated_dovolena = basic_entries["Dovolená hodiny"].get()
                updated_jmeno = basic_entries["Jméno a příjmení"].get()
                updated_smena = basic_entries["Směna"].get()
                updated_uvazek = basic_entries["Úvazek"].get()
                updated_roky = basic_entries["Roky"].get()
                with sqlite3.connect("service_plans.db") as conn:
                    conn.row_factory = sqlite3.Row
                    cursor = conn.cursor()
                    update_query = """
                        UPDATE plans
                        SET osobni_cislo = ?, stara_dovolena = ?, dovolena = ?, jmeno_prijmeni = ?, smena = ?, uvazek = ?, roky = ?, poradi = ?
                        WHERE id = ?
                    """
                    params = [
                        updated_osobni, updated_stara, updated_dovolena, updated_jmeno,
                        updated_smena, updated_uvazek, updated_roky, updated_poradi,
                        record_id
                    ]
                    cursor.execute(update_query, params)
                    conn.commit()
                log_action(f"Plán byl upraven uživatelem {current_user_name}")
                messagebox.showinfo("Úspěch", "Změny byly úspěšně uloženy.")
                detail_window.destroy()
                refresh_treeview()
            except Exception as e:
                logging.error(f"Chyba při ukládání změn v editaci záznamu: {e}")
                messagebox.showerror("Chyba", f"Došlo k chybě při ukládání změn: {e}")
    except Exception as e:
        logging.error(f"Chyba při načítání detailu záznamu: {e}")
        messagebox.showerror("Chyba", f"Došlo k chybě při načítání detailu: {e}")

# ----- Funkce pro smazání záznamu
def on_delete():
    """
    Smaže vybraný záznam ze seznamu a databáze.
    """
    try:
        log_action("Stisknuto tlačítko 'Smazat'")
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("Upozornění", "Nevybrali jste žádnou položku k smazání.")
            return
        if not messagebox.askyesno("Potvrzení", "Opravdu chcete smazat vybraného zaměstnance?"):
            return
        for item in tree.selection():
            try:
                with sqlite3.connect("service_plans.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM plans WHERE id = ?", (item,))
                    conn.commit()
                tree.delete(item)
                log_action(f"Záznam s ID {item} byl smazán z databáze")
            except Exception as e:
                logging.error(f"Chyba při mazání záznamu s ID {item}: {e}")
                messagebox.showerror("Chyba", f"Došlo k chybě při mazání záznamu: {e}")
        messagebox.showinfo("Úspěch", "Vybraná položka byla úspěšně smazána.")
    except Exception as e:
        logging.error(f"Obecná chyba při mazání: {e}")
        messagebox.showerror("Chyba", f"Došlo k chybě: {e}")

# ----- Funkce pro zobrazení plánu směny v záložce Zaměstnanec
def show_employee_plan():
    """
    Zobrazí detailní plán směny vybraného zaměstnance pro aktuální rok.
    """
    try:
        global current_record_id, month_frames
        for widget in plan_display_frame.winfo_children():
            widget.destroy()
        selected_employee = employee_combobox.get()
        current_year = datetime.now().year
        year_combobox.set(str(current_year))
        selected_year = str(current_year)
        if not selected_employee or not selected_year:
            messagebox.showwarning("Upozornění", "Vyberte min. Zaměstnance a Rok.")
            return
        with sqlite3.connect("service_plans.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM plans WHERE jmeno_prijmeni = ? AND roky = ?", (selected_employee, selected_year))
            record = cursor.fetchone()
        if record is None:
            messagebox.showinfo("Informace", "Pro vybraného Zaměstnance a Rok nebyl nalezen žádný plán.")
            return

        jmeno = record["jmeno_prijmeni"]
        osobni = record["osobni_cislo"]
        smena = record["smena"]
        uvazek = record["uvazek"]
        nova_dovolena = record["dovolena"]
        stara_dovolena = record["stara_dovolena"]
        try:
            celkem_dovolena = float(nova_dovolena) + float(stara_dovolena)
        except Exception:
            celkem_dovolena = 0.0

        # Definice měsíců pro první a druhé pololetí
        half1_months = ["leden", "unor", "brezen", "duben", "kveten", "cerven"]
        half2_months = ["cervenec", "srpen", "zari", "rijen", "listopad", "prosinec"]

        # Počítání výskytů znaku "-" pro Klouz I. a Klouz II.
        half1_dash_count = 0
        for m in half1_months:
            try:
                plan_list = json.loads(record[m])
            except Exception:
                plan_list = [""] * 32
            for cell in plan_list[1:]:
                if isinstance(cell, str):
                    half1_dash_count += cell.count("-")
        
        half2_dash_count = 0
        for m in half2_months:
            try:
                plan_list = json.loads(record[m])
            except Exception:
                plan_list = [""] * 32
            for cell in plan_list[1:]:
                if isinstance(cell, str):
                    half2_dash_count += cell.count("-")
        
        # Počítání výskytů znaku "r" pro sloupce r I. a r II.
        half1_r_count = 0
        for m in half1_months:
            try:
                plan_list = json.loads(record[m])
            except Exception:
                plan_list = [""] * 32
            for cell in plan_list[1:]:
                if isinstance(cell, str):
                    half1_r_count += cell.count("r")
        
        half2_r_count = 0
        for m in half2_months:
            try:
                plan_list = json.loads(record[m])
            except Exception:
                plan_list = [""] * 32
            for cell in plan_list[1:]:
                if isinstance(cell, str):
                    half2_r_count += cell.count("r")

        # Načtení globálních hodnot z nastavení
        # Pro "Klouz I." a "Klouz II." se čte pod klíči "vypustena"
        # Pro "r I." a "r II." se čte pod klíči "ranni"
        klouz1_value = 0
        klouz2_value = 0
        ranni1_value = 0
        ranni2_value = 0
        year_str = str(selected_year)
        shift_name = record["smena"]
        if "year_settings" in global_settings:
            if year_str in global_settings["year_settings"]:
                if shift_name in global_settings["year_settings"][year_str]:
                    klouz1_value = global_settings["year_settings"][year_str][shift_name].get("pololeti1", {}).get("vypustena", 0)
                    klouz2_value = global_settings["year_settings"][year_str][shift_name].get("pololeti2", {}).get("vypustena", 0)
                    ranni1_value = global_settings["year_settings"][year_str][shift_name].get("pololeti1", {}).get("ranni", 0)
                    ranni2_value = global_settings["year_settings"][year_str][shift_name].get("pololeti2", {}).get("ranni", 0)
        
         # Vytvoření kompozitních řetězců pro sloupce
        klouz1_display = f"{klouz1_value}/{half1_dash_count}"
        klouz2_display = f"{klouz2_value}/{half2_dash_count}"
        ranni1_display = f"{ranni1_value}/{half1_r_count}"
        ranni2_display = f"{ranni2_value}/{half2_r_count}"

        # Výpočet plánované dovolené
        dov_count = 0
        month_keys = ["leden", "unor", "brezen", "duben", "kveten", "cerven", 
                      "cervenec", "srpen", "zari", "rijen", "listopad", "prosinec"]
        uvazek_shifts = global_settings.get(uvazek, [])
        for key in month_keys:
            try:
                plan = json.loads(record[key])
            except Exception:
                plan = []
            for cell in plan[1:]:
                if isinstance(cell, str) and cell.strip() == "Dov":
                    dov_count += 1
        dov_hours = 0.0
        for entry in uvazek_shifts:
            if entry[0] == "Dov":
                try:
                    dov_hours = float(entry[1])
                except Exception:
                    dov_hours = 0.0
                break
        planned_vacation_hours = dov_count * dov_hours
        rozdil = celkem_dovolena - planned_vacation_hours

        # Výpočet celkového počtu směn dle uvazku:
        # Pro každý den ve všech měsících se prochází symboly,
        # přičemž pokud symbol není "Dov" a odpovídá záznamu v globálním nastavení s hodinami > 1,
        # započítá se tato instance.
        total_shifts = 0
        all_months = ["leden", "unor", "brezen", "duben", "kveten", "cerven",
                      "cervenec", "srpen", "zari", "rijen", "listopad", "prosinec"]
        for month in all_months:
            try:
                day_plan_list = json.loads(record[month])
            except Exception:
                day_plan_list = [""] * 32
            for cell in day_plan_list[1:]:
                if isinstance(cell, str):
                    symbol = cell.strip()
                    if symbol == "Dov":
                        continue
                    for entry in global_settings.get(uvazek, []):
                        try:
                            hours = float(entry[1])
                        except Exception:
                            hours = 0
                        if symbol == entry[0] and hours > 1:
                            total_shifts += 1
                            break
        celkem_smen_display = f"{total_shifts}"

        # Sestavení seznamu popisků a hodnot pro informační tabulku
        popisky = [
            "Jméno a příjmení", "Nová dovolená", "Stará dovolená", "Celkem dovolená", 
            "Naplánovat Dov", "Rozdíl Plán a Nárok", "Celkem směn", 
            "Klouz I.", "Klouz II.", "r I.", "r II."
        ]
        hodnoty = [
            jmeno,
            f"{nova_dovolena} hod.",
            f"{stara_dovolena} hod.",
            f"{celkem_dovolena} hod.",
            f"{planned_vacation_hours} hod.",
            f"{rozdil} hod.",
            celkem_smen_display,
            klouz1_display,
            klouz2_display,
            ranni1_display,
            ranni2_display
        ]

        # Vykreslení informační tabulky
        info_table_frame = tk.Frame(plan_display_frame, bd=2, relief="groove")
        info_table_frame.pack(fill=tk.X, padx=10, pady=10)
        columns = len(popisky)
        for col in range(columns):
            lbl = tk.Label(info_table_frame, text=popisky[col],
                           font=("TkDefaultFont", 10, "bold"),
                           borderwidth=1, relief="ridge", padx=5, pady=3)
            lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
        for col in range(columns):
            lbl = tk.Label(info_table_frame, text=hodnoty[col],
                           font=("TkDefaultFont", 10),
                           borderwidth=1, relief="ridge", padx=5, pady=3)
            lbl.grid(row=1, column=col, sticky="nsew", padx=1, pady=1)
        for col in range(columns):
            info_table_frame.grid_columnconfigure(col, weight=1)

        # Výpočet svátků
        selected_year_int = int(selected_year)
        easter_sunday = compute_easter(selected_year_int)
        easter_monday = easter_sunday + timedelta(days=1)
        easter_friday = easter_sunday - timedelta(days=2)
        holidays = [
            date(selected_year_int, 1, 1),
            easter_friday, easter_sunday, easter_monday,
            date(selected_year_int, 5, 1), date(selected_year_int, 5, 8),
            date(selected_year_int, 7, 5), date(selected_year_int, 7, 6),
            date(selected_year_int, 9, 28), date(selected_year_int, 10, 28),
            date(selected_year_int, 11, 17), date(selected_year_int, 12, 25),
            date(selected_year_int, 12, 26)
        ]
        month_frames = {}
        months_info = [
            ("leden", "Leden", 1),
            ("unor", "Únor", 2),
            ("brezen", "Březen", 3),
            ("duben", "Duben", 4),
            ("kveten", "Květen", 5),
            ("cerven", "Červen", 6),
            ("cervenec", "Červenec", 7),
            ("srpen", "Srpen", 8),
            ("zari", "Září", 9),
            ("rijen", "Říjen", 10),
            ("listopad", "Listopad", 11),
            ("prosinec", "Prosinec", 12)
        ]
        current_record_id = record["id"]
        for key, label, month_num in months_info:
            month_frames[key] = render_month_grid(plan_display_frame, selected_year_int, month_num,
                                                    record[key], label, holidays, record["uvazek"], record["smena"],
                                                    editable=True, highlight=False)
        
        half1_hours = 0
        for month in half1_months:
            try:
                day_plan_list = json.loads(record[month])
            except Exception:
                day_plan_list = [""] * 32
            hours, _ = calculate_month_summary(day_plan_list, record["uvazek"])
            half1_hours += hours
        half2_hours = 0
        for month in half2_months:
            try:
                day_plan_list = json.loads(record[month])
            except Exception:
                day_plan_list = [""] * 32
            hours, _ = calculate_month_summary(day_plan_list, record["uvazek"])
            half2_hours += hours
        total_hours = half1_hours + half2_hours
        tk.Label(plan_display_frame, text=f"Leden - Červen = {half1_hours} hodin", font=("TkDefaultFont", 10, "italic")).pack(pady=5)
        tk.Label(plan_display_frame, text=f"Červenec - Prosinec = {half2_hours} hodin", font=("TkDefaultFont", 10, "italic")).pack(pady=5)
        tk.Label(plan_display_frame, text=f"Celkem: {total_hours} hodin", font=("TkDefaultFont", 10, "italic", "bold")).pack(pady=5)
        
        if not hasattr(employee_frame, "save_btn_frame"):
            employee_frame.save_btn_frame = tk.Frame(employee_frame)
            employee_frame.save_btn_frame.pack(side=tk.LEFT, padx=5)
        else:
            for widget in employee_frame.save_btn_frame.winfo_children():
                widget.destroy()
        
        btn_state = "normal" if current_user_role in ["velitel", "admin", "superadmin"] else "disabled"
        save_btn = ttk.Button(employee_frame.save_btn_frame, text="Uložit změny", command=save_employee_plan, state=btn_state)
        save_btn.pack(side=tk.LEFT, padx=5)
        
    except Exception as e:
        logging.error(f"Chyba při zobrazení plánu zaměstnance: {e}")
        messagebox.showerror("Chyba", f"Došlo k chybě při zobrazení plánu: {e}")

# ----- Funkce pro uložení změn v plánu zaměstnance
def save_employee_plan():
    """
    Uloží upravený plán zaměstnance do databáze.
    """
    try:
        if current_record_id is None:
            messagebox.showwarning("Upozornění", "Není načten žádný plán ke uložení.")
            return
        updated_data = {}
        months_info = [
            ("leden", "Leden", 1),
            ("unor", "Únor", 2),
            ("brezen", "Březen", 3),
            ("duben", "Duben", 4),
            ("kveten", "Květen", 5),
            ("cerven", "Červen", 6),
            ("cervenec", "Červenec", 7),
            ("srpen", "Srpen", 8),
            ("zari", "Září", 9),
            ("rijen", "Říjen", 10),
            ("listopad", "Listopad", 11),
            ("prosinec", "Prosinec", 12)
        ]
        for key, label, month_num in months_info:
            frame = month_frames.get(key)
            if frame is not None:
                updated_data[key] = json.dumps(frame.day_plan_list, ensure_ascii=False)
        with sqlite3.connect("service_plans.db") as conn:
            cursor = conn.cursor()
            update_query = """
                UPDATE plans
                SET leden = ?, unor = ?, brezen = ?, duben = ?, kveten = ?,
                    cerven = ?, cervenec = ?, srpen = ?, zari = ?, rijen = ?,
                    listopad = ?, prosinec = ?
                WHERE id = ?
            """
            params = (
                updated_data.get("leden", ""),
                updated_data.get("unor", ""),
                updated_data.get("brezen", ""),
                updated_data.get("duben", ""),
                updated_data.get("kveten", ""),
                updated_data.get("cerven", ""),
                updated_data.get("cervenec", ""),
                updated_data.get("srpen", ""),
                updated_data.get("zari", ""),
                updated_data.get("rijen", ""),
                updated_data.get("listopad", ""),
                updated_data.get("prosinec", ""),
                current_record_id
            )
            cursor.execute(update_query, params)
            conn.commit()
        messagebox.showinfo("Úspěch", "Změny byly úspěšně uloženy.")
        refresh_treeview()
    except Exception as e:
        logging.error(f"Chyba při ukládání plánu zaměstnance: {e}")
        messagebox.showerror("Chyba", f"Došlo k chybě při ukládání: {e}")

# ----- Funkce pro smazání plánů pro zadaný rok
def delete_plans_by_year():
    """
    Smaže všechny plány pro zadaný rok.
    """
    try:
        year_to_delete = simpledialog.askstring("Smazat plány", "Zadejte rok, pro který chcete smazat všechny plány:")
        if not year_to_delete:
            return
        if messagebox.askyesno("Potvrzení", f"Opravdu chcete smazat všechny plány pro rok {year_to_delete}?"):
            with sqlite3.connect("service_plans.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM plans WHERE roky = ?", (year_to_delete,))
                conn.commit()
            log_action(f"Všechny plány pro rok {year_to_delete} byly smazány")
            messagebox.showinfo("Úspěch", f"Plány pro rok {year_to_delete} byly smazány.")
            refresh_treeview()
    except Exception as e:
        logging.error(f"Chyba při mazání plánů pro rok {year_to_delete}: {e}")
        messagebox.showerror("Chyba", f"Došlo k chybě při mazání plánů: {e}")

# ----- Funkce pro zobrazení plánu směny v záložce Směna
def zobraz_plan_smeny():
    """
    Zobrazí plán směny podle vybraného roku, měsíce a směny.
    """
    rok = combo_rok_smena.get().strip()
    mesic = combo_mesic_smena.get().strip()
    smena = combo_smena_smena.get().strip()
    if not rok or not mesic or not smena:
        messagebox.showwarning("Upozornění", "Vyberte Rok, Měsíc a Směnu.")
        return
    try:
        rok_int = int(rok)
    except ValueError:
        messagebox.showerror("Chyba", "Rok musí být číslo.")
        return
    mesice = {
        "Leden": ("leden", 1),
        "Únor": ("unor", 2),
        "Březen": ("brezen", 3),
        "Duben": ("duben", 4),
        "Květen": ("kveten", 5),
        "Červen": ("cerven", 6),
        "Červenec": ("cervenec", 7),
        "Srpen": ("srpen", 8),
        "Září": ("zari", 9),
        "Říjen": ("rijen", 10),
        "Listopad": ("listopad", 11),
        "Prosinec": ("prosinec", 12)
    }
    if mesic not in mesice:
        messagebox.showerror("Chyba", "Neznámý měsíc.")
        return
    col_name, month_num = mesice[mesic]
    with sqlite3.connect("service_plans.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM plans WHERE roky = ? AND smena = ? ORDER BY CAST(poradi as INTEGER) ASC"
        cursor.execute(query, (rok, smena))
        plans = cursor.fetchall()
    if not plans:
        messagebox.showinfo("Informace", "Pro zadaná kritéria nebyl nalezen žádný plán.")
        return
    for widget in smena_display_frame.winfo_children():
        widget.destroy()
    canvas = tk.Canvas(smena_display_frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(smena_display_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    display_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=display_frame, anchor="nw")
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    display_frame.bind("<Configure>", on_frame_configure)
    easter_sunday = compute_easter(rok_int)
    easter_monday = easter_sunday + timedelta(days=1)
    easter_friday = easter_sunday - timedelta(days=2)
    holidays = [
        date(rok_int, 1, 1),
        easter_friday, easter_sunday, easter_monday,
        date(rok_int, 5, 1), date(rok_int, 5, 8),
        date(rok_int, 7, 5), date(rok_int, 7, 6),
        date(rok_int, 9, 28), date(rok_int, 10, 28),
        date(rok_int, 11, 17), date(rok_int, 12, 25),
        date(rok_int, 12, 26)
    ]
    for plan in plans:
        header_text = f"Pořadí: {plan['poradi']} - {plan['jmeno_prijmeni']}"
        emp_frame = tk.LabelFrame(display_frame, text=header_text, font=("TkDefaultFont", 10, "bold"))
        emp_frame.pack(fill=tk.X, padx=10, pady=5)
        plan_json = plan[col_name]
        # MOD: předání směny (plan["smena"]) do renderování
        render_month_grid(emp_frame, rok_int, month_num, plan_json, mesic, holidays, plan["uvazek"], plan["smena"], editable=False, highlight=False)

# ----- Hlavní část GUI a konfigurace oken
root = tk.Tk()
root.title("Správa Plánu Služeb a Dovolených")
root.geometry("1370x900+0+0")

# ----- Vytvoření hlavního menu a přidání položky Nápověda a O Alikaci
menubar = tk.Menu(root)
root.config(menu=menubar)
help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Menu", menu=help_menu)
help_menu.add_command(label="Nápověda", command=show_help)
help_menu.add_command(label="O aplikaci", command=show_verze)

# ----- Přihlašovací panel
login_frame = tk.Frame(root)
login_frame.pack(fill=tk.X, padx=10, pady=5)
tk.Label(login_frame, text="Jméno:").pack(side=tk.LEFT, padx=5)
login_name_entry = tk.Entry(login_frame)
login_name_entry.pack(side=tk.LEFT, padx=5)
tk.Label(login_frame, text="Heslo:").pack(side=tk.LEFT, padx=5)
login_pwd_entry = tk.Entry(login_frame, show="*")
login_pwd_entry.pack(side=tk.LEFT, padx=5)
login_button = tk.Button(login_frame, text="Přihlásit se", command=login)
login_button.pack(side=tk.LEFT, padx=5)
logout_button = tk.Button(login_frame, text="Odhlásit se", command=logout)
logout_button.pack(side=tk.LEFT, padx=5)
login_status_label = tk.Label(login_frame, text="Nejste přihlášeni: Máte status (uživatel)")
login_status_label.pack(side=tk.LEFT, padx=10)

# ----- Hlavní záložkový widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Záložka Plány
tab_plany = ttk.Frame(notebook, width=1200, height=700)
tab_plany.pack(fill=tk.BOTH, expand=True)
notebook.add(tab_plany, text="Plány")

# Podzáložky pro Plány: Zaměstnanec a Směna
plans_notebook = ttk.Notebook(tab_plany)
plans_notebook.pack(expand=True, fill='both', padx=10, pady=10)
tab_zamestnanec = ttk.Frame(plans_notebook)
plans_notebook.add(tab_zamestnanec, text="Zaměstnanec")
tab_smena = ttk.Frame(plans_notebook)
plans_notebook.add(tab_smena, text="Směna")

# ----- Filtr pro záložku Směna
filter_smena_frame = tk.Frame(tab_smena)
filter_smena_frame.pack(fill=tk.X, padx=10, pady=5)
current_year = datetime.now().year
years = [str(current_year - 1), str(current_year), str(current_year + 1)]
months = ["Leden", "Únor", "Březen", "Duben", "Květen", "Červen", "Červenec", "Srpen", "Září", "Říjen", "Listopad", "Prosinec"]
shifts = ["", "Směna 1", "Směna 2", "Směna 3", "Směna 4", "Směna 5", "Směna 6"]

tk.Label(filter_smena_frame, text="Roky:", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=5)
combo_rok_smena = ttk.Combobox(filter_smena_frame, values=years, state="readonly", width=10)
combo_rok_smena.current(1)
combo_rok_smena.pack(side=tk.LEFT, padx=5)
tk.Label(filter_smena_frame, text="Měsíc:", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=5)
combo_mesic_smena = ttk.Combobox(filter_smena_frame, values=months, state="readonly", width=10)
combo_mesic_smena.current(datetime.now().month - 1)
combo_mesic_smena.pack(side=tk.LEFT, padx=5)
tk.Label(filter_smena_frame, text="Směna:", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=5)
combo_smena_smena = ttk.Combobox(filter_smena_frame, state="readonly", width=10)
combo_smena_smena['values'] = ["", "Směna 1", "Směna 2", "Směna 3", "Směna 4", "Směna 5", "Směna 6"]
combo_smena_smena.set("")
combo_smena_smena.pack(side=tk.LEFT, padx=5)
btn_zobraz_plan_smeny_smena = ttk.Button(filter_smena_frame, text="Zobraz plán Směny", command=zobraz_plan_smeny)
btn_zobraz_plan_smeny_smena.pack(side=tk.LEFT, padx=5)

# MOD: Přidání tlačítek Zamknout a Odemknout plán – ty budou viditelné pouze pro superadmina
btn_lock_plan = ttk.Button(filter_smena_frame, text="Zamknout Plán", command=lock_plan)
btn_lock_plan.pack(side=tk.LEFT, padx=5)
btn_unlock_plan = ttk.Button(filter_smena_frame, text="Odemknout Plán", command=unlock_plan)
btn_unlock_plan.pack(side=tk.LEFT, padx=5)

smena_display_frame = tk.Frame(tab_smena)
smena_display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# ----- Záložka Nastavení
tab_nastaveni = ttk.Frame(notebook)
notebook.add(tab_nastaveni, text="Nastavení")

filter_frame = tk.Frame(tab_nastaveni)
filter_frame.pack(pady=10, padx=10, anchor="w")
tk.Label(filter_frame, text="Filtr - Jméno a příjmení:").pack(side=tk.LEFT, padx=5)
filter_jmeno = ttk.Combobox(filter_frame, state="readonly", width=20)
filter_jmeno.pack(side=tk.LEFT, padx=5)
tk.Label(filter_frame, text="Rok:").pack(side=tk.LEFT, padx=5)
filter_rok = ttk.Combobox(filter_frame, state="readonly", width=10)
filter_rok.pack(side=tk.LEFT, padx=5)
tk.Label(filter_frame, text="Směna:").pack(side=tk.LEFT, padx=5)
filter_smena = ttk.Combobox(filter_frame, state="readonly", width=15)
filter_smena.pack(side=tk.LEFT, padx=5)

def apply_filters():
    selected_jmeno = filter_jmeno.get()
    selected_rok = filter_rok.get()
    selected_smena = filter_smena.get()
    refresh_treeview_filtered(jmeno_filter=selected_jmeno, rok_filter=selected_rok, smena_filter=selected_smena)

tk.Button(filter_frame, text="Filtrovat", command=apply_filters).pack(side=tk.LEFT, padx=5)
tk.Button(filter_frame, text="Zobrazit vše", command=refresh_treeview).pack(side=tk.LEFT, padx=5)

style = ttk.Style()
style.configure("Treeview.Heading", font=("TkDefaultFont", 10, "bold"))

tree = ttk.Treeview(tab_nastaveni, columns=("jmeno_prijmeni", "smena", "uvazek", "roky"), show="headings")
tree.heading("jmeno_prijmeni", text="Jméno a příjmení", command=lambda: treeview_sort_column(tree, "jmeno_prijmeni", False))
tree.heading("smena", text="Směna", command=lambda: treeview_sort_column(tree, "smena", False))
tree.heading("uvazek", text="Úvazek", command=lambda: treeview_sort_column(tree, "uvazek", False))
tree.heading("roky", text="Rok", command=lambda: treeview_sort_column(tree, "roky", False))
tree.column("smena", width=90)
tree.column("uvazek", width=100)
tree.column("roky", width=60)
tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Přidáme binding pro posouvání treeview kolečkem myši
tree.bind("<MouseWheel>", lambda event: tree.yview_scroll(-1 * (event.delta // 120), "units"))

button_frame = ttk.Frame(tab_nastaveni)
button_frame.pack(pady=10)
btn_new = ttk.Button(button_frame, text="Nový", command=on_new)
btn_new.grid(row=0, column=0, padx=5)
btn_edit = ttk.Button(button_frame, text="Edit", command=on_edit)
btn_edit.grid(row=0, column=1, padx=5)
btn_delete = ttk.Button(button_frame, text="Smazat", command=on_delete)
btn_delete.grid(row=0, column=2, padx=5)
btn_data = ttk.Button(button_frame, text="Data", command=open_settings_window)
btn_data.grid(row=0, column=3, padx=5)
# Přidání tlačítka "Fond" za tlačítkem "Data":
fond_button = ttk.Button(button_frame, text="Fond", command=open_fond_window)
fond_button.grid(row=0, column=4, padx=5)
btn_delete_year = ttk.Button(button_frame, text="Smazat plány pro rok", command=delete_plans_by_year)
btn_delete_year.grid(row=0, column=5, padx=5)

notebook.bind("<<NotebookTabChanged>>", lambda event: refresh_treeview() if event.widget.tab(event.widget.index("current"), "text") == "Nastavení" else None)

employee_frame = tk.Frame(tab_zamestnanec)
employee_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
tk.Label(employee_frame, text="Zaměstnanec:", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=5)
employee_combobox = ttk.Combobox(employee_frame, state="readonly")
employee_combobox.pack(side=tk.LEFT, padx=5)
tk.Label(employee_frame, text="Rok:", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=5)
year_combobox = ttk.Combobox(employee_frame, state="readonly")
year_combobox.pack(side=tk.LEFT, padx=5)
tk.Label(employee_frame, text="Směna:", font=("TkDefaultFont", 10, "bold")).pack(side=tk.LEFT, padx=5)
shift_filter_combobox = ttk.Combobox(employee_frame, state="readonly", width=10)
shift_filter_combobox['values'] = ["", "Směna 1", "Směna 2", "Směna 3", "Směna 4", "Směna 5", "Směna 6"]
shift_filter_combobox.set("")
shift_filter_combobox.pack(side=tk.LEFT, padx=5)
shift_filter_combobox.bind("<<ComboboxSelected>>", lambda event: update_employee_list())
show_plan_button = ttk.Button(employee_frame, text="Zobrazit plán", command=show_employee_plan)
show_plan_button.pack(side=tk.LEFT, padx=5)

employee_plan_frame = tk.Frame(tab_zamestnanec)
employee_plan_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

plan_display_canvas = tk.Canvas(employee_plan_frame)
plan_display_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
plan_v_scrollbar = ttk.Scrollbar(employee_plan_frame, orient="vertical", command=plan_display_canvas.yview)
plan_v_scrollbar.pack(side=tk.RIGHT, fill="y")
plan_h_scrollbar = ttk.Scrollbar(employee_plan_frame, orient="horizontal", command=plan_display_canvas.xview)
plan_h_scrollbar.pack(side=tk.BOTTOM, fill="x")
plan_display_canvas.configure(yscrollcommand=plan_v_scrollbar.set, xscrollcommand=plan_h_scrollbar.set)
plan_display_frame = tk.Frame(plan_display_canvas)
plan_display_canvas.create_window((0,0), window=plan_display_frame, anchor="nw")
plan_display_frame.bind("<Configure>", lambda event: plan_display_canvas.configure(scrollregion=plan_display_canvas.bbox("all")))

# ----- Inicializace databáze a nastavení GUI
init_db()
populate_employee_and_year()
apply_access_control()
refresh_treeview()

# ----- Plánovaná záloha databáze každých 24 hodin (86400000 ms)
backup_interval_ms = 86400000  # 24 hodin

def schedule_backup():
    """
    Plánuje pravidelnou zálohu databáze.
    """
    backup_dir = "db_backups"
    if os.path.exists(backup_dir):
        backup_files = [os.path.join(backup_dir, f) for f in os.listdir(backup_dir)
                        if f.startswith("service_plans_backup_") and f.endswith(".db")]
        if backup_files:
            latest_backup = max(backup_files, key=os.path.getmtime)
            last_backup_time = os.path.getmtime(latest_backup)
            if time.time() - last_backup_time >= backup_interval_ms / 1000:
                backup_database()
        else:
            backup_database()
    else:
        backup_database()
    root.after(backup_interval_ms, schedule_backup)
    
schedule_backup()

# ----- Hlavní smyčka GUI
root.mainloop()
