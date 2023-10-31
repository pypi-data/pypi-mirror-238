import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram import Client, filters
from pyrogram.types import Message

from Bdrl.config import BRANCH, HEROKU_API_KEY, HEROKU_APP_NAME
from Bdrl.helpers.adminHelpers import DEVS
from Bdrl.helpers.basic import edit_or_reply
from Bdrl.helpers.misc import token, url
from Bdrl.helpers.tools import get_arg
from Bdrl.utils import *

if token:
    GIT_USERNAME = url.split("com/")[1].split("/")[0]
    TEMP_REPO = url.split("https://")[1]
    UPSTREAM_REPO = f"https://{GIT_USERNAME}:{token}@{TEMP_REPO}"
    UPSTREAM_REPO_URL = UPSTREAM_REPO
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"• [{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n"
        )
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@Client.on_message(filters.command("cupdate", ["."]) & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command("update", prefix) & filters.me)
async def upstream(client: Client, message: Message):
    status = await edit_or_reply(message, "`Checking for Updates, Wait a Moment...`")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    try:
        txt = (
            "**Update Cannot Continue Because "
            + "Some ERROR Happened**\n\n**LOGTRACE:**\n"
        )
        repo = Repo()
    except NoSuchPathError as error:
        await status.edit(f"{txt}\n**Directory** `{error}` **Can not be found.**")
        repo.__del__()
        return
    except GitCommandError as error:
        await status.edit(f"{txt}\n**Early failure!** `{error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head(
            BRANCH,
            origin.refs[BRANCH],
        )
        repo.heads[BRANCH].set_tracking_branch(origin.refs[BRANCH])
        repo.heads[BRANCH].checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != BRANCH:
        await status.edit(
            f"**[UPDATER]:** `Looks like you are using your own custom branch ({ac_br}). in that case, Updater is unable to identify which branch is to be merged. please checkout to main branch`"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if "now" not in conf:
        if changelog:
            changelog_str = f"**Update Available For Branch [{ac_br}]:\n\nCHANGELOG:**\n\n`{changelog}`"
            if len(changelog_str) > 4096:
                await status.edit("**Changelog too big, sent as file.**")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await client.send_document(
                    message.chat.id,
                    "output.txt",
                    caption=f"**Type** `{prefix}update now` **To Update Userbot.**",
                )
                remove("output.txt")
            else:
                return await status.edit(
                    f"{changelog_str}\n**Type** `{prefix}update now` **To Update Userbot.**"
                )
        else:
            await status.edit(
                f"`Your BOT is`  **up-to-date**  `with branch`  [**{ac_br}**]",
                disable_web_page_preview=True,
            )
            repo.__del__()
            return
    if HEROKU_API_KEY is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await status.edit(
                "`Please set up the HEROKU_APP_NAME variable to be able to update userbot.`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await status.edit(
                f"{txt}\n`Invalid Heroku credentials for updating userbot dyno.`"
            )
            repo.__del__()
            return
        await status.edit("`[HEROKU]: Update In Progress...`")
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/main", force=True)
        except GitCommandError:
            pass
        await status.edit("`Userbot Updated Successfully! Userbot can be used again.`")
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await status.edit(
            "`Userbot Updated Successfully! Userbot can be used again.`",
        )
        args = [sys.executable, "-m", "Bdrl"]
        execle(sys.executable, *args, environ)
        return


modules_help["updater"] = {
    "update": "get list update for your userbot.",
    "update now": "For update your userbot.",
}
