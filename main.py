import discord
import os
import json
from config import secrets
from discord.ext import commands





class main(discord.ext.commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(secrets.PREFIXO),
                         case_insensitive=True,
                         pm_help=None,
                         description="um bot feito por Neo_ para a minha lojinha")
        
        self.dono = secrets.DONO

        self.logs = 686175562150051942

        self.bans = 679738999312744454

        self.guild = 679015306437460008

        self.token = 'blz,talvez outro dia.'
        
        self.cor = 0xf10cdb
        self.ecolor = 0xDD2E44
        self.neutral = 0x36393F
        
        for file in [c for c in os.listdir("cogs") if c.endswith(".py")]:
                name = file[:-3]
                try:
                    self.load_extension(f"cogs.{name}")
                    print(f'MÓDULO [{file}] CARREGADO')
                except Exception as e:
                    print(f"FALHA AO CARREGAR  [{file}] MODULO ERROR [{e}]")

    
    
    def formatPrefix(self, ctx):
        prefix = ctx.prefix if not str(self.user.id) in ctx.prefix else f'@{ctx.me} '
        return ctx.prefix.replace(ctx.prefix, prefix)

    # Embeds
    def embed(self, ctx, invisible=False):
        color = self.neutral if invisible else self.cor
        emb = discord.Embed(color=color)
        emb.set_footer(text=self.user.name + " © 2020", icon_url=self.user.avatar_url_as())
        emb.timestamp = ctx.message.created_at
        return emb

    def erEmbed(self, ctx, error='Erro!'):
        emb = discord.Embed(title=f':x: | {error}', color=self.ecolor)
        emb.set_footer(text=f'Executado por {ctx.author.name}', icon_url=ctx.author.avatar_url)
        emb.timestamp = ctx.message.created_at
        return emb

    async def on_message(self, message):
        return

    async def on_ready(self):
        print('---------- Bot Online -----------')
        print(f'Nome: {self.user.name}')
        print(f'Id: {self.user.id}')
        print(f'Usuários: {len(self.users) - len([c for c in self.users if c.bot])}')
        print(f'Bots: {len([c for c in self.users if c.bot])}')
        print(f'Guilds: {len(self.guilds)}')
        print('---------------------------------')

bot = main()

@bot.check
async def blacklist(ctx):
    with open('cogs/utils/users_banned.json') as bn:
        jsn = json.load(bn)
    if str(ctx.author.id) in jsn and not ctx.author.id == bot.dono:
        reason = jsn[str(ctx.author.id)]
        embed = discord.Embed(title=f':x: | Sem permissão!', description=f'Você foi banido de usar qualquer comando meu, o motivo é:\n`{reason}`', color=bot.ecolor)
        await ctx.send(embed=embed)
        return False
    return True

if __name__ == '__main__':
    try:
        bot.run("NjgyMjgwMjAwNjk5OTA0MDkx.Xlas9A.qYjW_Zo-C8HQXP6v7maeBgH1w10")
    except KeyboardInterrupt: 
        pass
