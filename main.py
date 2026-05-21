import os
import datetime
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

# ─────────────── colours / constants ───────────────
LIGHT_RED    = discord.Color(0xFF5555)
LIGHT_PURPLE = discord.Color(0xBB86FC)
LIGHT_GREEN  = discord.Color(0x00E676)

STAFF_CHANNEL_ID  = 1507023523674193962
GUILD_ID          = int(os.getenv("GUILD_ID", "0"))   # 0 = global sync
TIME_LIMIT_MINUTES = 60

# ─────────────── questions ───────────────
QUESTIONS: dict[str, list[str]] = {
    "Helper": [
        "Mi a Minecraft felhasználóneved és hány éves vagy?",
        "Mióta játszol Minecrafttal?",
        "Voltál már más szerveren Helper vagy Staff tag? Ha igen, hol és milyen pozícióban?",
        "Miért szeretnél Helper lenni ezen a szerveren?",
        "Mit gondolsz, mi egy jó Helper legfontosabb feladata?",
        "Hogyan kezelnél egy toxikus vagy szabályszegő játékost?",
        "Mit tennél, ha két játékos vitatkozna egymással a chaten?",
        "Mennyi időt tudsz átlagosan a szerveren tölteni naponta?",
        "Ismered a szerver szabályait, és be tudod tartatni őket?",
        "Hogyan segítenél egy új játékosnak, aki nem ismeri a szervert?",
        "Mit csinálnál, ha egy barátod megszegné a szabályokat?",
        "Mennyire tudsz csapatban együtt dolgozni más Staff tagokkal?",
        "Voltál már büntetve szerveren? Ha igen, miért?",
        "Hogyan reagálnál arra, ha valaki sértegetne téged Staffként?",
        "Miért téged válasszunk Helpernek más jelentkezők helyett?",
    ],
    "Moderátor": [
        "Mi a Minecraft neved és hány éves vagy?",
        "Mióta játszol Minecrafttal, és mióta vagy aktív multiplayer szervereken?",
        "Voltál már Moderátor vagy más Staff pozícióban? Ha igen, melyik szerveren és mennyi ideig?",
        "Miért szeretnél Moderátor lenni ezen a szerveren?",
        "Mit gondolsz, mi a Moderátor legfontosabb feladata?",
        "Hogyan kezelnél egy játékost, aki folyamatosan megszegi a szabályokat?",
        "Mit tennél, ha egy játékos csalással (hack, cheat) lenne gyanús?",
        "Hogyan reagálnál egy nagyobb chatvitára vagy toxikus viselkedésre?",
        "Mit csinálnál, ha egy másik Staff tag hibázna vagy szabálytalanul járna el?",
        "Mennyire tudsz nyugodt maradni stresszes helyzetekben?",
        "Mennyi időt tudsz naponta vagy hetente a szerveren tölteni?",
        "Mennyire ismered a szerver szabályzatát és büntetési rendszerét?",
        "Mit tennél, ha a barátod szabályt sértene a szerveren?",
        "Hogyan segítenéd a Helper csapat munkáját Moderátorként?",
        "Miért téged válasszunk Moderátornak a többi jelentkező helyett?",
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
        "Van olyen projekted vagy munkád, amire különösen büszke vagy?",
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

# ─────────────── in-memory stores ───────────────
#
# sessions[dm_user_id] = {
#   "submitter":     int,            # who asked / sent the invitation
#   "submitter_name":str,            # display name of the person filling the form
#   "type":          str,            # Helper / Moderátor / Fejlesztő / Admin
#   "channel":       DMChannel,
#   "answers":       {int: str},
#   "total":         int,
#   "started_at":    datetime,
#   "view":          SubmitViewConfirmation | None,
#   "review_msg_id": int | None,     # set after submitting to staff channel
# }
#
# review_sessions[staff_channel_msg_id] = {
#   "data": same as a fresh sessions[submitter_id] entry (captured at submit time)
# }
sessions:       dict[int, dict] = {}
review_sessions: dict[int, dict] = {}


# ─────────────── helpers ───────────────
def deadline_from_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=TIME_LIMIT_MINUTES)


def fmt_deadline(dt: datetime.datetime) -> str:
    return f"<t:{int(dt.timestamp())}:R>"


def fmt_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    if m:
        return f"{m} perc {s} másodperc"
    return f"{s} másodperc"


def build_qa_lines(role: str, answers: dict[int, str], total: int) -> str:
    lines = []
    for i in range(total):
        q = QUESTIONS[role][i]
        a = answers.get(i, "*– nincs válasz –*")
        lines.append(f"**{i+1}.** *{q}*\n**V:** {a}")
    return "\n\n".join(lines)


# ─────────────── Buttons ───────────────

class _CloseBtn(discord.ui.Button):
    """Reusable red cancel/close button tied to a role."""

    def __init__(self, role: str, label: str):
        super().__init__(label=label, style=discord.ButtonStyle.red)
        self.role = role

    async def callback(self, interaction: discord.Interaction) -> None:
        sessions.pop(interaction.user.id, None)
        if self.view:
            self.view.stop()
        for c in (self.view.children if self.view else []):
            c.disabled = True
        await interaction.response.edit_message(view=self.view)


# ─────────────── View 1 – initial embed ───────────────

class StartView(discord.ui.View):
    """Green 'Jelentkezés indítása' + red 'Mégsem' on the initial embed."""

    def __init__(self, role: str):
        super().__init__(timeout=None)
        self.role = role

        green = discord.ui.Button(
            label="Jelentkezés indítása", style=discord.ButtonStyle.green
        )
        green.callback = self._start
        self.add_item(green)
        self.add_item(_CloseBtn(role, "Mégsem"))

    async def _start(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        if uid not in sessions:
            return await interaction.response.send_message(
                "A munkamenet lejárt vagy nem található.", ephemeral=True
            )
        session = sessions[uid]
        role = session["type"]
        deadline = deadline_from_now()

        await interaction.response.edit_message(
            embed=discord.Embed(
                title="**Jelentkezés elindítva**",
                description=(
                    f"Sikeresen elindítottad a ChaosFFA {role} jelentkezést.\n"
                    f"Határidő: {fmt_deadline(deadline)}"
                ),
                color=LIGHT_PURPLE,
            ),
            view=None,
        )

        session["deadline"]  = deadline
        session["started_at"] = datetime.datetime.now(datetime.timezone.utc)
        session["step"]      = 0
        session["answers"]   = {}

        questions = QUESTIONS[role]
        total     = len(questions)
        q_view    = QuestionView(role, total)
        session["view"] = q_view

        q_embed = discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés – 1. kérdés**",
            description=questions[0],
            color=LIGHT_PURPLE,
        )
        q_embed.set_footer(
            text=f"Válaszként küldj egy DM üzenetet a botnak.\nLejárat: 7 napja\n1/{total} kérdés"
        )
        await session["channel"].send(embed=q_embed, view=q_view)


# ─────────────── View 2 – per question embed ───────────────

class QuestionView(discord.ui.View):
    """Red 'Jelentkezés lezárása' button shown under every question."""

    def __init__(self, role: str, total: int):
        super().__init__(timeout=None)
        self.role  = role
        self.total = total
        self.add_item(
            discord.ui.Button(
                label="Jelentkezés lezárása", style=discord.ButtonStyle.red            )
        )
        for child in self.children:
            child.callback = self._close  # type: ignore[assignment]

    async def _close(self, interaction: discord.Interaction) -> None:
        sessions.pop(interaction.user.id, None)
        self.stop()
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(
            embed=discord.Embed(
                title="**Jelentkezés megszakítva**",
                description=f"Sikeresen megszakítottad a ChaosFFA {self.role} jelentkezést!",
                color=LIGHT_RED,
            )
        )


# ─────────────── View 3 – "jóváhagyod / mégsem" confirmation ───────────────

class SubmitViewConfirmation(discord.ui.View):
    """Shown after ALL questions answered – 'Beküldése' green / 'Mégsem' red."""

    def __init__(self, uid: int, role: str, total: int,
                 started_at: datetime.datetime):
        super().__init__(timeout=None)
        self.uid        = uid
        self.role       = role
        self.total      = total
        self.started_at = started_at

        submit_btn = discord.ui.Button(
            label="Jelentkezés beküldése", style=discord.ButtonStyle.green
        )
        submit_btn.callback = self._submit
        self.add_item(submit_btn)
        self.add_item(_CloseBtn(role, "Mégsem"))

    async def _submit(self, interaction: discord.Interaction) -> None:
        uid = interaction.user.id
        session = sessions.get(uid)
        if not session:
            return await interaction.response.send_message(
                "A munkamenet nem található.", ephemeral=True
            )

        role        = session["type"]
        answers     = session["answers"]
        channel     = session["channel"]
        submitter_n = session["submitter_name"]
        started_at  = session["started_at"]

        now       = datetime.datetime.now(datetime.timezone.utc)
        elapsed_s = int((now - started_at).total_seconds())

        # ── disable buttons on this embed ──
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)

        # ── build DM summary embed ──
        summary = discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés**",
            description=(
                "Sikeresen megválaszoltad az összes kérdést.\n\n"
                "Ha biztos vagy benne, hogy beküldöd a jelentkezést, "
                "nyomd meg a beküldés gombot."
            ),
            color=LIGHT_PURPLE,
        )
        summary.add_field(name="Felhasználó", value=f"@{submitter_n}", inline=False)
        summary.add_field(name="Kitöltési idő", value=fmt_duration(elapsed_s), inline=False)
        summary.set_footer(
            text=f"Megválaszolt kérdések: {self.total}/{self.total}"
        )

        submit_view = SubmitView(
            submitter_id=self.uid,                  # used for button routing
            role=role,
            total=self.total,
            author_name=submitter_n,
            started_at=started_at,
        )
        await channel.send(embed=summary, view=submit_view)


