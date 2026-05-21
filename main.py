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
    "Fejlesztő": [
        "Mi a Minecraft neved és hány éves vagy?",
        "Mióta foglalkozol Minecraft fejlesztéssel?",
        "Milyen fejlesztői tapasztalataid vannak?",
        "Milyen szervereken dolgoztál korábban, és milyen feladatokat végeztél?",
        "Miért szeretnél fejlesztő lenni ezen a szerveren?",
        "Milyen pluginokkal vagy rendszerekkel dolgoztál már?",
        "Milyen programozási nyelveket ismersz? (pl. Java, JavaScript, Python)",
        "Tudsz saját plugint készíteni? Ha igen, mutass példát vagy írd le a tapasztalatod.",
        "Használtál már API-kat vagy külső integrációkat?",
        "Dolgoztál már Minecraft plugin API-val? (pl. Spigot, Paper, Bukkit)",
        "Mennyire ismered a YAML konfigurációkat?",
        "Készítettél már egyedi konfigurációkat vagy rendszerbeállításokat?",
        "Dolgoztál már MythicMobs, ItemsAdder, Oraxen vagy hasonló pluginokkal?",
        "Tudsz hibát keresni és console errorokat értelmezni?",
        "Mit tennél, ha egy plugin összeomlasztaná a szervert?",
        "Hogyan tesztelnéd egy új rendszer stabilitását?",
        "Használtál már verziókezelőt, például Gitet vagy GitHubot?",
        "Milyen fejlesztői eszközöket használsz? (pl. IntelliJ IDEA, VS Code)",
        "Készítettél már adatbázis-kezelést Minecraft projekthez? (pl. MySQL, SQLite)",
        "Tudsz optimalizálni lagos vagy rosszul működő rendszereket?",
        "Hogyan dokumentálod a munkádat vagy a rendszereidet?",
        "Mit csinálnál, ha sürgős hibát kellene javítani játékosok online jelenléte mellett?",
        "Tudsz csapatban dolgozni más fejlesztőkkel és Staff tagokkal?",
        "Hogyan kezeled a kritikát vagy a módosítási kéréseket?",
        "Mennyi időt tudsz hetente fejlesztésre fordítani?",
        "Dolgoztál már permission vagy rangrendszerekkel?",
        "Készítettél már egyedi GUI-kat, menüket vagy parancsrendszereket?",
        "Van olyan projekted vagy munkád, amire különösen büszke vagy?",
        "Mit gondolsz, mi különböztet meg egy átlagos fejlesztőt egy igazán jó fejlesztőtől?",
        "Miért téged válasszunk fejlesztőnek a szerverre?",
    ],
    "Admin": [
        "Mi a Minecraft neved és hány éves vagy?",
        "Mióta játszol Minecrafttal és mióta vagy aktív szervereken?",
        "Voltál már Admin vagy más Staff pozícióban? Ha igen, hol és mennyi ideig?",
        "Miért szeretnél Admin lenni ezen a szerveren?",
        "Mit gondolsz, mi egy Admin legfontosabb feladata?",
        "Hogyan kezelnél egy komoly szabályszegést vagy nagyobb konfliktust?",
        "Mit tennél, ha egy Moderátor vagy Helper visszaélne a jogaival?",
        "Hogyan reagálnál, ha több játékos egyszerre kérne segítséget?",
        "Mit csinálnál, ha a szerver hirtelen laggolni vagy hibázni kezdene?",
        "Mennyire tudsz higgadt maradni stresszes helyzetekben?",
        "Hogyan kezelnéd a toxikus vagy provokáló játékosokat?",
        "Mit tennél, ha egy barátod megszegné a szabályokat?",
        "Mennyire ismered a szerver szabályzatát és büntetési rendszerét?",
        "Tudsz csapatban dolgozni és irányítani más Staff tagokat?",
        "Voltál már olyan helyzetben, ahol gyors döntést kellett hoznod? Mesélj róla!",
        "Mennyi időt tudsz naponta vagy hetente a szerveren tölteni?",
        "Mennyire értesz pluginokhoz vagy szerverkezeléshez?",
        "Hogyan segítenéd a szerver fejlődését Adminként?",
        "Mit gondolsz, mitől lesz valaki jó vezető egy Staff csapatban?",
        "Miért téged válasszunk Adminnak a többi jelentkező helyett?",
    ],
}

