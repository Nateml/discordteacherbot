import os
import random
import sys
import data
from dotenv import load_dotenv


# 1
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')
teacher_list = ["Mr Bell", "Ms Viljouen", "Mr Entwistle", "Dr Kitshoff", "Mr Kruger", "Mr Purchase", "Ms Cloete", "Prof Sash"]

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "public":
            await channel.send(f"Welcome to the server {member.mention}, what grade are you in?")

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name="public")
    await channel.send(f"{member.name} was expelled")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    swear_words = [f"fuck", "wtf", "69", "shit", "ass", "poes", "nob", "knob", "dick", "penis", "vagina", "taint", "bitch", "slut", "whore", "kak", "cunt"]

    for word in swear_words:
        if(word in message.content.lower()):
            response = getTune(message.author.name)
            await message.channel.send(response)

    if ("nigga" in message.content.lower()):
        responses = ["my niggaaa", "whatsup my homie", "whadup my nigga", "bitch ass nigga"]
        response = random.choice(responses)
        await message.channel.send(response)

    elif("--members" in message.content.lower()):
        x = message.server.members
        members = 0
        for member in x:
            members += 1

        await message.channel.send(members)
    await bot.process_commands(message)

@bot.command(name="timetable")
async def timetable(ctx, day: str):
    member = ctx.message.author
    Gr11_timetable = {
        "MONDAY" : ["Maths", "History/IT/Business", "Bio/Accounting", "CAT"],
        "TUESDAY" : ["Afrikaans", "History/Art/AS?", "Science/Bio/Drama", "AP Maths"],
        "WEDNESDAY" : ["S-Test", "Maths", "English", "AP English"],
        "THURSDAY" : ["Bio/Business", "Afrikaans", "History/IT/Accounting", "CAT"],
        "FRIDAY" : ["History/Art/AS?", "English", "Science/Bio/Drama"]
                        }

    times = ["08:20", "10:10", "12:00", "1:45"]
    roles = member.roles
    member_role = "N/A"
    member_role = roles[1]

    embed = discord.Embed(title=f"{member_role.name} Timetable", color=0xeee657)
    day = day.upper()


    if(member_role.name == "Grade 11"):
        subjects = Gr11_timetable[day]
        count = 0
        for subject in subjects:
            embed.add_field(name=f"{times[count]}", value=subject, inline=False)
            count += 1

    await ctx.send(embed=embed)
        
    

        
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="TeacherBot", description="This bot does a variety of things, including telling people off for swearing", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="NaTisVinceris")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite this bot to their server
    embed.add_field(name="Invite", value="https://discordapp.com/api/oauth2/authorize?client_id=699909192135475251&permissions=8&scope=bot")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="TeacherBot", description="This bot does a variety of things, including telling people off for swearing. List of commands are:", color=0xeee657)

    embed.add_field(name="!schoolsong", value="Gives the lyrics to the school song (Oakhill the Brave)", inline=False)
    embed.add_field(name="!f", value="Spams fs in the chat", inline=False)
    embed.add_field(name="!coronavirus", value="Gives current global and local covid-19 stats ", inline=False)
    embed.add_field(name="!covid_in 'country'", value="Gives covid-19 stats for a country (If country is more than one word, surround it by quotes)", inline=False)
    embed.add_field(name="!timetable 'day'", value="Gives the timetable for your grade for the day you have mentioned (ask @BOARD CHAIRMAN to add your grades timetable to the system)", inline=False)
    embed.add_field(name="!info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="!help", value="Gives this message", inline=False)


    await ctx.send(embed=embed)

@bot.command(name="schoolsong")
async def schoollyrics(ctx):
    lyrics = "OAKHILL THE BRAVE\nHark! When the night is falling\nHear, hear; a voice is calling –\nLoudly and proudly calling, singing the truth.\nThen, when the hills are sleeping\nNow feel the blood a-leaping,\nHigh as the spirit of our new Knysna youth.\nWhere – ere your name may roam –\nOakhill my Knysna home’\nHigh may your proud banner gloriously roam -,\nSchool of my high Endeavour,\nSchool on the shining river,\nSchool of my heart forever:\nOakhill the brave!"
    await ctx.send(lyrics)


@bot.command(name="f")
async def fsinchat(ctx):
    response = "F\nF\nF\nF\nF\nF\nF\nF\nF\nF"
    await ctx.send(response)

@bot.command(name="coronavirus")
async def getCoronaSummary(ctx):
    summ = data.Summary()
    country = os.getenv("COUNTRY")
    summ.country(country)
    local_stats = summ.localSit()
    response = f"GLOBAL:\n{summ}\n\nSOUTH AFRICA:\n{local_stats}"
    await ctx.send(response)

@bot.command(name="covid_in")
async def getCoronaInCountry(ctx, country: str):
    summ = data.Summary()
    summ.country(country)
    local_stats = summ.localSit()
    embed = discord.Embed(title=country, description="Current COVID-19 statistics", color=0xFF6347)
    embed.add_field(name="Total cases", value=summ.country_data["total_cases"], inline=False)
    embed.add_field(name="New cases", value=summ.country_data["new_cases"], inline=False)
    embed.add_field(name="Deaths", value=summ.country_data["total_deaths"], inline=False)
    
    await ctx.send(embed=embed)


    

def getTune(user):
    global teacher_list
    cur_teacher = random.choice(teacher_list)
    
    if(cur_teacher == "Mr Bell"):
        responses = ["*deafens you with his whistle*"]
    elif(cur_teacher == "Ms Viljouen"):
        responses = ["GET BACK TO CLASS %s!" % user, "SELF REGULATION %s!" % user]
    elif(cur_teacher == "Mr Entwistle"):
        responses = ["Oi, %s. Please behave." % user, "No man %s!" % user, "Great diction %s!" % user]
    elif(cur_teacher == "Dr Kitshoff"):
        responses = ["*Looks at you with rage*"]
    elif(cur_teacher == "Mr Kruger"):
        responses = ["GET OUTTTTT %s" % user, "Give me your phone %s" % user]
    elif(cur_teacher == "Mr Purchase"):
        responses = ["%s please stop being disrespectful." % user]
    elif(cur_teacher == "Ms Cloete"):
        responses = ["%s, the connotations of your language have some serious consequences!" % user]
    elif(cur_teacher == "Prof Sash"):
        responses = ["%s, don't make me discombobulate you!" % user, "what's good %s" % user]

    response = random.choice(responses)
    return f"[{cur_teacher}]: {response}"

bot.run(TOKEN)