import discord
import botfunctions
import sillystuff
import time
import asyncio
import sys
import random

start_time = time.time()

testing = True
linux = False
if sys.platform == "linux":
    print("running linux")
    linux = True
    testing = False
rpi_dir = "/home/chloe/angel/"

statuses = []

token_dir = "../"

token = botfunctions.loadToken(token_dir + "thanosbot.tkn").strip()
cmd_prefix = "!thanos "
output_channel = "395422229074018320"
if testing:
    token = botfunctions.loadToken(token_dir + "testbot.tkn").strip()
    cmd_prefix = "!t_"
    statuses = ["chloe is tinkering"]
    output_channel = "395422229074018320"

all_servers = {}
all_channels = {}
message_logs = []
user_ids = {}
emoji = {}
snapture_editing = {
    "message":None,
    "edits":[],
    "content_new":""
}

client = discord.Client()

async def snapture_edit():
    await client.wait_until_ready()
    while not client.is_closed:
        if snapture_editing["message"] is not None:
            print("snapping...")
            snapture_editing["content_new"] = snapture_editing["message"].content
            print(snapture_editing["edits"])
            for e in snapture_editing["edits"][:-1]:
                print(e)
                snapture_editing["content_new"] += "\n" + e
                await client.edit_message(snapture_editing["message"],"```" + snapture_editing["content_new"] + "```")
                await asyncio.sleep(3*random.random())
            await client.edit_message(snapture_editing["message"], "```" + snapture_editing["content_new"] + "```" + snapture_editing["edits"][-1])
            print("snap done")
            snapture_editing["message"] = None
            snapture_editing["edits"] = []
            snapture_editing["content_new"] = ""
        await asyncio.sleep(1)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for s in client.servers:
        all_servers[s.id] = s
        for c in s.channels:
            all_channels[c.id] = c
        for m in s.members:
            user_ids[m.id] = m.name

    for m in user_ids:
        print(m + " " + user_ids[m])

    c_output = client.get_channel(output_channel)
    await client.send_message(c_output,"Dread it. Run from it. Destiny arrives all the same. And now, it's here. Or should I say, I am. [Thanosbot is online.]")

    print('ready')

    await client.change_presence(game=discord.Game(name="initializing..."))

@client.event
async def on_message(message):
    response = None
    responseChannel = message.channel

    if message.author.bot:
        pass
    else:
        if message.content.startswith(cmd_prefix):
            msgstr = message.content[len(cmd_prefix)::]
            if msgstr == "help":
                pass
            if msgstr.startswith("snapture"):
                print("snap called")
                if "slow" in msgstr:
                    if snapture_editing["message"] is None:
                        try:
                            snap_message = await client.send_file(responseChannel, "snap.png", filename="snap.png")
                        except FileNotFoundError:
                            snap_message = await client.send_file(responseChannel, rpi_dir + "snap.png",filename="snap.png")
                        print(snap_message.id)
                        snapture_editing["edits"] = sillystuff.infinitysnap(message.server.members)
                        snapture_editing["message"] = snap_message
                    else:
                        await client.send_message(responseChannel,"Whoa there Thanos, there's a snapture already in progress.")
                else:
                    snapstring = sillystuff.infinitysnap(message.server.members)
                    msg_content = "```" + "\n".join(snapstring[:-1]) + "```" + snapstring[-1]
                    try:
                        await client.send_file(responseChannel,"snap.png",filename = "snap.png",content=msg_content)
                    except FileNotFoundError:
                        await client.send_file(responseChannel, rpi_dir + "snap.png", filename="snap.png", content=msg_content)

    if response is not None:
        await client.send_message(responseChannel,response)

client.loop.create_task(bg_status())
client.loop.create_task(snapture_edit())
client.run(token)