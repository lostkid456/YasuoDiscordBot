import json,requests
import re 


region="na1"
LOL_CONFIG_FILE="lol.config"

class RiotAPI():

    def __init__(self,api_key,region=region):
        self.api_key=api_key
        self.region=region
    
    def get_api_version(self):
        api_url="https://ddragon.leagueoflegends.com/api/versions.json"
        response=requests.get(api_url)
        return response.json()
        
    
    def request_summoner(self,name):
        summoner_url="https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name+"?api_key="+self.api_key
        response=requests.get(summoner_url)
        if(response.status_code==404):
            raise Exception("Summoner not found")   
        return response.json()
    
    def request_summoner_rank(self,id):
        ranked_url="https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+id+"?api_key="+self.api_key
        response=requests.get(ranked_url)
        if(response.status_code==404):
            raise Exception("Summoner not found")  
        return response.json()
    
    def request_profile_icon(self,name):
        summoner_url="https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+name+"?api_key="+self.api_key
        response=requests.get(summoner_url)
        stuff=response.json()
        if(response.status_code==404):
            raise Exception("Summoner not found")  
        icon=stuff['profileIconId']
        profile_data_url="http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/img/profileicon/"+  str(icon) +".png"
        return profile_data_url
    
    
    def request_item_icon(self,item):
        items_url="http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/data/en_US/item.json"
        response=requests.get(items_url)
        stuff=response.json()
        items=stuff["data"]
        for i in items: 
            if(items[i]["name"].upper().replace("'","").replace("-","").replace(" ","").replace(".","")==item.upper().replace("'","").replace("-","").replace(" ","").replace(".","")):
                return "http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/img/item/"+str(i)+".png"
        raise Exception("Item not found")

    def request_champion(self,champion):
        champion_url="http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/data/en_US/champion.json"
        response=requests.get(champion_url)
        champ_list=response.json()
        champs=champ_list["data"]
        for i in champs:
            if(champs[i]["name"].upper().replace(".","").replace("'","").replace(" ","")==champion.upper().replace(".","").replace("'","").replace(" ","")):
                champ_url="http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/data/en_US/champion/"+str(champs[i]["id"])+".json"
                r=requests.get(champ_url)
                champ=r.json()
                champ_lore=champ["data"][str(champs[i]["id"])]["lore"]
                champ_stats=champ["data"][str(champs[i]["id"])]["stats"]
                champ_abilities=champ["data"][str(champs[i]["id"])]["spells"]
                champ_passive=champ["data"][str(champs[i]["id"])]["passive"]
                return str(champs[i]["name"]),champ_lore,champ_stats,champ_abilities,champ_passive
        raise Exception("Champion not found")
    
    def request_champion_icon(self,champion):
        champion_url="http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/data/en_US/champion.json"
        response=requests.get(champion_url)
        champ_list=response.json()
        champs=champ_list["data"]
        for i in champs:
            if(champs[i]["name"].upper().replace(".","").replace("'","").replace(" ","")==champion.upper().replace(".","").replace("'","").replace(" ","")):
                return "http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/img/champion/"+champs[i]["id"]+".png"
    
    def request_rune(self,rune):
        try:
            rune_url="http://ddragon.leagueoflegends.com/cdn/"+str(self.get_api_version()[0])+"/data/en_US/runesReforged.json"
            response=requests.get(rune_url)
            rune_list=response.json()
            for i in rune_list:
                tree=i["key"]
                for i in i["slots"]:
                    for i in i["runes"]:
                        if(i["name"].upper().replace(" ","").replace(":","")==rune.upper().replace(" ","").replace(":","")):
                            return tree,i
        except:
            raise Exception("Rune not found")

    def request_rune_icon(self,rune):
        return "https://ddragon.leagueoflegends.com/cdn/img/"+str(self.request_rune(rune)[1]["icon"])
    
    def request_patch_notes(self):
        patch_url="https://lolstatic-a.akamaihd.net/frontpage/apps/prod/harbinger-l10-website/en-us/production/en-us/page-data/news/game-updates/patch-10-25-notes/page-data.json"
        response=requests.get(patch_url)
        patch_note=response.json()
        string=""
        cleaner = re.compile('<.*?>')
        for i in patch_note["result"]["pageContext"]["data"]["sections"]:
            string+=re.sub(cleaner,' ',i["props"]["content"]).replace("&rArr;","->")
        return string.split()


