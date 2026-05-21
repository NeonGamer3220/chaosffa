import os
import json
import datetime
import asyncio
from pathlib import Path
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

# ─────────────── colours / constants ───────────────
LIGHT_RED    = discord.Color(0xFF5555)
LIGHT_PURPLE = discord.Color(0xBB86FC)
LIGHT_GREEN  = discord.Color(0x00E676)

STAFF_CHANNEL_ID  = 1507023523674193962
GUILD_ID          = int(os.getenv("GUILD_ID", "0"))
TIME_LIMIT_MINUTES = 60

# ─────────────── questions ───────────────
QUESTIONS: dict[str, list[str]] = {
    "Helper": [
        "Mi a Minecraft felhaszn\u00e1l\u00f3neved \u00e9s h\u00e1ny \u00e9ves vagy?",
        "Mio\u00f3ta j\u00e1tszol Minecrafttal?",
        "Volt\u00e1l m\u00e1s szerveren Helper vagy Staff tag? Ha igen, hol \u00e9s milyen poz\u00edci\u00f3ban?",
        "Mi\u00e9rt szeretn\u00e9l Helper lenni ezen a szerveren?",
        "Mit gondolsz, mi egy j\u00f3 Helper legfontosabb feladata?",
        "Hogyan kezeln\u00e9l egy toxikus vagy szab\u00e1lyszeg\u0151 j\u00e1t\u00e9kost?",
        "Mit tenn\u00e9l, ha k\u00e9t j\u00e1t\u00e9kos vitatkozna egym\u00e1ssal a chaten?",
        "Mennyi id\u0151t tudsz \u00e1tlagosan a szerveren t\u00f6lteni naponta?",
        "Ismered a szerver szab\u00e1lyait, \u00e9s be tudod tartatni \u0151ket?",
        "Hogyan seg\u00edten\u00e9l egy \u00faj j\u00e1t\u00e9kosnak, aki nem ismeri a szervert?",
        "Mit csin\u00e1ln\u00e1l, ha egy bar\u00e1tod megszegn\u00e9 a szab\u00e1lyokat?",
        "Mennyire tudsz csapatban egy\u00fctt dolgozni m\u00e1s Staff tagokkal?",
        "Volt\u00e1l m\u00e1r b\u00fcntetve szerveren? Ha igen, mi\u00e9rt?",
        "Hogyan reag\u00e1ln\u00e1l arra, ha valaki s\u00e9rtegetne t\u00e9ged Staffk\u00e9nt?",
        "Mi\u00e9rt t\u00e9ged v\u00e1lasszunk Helpernek m\u00e1s jelentkez\u0151k helyett?",
    ],
    "Moder\u00e1tor": [
        "Mi a Minecraft neved \u00e9s h\u00e1ny \u00e9ves vagy?",
        "Mio\u00f3ta j\u00e1tszol Minecrafttal, \u00e9s mio\u00f3ta vagy akt\u00edv multiplayer szervereken?",
        "Volt\u00e1l m\u00e1r Moder\u00e1tor vagy m\u00e1s Staff poz\u00edci\u00f3ban? Ha igen, melyik szerveren \u00e9s mennyi ideig?",
        "Mi\u00e9rt szeretn\u00e9l Moder\u00e1tor lenni ezen a szerveren?",
        "Mit gondolsz, mi a Moder\u00e1tor legfontosabb feladata?",
        "Hogyan kezeln\u00e9l egy j\u00e1t\u00e9kost, aki folyamatosan megszegi a szab\u00e1lyokat?",
        "Mit tenn\u00e9l, ha egy j\u00e1t\u00e9kos csal\u00e1ssal (hack, cheat) lenne gyan\u00fas?",
        "Hogyan reag\u00e1ln\u00e1l egy nagyobb chatvit\u00e1ra vagy toxikus viselked\u00e9sre?",
        "Mit csin\u00e1ln\u00e1l, ha egy m\u00e1sik Staff tag hib\u00e1zna vagy szab\u00e1lytalanul j\u00e1rna el?",
        "Mennyire tudsz nyugodt maradni stresszes helyzetekben?",
        "Mennyi id\u0151t tudsz naponta vagy hetente a szerveren t\u00f6lteni?",
        "Mennyire ismered a szerver szab\u00e1lyzat\u00e1t \u00e9s b\u00fcntet\u00e9si rendszer\u00e9t?",
        "Mit tenn\u00e9l, ha a bar\u00e1tod szab\u00e1lyt s\u00e9rt a szerveren?",
        "Hogyan seg\u00edten\u00e9d a Helper csapat munk\u00e1j\u00e1t Moder\u00e1tork\u00e9nt?",
        "Mi\u00e9rt t\u00e9ged v\u00e1lasszunk Moder\u00e1tornak a t\u00f6bbi jelentkez\u0151 helyett?",
    ],
    "Fejleszt\u0151": [
        "Mi a Minecraft neved \u00e9s h\u00e1ny \u00e9ves vagy?",
        "Mio\u00f3ta foglalkozol Minecraft fejleszt\u00e9ssel?",
        "Milyen fejleszt\u0151i tapasztalataid vannak?",
        "Milyen szervereken dolgozt\u00e1l kor\u00e1bban, \u00e9s milyen feladatokat v\u00e9gezt\u00e9l?",
        "Mi\u00e9rt szeretn\u00e9l fejleszt\u0151 lenni ezen a szerveren?",
        "Milyen pluginokkal vagy rendszerekkel dolgozt\u00e1l m\u00e1r?",
        "Milyen programoz\u00e1si nyelveket ismersz? (pl. Java, JavaScript, Python)",
        "Tudsz saj\u00e1t plugint k\u00e9sz\u00edteni? Ha igen, mutass p\u00e9ld\u00e1t vagy \u00edrd le a tapasztalatod.",
        "Haszn\u00e1lt\u00e1l m\u00e1r API-kat vagy k\u00fcls\u0151 integr\u00e1ci\u00f3kat?",
        "Dolgozt\u00e1l m\u00e1r Minecraft plugin API-val? (pl. Spigot, Paper, Bukkit)",
        "Mennyire ismered a YAML konfigur\u00e1ci\u00f3kat?",
        "K\u00e9sz\u00edtett\u00e9l m\u00e1r egyedi konfigur\u00e1ci\u00f3kat vagy rendszerbe\u00e1ll\u00edt\u00e1sokat?",
        "Dolgozt\u00e1l m\u00e1r MythicMobs, ItemsAdder, Oraxen vagy hasonl\u00f3 pluginokkal?",
        "Tudsz hib\u00e1t keresni \u00e9s console errorokat \u00e9rtelmezni?",
        "Mit tenn\u00e9l, ha egy plugin \u00f6sszeomlasztan\u00e1 a szervert?",
        "Hogyan teszteln\u00e9d egy \u00faj rendszer stabilit\u00e1s\u00e1t?",
        "Haszn\u00e1lt\u00e1l m\u00e1r verzi\u00f3kezel\u0151t, p\u00e9ld\u00e1ul Gitet vagy GitHubot?",
        "Milyen fejleszt\u0151i eszk\u00f6z\u00f6ket haszn\u00e1lsz? (pl. IntelliJ IDEA, VS Code)",
        "K\u00e9sz\u00edtett\u00e9l m\u00e1r adatb\u00e1zis-kezel\u00e9st Minecraft projekthez? (pl. MySQL, SQLite)",
        "Tudsz optimaliz\u00e1lni lagos vagy rosszul m\u0171k\u00f6d\u0151 rendszereket?",
        "Hogyan dokument\u00e1lod a munk\u00e1dat vagy a rendszereidet?",
        "Mit csin\u00e1ln\u00e1l, ha s\u00fcrg\u0151s hib\u00e1t kellene jav\u00edtani j\u00e1t\u00e9kosok online jelenl\u00e9te mellett?",
        "Tudsz csapatban dolgozni m\u00e1s fejleszt\u0151kkel \u00e9s Staff tagokkal?",
        "Hogyan kezeled a kritik\u00e1t vagy a m\u00f3dos\u00edt\u00e1si k\u00e9r\u00e9seket?",
        "Mennyi id\u0151t tudsz hetente fejleszt\u00e9sre fordítani?",
        "Dolgozt\u00e1l m\u00e1r permission vagy rangrendszerekkel?",
        "K\u00e9sz\u00edtett\u00e9l m\u00e1r egyedi GUI-kat, men\u00fcket vagy parancsrendszereket?",
        "Van olyan projekted vagy munk\u00e1d, amire k\u00fcl\u00f6n\u00f6sen b\u00fcszke vagy?",
        "Mit gondolsz, mi k\u00fcl\u00f6nb\u00f6ztet meg egy \u00e1tlagos fejleszt\u0151t egy igaz\u00e1n j\u00f3 fejleszt\u0151t\u0151l?",
        "Mi\u00e9rt t\u00e9ged v\u00e1lasszunk fejleszt\u0151nek a szerverre?",
    ],
    "Admin": [
        "Mi a Minecraft neved \u00e9s h\u00e1ny \u00e9ves vagy?",
        "Mio\u00f3ta j\u00e1tszol Minecrafttal \u00e9s mi\u00f3ta vagy akt\u00edv szervereken?",
        "Volt\u00e1l m\u00e1r Admin vagy m\u00e1s Staff poz\u00edci\u00f3ban? Ha igen, hol \u00e9s mennyi ideig?",
        "Mi\u00e9rt szeretn\u00e9l Admin lenni ezen a szerveren?",
        "Mit gondolsz, mi egy Admin legfontosabb feladata?",
        "Hogyan kezeln\u00e9l egy komoly szab\u00e1lyszeg\u00e9st vagy nagyobb konfliktust?",
        "Mit tenn\u00e9l, ha egy Moder\u00e1tor vagy Helper vissza\u00e9lne a jogaival?",
        "Hogyan reag\u00e1ln\u00e1l, ha t\u00f6bb j\u00e1t\u00e9kos egyszerre k\u00e9rne seg\u00edts\u00e9get?",
        "Mit csin\u00e1ln\u00e1l, ha a szerver hirtelen laggolni vagy hib\u00e1zni kezdene?",
        "Mennyire tudsz higgadt maradni stresszes helyzetekben?",
        "Hogyan kezeln\u00e9d a toxikus vagy provok\u00e1l\u00f3 j\u00e1t\u00e9kosokat?",
        "Mit tenn\u00e9l, ha egy bar\u00e1tod megszegn\u00e9 a szab\u00e1lyokat?",
        "Mennyire ismered a szerver szab\u00e1lyzat\u00e1t \u00e9s b\u00fcntet\u00e9si rendszer\u00e9t?",
        "Tudsz csapatban dolgozni \u00e9s ir\u00e1ny\u00edtani m\u00e1s Staff tagokat?",
        "Volt\u00e1l m\u00e1r olyan helyzetben, ahol gyors d\u00f6nt\u00e9st kellett hoznod? Mes\u00e9lj r\u00f3la!",
        "Mennyi id\u0151t tudsz naponta vagy hetente a szerveren t\u00f6lteni?",
        "Mennyire \u00e9rtesz pluginokhoz vagy szerverkezel\u00e9szhez?",
        "Hogyan seg\u00edten\u00e9d a szerver fejl\u0151d\u00e9s\u00e9t Admink\u00e9nt?",
        "Mit gondolsz, mit\u0151l lesz valaki j\u00f3 vezet\u0151 egy Staff csapatban?",
        "Mi\u00e9rt t\u00e9ged v\u00e1lasszunk Adminnak a t\u00f6bbi jelentkez\u0151 helyett?",
    ],
}

