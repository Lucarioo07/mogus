from discord.ext import commands


class UserBanned(commands.CheckFailure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class NotStaff(commands.CheckFailure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WrongServer(commands.CheckFailure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class CommandDisabled(commands.CheckFailure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BotLocked(commands.CheckFailure):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
