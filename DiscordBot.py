import discord
import json,requests
from LoLSetup import RiotAPI
import random,re
import giphy_client

DCORD_CONFIG_FILE="Dcord.config"

f=open(DCORD_CONFIG_FILE,"r")
config1=json.load(f)
Token=config1["discord_token"]

client=discord.Client()

LOL_CONFIG_FILE="lol.config"

f=open(LOL_CONFIG_FILE,"r")
config2=json.load(f)
api_key=config2["api_key"]

lolclient=RiotAPI(api_key,"na1")

GIPHY_CONFIG_FILE="giphy.config"
gif_client=giphy_client.DefaultApi()

f2=open(GIPHY_CONFIG_FILE,"r")
config3=json.load(f2)
gif_api_key=config3["api_key"]



command_list={'!yasprofile':'!yasprofile [name] - returns the summoners name,level,and rank. Only for NA'
,'!yasitems':'!yasitem [item] - returns a description of the item you ask for'
,'!yasrandom':'!yasrandom - Be brave, returns a random champion, summoner spell sets, and items sets. Summoners Rift exclusive. Dont really recommend if you are new'
,'!yasrune':'!yasrune [rune]- returns a description of the rune that you ask for '
,'!yaspatchnotes':' !yaspatchnotes - returns the most recent patch notes - Sorry about the bad formatting. Scraped information to the best of my ability'
,'!yasinfo':'!yasinfo [champion_name] - returns info about the selected champion (UNFORTUNATELY THE ULT NUMBERS ARE OFF BECAUSE OF RIOT) '
,'!yashelp':'!yashelp - returns all commands and the descriptiuon of those comands'
,'!yas':'!yas - something special with Yasou '}

mythic_items=["Divine Sunderer","Duskblade of Draktharr","Eclipse","Everfrost","Frostfire Gauntlet","Galeforce","Goredrinker",
"Hextech Rocketbelt","Immortal Shieldbow","Imperial Mandate"," Kraken Slayer","Liandry's Anguish","Locket of the Iron Solari",
"Luden's Tempest","Moonstone Renewer","Night Harvester"," Prowler's Claw","Riftmaker","Shurelya's Battlesong","Stridebreaker",
"Sunfire Aegis","Trinity Force","Turbo Chemtank"]

final_items=["Divine Sunderer","Duskblade of Draktharr","Eclipse","Everfrost","Frostfire Gauntlet","Galeforce","Goredrinker",
"Hextech Rocketbelt","Immortal Shieldbow","Imperial Mandate"," Kraken Slayer","Liandry's Anguish","Locket of the Iron Solari",
"Luden's Tempest","Moonstone Renewer","Night Harvester"," Prowler's Claw","Riftmaker","Shurelya's Battlesong","Stridebreaker",
"Sunfire Aegis","Trinity Force","Turbo Chemtank","Abyssal Mask","Archangel's Staff","Ardent Censer","Banshee's Veil","Black Cleaver",
"Black Mist Scythe","Blade of the Ruined King","Bloodthirster","Bulwark of the Mountain","Chempunk Chainsword","Chempunk Chainsword","Chemtech Putrifier",
"Cosmic Drive","Dead Man's Plate","Death's Dance","Demonic Embrace","Edge of Night","Essence Reaver","Force of Nature","Frozen Heart",
"Gargoyle Stoneplate","Guardian Angel","Guinsoo's Rageblade","Horizon Focus","Infinity Edge","Knight's Vow","Lich Bane","Lord Dominik's Regards",
"Manamune","Maw of Malmortius","Mejai's Soulstealer","Mercurial Scimitar","Mikael's Blessing","Morellonomicon","Mortal Reminder","Muramana",
"Nashor's Tooth","Navori Quickblades","Pauldrons of Whiterock","Phantom Dancer","Rabadon's Deathcap","Randuin's Omen","Rapid Firecannon",
"Ravenous Hydra","Redemption","Runaan's Hurricane","Rylai's Crystal Scepter","Sanguine Blade","Seraph's Embrace","Serpent's Fang",
"Serylda's Grudge","Shard of True Ice","Silvermere Dawn","Spirit Visage","Staff of Flowing Water","Sterak's Gage","Stormrazor",
"The Collector","Thornmail","Titanic Hydra","Umbral Glaive","Vigilant Wardstone","Void Staff","Warmog's Armor","Wit's End","Youmuu's Ghostblade",
"Zeke's Convergence","Zhonya's Hourglass","Berserker's Greaves","Boots of Swiftness","Ionian Boots of Lucidity","Mercury's Treads","Mobility Boots",
"Plated Steelcaps","Sorcerer's Shoes"] 

