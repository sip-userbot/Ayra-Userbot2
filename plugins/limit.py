from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest


@ultroid_cmd(pattern="limit$")
async def demn(ult):
    chat = "@SpamBot"
    await ult.edit("Memeriksa Apakah Anda Terbatas...")
    async with ult.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(incoming=True, from_users=178220800))
            await ult.client.send_message(chat, "/start")
            response = await response
        except YouBlockedUserError:
            await ult.reply("Silahkan Buka Blokir @SpamBot ")
            return
        await eor(ult, response.message.message)
