import asyncio
import datetime
import glob
import random
from datetime import datetime

from discord.ext import commands
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


class Music(commands.Cog):
   def __init__(self, bot):
      self.bot = bot
      self.playback = ""
      self.target = 6
      self.minute = 0
      self.flag = False
      self.alram = True
      self.repeat = 1
      self.repeat_tmp = 0

   @commands.Cog.listener()
   async def on_ready(self):
      print(f"We have logged in as {self.bot.user}")
      await self.loop()

   @commands.Cog.listener()
   async def on_message(self, message):
      if message.author == self.bot.user:
         return
      if message.content.startswith("起きた"):
         self.playback.stop()
         await message.channel.send("おはようございます")
         self.repeat_tmp = 0
         await asyncio.sleep(60)
         self.flag = False

   async def loop(self):
      while True:
         now = datetime.now()
         if (
            now.hour == self.target
            and now.minute == self.minute
            and self.flag is False
            and self.alram is True
         ):
            self.repeat_tmp = self.repeat
            self.flag = True
            files = glob.glob("mp3/*.mp3")
            path = random.choice(files)
            audio = AudioSegment.from_mp3(path)
            self.playback = _play_with_simpleaudio(audio)
            channel = self.bot.get_channel(1085077066657038407)
            await channel.send(
               "アラームを慣らしています。起きない場合はこれで叩き起こしてください\n```起きろ！！朝だぞ！！```"
            )
         elif self.flag is True:
            if self.repeat_tmp > 0 and self.playback.is_playing() is False:
               self.repeat_tmp -= 1
               files = glob.glob("mp3/*.mp3")
               path = random.choice(files)
               audio = AudioSegment.from_mp3(path)
               self.playback = _play_with_simpleaudio(audio + 20)

         await asyncio.sleep(10)

   @commands.slash_command()
   async def status(self, ctx):
      await ctx.respond(
         f"アラーム: {self.alram}\n時間: {self.target}:{self.minute}\n繰り返し: {self.repeat}回"
      )

   @commands.slash_command(name="テスト")
   async def test(self, ctx):
      files = glob.glob("mp3/*.mp3")
      path = random.choice(files)
      audio = AudioSegment.from_mp3(path)
      self.playback = _play_with_simpleaudio(audio)
      await ctx.respond(
         "アラームを慣らしています。起きない場合はこれで叩き起こしてください\n```起きろ！！朝だぞ！！```"
      )

   @commands.slash_command(name="時間設定")
   async def set_time(self, ctx, hour: int, minute: int):
      self.target = hour
      self.minute = minute
      await ctx.respond("時間を設定しました")

   @commands.slash_command(name="アラームオン")
   async def on(self, ctx):
      self.alram = True
      await ctx.respond("アラームをオンにしました")

   @commands.slash_command(name="アラームオフ")
   async def off(self, ctx):
      self.alram = False
      await ctx.respond("アラームをオフにしました")

   @commands.slash_command(name="繰り返し")
   async def repeat(self, ctx, repeat: int):
      self.repeat = repeat
      await ctx.respond(f"繰り返し回数を{repeat}回に設定しました")


def setup(bot):
   bot.add_cog(Music(bot))
