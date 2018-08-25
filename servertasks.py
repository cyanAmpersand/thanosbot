import discord
import asyncio
import random

class ServerTask:
    def __init__(self,client : discord.Client):
        self.client = client
        self.snap_in_progress = False
        self.snapinfo = None

    def set_snap_info(self,snapinfo):
        self.snapinfo = snapinfo

    async def blank_task(self):
        await self.client.wait_until_ready()
        #preconditions here
        while not self.client.is_closed:
            pass
            #loop here

    async def flip_flop(self,m : discord.Message):
        await self.client.wait_until_ready()
        flip = True
        while not self.client.is_closed:
            if flip:
                await self.client.edit_message(m, new_content="flip")
                flip = False
                await asyncio.sleep(2)
            else:
                await self.client.edit_message(m, new_content="flop")
                flip = True
                await asyncio.sleep(2)

    async def snapture_edit(self,snapinfo):
        await self.client.wait_until_ready()
        self.snapinfo = snapinfo
        #while not self.client.is_closed:
        if not self.snap_in_progress:
            self.snap_in_progress = True
            print("snapping...")
            snapinfo["content_new"] = snapinfo["message"].content
            for e in snapinfo["edits"][:-1]:
                snapinfo["content_new"] += "\n" + e
                await self.client.edit_message(snapinfo["message"],
                                          "```" + snapinfo["content_new"] + "```")
                #await asyncio.sleep(3*random.random())
            await self.client.edit_message(snapinfo["message"],
                                      "```" + snapinfo["content_new"] + "```" + snapinfo["edits"][
                                          -1])
            print("snap done")
            self.snap_in_progress = False