# ─────────────── persistent store (Railway serverless-safe) ───────────────
_STORE   = Path("/data/sessions.json")
_FP_PATH = Path("/data/fp.json")       # message-id fingerprints (anti-dupe)
_lock    = asyncio.Lock()

def _now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)

def _iso(dt: datetime.datetime) -> str:
    return dt.isoformat()

def _dt(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s)

async def load_state() -> None:
    """Restore sessions + fingerprints from disk into the global dict."""
    try:
        data = json.loads(_STORE.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    now = _now()
    for uid_s, blob in data.items():
        try:
            if blob.get("deadline") and now > _dt(blob["deadline"]):
                continue
        except Exception:
            pass
        if isinstance(blob.get("_seen"), list):
            blob["_seen"] = set(blob["_seen"])
        sessions[int(uid_s)] = blob

    # merge fingerprint overrides
    try:
        fp = json.loads(_FP_PATH.read_text(encoding="utf-8"))
    except Exception:
        fp = {}
    for uid_s, ids in fp.items():
        uid = int(uid_s)
        if uid in sessions:
            old = sessions[uid].get("_seen", set())
            if not isinstance(old, set):
                old = set()
            sessions[uid]["_seen"] = old | set(ids if isinstance(ids, list) else [ids])

def _fingerprints() -> dict[str, list[int]]:
    return {str(uid): sorted(s.get("_seen", set()))
            for uid, s in sessions.items() if s.get("_seen")}

async def save_state() -> None:
    """Write sessions + fingerprints to disk. Atomic, caller-awaitable."""
    copies: dict[str, dict] = {}
    for uid, s in sessions.items():
        safe: dict = {}
        for k, v in s.items():
            if isinstance(v, set):
                safe[k] = sorted(v)
            elif isinstance(v, discord.ui.View):
                continue
            elif isinstance(v, discord.ui.Button):
                continue
            elif isinstance(v, (discord.TextInput, discord.ui.Modal)):
                continue
            else:
                safe[k] = v
        if isinstance(safe.get("started_at"), datetime.datetime):
            safe["started_at"] = safe["started_at"].isoformat()
        if isinstance(safe.get("deadline"), datetime.datetime):
            safe["deadline"] = safe["deadline"].isoformat()
        copies[str(uid)] = safe

    _STORE.parent.mkdir(parents=True, exist_ok=True)
    tmp = _STORE.with_suffix(".tmp")
    try:
        tmp.write_text(json.dumps(copies, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(_STORE)
    except Exception as exc:
        print(f"[WARN] sessions save failed: {exc}")

    fp = _fingerprints()
    if fp:
        tmpf = _FP_PATH.with_suffix(".tmp")
        try:
            tmpf.write_text(json.dumps(fp, indent=2), encoding="utf-8")
            tmpf.replace(_FP_PATH)
        except Exception as exc:
            print(f"[WARN] fp save failed: {exc}")

async def save_async() -> None:
    """Save state synchronously; callers already run sequentially so no lock needed."""
    await save_state()

# ─────────────── in-memory stores ───────────────
sessions:      dict[int, dict] = {}   # uid → session dict
reviews:       dict[int, dict] = {}   # staff-msg-id → review data

# ─────────────── helper to rebuild a DM channel from persisted data ───────────────
async def dm_ch(sess: dict) -> discord.abc.Messageable | None:
    cid = sess.get("dm_channel_id")
    uid = sess.get("submitter_id") or sess.get("submitter")
    if not cid or not uid:
        return None
    ch = bot.get_channel(cid)
    if ch:
        return ch
    try:
        u = await bot.fetch_user(uid)
        return await u.create_dm()
    except Exception:
        return None

def fmt_deadline(dt: datetime.datetime) -> str:
    return f"<t:{int(dt.timestamp())}:R>"

def fmt_duration(s: int) -> str:
    m, r = divmod(s, 60)
    return f"{m} perc {r} m\u00e1sodperc" if m else f"{r} m\u00e1sodperc"

def qa_lines(role: str, answers: dict[int, str], total: int) -> str:
    rows = []
    for i in range(total):
        q = QUESTIONS[role][i]
        a = answers.get(i, "*\u2013 nincs v\u00e1lasz \u2013*")
        rows.append(f"**{i+1}.** *{q}*\n**V:** {a}")
    return "\n\n".join(rows)


# ─────────────── Buttons ───────────────

class CloseBtn(discord.ui.Button):
    def __init__(self, role: str, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.red)
        self.role = role

    async def callback(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        sessions.pop(uid, None)
        await save_async()
        if self.view:
            self.view.stop()
        for c in self.view.children:
            c.disabled = True
        await interaction.response.edit_message(view=self.view)
        try:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="**Jelentkez\u00e9s megszak\u00edtva**",
                    description=f"Sikeresen megszak\u00edtottad a ChaosFFA {self.role} jelentkez\u00e9st!",
                    color=LIGHT_RED,))
        except Exception:
            pass


# ─────────────── View 1 – initial embed ───────────────

class StartView(discord.ui.View):
    def __init__(self, role: str):
        super().__init__(timeout=None)
        self.role = role
        g = discord.ui.Button(label="Jelentkez\u00e9s ind\u00edt\u00e1sa", style=discord.ButtonStyle.green)
        g.callback = self._go
        self.add_item(g)
        self.add_item(CloseBtn(role, "M\u00e9gsem"))

async def _go(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        sess = sessions.get(uid)
        if not sess:
            return await interaction.response.send_message(
                "A munkamenet lejárt vagy nem található.", ephemeral=True)

        # prevent double-press / double-callback race
        if sess.get("_handling"):
            return await interaction.response.defer(ephemeral=True)
        sess["_handling"] = True
        await save_async()  # persist handling flag

        role   = sess["type"]
        dl     = _now() + datetime.timedelta(minutes=TIME_LIMIT_MINUTES)

        # block duplicate presses (same interaction = same message)
        await interaction.response.edit_message(
            embed=discord.Embed(
                title="**Jelentkez\u00e9s elind\u00edtva**",
                description=(
                    f"Sikeresen elind\u00edtottad a ChaosFFA {role} jelentkez\u00e9st.\n"
                    f"Hat\u00e1rid\u0151: {fmt_deadline(dl)}"),
                color=LIGHT_PURPLE),
            view=None)

        sess["deadline"]    = dl
        sess["started_at"]  = _now()
        sess["step"]        = 0
        sess["answers"]     = {}
        sess["_interacted"] = True   # mark as started — ignore old re-send attempts
        await save_async()

        qs   = QUESTIONS[role]
        total = len(qs)
        v    = QuestionView(role, total)
        sess["_qv"] = v

        ch = await dm_ch(sess)
        if ch is None:
            return await interaction.followup.send(
                "Nem sikerült újra megnyitni a DM csatornát.", ephemeral=True)

        e = discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés – 1. kérdés**",
            description=qs[0], color=LIGHT_PURPLE)
        e.set_footer(text=f"Válaszként küldj DM üzenetet a botnak.\n"
                            f"Lejárat: 7 napja\n1/{total} kérdés")
        await ch.send(embed=e, view=v)
        print(f"[DEBUG] _go: sent first question to uid={uid}, step=0")


# ─────────────── View 2 – per-question ───────────────

class QuestionView(discord.ui.View):
    def __init__(self, role: str, total: int):
        super().__init__(timeout=None)
        self.role  = role
        self.total = total
        b = discord.ui.Button(label="Jelentkez\u00e9s lez\u00e1r\u00e1sa", style=discord.ButtonStyle.red)
        b.callback = self._close
        self.add_item(b)

    async def _close(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        sessions.pop(uid, None)
        await save_async()
        self.stop()
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=discord.Embed(
                title="**Jelentkez\u00e9s megszak\u00edtva**",
                description=f"Sikeresen megszak\u00edtottad a ChaosFFA {self.role} jelentkez\u00e9st!",
                color=LIGHT_RED))


# ─────────────── View 3 – all-answered confirmation ───────────────

class ConfirmView(discord.ui.View):
    def __init__(self, uid: int, role: str, total: int, started_at: datetime.datetime):
        super().__init__(timeout=None)
        self.uid   = uid
        self.role  = role
        self.total = total
        self.sta   = started_at
        b = discord.ui.Button(label="Jelentkez\u00e9s bek\u00fcld\u00e9se", style=discord.ButtonStyle.green)
        b.callback = self._go
        self.add_item(b)
        self.add_item(CloseBtn(role, "M\u00e9gsem"))

    async def _go(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        sess = sessions.pop(uid, None)
        if not sess:
            return await interaction.response.send_message(
                "A munkamenet nem tal\u00e1lhat\u00f3.", ephemeral=True)

        answers     = sess["answers"]
        role        = self.role
        total       = self.total
        submitter_n = sess["submitter_name"]
        sta         = self.sta
        now         = _now()
        elapsed     = int((now - sta).total_seconds())

        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)
        await save_async()

        ch = await dm_ch(sess)
        if ch is None:
            return

        e = discord.Embed(
            title=f"**ChaosFFA {role} jelentkez\u00e9s**",
            description=(
                "Sikeresen megv\u00e1laszoltad az \u00f6sszes k\u00e9rd\u00e9st.\n\n"
                "Ha biztos vagy benne, hogy bek\u00fcld\u00f6d a jelentkez\u00e9st, "
                "nyomd meg a bek\u00fcld\u00e9s gombot."),
            color=LIGHT_PURPLE)
        e.add_field(name="Felhaszn\u00e1l\u00f3", value=f"@{submitter_n}", inline=False)
        e.add_field(name="Kit\u00f6lt\u00e9si id\u0151", value=fmt_duration(elapsed), inline=False)
        e.set_footer(text=f"Megv\u00e1laszolt k\u00e9rd\u00e9sek: {total}/{total}")

        await ch.send(embed=e, view=SubmitView(
            uid, role, total, submitter_n, sta))


# ─────────────── View 4 – submit to staff ───────────────

class SubmitView(discord.ui.View):
    def __init__(self, submitter_id: int, role: str, total: int,
                 author_name: str, started_at: datetime.datetime):
        super().__init__(timeout=None)
        self.sid    = submitter_id
        self.role   = role
        self.total  = total
        self.aname  = author_name
        self.sta    = started_at
        b = discord.ui.Button(label="Jelentkez\u00e9s bek\u00fcld\u00e9se", style=discord.ButtonStyle.green)
        b.callback = self._go
        self.add_item(b)
        self.add_item(CloseBtn(role, "Jelentkez\u00e9s lez\u00e1r\u00e1sa"))

    async def _go(self, interaction: discord.Interaction) -> None:
        uid = self.sid
        sess = sessions.pop(uid, None)
        if not sess:
            return await interaction.response.send_message(
                "A munkamenet nem tal\u00e1lhat\u00f3.", ephemeral=True)

        answers  = sess["answers"]
        role     = self.role
        total    = self.total
        a_name   = self.aname
        sub_name = sess["submitter_name"]
        staff_ch = bot.get_channel(STAFF_CHANNEL_ID)

        self.stop()
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)
        await save_async()

        e = discord.Embed(
            title=f"**ChaosFFA {role} jelentkez\u00e9s**",
            description=qa_lines(role, answers, total),
            color=LIGHT_PURPLE)
        e.add_field(name="Jelentkez\u0151",    value=f"@{a_name}", inline=True)
        e.add_field(name="Jelentkez\u00e9s t\u00edpusa", value=role, inline=True)
        e.add_field(name="Bek\u00fcld\u00e9s ideje",
                    value=f"<t:{int(self.sta.timestamp())}:F>", inline=False)
        rv = StaffReview(uid, sub_name, role, total)
        msg = await staff_ch.send(embed=e, view=rv)
        reviews[msg.id] = dict(
            submitter_id=uid, submitter_name=sub_name,
            role=role, total=total, answers=dict(answers),
            dm_cid=sess.get("dm_channel_id"))

        await interaction.followup.send(
            embed=discord.Embed(
                title="**Jelentkez\u00e9s bek\u00fcldve**",
                description="A staff tagok mostant\u00f3l elb\u00edr\u00e1lj\u00e1k a jelentkez\u00e9sedet.",
                color=LIGHT_GREEN),
            ephemeral=True)


# ─────────────── View 5 – staff review ───────────────

class StaffReview(discord.ui.View):
    def __init__(self, submitter_id: int, submitter_name: str, role: str, total: int):
        super().__init__(timeout=None)
        self.sid   = submitter_id
        self.sname = submitter_name
        self.role  = role
        self.total = total
        a = discord.ui.Button(label="Elfogad\u00e1s", style=discord.ButtonStyle.green)
        a.callback = self._accept
        self.add_item(a)
        r = discord.ui.Button(label="Elutas\u00edt\u00e1s", style=discord.ButtonStyle.red)
        r.callback = self._reject
        self.add_item(r)

    async def _accept(self, i: discord.Interaction) -> None:
        await self._modal(i, "elfogadva", discord.Color(0x00E676))

    async def _reject(self, i: discord.Interaction) -> None:
        await self._modal(i, "elutas\u00edtva", discord.Color(0xFF1744))

    async def _modal(self, i: discord.Interaction, verdict: str, color: discord.Color) -> None:
        self._msg = i.message
        await i.response.send_modal(
            ReviewModal(parent=self, staff_msg=i.message, verdict=verdict, color=color))


class ReviewModal(discord.ui.Modal):
    def __init__(self, parent: StaffReview, staff_msg: discord.Message,
                 verdict: str, color: discord.Color):
        super().__init__(title=f"Jelentkez\u00e9s {verdict} \u2013 \u00fczenet \u00edr\u00e1sa")
        self._parent  = parent
        self._msg     = staff_msg
        self._verdict = verdict
        self._color   = color
        self.txt = discord.ui.TextInput(
            label="Elb\u00edr\u00e1l\u00f3 \u00fczenet",
            placeholder="\u00cdrd le az elb\u00edr\u00e1l\u00e1sod r\u00f6viden ...",
            style=discord.TextStyle.long, max_length=2000, required=False)
        self.add_item(self.txt)

    async def on_submit(self, i: discord.Interaction) -> None:
        text  = self.txt.value.strip() or "Nincs megadva."
        rname = str(i.user)
        rev   = reviews.get(self._msg.id, {})
        role  = rev.get("role", "?")

        # edit staff embed
        for c in self._parent.children:
            c.disabled = True
        await i.response.edit_message(
            embed=discord.Embed(
                title=f"**ChaosFFA {role} jelentkez\u00e9s {self._verdict}**",
                description=f"**Elb\u00edr\u00e1l\u00f3:** {rname}",
                color=self._color),
            view=self._parent)

        # DM applicant
        try:
            dm_cid = rev.get("dm_cid")
            applid = rev.get("submitter_id")
            if not dm_cid or not applid:
                return
            ch = bot.get_channel(dm_cid)
            if not ch:
                u = await bot.fetch_user(applid)
                ch = await u.create_dm()
            desc = (f"A jelentkez\u00e9sedet {rname} b\u00edr\u00e1lta el.\n\n"
                    f"**Elb\u00edr\u00e1l\u00f3 \u00fczenete:**\n{text}")
            if self._verdict == "elfogadva":
                desc += ("\n\nA jelentkez\u00e9sed elfogad\u00e1sra ker\u00fclt.\n\n"
                         "K\u00f6sz\u00f6nj\u00fck hogy kit\u00f6lt\u00f6tt\u00e9d! "
                         "K\u00e9rj\u00fclk a hibajegyben v\u00e1lassz ki egy id\u0151pontot "
                         "a sz\u00f3beli meghallgat\u00e1sra.")
            await ch.send(embed=discord.Embed(
                title=f"**ChaosFFA {role} jelentkez\u00e9s {self._verdict}**",
                description=desc, color=self._color))
        except Exception:
            pass


# ─────────────── Bot ───────────────

intents = discord.Intents.none()
intents.guilds         = True
intents.guild_messages = True
intents.dm_messages    = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

_prv = {i for i, v in bot.intents if v and i not in
        {"guilds","guild_messages","dm_messages","message_content"}}
print("[BOOT] Intents OK" if not _prv else f"[BOOT] Extra privileged: {sorted(_prv)}")
print("[BOOT] In use:", sorted(i for i,v in bot.intents if v))


@bot.event
async def on_ready():
    await load_state()
    print(f"[STORE] Restored {len(sessions)} sessions")

    # guild-level sync (instant) + global fallback
    synced = []
    try:
        if GUILD_ID:
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        else:
            synced = await bot.tree.sync()
    except Exception as e:
        print(f"[SYNC] error: {e}")

    if not synced:
        inv = (f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}"
               f"&scope=bot+applications.commands&permissions=0")
        print(f"[INVITE] 0 cmds — re-invite:\n{inv}")
    print(f"[SYNC] {len(synced)} commands synced")

    st = os.getenv("STATUS_TEXT", "ChaosFFA")
    ty = os.getenv("STATUS_TYPE", "online").lower()
    sm = {"online":discord.Status.online,"idle":discord.Status.idle,
          "dnd":discord.Status.do_not_disturb,"invisible":discord.Status.offline}
    await bot.change_presence(status=sm.get(ty, discord.Status.online),
                              activity=discord.CustomActivity(name=st))
    print(f"[STATUS] {ty} | {st}")