# ─────────────── persistent session store (serverless-safe) ───────────────
# Railway wipes in-memory state between invocations on the free/serverless tier.
# Sessions are serialised to JSON at /data/sessions.json and restored on cold start.

_STORE_PATH = Path(os.getenv("SESSION_STORE", "/data/sessions.json"))
_SAVE_LOCK  = asyncio.Lock()


def _now_utc() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _iso(dt: datetime.datetime) -> str:
    return dt.isoformat()


def _dt(s: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(s)


async def _load_sessions() -> dict[int, dict]:
    """Load persisted sessions, dropping any that are past their deadline."""
    try:
        raw = _STORE_PATH.read_text(encoding="utf-8")
        data = json.loads(raw)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

    now = _now_utc()
    sessions = {}
    for uid_str, blob in data.items():
        try:
            if blob.get("deadline") and now > _dt(blob["deadline"]):
                continue  # expired
        except Exception:
            pass
        sessions[int(uid_str)] = blob
    return sessions


async def _save_sessions() -> None:
    """Persist sessions to disk, stripping non-serialisable fields."""
    async with _SAVE_LOCK:
        to_save = {}
        for uid, s in globals()["sessions"].items():
            safe = {k: v for k, v in s.items() if k not in ("channel", "view", "review_msg")}
            if isinstance(safe.get("started_at"), datetime.datetime):
                safe["started_at"] = _iso(safe["started_at"])
            if isinstance(safe.get("deadline"), datetime.datetime):
                safe["deadline"] = _iso(safe["deadline"])
            to_save[str(uid)] = safe
        _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        tmp = _STORE_PATH.with_suffix(".tmp")
        tmp.write_text(json.dumps(to_save, ensure_ascii=False, indent=2), encoding="utf-8")
        # atomic replace
        try:
            tmp.replace(_STORE_PATH)
        except Exception:
            pass


async def _async_save() -> None:
    """Fire-and-forget saver — don't block the caller."""
    asyncio.create_task(_save_sessions())


# ─────────────── in-memory stores ───────────────
#
# sessions[uid] = {
#   "submitter":      int,         # staff member who launched the invite
#   "submitter_name": str,         # display name of the person filling the form
#   "submitter_id":   int,         # discord user id of the applicant
#   "type":           str,         # Helper / Moder\u00e1tor / Fejlesztő / Admin
#   "dm_channel_id":  int,         # DM channel id (for re-opening after cold start)
#   "answers":        {int: str},
#   "total":          int,
#   "started_at":     datetime,    # UTC
#   "deadline":       datetime,    # UTC – auto-reject after this
#   "step":           int | None,  # None = waiting to press start; 0..n = question index
#   "view":           object | None,  # not persisted; None = no active view
# }
sessions:       dict[int, dict] = {}
review_sessions: dict[int, dict] = {}


# ─────────────── helpers ───────────────

def deadline_from_now() -> datetime.datetime:
    return _now_utc() + datetime.timedelta(minutes=TIME_LIMIT_MINUTES)


def fmt_deadline(dt: datetime.datetime) -> str:
    return f"<t:{int(dt.timestamp())}:R>"


def fmt_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m} perc {s} m\u00e1sodperc" if m else f"{s} m\u00e1sodperc"


def build_qa_lines(role: str, answers: dict[int, str], total: int) -> str:
    lines = []
    for i in range(total):
        q = QUESTIONS[role][i]
        a = answers.get(i, "*\u2013 nincs v\u00e1lasz \u2013*")
        lines.append(f"**{i+1}.** *{q}*\n**V:** {a}")
    return "\n\n".join(lines)


# ─────────────── Buttons ───────────────

class _CloseBtn(discord.ui.Button):
    """Reusable red cancel/close button tied to a role."""

    def __init__(self, role: str, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.red)
        self.role = role

    async def callback(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        sessions.pop(uid, None)
        await _async_save()
        if self.view:
            self.view.stop()
        for c in (self.view.children if self.view else []):
            c.disabled = True
        await interaction.response.edit_message(view=self.view)
        try:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="**Jelentkez\u00e9s megszak\u00edtva**",
                    description=f"Sikeresen megszak\u00edtottad a ChaosFFA {self.role} jelentkez\u00e9st!",
                    color=LIGHT_RED,
                )
            )
        except Exception:
            pass


