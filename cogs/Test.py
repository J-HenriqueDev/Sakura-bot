import discord
from datetime import datetime, timedelta
import pytz
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord.ext import commands
from asyncio import sleep
import requests




class bem-vindo(commands.Cog)
    def __init__(self,bot):
        self.bot = bot



    @commands.Cog.listener()  
    async def on_member_join(self, member):
       if member.guild.id == 570906068277002271 and not member.bot:
        cat = member.created_at.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone('America/Sao_Paulo')).strftime('`%d/%m/%Y`')
        dias = (datetime.utcnow() - member.created_at).days
        embed = discord.Embed(color=0x7289DA, description=f'**{member.mention}(`{member.id}`) entrou no servidor, com a conta criada em {cat}({dias} dias).**')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=self.bot.user.name+" © 2019", icon_url=self.bot.user.avatar_url_as())
        await self.bot.get_channel(580095031591829518).send(embed=embed)
        
        ###################################################################
        
        url = requests.get(member.avatar_url_as(format="png"))
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((220, 220));
        bigsize = (avatar.size[0] * 2,  avatar.size[1] * 2)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        saida = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        saida.putalpha(mask)

        fundo = Image.open('cogs/img/bemvindo.png')
        fonte = ImageFont.truetype('cogs/img/arial.ttf',42)
        fonte2 = ImageFont.truetype('cogs/img/arial.ttf',58)

        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(365,160), text=str(member.name),fill=(0,0,0),font=fonte)
        escrever.text(xy=(380,220), text=str(member.discriminator),fill=(0,0,0),font=fonte2)
        escrever.text(xy=(365,305), text="New Dev's",fill=(0,0,0),font=fonte)

        fundo.paste(saida, (43, 91), saida)
        fundo.save("cogs/img/welcome.png")   
        canal = discord.utils.get(member.guild.channels, id=581544881206329354)
        await canal.send(f"Olá {member.mention}, seja bem vindo ao **New Dev's**, caso queria algum **CARGO** use o <#581216249170624512> para pegar, e leia as <#581081932935200769> para ficar por dentro do servidor.", file=discord.File('cogs/img/welcome.png'))
      
def setup(cog)
