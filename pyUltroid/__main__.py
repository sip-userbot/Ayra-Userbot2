# Ayra - UserBot
# Copyright (C) 2021-2022 TeamAyra
#
# This file is a part of < https://github.com/TeamAyra/Ayra/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamAyra/pyAyra/blob/main/LICENSE>.

from . import *


def main():
    import os
    import sys
    import time

    from .fns.helper import time_formatter, updater, bash
    from .startup.funcs import (
        WasItRestart,
        autopilot,
        customize,
        plug,
        ready,
        startup_stuff,
    )
    from .startup.loader import load_other_plugins

    # Option to Auto Update On Restarts..
    if (
        udB.get_key("UPDATE_ON_RESTART")
        and os.path.exists(".git")
        and Ayra_bot.run_in_loop(updater())
    ):
        Ayra_bot.run_in_loop(bash("bash installer.sh"))

        os.execl(sys.executable, "python3", "-m", "pyAyra")

    Ayra_bot.run_in_loop(startup_stuff())

    Ayra_bot.me.phone = None

    if not Ayra_bot.me.bot:
        udB.set_key("OWNER_ID", Ayra_bot.uid)

    LOGS.info("Initialising...")

    Ayra_bot.run_in_loop(autopilot())

    pmbot = udB.get_key("PMBOT")
    manager = udB.get_key("MANAGER")
    addons = udB.get_key("ADDONS") or Var.ADDONS
    vcbot = udB.get_key("VCBOT") or Var.VCBOT
    if HOSTED_ON == "okteto":
        vcbot = False

    if (HOSTED_ON == "termux" or udB.get_key("LITE_DEPLOY")) and udB.get_key(
        "EXCLUDE_OFFICIAL"
    ) is None:
        _plugins = "autocorrect autopic audiotools compressor forcesubscribe fedutils gdrive glitch instagram nsfwfilter nightmode pdftools profanityfilter writer youtube"
        udB.set_key("EXCLUDE_OFFICIAL", _plugins)

    load_other_plugins(addons=addons, pmbot=pmbot, manager=manager, vcbot=vcbot)

    suc_msg = """
            ----------------------------------------------------------------------
                Ayra has been deployed! Visit @TheAyra for updates!!
            ----------------------------------------------------------------------
    """

    # for channel plugins
    plugin_channels = udB.get_key("PLUGIN_CHANNEL")

    # Customize Ayra Assistant...
    Ayra_bot.run_in_loop(customize())

    # Load Addons from Plugin Channels.
    if plugin_channels:
        Ayra_bot.run_in_loop(plug(plugin_channels))

    # Send/Ignore Deploy Message..
    if not udB.get_key("LOG_OFF"):
        Ayra_bot.run_in_loop(ready())

    # Edit Restarting Message (if It's restarting)
    Ayra_bot.run_in_loop(WasItRestart(udB))

    try:
        cleanup_cache()
    except BaseException:
        pass

    LOGS.info(
        f"Took {time_formatter((time.time() - start_time)*1000)} to start •Ayra•"
    )
    LOGS.info(suc_msg)


if __name__ == "__main__":
    main()

    asst.run()