# ─────────────── View 1 – initial embed ───────────────

class StartView(discord.ui.View):
    """Green 'Jelentkez\u00e9s ind\u00edt\u00e1sa' / red 'M\u00e9gsem'."""

    def __init__(self, role: str):
        super().__init__(timeout=None)
        self.role = role
        green = discord.ui.Button(label="Jelentkez\u00e9s ind\u00edt\u00e1sa", style=discord.ButtonStyle.green)
        green.callback = self._start
        self.add_item(green)
        self.add_item(_CloseBtn(role, "M\u00e9gsem"))

    async def _start(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        if uid not in sessions:
            # session might be cold-start-lost — ask admin to re-send
            return await interaction.response.send_message(
                "A munkamenet lej\u00e1rt (szerver \u00e9brentes). K\u00e9rj\u00fclk, k\u00e9rd a staffot, hogy \u00fajra k\u00fcldje a jelentkez\u00e9si \u00edvet.",
                ephemeral=True,
            )

        session = sessions[uid]
        role = session["type"]
        deadline = deadline_from_now()

        await interaction.response.edit_message(
            embed=discord.Embed(
                title="**Jelentkez\u00e9s elind\u00edtva**",
                description=(
                    f"Sikeresen elind\u00edtottad a ChaosFFA {role} jelentkez\u00e9st.\n"
                    f"Hat\u00e1rid\u0151: {fmt_deadline(deadline)}"
                ),
                color=LIGHT_PURPLE,
            ),
            view=None,
        )

        session["deadline"]  = deadline
        session["started_at"] = _now_utc()
        session["step"]      = 0
        session["answers"]   = {}

        questions = QUESTIONS[role]
        total     = len(questions)
        q_view    = QuestionView(role, total)
        session["view"] = q_view
        await _async_save()

        q_embed = discord.Embed(
            title=f"**ChaosFFA {role} jelentkez\u00e9s \u2013 1. k\u00e9rd\u00e9s**",
            description=questions[0],
            color=LIGHT_PURPLE,
        )
        q_embed.set_footer(
            text=f"V\u00e1laszk\u00e9nt k\u00fcldj egy DM \u00fczenetet a botnak.\nLej\u00e1rat: 7 napja\n1/{total} k\u00e9rd\u00e9s"
        )
        await session["channel"].send(embed=q_embed, view=q_view)


# ─────────────── View 2 – per question embed ───────────────

class QuestionView(discord.ui.View):
    """Red 'Jelentkez\u00e9s lez\u00e1r\u00e1sa' button under every question."""

    def __init__(self, role: str, total: int):
        super().__init__(timeout=None)
        self.role  = role
        self.total = total
        btn = discord.ui.Button(label="Jelentkez\u00e9s lez\u00e1r\u00e1sa", style=discord.ButtonStyle.red)
        btn.callback = self._close
        self.add_item(btn)

    async def _close(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        sessions.pop(uid, None)
        await _async_save()
        self.stop()
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=discord.Embed(
                title="**Jelentkez\u00e9s megszak\u00edtva**",
                description=f"Sikeresen megszak\u00edtottad a ChaosFFA {self.role} jelentkez\u00e9st!",
                color=LIGHT_RED,
            )
        )


# ─────────────── View 3 – beküldés confirmation ───────────────

class SubmitViewConfirmation(discord.ui.View):
    """Green 'Jelentkez\u00e9s bek\u00fcld\u00e9se' / red 'M\u00e9gsem'."""

    def __init__(self, uid: int, role: str, total: int, started_at: datetime.datetime):
        super().__init__(timeout=None)
        self.uid        = uid
        self.role       = role
        self.total      = total
        self.started_at = started_at

        submit_btn = discord.ui.Button(label="Jelentkez\u00e9s bek\u00fcld\u00e9se", style=discord.ButtonStyle.green)
        submit_btn.callback = self._submit
        self.add_item(submit_btn)
        self.add_item(_CloseBtn(role, "M\u00e9gsem"))

    async def _submit(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        session = sessions.get(uid)
        if not session:
            return await interaction.response.send_message(
                "A munkamenet nem tal\u00e1lhat\u00f3.", ephemeral=True
            )

        role        = session["type"]
        answers     = session["answers"]
        channel     = session["channel"]
        submitter_n = session["submitter_name"]
        started_at  = session["started_at"]

        now       = _now_utc()
        elapsed_s = int((now - started_at).total_seconds())

        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)

        summary = discord.Embed(
            title=f"**ChaosFFA {role} jelentkez\u00e9s**",
            description=(
                "Sikeresen megv\u00e1laszoltad az \u00f6sszes k\u00e9rd\u00e9st.\n\n"
                "Ha biztos vagy benne, hogy bek\u00fcld\u00f6d a jelentkez\u00e9st, "
                "nyomd meg a bek\u00fcld\u00e9s gombot."
            ),
            color=LIGHT_PURPLE,
        )
        summary.add_field(name="Felhaszn\u00e1l\u00f3", value=f"@{submitter_n}", inline=False)
        summary.add_field(name="Kit\u00f6lt\u00e9si id\u0151", value=fmt_duration(elapsed_s), inline=False)
        summary.set_footer(text=f"Megv\u00e1laszolt k\u00e9rd\u00e9sek: {self.total}/{self.total}")

        submit_view = SubmitView(
            submitter_id=self.uid, role=role, total=self.total,
            author_name=submitter_n, started_at=started_at,
        )
        await channel.send(embed=summary, view=submit_view)


# ─────────────── View 4 – beküldés staffnak / lezárás ───────────────

class SubmitView(discord.ui.View):
    """Green 'Jelentkez\u00e9s bek\u00fcld\u00e9se' -> staff channel
       Red  'Jelentkez\u00e9s lez\u00e1r\u00e1sa' -> close."""

    def __init__(self, submitter_id: int, role: str, total: int,
                 author_name: str, started_at: datetime.datetime):
        super().__init__(timeout=None)
        self.submitter_id = submitter_id
        self.role         = role
        self.total        = total
        self.author_name  = author_name
        self.started_at   = started_at

        submit_btn = discord.ui.Button(label="Jelentkez\u00e9s bek\u00fcld\u00e9se", style=discord.ButtonStyle.green)
        submit_btn.callback = self._submit_to_staff
        self.add_item(submit_btn)
        self.add_item(_CloseBtn(role, "Jelentkez\u00e9s lez\u00e1r\u00e1sa"))

    async def _submit_to_staff(self, interaction: discord.Interaction) -> None:
        uid = self.submitter_id
        session = sessions.pop(uid, None)
        if not session:
            return await interaction.response.send_message(
                "A munkamenet nem tal\u00e1lhat\u00f3.", ephemeral=True
            )

        answers     = session["answers"]
        role        = self.role
        total       = self.total
        a_name      = self.author_name
        submitter_n = session["submitter_name"]
        staff_ch    = bot.get_channel(STAFF_CHANNEL_ID)

        self.stop()
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)
        await _async_save()

        qa_lines = build_qa_lines(role, answers, total)
        staff_embed = discord.Embed(
            title=f"**ChaosFFA {role} jelentkez\u00e9s**",
            description=qa_lines,
            color=LIGHT_PURPLE,
        )
        staff_embed.add_field(name="Jelentkez\u0151",    value=f"@{a_name}",       inline=True)
        staff_embed.add_field(name="Jelentkez\u00e9s t\u00edpusa", value=role, inline=True)
        staff_embed.add_field(
            name="Bek\u00fcld\u00e9s ideje",
            value=f"<t:{int(self.started_at.timestamp())}:F>",
            inline=False,
        )

        review_view = StaffReviewView(
            submitter_id=uid, submitter_name=submitter_n, role=role, total=total
        )
        staff_msg = await staff_ch.send(embed=staff_embed, view=review_view)

        review_sessions[staff_msg.id] = {
            "submitter_id":   uid,
            "submitter_name": submitter_n,
            "role":           role,
            "total":          total,
            "answers":       dict(answers),
            "dm_channel_id": session.get("dm_channel_id"),
        }

        await interaction.followup.send(
            "A jelentkez\u00e9sedet sikeresen elk\u00fcldt\u00fck a staffnak!",
            embed=discord.Embed(
                title="**Jelentkez\u00e9s bek\u00fcldve**",
                description="A staff tagok mostant\u00f3l elb\u00edr\u00e1lj\u00e1k a jelentkez\u00e9sedet.",
                color=LIGHT_GREEN,
            ),
            ephemeral=True,
        )


