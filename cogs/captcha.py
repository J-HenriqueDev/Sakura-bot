import discord
from asyncio import TimeoutError as Esgotado   
from captcha.image import ImageCaptcha
from discord.ext import commands
from discord.ext.commands import Bot
from random import randint
import asyncio

class captcha(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.formulario = []
    '''
    @commands.command()
    async def captcha(self,ctx):
        try:
            await ctx.message.delete()
            canal = discord.utils.get(ctx.author.guild.channels, name='🔑│captcha')
            if ctx.channel != canal:
                msg_1 = await ctx.send(f'{ctx.author.mention} Você ja é um membro.')
                await asyncio.sleep(10)
                await msg_1.delete()
            else:
                numeros = randint(1000,10000)
                image = ImageCaptcha()
                data = image.generate('12345')
                send_img = image.write(str(numeros), 'out.png')
                mention = await ctx.send(ctx.author.mention)
                embed = discord.Embed(description="",color=0x7289da)
                embed.set_author(name="🔑| Captcha")
                embed.add_field(name='Por favor escreva os números a baixo (sem espaço) ',value= f"**--Tempo maximo de 5 minutos--**")
                embed.set_image(url="attachment://out.png")
                embed_enviado = await ctx.send(embed=embed, file=discord.File('out.png'))
                #def check(m):
                    #return m.content and ctx.author == ctx.author
                check=lambda m: m.channel == ctx.channel and m.author == ctx.author
                msg = await self.bot.wait_for('message', check=check, timeout=300)

                if msg.content == str(numeros):
                    msg_sucesso = await ctx.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                    await ctx.author.remove_roles(ctx.author.guild.get_role(572530404737810444))
                    await ctx.author.add_roles(ctx.author.guild.get_role(570739008317947932))
                    await asyncio.sleep(10)
                    await mention.delete()
                    await ctx.message.delete()
                    await msg_sucesso.delete()
                    await embed_enviado.delete()
                    await msg.delete()
                else:
                    msg_erro = await ctx.send('**Você errou o captcha digite h.captcha para ter uma nova chance**')
                    await asyncio.sleep(10)
                    await mention.delete()
                    await ctx.message.delete()
                    await msg_erro.delete()
                    await msg.delete()
                    await embed_enviado.delete()

        except Exception as e:
            print(e)
            '''
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id == 679015306437460008 and not member.bot:
            canal = discord.utils.get(member.guild.channels, name='🔑│captcha')
            canal_boasvindas = discord.utils.get(member.guild.channels, name='💥│bem-vindo')
            await member.add_roles(member.guild.get_role(679026020543889420))
            #await canal_boasvindas.send(f'{member.mention}, seja bem vindo ao botmann Haus, leia as regras e seja feliz <3')
            try:
                numeros = randint(1000,10000)
                image = ImageCaptcha()
                data = image.generate('12345')
                send_img = image.write(str(numeros), 'out.png')
                mention = await canal.send(member.mention)
                self.formulario.append(member.id)
                embed = discord.Embed(description="",color=0x7289da)
                embed.set_author(name="🔑| Captcha")
                embed.add_field(name='Por favor escreva os números abaixo (sem espaço)',value= f"**--Tempo máximo de 5 minutos--**")
                embed.set_image(url="attachment://out.png")
                embed_enviado = await canal.send(embed=embed, file=discord.File('out.png'))

                check=lambda m: m.author == member

                '''
                if msg.content == str(numeros):
                    msg_sucesso = await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                    await member.remove_roles(member.guild.get_role(572530404737810444))
                    await member.add_roles(member.guild.get_role(570739008317947932))
                    await asyncio.sleep(10)
                    await mention.delete()
                    await msg_sucesso.delete()
                    await msg.delete()
                    await embed_enviado.delete()

                else:
                    msg_erro = await canal.send('**Você errou o captcha digite h.captcha para ter uma nova chance**')
                    await asyncio.sleep(10)
                    await mention.delete()
                    await msg_erro.delete()
                    await msg.delete()
                    await embed_enviado.delete()
                '''

                captcha = None
                tentativas = 0
                while captcha is None:
                    try:
                        resposta = await self.bot.wait_for("message", check=check, timeout=300)
                    except Esgotado:
                        await canal.send(f"**{member.name}**, você demorou muito para fornecer o captcha,então voçê será kickado!", delete_after=30)
                        await member.kick()
                        await embed_enviado.delete()
                        break
                    if tentativas == 4:
                        await canal.send(f"**{member.name}**, você errou o captcha 5 vezes então será kickado!", delete_after=20)
                        self.formulario.remove(member.id)
                        await member.kick()
                        await embed_enviado.delete()
                        break
                    elif resposta.content == str(numeros):
                        await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                        await member.remove_roles(member.guild.get_role(679026020543889420))
                        await member.add_roles(member.guild.get_role(679026175762235403)) 
                        await asyncio.sleep(3)
                        await embed_enviado.delete()
                        break
                    
                    elif not resposta.content == str(numeros):
                        tentativas += 1
                        await canal.send(f"**Você errou o captcha pqp otário,tente novamente.**\nTentativa: `{tentativas}/5`", delete_after=60)
                    else:
                        nome = resposta.content        
 
                if not nome:
                    return self.formulario.remove(member.id)

                
                await canal.send('**Catpcha concluido com sucesso.**\n**Agora você se tornou um membro.**')
                await member.remove_roles(member.guild.get_role(679026020543889420))
                await member.add_roles(member.guild.get_role(679026175762235403))
                await embed_enviado.delete()
                await canal.purge(limit=100)
            except Exception as e:
                print(e)


def setup(bot):
    bot.add_cog(captcha(bot))
