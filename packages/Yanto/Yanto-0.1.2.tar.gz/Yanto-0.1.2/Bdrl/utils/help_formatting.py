from Bdrl.helpers.sql.globals import gvarstatus


class ModulesHelpDict(dict):
    def append(self, obj: dict):
        # convert help from old to new type
        module_name = list(obj.keys())[0]
        cmds = obj[module_name]
        commands = {}
        for cmd in cmds:
            cmd_name = list(cmd.keys())[0]
            cmd_desc = cmd[cmd_name]
            commands[cmd_name] = cmd_desc
        self[module_name] = commands


modules_help = ModulesHelpDict()
prefix = gvarstatus("PREFIX") or "."


def format_module_help(module_name: str):
    commands = modules_help[module_name]

    help_text = f"──「 <b> Help for</b> <code>{module_name}</code> 」──\n\n"

    for command, desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " <code>" + cmd[1] + "</code>" if len(cmd) > 1 else ""
        help_text += f"<code>{prefix}{cmd[0]}</code>{args} — {desc}\n"
    help_text += "\n©️ 2022-present Bdrl"
    return help_text


def format_small_module_help(module_name: str):
    commands = modules_help[module_name]

    help_text = f"──「 <b> Command list of</b> <code>{module_name}</code> 」──\n\n"
    for command, desc in commands.items():
        cmd = command.split(maxsplit=1)
        args = " <code>" + cmd[1] + "</code>" if len(cmd) > 1 else ""
        help_text += f"<code>{prefix}{cmd[0]}</code>{args}\n"
    help_text += f"\nFull usage: <code>{prefix}help {module_name}</code></b>"

    return help_text