# ─────────────── View 4 – submit-to-staff / close ───────────────

class SubmitView(discord.ui.View):
    """Green 'Jelentkezés beküldése' → staff channel
       Red  'Jelentkezés lezárása'   → just close."""

    def __init__(self, submitter_id: int, role: str, total: int,
                 author_name: str, started_at: datetime.datetime):
        super().__init__(timeout=None)
        self.submitter_id  = submitter_id
        self.role          = role
        self.total         = total
        self.author_name   = author_name
        self.started_at    = started_at

        submit_btn = discord.ui.Button(
            label="Jelentkezés beküldése", style=discord.ButtonStyle.green
        )
        submit_btn.callback = self._submit_to_staff
        self.add_item(submit_btn)
        self.add_item(_CloseBtn(role, "Jelentkezés lezárása"))

    async def _submit_to_staff(self, interaction: discord.Interaction) -> None:
        uid = self.submitter_id
        session = sessions.pop(uid, None)
        if not session:
            return await interaction.response.send_message(
                "A munkamenet nem található.", ephemeral=True
            )

        answers     = session["answers"]
        role        = self.role
        total       = self.total
        a_name      = self.author_name
        submitter_n = session["submitter_name"]
        staff_ch    = bot.get_channel(STAFF_CHANNEL_ID)

        # ── disable buttons ──
        self.stop()
        for c in self.children:
            c.disabled = True
        await interaction.response.edit_message(view=self)

        # ── build staff embed ──
        qa_lines = build_qa_lines(role, answers, total)
        staff_embed = discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés**",
            description=qa_lines,
            color=LIGHT_PURPLE,
        )
        staff_embed.add_field(name="Jelentkező",    value=f"@{a_name}",       inline=True)
        staff_embed.add_field(name="Jelentkezés típusa", value=role,            inline=True)
        staff_embed.add_field(
            name="Beküldés ideje",
            value=f"<t:{int(self.started_at.timestamp())}:F>",
            inline=False,
        )

        review_view = StaffReviewView(
            submitter_id=uid, submitter_name=submitter_n, role=role, total=total
        )
        staff_msg = await staff_ch.send(embed=staff_embed, view=review_view)

        # remember which applicant this staff-message belongs to
        review_sessions[staff_msg.id] = {
            "submitter_id":   uid,
            "submitter_name": submitter_n,
            "role":           role,
            "total":          total,
            "answers":       dict(answers),
            "dm_channel_id": session["channel"].id,
        }

        # ── ephemeral ack ──
        await interaction.followup.send(
            "A jelentkezésedet sikeresen elküldtük a staffnak!",
            embed=discord.Embed(
                title="**Jelentkezés beküldve**",
                description="A staff tagok mostantól elbírálják a jelentkezésedet.",
                color=LIGHT_GREEN,
            ),
            ephemeral=True,
        )


