import requests


class LeagueAPI:

    def __init__(self, api_key="", platform="kr", region="asia"):   
        self.api_key = api_key
        self.platform = platform
        self.region = region

    def get_current_gameInfo(self,
                            encryptedSummonerId
                            ):     
        url = f'https://{self.platform}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{encryptedSummonerId}'
        res = requests.get(
                        url=url,
                        headers={
                            "X-Riot-Token":self.api_key
                        }
                )
        res.raise_for_status()
        
        return res

    def get_recent_matchId(self, 
                            summoner_name,
                            startTime=None,
                            endTime=None,
                            queue=None,
                            type=None,
                            start=0,
                            count=20
                        ):
        """Get a list of match ids by puuid

        summoner_name: str      #소환사 명.
        startTime: long         #Epoch timestamp in seconds. (>06-16-2021)
        endTime: long           #Epoch timestamp in seconds.
        queue: int              #
        type: string            #
        start: int              #Defaults to 0. Start index.
        count: int              #Defaults to 20. (valid: 0 to 100)

        return -> List[string]
        """
        
        summonerDto = self._get_summonerDto(summoner_name=summoner_name)
        puuid = summonerDto['puuid']
        
        url = f'https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids'
        res = requests.get(
                        url=url,
                        headers={
                            "X-Riot-Token":self.api_key
                        },
                        params={
                            "startTime":startTime,
                            "endTime":endTime,
                            "queue":queue,
                            "type":type,
                            "start":start,
                            "count":count
                        }
                )
        res.raise_for_status()

        return res.json()

    def get_summonerDto(self, summoner_name):
        return self._get_summonerDto(summoner_name=summoner_name)

    def _get_summonerDto(self, summoner_name):
        url = f'https://{self.platform}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}'
        res = requests.get(
                        url=url,
                        headers={
                            "X-Riot-Token":self.api_key
                        }    
                )   
        res.raise_for_status()

        return res.json()

    def get_matchDto(self, matchId):
        url = f'https://{self.region}.api.riotgames.com/lol/match/v5/matches/{matchId}'
        res = requests.get(
                        url=url,
                        headers={
                            "X-Riot-Token":self.api_key
                        }
                )
        res.raise_for_status()

        return res.json()


    
if __name__ == '__main__':
    lol = LeagueAPI(api_key="Your API KEY")
    
    summoner = lol.get_summonerDto(summoner_name="소환사 명")
    matchIds = lol.get_recent_matchId(summoner_name="소환사 명")
    match = lol.get_matchDto(matchId="matchId")