# ─── /sendtgf ──────────────────────────────────────────────

def _uid(s: str) -> int | None:
    d = s.strip("<@!> ")
    return int(d) if d.isdigit() else None

@bot.tree.command(name="sendtgf", description="ChaosFFA jelentkez\u00e9si k\u00e9rd\u0151\u00edv k\u00fcld\u00e9se DM-ben.")
@app_commands.describe(username="C\u00e9l felhaszn\u00e1l\u00f3", type_="Jelentkez\u00e9s t\u00edpusa")
@app_commands.choices(type_=[
    app_commands.Choice(name="Helper",       value="Helper"),
    app_commands.Choice(name="Moder\u00e1tor",value="Moder\u00e1tor"),
    app_commands.Choice(name="Fejleszt\u0151",value="Fejleszt\u0151"),
    app_commands.Choice(name="Admin",        value="Admin"),
])
@app_commands.checks.has_permissions(administrator=True)
async def sendtgf(interaction: discord.Interaction,
                  username: str, type_: app_commands.Choice[str]):
    role = type_.value
    member: discord.Member | None = None

    tid = _uid(username)
    if tid:
        try:
            member = await interaction.guild.fetch_member(tid)
        except discord.NotFound:
            pass

    if member is None:
        try:
            g = interaction.guild or (await bot.fetch_guild(GUILD_ID) if GUILD_ID else None)
            if g:
                for m in g.members:
                    if m.name.lower() == username.lower():
                        member = m
                        break
        except Exception:
            pass

    if member is None:
        return await interaction.response.send_message(
            f"Nem tal\u00e1lhat\u00f3 felhaszn\u00e1l\u00f3: `{username}`", ephemeral=True)

    embed = discord.Embed(
        title=f"**ChaosFFA {role} jelentkez\u00e9s**",
        description=(
            "Ha szeretn\u00e9d elkezdeni a jelentkez\u00e9st, nyomd meg az ind\u00edt\u00e1s gombot.\n\n"
            "A kit\u00f6lt\u00e9sre 60 perced lesz. A k\u00e9rd\u00e9sekre DM-ben, egyes\u00e9vel "
            "kell v\u00e1laszolnod. Ha megszak\u00edtod vagy lej\u00e1r az id\u0151, "
            "a jelentkez\u00e9s nem ker\u00fcl bek\u00fcld\u00e9sre."),
        color=LIGHT_RED)
    view = StartView(role)

    try:
        dm_channel = await member.create_dm()
        await dm_channel.send(embed=embed, view=view)
    except discord.Forbidden:
        return await interaction.response.send_message(
            f"Nem siker\u00fclt DM-t k\u00fcldeni {member.mention}-nak.", ephemeral=True)

    sessions[member.id] = {
        "submitter":      interaction.user.id,
        "submitter_name": member.display_name,
        "submitter_id":   member.id,
        "type":           role,
        "dm_channel_id":  dm_channel.id,
        "step":           None,
        "answers":        {},
        "total":          None,
        "started_at":     None,
        "deadline":       None,
        "_seen":          set(),
        "_interacted":    False,
        "_qv":            None,
    }
    await save_async()

    await interaction.response.send_message(
        f"Jelentkez\u00e9si k\u00e9rd\u0151\u00edv elk\u00fcldve {member.mention} ({role}).",
        ephemeral=True)