# ─────────────── View 5 – staff accept / reject ───────────────

class StaffReviewView(discord.ui.View):
    """Elfogadás / Elutasítás buttons on the staff-channel embed."""

    def __init__(self, submitter_id: int, submitter_name: str,
                 role: str, total: int):
        super().__init__(timeout=None)
        self.submitter_id   = submitter_id
        self.submitter_name = submitter_name
        self.role           = role
        self.total          = total

        accept_btn = discord.ui.Button(
            label="Elfogadás", style=discord.ButtonStyle.green
        )
        accept_btn.callback = self._accept
        self.add_item(accept_btn)

        reject_btn = discord.ui.Button(
            label="Elutasítás", style=discord.ButtonStyle.red
        )
        reject_btn.callback = self._reject
        self.add_item(reject_btn)

    async def _accept(self, interaction: discord.Interaction) -> None:
        await self._prompt(interaction, "elfogadva", discord.Color(0x00E676))

    async def _reject(self, interaction: discord.Interaction) -> None:
        await self._prompt(interaction, "elutasítva", discord.Color(0xFF1744))

    async def _prompt(
        self,
        interaction: discord.Interaction,
        verdict:    str,
        color:      discord.Color,
    ) -> None:
        """Send the review message modal to the staff member.
        Store the message reference so the modal can disable buttons later."""
        self._staff_msg = interaction.message  # type: ignore[attr-defined]
        await interaction.response.send_modal(
            ReviewModal(
                parent=self,
                staff_msg=self._staff_msg,      # type: ignore[attr-defined]
                verdict=verdict,
                verdict_color=color,
            )
        )


