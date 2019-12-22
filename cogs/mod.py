import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils.dataIO import dataIO
import json
import asyncio
import datetime

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ang = 'data/mod/settings.json'
        self.data = dataIO.load_json(self.ang)
        self.cass = 'data/mod/case.json'
        self.case = dataIO.load_json(self.cass)

    async def owner(ctx):
        ctx.author.id == 431085681847042048

    async def admin(ctx):
        if ctx.author.id == 431085681847042048:
            return True
        elif ctx.author.guild_permissions.administrator == True:
            return True
    
    @commands.command(pass_context=True, no_pm=True)
    @commands.check(owner)
    async def asdf(self, ctx):
        return await self.send_cmd_help(ctx)

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    @commands.has_permissions(administrator=True)
    async def language(self, ctx, language=None):
        """봇의 언어를 설정하는 명령어 입니다!"""
        server = ctx.guild
        if language == None:
            return await self.language_setting(ctx)
        if language == 'ko':
            try:
                self.data[f'{server.id}'].update({"language": "ko"})
            except KeyError:
                self.data[f'{server.id}'] = {}
                self.data[f'{server.id}'].update({"language": "ko"})
            await ctx.send('> 언어가 성공적으로 `한글` 로 설정 되었습니다! | Succees to language has been set!')
            dataIO.save_json(self.ang, self.data)
        if language == 'en':
            try:
                self.data[f'{server.id}'].update({"language": "en"})
            except KeyError:
                self.data[f'{server.id}'] = {}
                self.data[f'{server.id}'].update({"language": "en"})
            await ctx.send('> 언어가 성공적으로 `영어` 로 설정 되었습니다! | Succees to language has been set!')
            dataIO.save_json(self.ang, self.data)
        else:
            return await self.language_setting(ctx)
            
    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    async def ban(self, ctx, user:discord.Member=None, *, reason=None):
        """악성 유저를 벤 하는 명령어입니다!"""
        if user == None:
            return await ctx.send('> 벤할 유저를 멘션해주세요!')
        elif reason == None:
            reason = '없음'
        else:
            pass
        try:
            await user.ban(reason=reason)
            return await ctx.send(f'> 벤이 정상적으로 진행되었어요!\n 사유: {reason}')
        except:
            await ctx.send("> 권한이 없거나 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주시고 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!")
            return     

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    async def unban(self, ctx: commands.Context, user_id: int, *, reason: str = None):
        """유저를 언벤 하는 명령어입니다!"""
        guild = ctx.guild
        if id == None:
            return await ctx.send('> 언벤할 유저의 ID를 적어주세요!')
        elif reason == None:
            reason = '없음'
        else:
            pass
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.errors.NotFound:
            await ctx.send("> 유저를 찾지 못했어요!")
            return
        bans = await guild.bans()
        bans = [be.user for be in bans]
        if user not in bans:
            await ctx.send("> 이 유저는 애초에 벤이 되있지 않습니다! 다시 한번 더 확인해주세요!")
            return
        try:
            await guild.unban(user, reason=reason)
            await ctx.send('> 완료하였습니다!')
        except discord.HTTPException:
            await ctx.send("> 권한이 없거나 혹은 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주시고 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!")
            return     

    @commands.command(pass_context=True, no_pm=True)
    @commands.check(admin)
    async def hackban(self, ctx: commands.Context, user_id: int, *, reason: str = None):
        """악성유저가 이 서버에 없을경우 대처를 하기 위해 벤하는 명령어입니다!"""
        guild = ctx.guild
        if id == None:
            return await ctx.send('> 핵벤할 유저의 ID를 적어주세요!')
        elif reason == None:
            reason = '없음'
        else:
            pass
        try:
            user = await self.bot.fetch_user(user_id)
        except discord.errors.NotFound:
            await ctx.send("> 유저를 찾지 못했어요!")
            return
        bans = await guild.bans()
        bans = [be.user for be in bans]
        if user in bans:
            await ctx.send("> 이 유저는 애초에 벤이 되있습니다!")
            return
        try:
            await guild.ban(user, reason=reason)
            await ctx.send('> 완료하였습니다!')
        except discord.HTTPException:
            await ctx.send("> 권한이 없거나 혹은 디스코드 API에 문제가 있는거 같습니다!\n> 권한을 추가 해 주시고 다시 시도 해주시기 바라며, 그래도 안될시 API 문제이니 잠시후에 다시 해주세요!")
            return        
            


    async def send_cmd_help(self, ctx):
        c = self.bot.get_channel(ctx.message.channel.id)
        em = discord.Embed(colour=ctx.author.colour)
        em.add_field(name='그 명령어는 없는 명령어입니다!', value='`{0.prefix}help` 으로 확인하세요!'.format(ctx))
        em.set_footer(text='제대로 작성하였는지 확인해주시고 사용해주세요!')
        return await c.send(embed=em)

    async def language_setting(self, ctx):
        author = ctx.author
        c = self.bot.get_channel(ctx.message.channel.id)
        em = discord.Embed(colour=author.colour, title=':thinking: 언어 설정 | LANGUAGE SETTINGS :thinking:', timestamp=datetime.datetime.utcnow())
        em.add_field(name='사용 가능한 언어 | AVAILABLE LANGUAGES', value=':arrow_right: ko_kr(한글), en_us(영어) :arrow_left:')
        if author.avatar_url:
            em.set_footer(text=f'Request By {author}', icon_url=author.avatar_url)
        else:
            em.set_footer(text=f'Request By {author}')
        return await c.send(embed=em)


def setup(bot):
    bot.add_cog(Mod(bot))