# ─────────────── View 5 – staff elfogad/utasit ───────────────

class StaffReviewView(discord.ui.View):
    """Elfogad\u00e1s / Elutas\u00edt\u00e1s buttons on the staff-channel embed."""

    def __init__(self, submitter_id: int, submitter_name: str,
                 role: str, total: int):
        super().__init__(timeout=None)
        self.submitter_id   = submitter_id
        self.submitter_name = submitter_name
        self.role           = role
        self.total          = total

        accept_btn = discord.ui.Button(label="Elfogad\u00e1s", style=discord.ButtonStyle.green)
        accept_btn.callback = self._accept
        self.add_item(accept_btn)

        reject_btn = discord.ui.Button(label="Elutas\u00edt\u00e1s", style=discord.ButtonStyle.red)
        reject_btn.callback = self._reject
        self.add_item(reject_btn)

    async def _accept(self, interaction: discord.Interaction) -> None:
        await self._prompt(interaction, "elfogadva", discord.Color(0x00E676))

    async def _reject(self, interaction: discord.Interaction) -> None:
        await self._prompt(interaction, "elutas\u00edtva", discord.Color(0xFF1744))

    async def _prompt(self, interaction: discord.Interaction,
                      verdict: str, color: discord.Color) -> None:
        self._staff_msg = interaction.message
        await interaction.response.send_modal(
            ReviewModal(parent=self, staff_msg=self._staff_msg,
                        verdict=verdict, verdict_color=color)
        )