# ─────────────── Modal ───────────────

class ReviewModal(discord.ui.Modal):
    """Staff types their review message, then the decision is finalised."""

    def __init__(self, parent: StaffReviewView,
                 staff_msg: discord.Message,
                 verdict: str, verdict_color: discord.Color):
        super().__init__(title=f"Jelentkezés {verdict} – üzenet írása")
        self._parent     = parent
        self._staff_msg  = staff_msg
        self._verdict    = verdict
        self._color      = verdict_color

        self.message_input = discord.ui.TextInput(
            label="Elbíráló üzenet",
            placeholder="Írd le az elbírálásod röviden ...",
            style=discord.TextStyle.long,
            max_length=2000,
            required=False,
            default="",
        )
        self.add_item(self.message_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self._parent._staff_msg.edit(
            embed=self._build_final_embed(interaction),
            view=self._parent,         # buttons come back already disabled
        )

        # ── 2. DM the applicant ──
        try:
            review = review_sessions.get(self._staff_msg.id)
            if review:
                dm_ch = interaction.client.get_channel(review["dm_channel_id"])
                if dm_ch is None:
                    raise ValueError("channel gone")
                await dm_ch.send(
                    embed=discord.Embed(
                        title=f"**ChaosFFA {review['role']} jelentkezés {self._verdict}**",
                        description=self._build_dm_description(interaction),
                        color=self._color,
                    )
                )
        except Exception:
            pass

    def _build_final_embed(self, interaction: discord.Interaction) -> discord.Embed:
        reviewer_name = str(interaction.user)
        review = review_sessions.get(self._staff_msg.id, {})
        role = review.get("role", "?")
        return discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés {self._verdict}**",
            description=f"**Elbíráló:** {reviewer_name}",
            color=self._color,
        )

    def _build_dm_description(self, interaction: discord.Interaction) -> str:
        reviewer_name = str(interaction.user)
        msg_text      = self.message_input.value.strip() or "Nincs megadva."
        desc = (
            f"A jelentkezésedet {reviewer_name} bírálta el.\n\n"
            f"**Elbíráló üzenete:**\n{msg_text}"
        )
        if self._verdict == "elfogadva":
            desc += (
                "\n\nA jelentkezésed elfogadásra került.\n\n"
                "Köszönjük hogy kitöltötted! "
                "Kérlek a hibajegyben válassz ki egy időpontot a szóbeli meghallgatásra."
            )
        return desc


# ─────────────── Bot ───────────────

intents = discord.Intents.none()
intents.guilds            = True   # slash commands need guild presence
intents.guild_messages    = True   # ephemeral ack, slash command context
intents.dm_messages       = True   # read DM answers from applicants
intents.message_content   = True   # read DM message bodies

bot = commands.Bot(command_prefix="!", intents=intents)

# ─── diagnostics ───────────────────────────────────────────
_PRIVLEGED = [i for i, v in bot.intents if v and i not in (
    "guilds", "guild_messages", "dm_messages", "message_content"
)]
if _PRIVLEGED:
    print(f"[BOOT] Unnecessary privileged intents enabled: {_PRIVLEGED}")
else:
    print("[BOOT] All intents OK — no privileged gateway warnings")