boots=["Berserker's Greaves","Boots of Swiftness","Ionian Boots of Lucidity","Mercury's Treads","Mobility Boots",
"Plated Steelcaps","Sorcerer's Shoes"]

support=["Pauldrons of Whiterock","Shard of True Ice","Black Mist Scythe","Bulwark of the Mountain"]

crit_modifiers=["Guinsoo's Rageblade","Infinity Edge"]

hydra=["Ravenous Hydra","Titanic Hydra"]

wispher=["Lord Dominik's Regards","Serylda's Grudge"]

lifeline=["Immortal Shieldbow","Maw of Malmortius","Sterak's Gage"]

mana_charge=["Archangel's Staff","Manamune","Muramana"," Seraph's Embrace"]

quicksilver=["Mercurial Scimitar","Silvermere Dawn"]


champion_list=['Aatrox', 'Ahri', 'Akali', 'Alistar', 'Amumu', 'Anivia', 'Annie', 'Aphelios', 'Ashe', 'Aurelion Sol', 'Azir', 
'Bard', 'Blitzcrank', 'Brand', 'Braum', 'Caitlyn', 'Camille', 'Cassiopeia', "Cho'Gath", 'Corki', 'Darius', 'Diana', 'Draven', 
'Dr. Mundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 
'Gragas', 'Graves', 'Hecarim', 'Heimerdinger', 'Illaoi', 'Irelia', 'Ivern', 'Janna', 'Jarvan IV', 'Jax', 'Jayce', 'Jhin', 
'Jinx', "Kai'Sa", 'Kalista', 'Karma', 'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', "Kha'Zix", 'Kindred', 
'Kled', "Kog'Maw", 'LeBlanc', 'Lee Sin', 'Leona', 'Lillia', 'Lissandra', 'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 
'Maokai', 'Master Yi', 'Miss Fortune', 'Wukong', 'Mordekaiser', 'Morgana', 'Nami', 'Nasus', 'Nautilus', 'Neeko', 'Nidalee',
'Nocturne', 'Nunu & Willump', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 
"Rek'Sai", 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 'Seraphine', 'Sett', 'Shaco', 
'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 'Skarner', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'Tahm Kench', 'Taliyah', 
'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 'Twisted Fate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 
'Vayne', 'Veigar', "Vel'Koz", 'Vi', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Xayah', 'Xerath', 'Xin Zhao', 'Yasuo', 
'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Ziggs', 'Zilean', 'Zoe', 'Zyra']

ranged_and_meele=["Elise","Gnar","Jayce","Kayle","Nidalee"]

meele=['Aatrox','Akali','Alistar', 'Amumu','Blitzcrank','Braum','Camille',"Cho'Gath",'Darius', 'Diana','Dr. Mundo',
'Ekko', 'Elise', 'Evelynn','Fiora', 'Fizz','Galio', 'Gangplank', 'Garen', 'Gnar','Gragas','Hecarim','Illaoi', 'Irelia',
'Jarvan IV', 'Jax', 'Jayce','Kassadin','Katarina','Kayn',"Kha'Zix",'Kled','Lee Sin', 'Leona','Malphite','Maokai', 'Master Yi',
'Mordekaiser','Nasus','Nautilus','Nidalee','Nocturne', 'Nunu & Willump','Olaf','Ornn','Pantheon', 'Poppy', 'Pyke','Qiyana','Rammus', 
"Rek'Sai", 'Rell', 'Renekton', 'Rengar', 'Riven', 'Rumble','Sejuani','Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion','Skarner',
'Sylas','Tahm Kench','Talon', 'Taric','Trundle', 'Tryndamere','Udyr','Vi','Volibear','Warwick','Wukong','Xin Zhao','Yasuo', 
'Yone', 'Yorick','Zac', 'Zed']


