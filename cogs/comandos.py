import discord
import requests
import time
import datetime
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps

class comandos(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.bot_has_permissions(embed_links=True)
    @commands.command(description='Mostra o meu ping', usage='c.ping')
    async def ping(self, ctx):
        embed = discord.Embed(title="🏓 Pong!",
                              description=f' No Momento estou com: **{round(self.bot.latency * 1000)}ms**.',
                              color=0x36393f)
        embed.set_footer(text=self.bot.user.name + " © 2020", icon_url=self.bot.user.avatar_url_as())
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=90)



    @commands.command()
    async def spotify(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        act = member.activity
        if act is None or not act.type == discord.ActivityType.listening:
            if member == ctx.author:
                await ctx.send(f'{ctx.author.mention} Você não está ouvindo Spotify.')
            else:
                await ctx.send(f'{ctx.author.mention} Esse usuário não está ouvindo Spotify.')
        else:
            end = act.end - datetime.datetime.utcnow()
            end = str(act.duration - end)[2:7]
            dur = str(act.duration)[2:7]
            act = member.activity
            url = requests.get(act.album_cover_url)
            thumb = Image.open(BytesIO(url.content))
            thumb = thumb.resize((245, 245));
            bigsize = (thumb.size[0] * 3, thumb.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(thumb.size, Image.ANTIALIAS)
            thumb.putalpha(mask)

            output = ImageOps.fit(thumb, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)

            if len(act.title) >= 21:
                titulo = act.title[:22]+"..."
            else:
                titulo = act.title
            if len(act.artist) >= 21:
                cantor = act.artist[:22]+"..."
            else:
                cantor = act.artist
            fundo = Image.open('./files/imagem.png')
            fonte = ImageFont.truetype('./files/Err Hostess.otf', 35)
            escrever = ImageDraw.Draw(fundo)
            escrever.text(xy=(365,150), text=str(titulo),fill=(0,0,0),font=fonte)
            escrever.text(xy=(360,230), text=str(end + ' - ' + dur),fill=(0,0,0),font=fonte)
            escrever.text(xy=(365,315), text=str(cantor),fill=(0,0,0),font=fonte)
            fundo.paste(thumb, (45, 113), thumb)
            fundo.save('./files/imagem1.png')

            print('enviando')
            await ctx.send(file=discord.File('./files/imagem1.png'))

    

def setup(bot):
    bot.add_cog(comandos(bot))
