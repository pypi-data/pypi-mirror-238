import aiohttp
import json

LINK_STATS = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/stats.json"
LINK_WEAPON = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/weapons.json"
LINK_AVATAR = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/avatar.json"
LINK_RELICT_SETS = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/relict_sets.json"
LINK_PATH = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/paths.json"
LINK_ELEMENT = "https://raw.githubusercontent.com/DEViantUA/StarRailCardUA/main/element.json"

data_stats = {}
data_weapon = {}
data_avatar = {}
data_relict_sets = {}
data_paths = {}
data_element = {}

async def get_json_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                text = await response.text()
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return None
            else:
                return None
            
async def get_translate_data():
    global data_stats
    global data_weapon
    global data_avatar
    global data_relict_sets
    
    if data_stats == {}:
        data_stats = await get_json_data(LINK_STATS)
        
    if data_weapon == {}:
        data_weapon = await get_json_data(LINK_WEAPON)
    
    if data_avatar == {}:
        data_avatar = await get_json_data(LINK_AVATAR)
        
    if data_relict_sets == {}:
        data_relict_sets = await get_json_data(LINK_RELICT_SETS)
    
    if data_paths == {}:
        data_paths = await get_json_data(LINK_RELICT_SETS)
    
    if data_element == {}:
        data_paths = await get_json_data(LINK_RELICT_SETS)
    
    return data_stats,data_weapon,data_avatar,data_relict_sets,data_paths,data_element