role=["Top","Jungle","Mid","ADC","Support"]

summoners=["Heal","Ghost","Barrier","Exhaust","Clarity","Flash","Teleport","Smite","Cleanse","Ignite"]

rune_tree=["Precision","Domination","Sorcery","Resolve","Inspiration"]


@client.event
async def on_ready():
    print('League bot ready to go. Type !yashelp for a list of commands ')

@client.event
async def on_message(message):
    if message.author==client.user:
        pass
    else:
        arg=message.content.split(' ')
        if arg[0]=="!yasprofile" and len(arg)>1:
            try:
                embed=discord.Embed(color=0x00ff00)
                embed.title=arg[1]+" info "
                simple_info=profile_function(arg[1])[0]
                rank_info=profile_function(arg[1])[1]
                embed.set_author(name="YasProfile: "+arg[1],icon_url=summoner_icon_function(arg[1]))
                embed.set_thumbnail(url=summoner_icon_function(arg[1]))
                embed.add_field(name="name",value=simple_info["name"],inline=False)
                embed.add_field(name="level",value=simple_info["level"],inline=False)
                for ranks in rank_info:
                    embed.add_field(name=ranks[0],value=ranks[1],inline=False)
                print("Print successful")
                await message.channel.send(embed=embed)
            except:
                print("Print unsucessful")
                await message.channel.send("Summoner not found in NA or something went wrong")
        if arg[0]=="!yashelp":
            embed=discord.Embed(color=0x00ff00)
            embed.title="List and Description of commands"
            embed.description=help_function()
            await message.channel.send(embed=embed)
        if arg[0]=="!yasitem" and len(arg)>1:
            item=""
            try:
                for i in range(1,len(arg)):
                    if i==len(arg)-1:
                        item+=arg[i]
                    else:    
                        item+=arg[i]+" "
                embed=discord.Embed(color=0x00ff00)
                embed.title=get_item_function(item)["name"]+" Info"
                embed.set_author(name="YasItem: "+ get_item_function(item)["name"],icon_url=item_icon_function(item))
                embed.set_thumbnail(url=item_icon_function(item))
                embed.add_field(name="Name",value=get_item_function(item)["name"],inline=False)
                embed.add_field(name="Stats",value=get_item_function(item)["stats"],inline=False)
                embed.add_field(name="Description",value=get_item_function(item)["description"],inline=False)
                embed.add_field(name="Cost",value=get_item_function(item)["cost"],inline=False)
                print("Print successful")
                await message.channel.send(embed=embed)
            except:
                await message.channel.send("Item not found")
        if arg[0]=="!yasinfo" and len(arg)>1:
            try:
                champion=""
                for i in range(1,len(arg)):
                    if(i==len(arg)-1):
                        champion+=arg[i]
                    else:
                        champion+=arg[i]+" "
                champ_stats=champ_info_function(champion)[2]
                stats="Health:"+str(champ_stats["hp"])+" (+"+str(champ_stats["hpperlevel"])+")\nMana:"+str(champ_stats["mp"])+" (+"+str(champ_stats["mpperlevel"])+")\n"+"Movement Speed:"+str(champ_stats["movespeed"])+"\nArmor:"+str(champ_stats["armor"])+" (+"+str(champ_stats["armorperlevel"])+")\nMagic Resist:"+str(champ_stats["spellblock"])+" (+"+str(champ_stats["spellblockperlevel"])+")\nAttack Range:"+str(champ_stats["attackrange"])+"\nHealth Regen:"+str(champ_stats["hpregen"])+" (+"+str(champ_stats["hpregenperlevel"])+")\nMana Regen:"+str(champ_stats["mpregen"])+" (+"+str(champ_stats["mpregenperlevel"])+")\nAttack Damage:"+str(champ_stats["attackdamage"])+" (+"+str(champ_stats["attackdamageperlevel"])+")\nAttack Speed:"+str(champ_stats["attackspeed"])+" (+"+str(champ_stats["attackspeedperlevel"])+")"
                champ_abilities=champ_info_function(champion)[3]
                abilities=[]
                cleaner = re.compile('<.*?>')
                for i in champ_abilities:
                    abilities.append({"name":i["name"],"description":re.sub(cleaner,'',i["description"]),"effect":i["effect"][1],"cost":i["cost"],"range":str(i["rangeBurn"])})
                embed=discord.Embed(color=0x00ff00)
                embed.title=champ_info_function(champion)[0]+" Info"
                embed.description="Note: The Ultimate Numbers are wrong because of Riot"
                embed.set_thumbnail(url=champ_icon_function(champion))
                embed.add_field(name="Lore",value=champ_info_function(champion)[1],inline=False)
                embed.add_field(name="Stats:",value=stats,inline=True)
                embed.add_field(name="Q: "+abilities[0]["name"],value=abilities[0],inline=False)
                embed.add_field(name="W: "+abilities[1]["name"],value=abilities[1],inline=False)
                embed.add_field(name="E: "+abilities[2]["name"],value=abilities[2],inline=False)
                embed.add_field(name="R: "+abilities[3]["name"],value=abilities[3],inline=False)
                print("Print sucessful")
                await message.channel.send(embed=embed)
            except:
                print("Print unsucessful")
                await message.channel.send("Champion not found")
        if arg[0]=="!yasrune" and len(arg)>1:
            try:
                rune=""
                for i in range(1,len(arg)):
                    if(i==len(arg)-1):
                        rune+=arg[i]
                    else:
                        rune+=arg[i]+" "
                rune_info=rune_function(rune)
                embed=discord.Embed(color=0x00ff00)
                embed.title=rune_info[1]["name"]
                embed.set_thumbnail(url=rune_icon_function(rune))
                embed.add_field(name="Tree:",value=rune_info[0],inline=False)
                cleaner = re.compile('<.*?>')
                embed.add_field(name="Description",value=re.sub(cleaner,' ',rune_info[1]["longDesc"]),inline=False)
                print("Print sucessful")
                await message.channel.send(embed=embed)
            except:
                print("Print Unsucessful")
                await message.channel.send("Rune not found")
        if arg[0]=="!yaspatchnotes":
            patch_notes=get_patchnotes_function()
            lst=parsing_patchnotes(patch_notes,100)
            write_patchnotes_tofile(lst)
            with open("patchnotes.txt", "rb") as file:
                await message.channel.send("Patch Notes",file=discord.File(file,"patchnotes.txt"))
            embed=discord.Embed(title="Patch Notes Link",url="https://na.leagueoflegends.com/en-us/news/game-updates/patch-10-25-notes/",color=0x00ff00)
            print("Print sucessful")
            await message.channel.send(embed=embed)
        if arg[0]=="!yasrandom":
            random_stuff=all_random_function()
            embed=discord.Embed(color=0x00ff00)
            embed.title="RANDOM BUILD"
            embed.set_thumbnail(url=champ_icon_function(random_stuff[0]))
            embed.add_field(name="Name",value=random_stuff[0],inline=False)
            embed.add_field(name="Role",value=random_stuff[1],inline=False)
            embed.add_field(name="Summoner Spell 1",value=random_stuff[2],inline=False)
            embed.add_field(name="Summoner Spell 2",value=random_stuff[3],inline=False)
            embed.add_field(name="Primary Rune Tree",value=random_stuff[4],inline=False)
            embed.add_field(name="Secondary Rune Tree",value=random_stuff[5],inline=False)
            embed.add_field(name="Item",value=random_stuff[6],inline=False)
            embed.add_field(name="Item",value=random_stuff[7],inline=False)
            embed.add_field(name="Item",value=random_stuff[8],inline=False)
            embed.add_field(name="Item",value=random_stuff[9],inline=False)
            embed.add_field(name="Item",value=random_stuff[10],inline=False)
            embed.add_field(name="Item",value=random_stuff[11],inline=False)
            print("Print sucessful")
            await message.channel.send(embed=embed)
        if arg[0]=="!yas":
            print("Print sucessful")
            await message.channel.send("URL :"+yasou_function())
            

