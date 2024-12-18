class Processor:
    def __init__(self, users: list, current_guild: str):
        self.__users__ = users
        self.current_guild = current_guild
    
    def get_mutuals(self):
        mutual_servers_dict = {}
        for user in self.__users__:
            if user["bot"] == False:
                mutual_servers = user.mutual_guilds
                mutual_servers.remove(self.current_guild)

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
    
