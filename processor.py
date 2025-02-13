class Processor:
    def __init__(self, users: list, current_guild: str):
        self.__users__ = users
        self.current_guild = current_guild
    
    def get_mutuals(self):
        mutual_servers_dict = {}
        for user in self.__users__:
            if user["bot"] == False:
                mutual_servers = user["mutual_guilds"]
                _ = (mutual_servers.pop(mutual_servers.index(self.current_guild)) if self.current_guild in mutual_servers else None)
                if len(mutual_servers) < 2:
                    if mutual_servers[0] not in mutual_servers_dict.keys():
                        mutual_servers_dict[mutual_servers[0]] = []
                    mutual_servers_dict[mutual_servers[0]].append(
                        {
                            "name": user["name"],
                            "id": user["id"],
                            "global_name": user["global_name"],
                            "avatar": user["avatar"]
                        }
                    )
                else:
                    for mutual_server in mutual_servers:
                        if mutual_server not in mutual_servers_dict.keys():
                            mutual_servers_dict[mutual_server] = []
                        mutual_servers_dict[mutual_server].append(
                            {
                                "name": user["name"],
                                "id": user["id"],
                                "global_name": user["global_name"],
                                "avatar": user["avatar"]
                            }
                        )
            
        return mutual_servers_dict
    
    @staticmethod
    def group_mutual_users(cls, mutual_servers_dict: dict = None):
        if mutual_servers_dict == None:
            mutual_servers_dict = self.get_mutuals()
        
        users = {}

        for guild_id in mutual_servers_dict:
            for user in mutual_servers_dict[guild_id]:
                if user['name'] in users:
                    users[user['name']]['guilds'].append(guild_id)

                else:
                    users[user['name']] = user
                    
                    if "guilds" not in users[user['name']]:
                        users[user['name']]['guilds'] = []
                    
                    users[user['name']]['guilds'].append(guild_id)

        return users