def profile_function(user):
    summoner=lolclient.request_summoner(user)
    id = summoner["id"]
    rank=lolclient.request_summoner_rank(id)
    name_level={"name":summoner["name"],"level":str(summoner["summonerLevel"])}
    ranks=[]
    for entries in rank:
        r=entries["tier"]+ " "+str(entries["rank"])+ " "+str(entries["leaguePoints"])+ " LP/ "+str(entries["wins"]) + "W "+ str(entries["losses"])+ "L\nWinrate: "+format(entries["wins"]/(entries["wins"]+entries["losses"])*100,'.0f')+"%"
        ranks.append((entries["queueType"],r))
    return name_level,ranks

def get_item_function(item):
    with open('ListofItems.json') as f:
        data = json.load(f)
    stuff=data["data"]
    for items in stuff:
        if(stuff[items]["name"].upper().replace("'","").replace("-","").replace(".","").replace(" ","")==item.upper().replace("'","").replace("-","").replace(".","").replace(" ","")):
            return {"name":stuff[items]["name"],"stats":stuff[items]["stats"],"description":stuff[items]["description"],"cost":stuff[items]["cost"]}
    raise Exception("Item not found")
        

def item_icon_function(item):
    return lolclient.request_item_icon(item)

def all_random_function():
    lst=[]
    items=[]
    champ=random.choice(champion_list)
    lst.append(champ)
    r=random.choice(role)
    lst.append(r)
    summoner_spells=get_summoner_spells(r)
    for i in summoner_spells:
        lst.append(i)
    primary_tree=random.choice(rune_tree)
    lst.append(primary_tree)
    secondary_tree=random.choice(rune_tree)
    while(secondary_tree==primary_tree):
        secondary_tree=random.choice(rune_tree)
    lst.append(secondary_tree)
    for i in range(6):
        items.append(random.choice(final_items))
    it=check_item_list(items,champ)
    for i in it:
        lst.append(i)
    return lst