def _intents_in_use() -> list[str]:
    return [i for i, v in bot.intents if v]

def _intents_missing() -> list[str]:
    # Discord flags these as privileged if not explicitly toggled in portal
    _PRIV = {"message_content"}
    return [i for i in _PRIV if i in {i for i, v in bot.intents if v}]

print(f"[BOOT] Intents in use: {_intents_in_use()}")
print(f"[BOOT] Intents missing portal approval: {_intents_missing()}")


@bot.event
async def on_ready():
    try:
        if GUILD_ID:
            synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
            scope = f"guild {GUILD_ID}"
        else:
            synced = await bot.tree.sync()
            scope = "global"
        print(f"Logged in as {bot.user} | synced {len(synced)} slash commands ({scope})")

        # Print re-invite link if bot lacks applications.commands scope
        if not synced:
            invite = (
                f"https://discord.com/oauth2/authorize"
                f"?client_id={bot.user.id}"
                f"&scope=bot+applications.commands"
                f"&permissions=0"
            )
            print(f"[INVITE] 0 commands synced — re-invite with applications.commands scope:")
            print(f"[INVITE] {invite}")
    except Exception as e:
        print(f"Sync error: [{type(e).__name__}] {e}")
        import traceback; traceback.print_exc()

    # ── Status ──────────────────────────────────────────────
    status_text = os.getenv("STATUS_TEXT", "ChaosFFA")
    status_type = os.getenv("STATUS_TYPE", "online").lower()
    _STATUS_MAP = {
        "online":   discord.Status.online,
        "idle":     discord.Status.idle,
        "dnd":      discord.Status.do_not_disturb,
        "invisible":discord.Status.offline,
    }
    activity = discord.CustomActivity(name=status_text)
    await bot.change_presence(status=_STATUS_MAP.get(status_type, discord.Status.online), activity=activity)
    print(f"[STATUS] {status_type} | {status_text}")

    # ── Per-guild instant sync to every guild the bot is already in ──
    if bot.guilds:
        ok = fail = 0
        for g in bot.guilds:
            try:
                r = await bot.tree.sync(guild=discord.Object(id=g.id))
                ok += 1
                print(f"  [SYNC] guild {g.name} ({g.id}): {len(r)} commands")
            except Exception as exc:
                fail += 1
                print(f"  [SYNC] guild {g.name} ({g.id}): FAILED {exc}")
        print(f"[SYNC] Guilds done: {ok} ok, {fail} failed")
    else:
        print("[SYNC] Bot is in 0 guilds — cannot sync any commands")

    # ── Print re-invite URL if the bot was added without applications.commands scope ──
    total_synced = len(await bot.tree.fetch_commands())
    if not total_synced:
        invite = (
            f"https://discord.com/api/oauth2/authorize"
            f"?client_id={bot.user.id}"
            f"&scope=bot+applications.commands"
            f"&permissions=0"
        )
        print(f"[INVITE] 0 commands available — re-invite the bot:")
        print(f"[INVITE] {invite}")



# ─── Slash command ───────────────────────────────────────────────