# ─────────────── Modal ───────────────

class ReviewModal(discord.ui.Modal):
    """Staff types their review message, then the decision is finalised."""

    def __init__(self, parent: StaffReviewView,
                 staff_msg: discord.Message, verdict: str,
                 verdict_color: discord.Color):
        super().__init__(title=f"Jelentkez\u00e9s {verdict} \u2013 \u00fczenet \u00edr\u00e1sa")
        self._parent     = parent
        self._staff_msg  = staff_msg
        self._verdict    = verdict
        self._color      = verdict_color

        self.msg = discord.ui.TextInput(
            label="Elb\u00edr\u00e1l\u00f3 \u00fczenet",
            placeholder="\u00cdrd le az elb\u00edr\u00e1l\u00e1sod r\u00f6viden ...",
            style=discord.TextStyle.long,
            max_length=2000,
            required=False,
            default="",
        )
        self.add_item(self.msg)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        text = self.msg.value.strip() or "Nincs megadva."
        reviewer_name = str(interaction.user)

        # 1. edit the staff embed
        review = review_sessions.get(self._staff_msg.id, {})
        role = review.get("role", "?")
        await interaction.response.edit_message(
            embed=discord.Embed(
                title=f"**ChaosFFA {role} jelentkez\u00e9s {self._verdict}**",
                description=f"**Elb\u00edr\u00e1l\u00f3:** {reviewer_name}",
                color=self._color,
            ),
            view=self._parent,
        )

        # 2. DM the applicant
        try:
            dm_cid = review.get("dm_channel_id")
            applic_uid = review.get("submitter_id")
            if not dm_cid or not applic_uid:
                return
            dm_ch = bot.get_channel(dm_cid)
            if not dm_ch:
                user = await bot.fetch_user(applic_uid)
                dm_ch = await user.create_dm()
            desc = (
                f"A jelentkez\u00e9sedet {reviewer_name} b\u00edr\u00e1lta el.\n\n"
                f"**Elb\u00edr\u00e1l\u00f3 \u00fczenete:**\n{text}"
            )
            if self._verdict == "elfogadva":
                desc += (
                    "\n\nA jelentkez\u00e9sed elfogad\u00e1sra ker\u00fclt.\n\n"
                    "K\u00f6sz\u00f6nj\u00fck hogy kit\u00f6lt\u00f6tt\u00e9d! "
                    "K\u00e9rj\u00fclk a hibajegyben v\u00e1lassz ki egy id\u0151pontot a sz\u00f3beli meghallgat\u00e1sra."
                )
            await dm_ch.send(
                embed=discord.Embed(
                    title=f"**ChaosFFA {role} jelentkez\u00e9s {self._verdict}**",
                    description=desc,
                    color=self._color,
                )
            )
        except Exception:
            pass


# ─────────────── Bot ───────────────

intents = discord.Intents.none()
intents.guilds         = True   # guild presence for / commands
intents.guild_messages = True   # ephemeral acks, guild context
intents.dm_messages    = True   # DM answers
intents.message_content = True  # DM message bodies