def check_item_list(item_lst,champion):
    mythic_counter=0
    boots_counter=0
    support_counter=0
    crit_modifier=0
    hydra_counter=0
    wispher_counter=0
    lifeline_counter=0
    mana_charge_counter=0
    quicksilver_counter=0
    while(True):
        if(champion=="Cassiopeia"):
            for i in item_lst:
                if i in mythic_items:
                    mythic_counter+=1
                if i in boots:
                    boots_counter+=1
                if i in support:
                    support_counter+=1
                if i in crit_modifiers:
                    crit_modifier+=1
                if i in hydra:
                    hydra_counter+=1
                if i in wispher:
                    wispher_counter+=1
                if i in lifeline:
                    lifeline_counter+=1
                if i in mana_charge:
                    mana_charge_counter+=1
                if i in quicksilver:
                    quicksilver_counter+=1
                if mythic_counter>1 or boots_counter>0 or support_counter>1 or crit_modifier>1 or hydra_counter>1 or wispher_counter>1 or lifeline_counter>1 or mana_charge_counter>1 or quicksilver_counter>1:
                    item_lst.remove(i)
                    item_lst.append(random.choice(final_items))
                    check_item_list(item_lst,champion)
        else:
            if champion in meele and champion not in ranged_and_meele:
                for i in item_lst:
                    if i in mythic_items:
                        mythic_counter+=1
                    if i in boots:
                        boots_counter+=1
                    if i in support:
                        support_counter+=1
                    if i in crit_modifiers:
                        crit_modifier+=1
                    if i in hydra:
                        hydra_counter+=1
                    if i in wispher:
                        wispher_counter+=1
                    if i in lifeline:
                        lifeline_counter+=1
                    if i in mana_charge:
                        mana_charge_counter+=1
                    if i in quicksilver:
                        quicksilver_counter+=1
                    if i=="Runaan's Hurricane":
                        item_lst.remove(i)
                        item_lst.append(random.choice(final_items))
                        check_item_list(item_lst,champion)
                    if mythic_counter>1 or boots_counter>1 or support_counter>1 or crit_modifier>1 or hydra_counter>1 or wispher_counter>1 or lifeline_counter>1 or mana_charge_counter>1 or quicksilver_counter>1:
                        item_lst.remove(i)
                        item_lst.append(random.choice(final_items))
                        check_item_list(item_lst,champion)
            else:
                for i in item_lst:
                    if i in mythic_items:
                        mythic_counter+=1
                    if i in boots:
                        boots_counter+=1
                    if i in support:
                        support_counter+=1
                    if i in crit_modifiers:
                        crit_modifier+=1
                    if i in hydra:
                        hydra_counter+=1
                    if i in wispher:
                        wispher_counter+=1
                    if i in lifeline:
                        lifeline_counter+=1
                    if i in mana_charge:
                        mana_charge_counter+=1
                    if i in quicksilver:
                        quicksilver_counter+=1
                    if mythic_counter>1 or boots_counter>1 or support_counter>1 or crit_modifier>1 or hydra_counter>1 or wispher_counter>1 or lifeline_counter>1 or mana_charge_counter>1 or quicksilver_counter>1:
                        item_lst.remove(i)
                        item_lst.append(random.choice(final_items))
                        check_item_list(item_lst,champion)
        unique=[]
        duplicate=[]
        for i in item_lst:
            if i not in unique:
                unique.append(i)
            else:
                duplicate.append(i)
        print(unique)
        print(duplicate)
        if len(duplicate)!=0:
            for i in duplicate:
                item_lst.remove(i)
            for i in duplicate:
                item_lst.append(random.choice(final_items))
            check_item_list(item_lst,champion)
        break
    return item_lst

