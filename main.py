import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "__**🤠 Kıyıcı Tagger**, Sunucunuzu aktif tutmak istiyorsanız doğru bot seçimi yaptınız 🤩🤍\nTıkla ve komutları gör! **/yardim** __\n\n",
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Destek Sunucumuz', 'https://t.me/kiyicitayfaaa')
        Button.url('🤠 Sahibim', 'https://t.me/officialkiyici')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/yardim$"))
async def help(event):
  helptext = "**🤍 Yardım Menüsü 🤍**\n\nKomut: /eko\n__Komutunu kullanarak sunucunuzdaki herkesi etiketleyebilirsiniz.__\n`Örnek: /eko Kıyıcı Tayfa Yazalım Farkıyla!`\n__Etiket botumuzun sayesinde aktifliğinizi koruyun ❤️‍🩹__.\n\n"
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('📣 Destek Sunucumuz', 'https://t.me/ektonc'),
        Button.url('🤠 Sahibim', 'https://t.me/officialkiyici')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/eko ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__This command can be use in groups and channels!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__Yanlızca Adminler Kullanabilir Komutu!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__Give me one argument!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("__I can't mention members for older messages! (messages which are sent before I'm added to this group)__")
  else:
    return await event.respond("__Reply to a message or give me some text to mention others!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/iptal$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('__There is no proccess on going...__')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('__Stopped.__')

print(">> BOT AKTİF <<")
client.run_until_disconnected()