bot = commands.Bot(command_prefix="!", intents=intents)

_PRIV = {i for i, v in bot.intents if v and i not in
         {"guilds", "guild_messages", "dm_messages", "message_content"}}
if _PRIV:
    print(f"[BOOT] Unexpected privileged intents on: {sorted(_PRIV)}")
else:
    print("[BOOT] Intents OK")
print("[BOOT] In use:", sorted(i for i, v in bot.intents if v))


# ─── on_ready ───────────────────────────────────────────────────

@bot.event
async def on_ready():
    # restore persisted sessions
    globals()["sessions"].update(await _load_sessions())
    print(f"[STORE] Loaded {len(sessions)} persisted sessions")

    # slash-command sync
    try:
        if GUILD_ID:
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            scope = f"guild {GUILD_ID}"
        else:
            synced = await bot.tree.sync()
            scope = "global"
        print(f"Logged in as {bot.user} | synced {len(synced)} slash commands ({scope})")

        if not synced:
            invite = (
                f"https://discord.com/api/oauth2/authorize"
                f"?client_id={bot.user.id}"
                f"&scope=bot+applications.commands"
                f"&permissions=0"
            )
            print(f"[INVITE] 0 cmds synced \u2013 re-invite:")
            print(f"[INVITE] {invite}")
    except Exception as e:
        print(f"Sync error: [{type(e).__name__}] {e}")
        import traceback; traceback.print_exc()

    # per-guild sync with diagnostics
    if bot.guilds:
        for g in bot.guilds:
            try:
                r = await bot.tree.sync(guild=discord.Object(id=g.id))
                print(f"  [SYNC] {g.name} ({g.id}): {len(r)} commands")
            except Exception as exc:
                print(f"  [SYNC] {g.name} ({g.id}): FAILED {exc}")
    else:
        print("[SYNC] Bot is in 0 guilds")

    # status
    st = os.getenv("STATUS_TEXT", "ChaosFFA")
    ty = os.getenv("STATUS_TYPE", "online").lower()
    _SM = {"online": discord.Status.online, "idle": discord.Status.idle,
           "dnd": discord.Status.do_not_disturb, "invisible": discord.Status.offline}
    await bot.change_presence(status=_SM.get(ty, discord.Status.online),
                              activity=discord.CustomActivity(name=st))
    print(f"[STATUS] {ty} | {st}")


# ─── slash command ──────────────────────────────────────────────

@bot.tree.command(name="sendtgf",
                  description="ChaosFFA jelentkez\u00e9si k\u00e9rd\u0151\u00edvet k\u00fcld egy felhaszn\u00e1l\u00f3nak DM-ben.")
@app_commands.describe(
    username="A c\u00e9l Discord felhaszn\u00e1l\u00f3 (mention, felhaszn\u00e1l\u00f3n\u00e9v vagy ID)",
    type_="A jelentkez\u00e9s t\u00edpusa",
)
@app_commands.choices(type_=[
    app_commands.Choice(name="Helper",       value="Helper"),
    app_commands.Choice(name="Moder\u00e1tor",value="Moder\u00e1tor"),
    app_commands.Choice(name="Fejleszt\u0151",value="Fejleszt\u0151"),
    app_commands.Choice(name="Admin",        value="Admin"),
])
@app_commands.checks.has_permissions(administrator=True)
async def sendtgf(interaction: discord.Interaction,
                  username: str, type_: app_commands.Choice[str]):
    role   = type_.value

    def _uid(s: str) -> int | None:
        d = s.strip("<@!> ").strip()
        return int(d) if d.isdigit() else None

    target_id = _uid(username)

    # REST fetch — bypasses empty member cache (no privileged intent needed)
    member: discord.Member | None = None
    if target_id:
        try:
            member = await interaction.guild.fetch_member(target_id)
        except discord.NotFound:
            pass

    if member is None:
        try:
            guild = interaction.guild or await bot.fetch_guild(GUILD_ID) if GUILD_ID else None
            if guild:
                for m in guild.members:
                    if m.name.lower() == username.lower():
                        member = m
                        break
        except Exception:
            pass

    if member is None:
        return await interaction.response.send_message(
            f"Nem tal\u00e1lhat\u00f3 felhaszn\u00e1l\u00f3 a szerveren: `{username}`",
            ephemeral=True,
        )

    embed = discord.Embed(
        title=f"**ChaosFFA {role} jelentkez\u00e9s**",
        description=(
            "Ha szeretn\u00e9d elkezdeni a jelentkez\u00e9st, nyomd meg az ind\u00edt\u00e1s gombot.\n\n"
            "A kit\u00f6lt\u00e9sre 60 perced lesz. A k\u00e9rd\u00e9sekre DM-ben, egyes\u00e9vel kell v\u00e1laszolnod. "
            "Ha megszak\u00edtod vagy lej\u00e1r az id\u0151, a jelentkez\u00e9s nem ker\u00fcl bek\u00fcld\u00e9sre."
        ),
        color=LIGHT_RED,
    )

    view = StartView(role)

    try:
        dm_channel = await member.create_dm()
        await dm_channel.send(embed=embed, view=view)
    except discord.Forbidden:
        return await interaction.response.send_message(
            f"Nem siker\u00fclt DM-ben \u00fczenetet k\u00fcldeni {member.mention}-nak: a DM-ek le vannak z\u00e1rva.",
            ephemeral=True,
        )

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
        "view":           None,
        "review_msg_id":  None,
    }
    await _async_save()

    await interaction.response.send_message(
        f"Jelentkez\u00e9si k\u00e9rd\u0151\u00edv elk\u00fcldve {member.mention} felhaszn\u00e1l\u00f3nak ({role}).",
        ephemeral=True,
    )