def get_summoner_spells(role):
    lst=[]
    if role=="Jungle":
        lst.append("Smite")
        first="Smite"
        second=random.choice(summoners)
        while(first==second):
            second=random.choice(summoners)
        lst.append(second)
    else:
        first=random.choice(summoners)
        second=random.choice(summoners)
        lst.append(first)
        while(first==second):
            second=random.choice(summoners)
        lst.append(second)
    return lst


def rune_function(rune):
    return lolclient.request_rune(rune)

def rune_icon_function(rune):
    return lolclient.request_rune_icon(rune)

def get_patchnotes_function():
    return lolclient.request_patch_notes()

def parsing_patchnotes(lst,max_length):
    l=[]
    counter=0
    string=""
    for i in lst:
        if(counter==max_length):
            string+=i+" "
            l.append(string)
            counter=0
            string=""
        else:
            if i in champion_list:
                string+="\n\n"
            if i in final_items:
                string+="\n\n"
            string+=i+" "
            counter+=1
    return l

def write_patchnotes_tofile(lst):
    f=open("patchnotes.txt","w")
    for i in lst:
        f.write(i)
    f.close()



def champ_info_function(champion):
    return lolclient.request_champion(champion)

def champ_icon_function(champion):
    return lolclient.request_champion_icon(champion)

def help_function():
    string="Commands for the bot and what they do:\n\n"
    i=1
    for k,v in command_list.items():
        string+=str(i)+".  " +str(v)+"\n\n"
        i+=1
    return string

def yasou_function():
    response=gif_client.gifs_search_get(gif_api_key,"yasuo",limit=100,rating='g')
    lst=list(response.data)
    gif=random.choices(lst)

    return gif[0].url

def summoner_icon_function(user):
   icon=lolclient.request_profile_icon(user)
   return icon 
    


    


client.run(Token)
