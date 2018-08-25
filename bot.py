import discord
import botfunctions
import snapture
import time
import asyncio
import sys
import random
import servertasks as st

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
output_channel = "397580213980233739"
if testing:
    token = botfunctions.loadToken(token_dir + "testbot.tkn").strip()
    cmd_prefix = "!t_"
    statuses = ["chloe is tinkering"]
    output_channel = "395422229074018320"

snapture_editing = {
    "message":None,
    "users":{},
    "edits":[],
    "content_new":""
}

server_tasks = {}

server_info = {}

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    for s in client.servers:
        print(s.id + ", " + s.name)
        server_tasks[s.id] = st.ServerTask(client)

    c_output = client.get_channel(output_channel)
    await client.send_message(c_output,"Dread it. Run from it. Destiny arrives all the same. And now, it's here. Or should I say, I am. [Thanosbot is online.]")

    print('ready')

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
            if msgstr == "did i die":
                if server_tasks[message.server.id].snapinfo is None:
                    await client.send_message(message.channel,"no snapture yet")
                elif server_tasks[message.server.id].snap_in_progress:
                    await client.send_message(message.channel, "There is a snapture in progress. Channel: " + message.channel.name)
                elif server_tasks[message.server.id].snapinfo["users"][message.author.id]["alive"]:
                    await client.send_message(message.channel, "no")
                elif not server_tasks[message.server.id].snapinfo["users"][message.author.id]["alive"]:
                    await client.send_message(message.channel, "yes")
                else:
                    await client.send_message(message.channel, "oopsie")
            if msgstr.startswith("snapture"):
                snapresult = snapture.infinitysnap(message.server.members)
                snapture_editing["edits"] = snapture.snapstring(snapresult)
                snapture_editing["users"] = snapresult
                server_tasks[message.server.id].set_snap_info(snapture_editing)
                if not server_tasks[message.server.id].snap_in_progress:
                    if "slow" in msgstr:
                        try:
                            snap_message = await client.send_file(responseChannel, "snap.png", filename="snap.png")
                        except FileNotFoundError:
                            snap_message = await client.send_file(responseChannel, rpi_dir + "snap.png",filename="snap.png")
                        snapture_editing["message"] = snap_message
                        await server_tasks[message.server.id].snapture_edit(snapture_editing.copy())
                    else:
                        snaplines = server_tasks[message.server.id].snapinfo["edits"]
                        msg_content = "```" + "\n".join(snaplines[:-1]) + "```" + snaplines[-1]
                        try:
                            await client.send_file(responseChannel,"snap.png",filename = "snap.png",content=msg_content)
                        except FileNotFoundError:
                            await client.send_file(responseChannel, rpi_dir + "snap.png", filename="snap.png", content=msg_content)
                else:
                    await client.send_message(responseChannel, "There is a snapture already in progress. Channel: " + message.channel.name)

    if response is not None:
        await client.send_message(responseChannel,response)

client.run(token)