@bot.tree.command(
    name="sendtgf",
    description="ChaosFFA jelentkezési kérdőívet küld egy felhasználónak DM-ben.",
)
@app_commands.describe(
    username="A cél Discord felhasználó (mention, felhasználónév vagy ID)",
    type_="A jelentkezés típusa",
)
@app_commands.choices(type_=[
    app_commands.Choice(name="Helper",    value="Helper"),
    app_commands.Choice(name="Moderátor", value="Moderátor"),
    app_commands.Choice(name="Fejlesztő", value="Fejlesztő"),
    app_commands.Choice(name="Admin",     value="Admin"),
])
@app_commands.checks.has_permissions(administrator=True)
async def sendtgf(
    interaction: discord.Interaction,
    username: str,
    type_: app_commands.Choice[str],
):
    role = type_.value
    member: discord.Member | None = None

    def _extract_id(raw: str) -> int | None:
        clean = raw.strip("<@!> ")
        return int(clean) if clean.isdigit() else None

    # ① Try mention / raw numeric ID → REST fetch_user (always works, no cache / intent needed)
    target_id = _extract_id(username)
    if not target_id:
        target_id = _extract_id(username.strip())

    candidate_user: discord.User | None = None
    if target_id:
        try:
            candidate_user = await bot.fetch_user(target_id)
        except discord.NotFound:
            candidate_user = None

    if candidate_user and interaction.guild:
        # Convert the User → Member (REST, not cache)
        try:
            member = await interaction.guild.fetch_member(candidate_user.id)
        except discord.NotFound:
            member = None

    # ② Fall back: scan guild.members via cache
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
        name_part = f" (`{username}`)"
        return await interaction.response.send_message(
            f"Nem található felhasználó a szerveren{name_part}.",
            ephemeral=True,
        )

    # ── Build initial embed ──
    embed = discord.Embed(
        title=f"**ChaosFFA {role} jelentkezés**",
        description=(
            "Ha szeretnéd elkezdeni a jelentkezést, nyomd meg az indítás gombot.\n\n"
            "A kitöltésre 60 perced lesz. A kérdésekre DM-ben, egyesével kell válaszolnod. "
            "Ha megszakítod vagy lejár az idő, a jelentkezés nem kerül beküldésre."
        ),
        color=LIGHT_RED,
    )

    view = StartView(role)

    try:
        dm_channel = await member.create_dm()
        await dm_channel.send(embed=embed, view=view)
    except discord.Forbidden:
        return await interaction.response.send_message(
            f"Nem sikerült DM-ben üzenetet küldeni {member.mention}-nak: "
            "a DM-ek le vannak zárva.",
            ephemeral=True,
        )

    # ── Save session ──
    sessions[member.id] = {
        "submitter":     interaction.user.id,
        "submitter_name": member.display_name,
        "type":          role,
        "channel":       dm_channel,
        "step":          None,
        "answers":       {},
        "total":         None,
        "started_at":    None,
        "view":          view,
        "review_msg_id": None,
    }

    await interaction.response.send_message(
        f"Jelentkezési kérdőív elküldve {member.mention} felhasználónak ({role}).",
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

    # guard: session not yet started
    if session.get("step") is None or session.get("channel") is None:
        return

    # deadline check
    deadline = session.get("deadline")
    if deadline and datetime.datetime.now(datetime.timezone.utc) > deadline:
        sessions.pop(uid, None)
        if session.get("view"):
            session["view"].stop()
        return await message.channel.send(
            "⏰ A jelentkezési idő **lejárt**! A jelentkezés nem került beküldésre."
        )

    role    = session["type"]
    questions = QUESTIONS[role]
    total   = session["total"] = len(questions)
    step    = session["step"]          # current question index (0-based)

    # ── Save this answer ──
    session["answers"][step] = message.content.strip()
    step += 1
    session["step"] = step

    if step >= total:
        # ─── All questions answered ───
        # capture stuff before popping
        started_at = session.get("started_at") or datetime.datetime.now(datetime.timezone.utc)
        channel    = session["channel"]

        # remove from active sessions; nothing more to track here
        sessions.pop(uid, None)

        now       = datetime.datetime.now(datetime.timezone.utc)
        elapsed_s = int((now - started_at).total_seconds())

        # confirmation embed
        embed = discord.Embed(
            title=f"**ChaosFFA {role} jelentkezés**",
            description=(
                "Sikeresen megválaszoltad az összes kérdést.\n\n"
                "Ha biztos vagy benne, hogy beküldöd a jelentkezést, "
                "nyomd meg a beküldés gombot."
            ),
            color=LIGHT_PURPLE,
        )
        embed.add_field(
            name="Felhasználó", value=f"@{message.author.display_name}", inline=False
        )
        embed.add_field(
            name="Kitöltési idő", value=fmt_duration(elapsed_s), inline=False
        )
        embed.set_footer(text=f"Megválaszolt kérdések: {total}/{total}")

        confirm_view = SubmitViewConfirmation(
            uid=uid, role=role, total=total, started_at=started_at
        )
        await channel.send(embed=embed, view=confirm_view)
        return

    # ─── Next question ──
    q_num = step          # 1-based
    embed = discord.Embed(
        title=f"**ChaosFFA {role} jelentkezés – {q_num}. kérdés**",
        description=questions[step],
        color=LIGHT_PURPLE,
    )
    embed.set_footer(
        text=f"Válaszként küldj egy DM üzenetet a botnak.\n"
             f"Lejárat: 7 napja\n{q_num}/{total} kérdés"
    )
    await message.channel.send(embed=embed)


# ─────────────── entry-point ───────────────

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "DISCORD_BOT_TOKEN nincs beállítva a .env fájlban!"
        )
    bot.run(token)
