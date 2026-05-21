# ChaosFFA Jelentkezési Bot – Komplett Beállítási Útmutató

## 1. Előfeltételek
- Python 3.12+
- Discord bot token (létrehozva: https://discord.com/developers/applications)
- Discord szerver, ahoväl a botot hívod

---

## 2. Lokális futtatás

```bash
cd "C:\Users\neong\Documents\Discord Botok\chaosffa bot"
pip install -r requirements.txt

# másold a .env.example-t .env néven és írd be a token-t:
copy .env.example .env
# vagy manuálisan:
# DISCORD_BOT_TOKEN=ide_a_bot_token
# GUILD_ID=0  # 0 = global sync (1 óra), vagy töltsd fel a szerver ID-val

python main.py
```

### Környezeti változók (`.env` fájl)

| Változó | Kötelező? | Leírás |
|---|---|---|
| `DISCORD_BOT_TOKEN` | ✅ Igen | A bot token a Developer Portalról |
| `GUILD_ID` | ❌ Nem | Szerver ID az azonnali slash parancs szinkronizáláshoz |

**`GUILD_ID` beszerzése:** Discord → Beállítások → Fejlesztői → Fejlesztői mód be → Jobb klikk a szerverre → "Szerver azonosító másolása"

---

## 3. Railway deploy

### 3a. GitHub feltöltés
```bash
git push -u origin main
```

### 3b. Railway projekt létrehozása
1. Menj a [railway.app](https://railway.app) → New Project → Empty Project
2. Katt a **+ New** gombra → **GitHub Repo** → válaszd ki a `chaosffa` repót
3. Railway automatikusan észleli a `railway.json`-t és `requirements.txt`-t

### 3c. Környezeti változók Railway-ben
Variables fül → Add:
```
DISCORD_BOT_TOKEN = <te_bot_tokened>
GUILD_ID          = <te_szerver_ID_d>   # vagy 0 a globális sync-hez
```

### 3d. Serverless beállítás (INGYENES csomag)
- Settings → Deployments → **Enable Serverless** = ON
- **Figyelem:** Ne használd `sleepApplication`, a Railway mostantól kezeli automatikusan

---

## 4. Discord Developer Portal beállításai

Alap URL: https://discord.com/developers/applications

### 4a. OAuth2 → URL Generator (bot meghívása a szerverre)
- **Scopes:** `bot`, `applications.commands`
- **Bot Permissions:** nincs különleges jog szükséges a DM alapú folyamathoz
- A generált link használatával add hozzá a botot a szerverhez

### 4b. Privileged Gateway Intents
**FONTOS** – a bot futásához ez KÖTELEZŐ:

| Intent | Be? | Miért? |
|---|---|---|
| ✅ **Message Content Intent** | **BE** | DM válaszok olvasásához szükséges |
| ⬜ Server Members Intent | Nem kell | A kód REST API-val dolgozik |
| ⬜ Presence Intent | Nem kell | Nem használjuk |

Ha a **Message Content Intent** nincs BE, a bot futáskor el fog bukni a következő hibával:
```
discord.errors.PrivilegedIntentsRequired
```

---

## 5. Elérhető jelentkezési típusok

| Típus | Parancs értéke | Kérdések száma |
|---|---|---|
| Helper | `helper` | 15 |
| Moderátor | `mod` | 15 |
| Fejlesztő | `fejleszto` | 30 |
| Admin | `admin` | 20 |

---

## 6. Használat

### Staff oldal:
```
/sendtgf @felhasznalo tipus
```
pl. `/sendtgf @NeonGamer3220 helper`

A bot DM-ben küldi az induló kérdőívet a célfelhasználónak.

### Felhasználó oldal:
1. Kap egy DM-t a bottól → nyomja a **Jelentkezés indítása** gombot
2. Válaszoljon egyesével a kérdésekre DM-ben
3. Utolsó válasz után nyomja a **Jelentkezés beküldése** gombot
4. A bot elküldi a kérdőívet a **<#1507023523674193962>** csatornára a staffnak

### Staff elbírálás:
- A csatornában megjelenik az összes kérdés és válasz
- **✅ Elfogadás** → megjelenik egy modal, ahová beírhatod a visszajelzést
- **❌ Elutasítás** → ugyanúgy, de elutasító üzenetet küld a jelentkezőnek DM-ben
- Elfogadás esetén a jelentkező kap egy üzenetet, hogy válasszon időpontot a szóbeli meghallgatásra

---

## 7. Közös hibák és javításaik

| Hiba | Oka | Javítás |
|---|---|---|
| `PrivilegedIntentsRequired` | Message Content Intent nincs BE a Dev Portalban | 4b. lépés |
| 0 slash commands | Bot nincs `applications.commands` scope-tal invítálva | 4a. lépés újrahívása |
| Bot nem válaszol DM-ben | A felhasználó bezárta a DM-eket | Felhasználó nyissa meg a DM-eket |
| Nem küldi a kérdőívet | `STAFF_CHANNEL_ID` nem elérhető a bottól | Ellenőrizd a csatorna azonosítót |