# ─── DM answer handler ─────────────────────────────────────

@bot.event
async def on_message(message: discord.Message):
    try:
        await bot.process_commands(message)
        if not isinstance(message.channel, discord.DMChannel) or message.author.bot:
            return

        uid  = message.author.id
        sess = sessions.get(uid)
        if not sess:
            print(f"[DEBUG] on_message: no session for uid={uid}")
            return
        if sess.get("step") is None:
            print(f"[DEBUG] on_message: step is None for uid={uid}")
            return
        if not sess.get("_interacted"):
            print(f"[DEBUG] on_message: _interacted is False for uid={uid}")
            return

        # ── idempotency: skip messages already processed ──
        seen: set[int] = sess.get("_seen", set())
        if message.id in seen:
            print(f"[DEBUG] on_message: message {message.id} already seen, skipping")
            return
        seen.add(message.id)
        sess["_seen"] = seen
        await save_state()

        # ── deadline ──
        dl = sess.get("deadline")
        if dl and _now() > _dt(dl):
            sessions.pop(uid, None)
            await save_state()
            return await message.channel.send(
                "⏰ A jelentkezési idő **lejárt**! A jelentkezés nem kerül beküldésre.")

        role     = sess["type"]
        qs       = QUESTIONS[role]
        total    = sess["total"] = len(qs)
        step     = sess["step"]

        sess["answers"][step] = message.content.strip()
        sess["step"] = step + 1
        await save_state()

        # ── all done → confirmation embed ──
        if step + 1 >= total:
            sta = sess.get("started_at") or _now()
            el  = int((_now() - sta).total_seconds())
            sessions.pop(uid, None)
            await save_state()
            e = discord.Embed(
                title=f"**ChaosFFA {role} jelentkezés**",
                description=(
                    "Sikeresen megválaszoltad az összes kérdést.\n\n"
                    "Ha biztos vagy benne, hogy beküldöd a jelentkezést, "
                    "nyomj a beküldés gombra."),
                color=LIGHT_PURPLE)
            e.add_field(name="Felhasználó",
                        value=f"@{message.author.display_name}", inline=False)
            e.add_field(name="Kitöltési idő", value=fmt_duration(el), inline=False)
            e.set_footer(text=f"Megválaszolt kérdések: {total}/{total}")
            await message.channel.send(embed=e, view=ConfirmView(uid, role, total, sta))
            print(f"[DEBUG] on_message: all done for uid={uid}, showing confirmation")
            return

        # ── next question ──
        nxt  = sess["step"]  # use updated step (not step + 1 which was old)
        q    = qs[nxt]
        e    = discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés – {nxt + 1}. kérdés**",
            description=q, color=LIGHT_PURPLE)
        e.set_footer(text=f"Válaszként küldj DM üzenetet a botnak.\n"
                            f"Lejárat: 7 napja\n{nxt + 1}/{total} kérdés")
        await message.channel.send(embed=e)
        print(f"[DEBUG] on_message: sent next question {nxt + 1}/{total} to uid={uid}")
    except Exception as exc:
        print(f"[ERROR] on_message failed: {exc}")
        import traceback; traceback.print_exc()


if __name__ == "__main__":
    load_dotenv()
    t = os.getenv("DISCORD_BOT_TOKEN")
    if not t:
        raise RuntimeError("DISCORD_BOT_TOKEN hi\u00e1nyzik a .env f\u00e1jlb\u00f3l!")
    bot.run(t)