# ─── DM answer handler ──────────────────────────────────────────

@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)

    if not isinstance(message.channel, discord.DMChannel) or message.author.bot:
        return

    uid = message.author.id
    session = sessions.get(uid)
    if not session:
        return

    if session.get("step") is None:
        return

    deadline = session.get("deadline")
    if deadline and _now_utc() > _dt(deadline):
        sessions.pop(uid, None)
        await _async_save()
        return await message.channel.send(
            "⏰ A jelentkez\u00e9si id\u0151 **lej\u00e1rt**! A jelentkez\u00e9s nem ker\u00fcl bek\u00fcld\u00e9sre."
        )

    role       = session["type"]
    questions  = QUESTIONS[role]
    total      = session["total"] = len(questions)
    step       = session["step"]

    session["answers"][step] = message.content.strip()
    step += 1
    session["step"] = step
    await _async_save()

    if step >= total:
        started_at = session.get("started_at") or _now_utc()
        now        = _now_utc()
        elapsed_s  = int((now - started_at).total_seconds())
        sessions.pop(uid, None)
        await _async_save()

        embed = discord.Embed(
            title=f"**ChaosFFA {role} jelentkez\u00e9s**",
            description=(
                "Sikeresen megv\u00e1laszoltad az \u00f6sszes k\u00e9rd\u00e9st.\n\n"
                "Ha biztos vagy benne, hogy bek\u00fcld\u00f6d a jelentkez\u00e9st, "
                "nyomd meg a bek\u00fcld\u00e9s gombot."
            ),
            color=LIGHT_PURPLE,
        )
        embed.add_field(name="Felhaszn\u00e1l\u00f3",
                        value=f"@{message.author.display_name}", inline=False)
        embed.add_field(name="Kit\u00f6lt\u00e9si id\u0151", value=fmt_duration(elapsed_s), inline=False)
        embed.set_footer(text=f"Megv\u00e1laszolt k\u00e9rd\u00e9sek: {total}/{total}")

        view = SubmitViewConfirmation(uid=uid, role=role, total=total,
                                      started_at=started_at)
        await message.channel.send(embed=embed, view=view)
        return

    q_num = step
    q_embed = discord.Embed(
        title=f"**ChaosFFA {role} jelentkez\u00e9s \u2013 {q_num}. k\u00e9rd\u00e9s**",
        description=questions[step],
        color=LIGHT_PURPLE,
    )
    q_embed.set_footer(
        text=f"V\u00e1laszk\u00e9nt k\u00fcldj egy DM \u00fczenetet a botnak.\n"
             f"Lej\u00e1rat: 7 napja\n{q_num}/{total} k\u00e9rd\u00e9s"
    )
    await message.channel.send(embed=q_embed)


# ─────────────── entry-point ───────────────

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN nincs be\u00e1ll\u00edtva a .env f\u00e1jlban!"
        )
    bot.run(token)
