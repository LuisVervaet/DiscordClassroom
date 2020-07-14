import pymongo
import asyncio
import config
import discord
from discord.ext import commands

import utils


class Profile(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def note(self, ctx, *, note:str=None):
        account, first_time = utils.get_profile(ctx.author.id)
        if note is None:
            embed = discord.Embed(title="<:news:732103029565685770> Note",
                                  description=f"Reply with a new note to change the note shown on your profile.\n\n*reply with `cancel` to cancel*",
                                  color=config.MAINCOLOR)
            embed.set_footer(text="Message timout in 60 seconds",
                             icon_url="https://cdn.discordapp.com/emojis/732714132461191330.png?v=1")
            start_message = await ctx.send(embed=embed)

            def check(msg):
                return msg.author.id == ctx.author.id and msg.channel.id == ctx.channel.id and len(msg.content) < 100

            try:
                note_message = await self.bot.wait_for('message', check=check, timeout=60.0)
                if note_message.content.lower() == "cancel":
                    embed.description = "Note has not been changed."
                    embed.set_footer()
                    await start_message.edit(embed=embed)
                    return
                note = note_message.content
            except asyncio.TimeoutError:
                embed.description = "Note change has timed out. Please type `d!note` to try again."
                embed.set_footer()
                await start_message.edit(embed=embed)
                return
        config.USERS.update({'user_id': ctx.author.id}, {'$set': {'note': note}})
        await ctx.send(embed=discord.Embed(title="<:checkb:732103029020557323> Note has been changed!"))

    @commands.command(aliases=['p', 'user'])
    async def profile(self, ctx, user: discord.Member = None):
        owner = False
        if user is None:
            user = ctx.author
            owner = True
        account, first_time = utils.get_profile(user.id)
        embed = discord.Embed(title=f"<:enter:732105777577459723> {user.name}'s Profile",
                              color=config.MAINCOLOR)
        embed.set_thumbnail(url=str(user.avatar_url))
        account_classes = list(utils.get_user_classes(ctx.author.id))
        account_teaching_classes = list(utils.get_teaching_classes(ctx.author.id))

        if owner and account['is_student'] and len(account_classes) < 1:
            embed.set_footer(text="Are you a teacher? Make sure to type 'd!class'", icon_url="https://cdn.discordapp.com/emojis/732116410553073674.png?v=1")
        if account['bio'] is None:
            embed.add_field(name="<:news:732103029565685770> Note", value=f"{user.name}'s Note can be set using `d!note`", inline=False)
        else:
            embed.add_field(name="<:news:732103029565685770> Note", value=f"{account['bio']}", inline=False)

        if account['google_classroom'] is not None:
            embed.add_field(name="<:people:732103029565947934> Google Classroom", value=f"{account['google_classroom']} <:check_verify:732103029121089638>", inline=False)
        else:
            if owner:
                embed.add_field(name="<:people:732103029565947934> Google Classroom",
                                value="<:cross:732103029712617482> Not Linked. [**Link now**](https://classroom.google.com)", inline=False)
            else:
                embed.add_field(name="<:people:732103029565947934> Google Classroom", value="<:cross:732103029712617482> Not Linked.", inline=False)

        classes_string = ""
        if len(account_classes) > 0:
            classes_string += f"{str(len(account_classes))} Classes joined"
        if len(account_teaching_classes) > 0:
            classes_string += f"\n{str(len(account_teaching_classes))} Classes teaching"
        if classes_string != "":
            embed.add_field(name="<:inv:732103029213364295> Classes", value=classes_string, inline=True)

        if account['is_student']:
            embed.add_field(name="<:auth:732103030110945332> Role", value=f"Student", inline=True)
        else:
            embed.add_field(name="<:auth:732103030110945332> Role", value=f"Teacher", inline=True)



        await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Profile(bot))
