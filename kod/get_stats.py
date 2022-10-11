import pandas as pd 
from get_data import Game
import general_functions as gf


class Stats:
# class variables
    possession_gained = {'skott', 'frislag', 'närkamp', 'inslag', 'utkast', 'avslag', 
                        'friläge', 'boll', 'brytning', 'passning'}    
    possession_lost = {'bolltapp', 'rensning', 'offside'}
    await_next = {'timeout', 'mål', 'stop', 'utvisning', 'hörna', 'straff', 'skottyp'}
    start_of_play = {'avslag', 'frislag', 'inslag', 'utkast', 'hörna', 'straff'}

# constructor
    def __init__(self, teams: set, filename: str, dummy = False) -> None:
        # this is where we put everything we're printing
        self.prints = dict()
        # dummy is only used if we are adding two ojects
        if not dummy: 
            self.teams = teams
            self.big_df = gf.read_csv_as_df(filename)
            self.df_dict = dict()
            self.out = filename + '.txt'
            self.possession_list = list()
            
        return

# dunder add, for Stats() + Stats()
    def __add__(self, other) -> None:
        if not isinstance(other, Stats):
            return NotImplemented
        # new empty object
        obj = Stats(set(), str(), dummy = True)
        obj.out = f'{self.out[:-4]} och {other.out}'
        obj.teams = self.teams
        obj.prints['score'] = self.add_score(other)
        obj.prints['possession'] = self.add_possession(other)
        obj.prints['duels'] = self.add_duels(other)
        obj.prints['shot types'] = self.add_shottypes(other)
        obj.prints['shot origins'] = self.add_shot_origins(other)
        #obj.write_stats() removing this to better resemble the constructor
        return obj

# non-static methods
    def write_stats(self) -> None:
        '''calls all write methods in order
            writing to the output file'''
        self.write_header()
        self.write_score()
        self.write_possession()
        self.write_duels()
        self.write_shottypes()
        self.write_shot_origins()
        return

    def write_header(self) -> None:
        '''writes the team names
            must be called first in order for the txt file to look good'''
        with open(self.out, 'w', encoding='utf-8') as f:
            f.write(f'{" - ".join(self.teams).title()} \n')
            f.write(f'\tdata från: {self.out[:-4]}\n')
        return 

    def get_score_dict(self) -> dict:
        '''returns a dictionary of the score
            if need be it fills self.prints'''
        if 'score' not in self.prints:
            score_df = self.get_score_df()
            score_dict = {team: 0 for team in self.teams}
            for team in score_dict:
                score_dict[team] = len(score_df.loc[score_df['team'] == team].index)
            self.prints['score'] = score_dict
        return self.prints['score']

    def write_score(self) -> None:
        '''prints the score to the output file'''
        score_dict = self.get_score_dict()
        with open(self.out, 'a', encoding='utf-8') as f:
            f.write('Mål \n')
            for team in score_dict:
                f.write(f'\t{team.title()}: {score_dict[team]} \n')
        return

    def add_score(self, other) -> dict:
        '''returns the score of the added objects
            expects type to already have been checked'''
        return_dict = dict()
        for team in self.prints['score']:
            return_dict[team] = self.prints['score'][team] + other.prints['score'][team]
        return return_dict

    def get_duels_dict(self) -> dict:
        '''returns a dictionary of the duels
            if need be it fills self.prints'''
        if 'duels' not in self.prints:
            duels_df = self.get_duels_df()
            duels_dict = {team: 0 for team in self.teams}
            for team in duels_dict:
                duels_dict[team] = len(duels_df.loc[duels_df['team'] == team].index)
            self.prints['duels'] = duels_dict
        return self.prints['duels']

    def write_duels(self) -> None:
        '''calculates the score and writes it to the output file'''
        duels_dict = self.get_duels_dict()
        with open(self.out, 'a', encoding='utf-8') as f:
            f.write('Närkamper och brytningar \n')
            for team in duels_dict:
                f.write(f'\t{team.title()}: {duels_dict[team]} \n')
        return

    def add_duels(self, other) -> dict:
        '''returns the duels of the added objects
            expects type to already have been checked'''
        return_dict = dict()
        for team in self.prints['duels']:
            return_dict[team] = self.prints['duels'][team] + other.prints['duels'][team]
        return return_dict

    def get_possession_dict(self) -> dict:
        '''returns a dictionary of the possession
            if need be it fills self.prints'''
        if 'possession' not in self.prints:
            poss_dict = {team: 0 for team in self.teams}
            self.make_possession_list()
            for i in range(len(self.possession_list) - 1):
                if self.possession_list[i][0] in self.teams: # this is the current team
                    poss_dict[self.possession_list[i][0]] += gf.readable_to_sec(self.possession_list[i+1][1]) - gf.readable_to_sec(self.possession_list[i][1])
            for team in poss_dict:
                poss_dict[team] = gf.sec_to_readable(poss_dict[team])
            self.prints['possession'] = poss_dict
        return self.prints['possession']

    def write_possession(self) -> None:
        '''calculates the possession based on poss_list and writes it to output
            possession_list looks like [[team, time], [team, time] ... ]'''
        poss_dict = self.get_possession_dict()
        with open(self.out, 'a', encoding='utf-8') as f:
            f.write('Bollinnehav \n')
            for team in poss_dict:
                f.write(f'{team.title()}: {poss_dict[team]} \n')
        return

    def add_possession(self, other) -> dict:
        '''returns the possession of the two added objects
            expects type to already have been checked'''
        return_dict = dict()
        for team in self.prints['possession']:
            return_dict[team] = gf.sec_to_readable(gf.readable_to_sec(self.prints['possession'][team]) + gf.readable_to_sec(other.prints['possession'][team]))
        return return_dict

    def get_shottypes_dict(self) -> dict:
        '''returns a dictionary of the shot types
            if need be it fills self.prints'''
        if 'shot types' not in self.prints:
            st_dict = {team: dict() for team in self.teams}
            for team in self.teams:
                st_df = self.get_shottypes_df().loc[self.get_shottypes_df()['team'] == team]
                for shottype in Game.events_and_their_subevents['skottyp']:
                    if len(st_df.loc[st_df['subevent'] == shottype].index) > 0:
                        st_dict[team][shottype] = len(st_df.loc[st_df['subevent'] == shottype].index)
            self.prints['shot types'] = st_dict
        return self.prints['shot types']

    def write_shottypes(self) -> None:
        '''writes the shot types for each team to output'''
        st_dict = self.get_shottypes_dict()
        with open(self.out, 'a', encoding='utf-8') as f:
            f.write('Skottyper \n')
            for team in st_dict:
                f.write(f'{team.title()} \n')
                for shottype in st_dict[team]:
                    f.write(f'\t{shottype}: {st_dict[team][shottype]} \n')
        return 

    def add_shottypes(self, other) -> dict:
        '''returns the shot types of the added objects
            expects type to already have been checked'''
        return_dict = {team: dict() for team in self.teams}
        for team in self.prints['shot types']:
            for shottype in self.prints['shot types'][team]:
                if shottype in other.prints['shot types'][team]:
                    return_dict[team][shottype] = self.prints['shot types'][team][shottype] + other.prints['shot types'][team][shottype]
                else:
                    return_dict[team][shottype] = self.prints['shot types'][team][shottype] 
            for shottype in other.prints['shot types'][team]:
                if shottype not in return_dict[team]:
                    return_dict[team][shottype] = other.prints['shot types'][team][shottype]
        return return_dict

    def shot_origins_df(self) -> pd.core.frame.DataFrame:
        '''returns a df object of shot origins
            fills the df_dict if need be'''
        if 'shot origins' not in self.df_dict:
            keys = ['team', 'shot origin', 'attack time', 'goal']
            values = [[] for i in range(len(keys))]
            possession_team = None
            possession_gained = None
            time_gained = 0 

            for index, row in self.big_df.iterrows():
                # a shot is made; save shot origin info
                if row['event'] == 'skott' or row['event'] == 'mål':
                    values[0].append(possession_team)
                    values[1].append(possession_gained)
                    values[2].append(gf.readable_to_sec(row['time']) - time_gained)
                    values[3].append(row['event'] == 'mål')
                # new team gains possession OR new start of play
                elif (row['event'] in Stats.possession_gained and row['team'] != possession_team) or row['event'] in Stats.start_of_play:
                    possession_team = row['team']
                    possession_gained = row['event']
                    time_gained = gf.readable_to_sec(row['time'])
                # old team loses possession
                elif row['event'] in Stats.possession_lost and row['team'] == possession_team:
                    possession_team = self.opposite_team(row['team'])
                    possession_gained = row['event']
                    time_gained = gf.readable_to_sec(row['time'])
            self.df_dict['shot origins'] = gf.make_df(keys, values)
        return self.df_dict['shot origins']

    def shot_origins_dict(self) -> dict:
        '''returns a dictionary of the shot origins
            if need be it fills self.prints'''
        if 'shot origins' not in self.prints:
            so_df = self.shot_origins_df()
            so_dict = {team: dict() for team in self.teams}
            for index, row in so_df.iterrows():
                if row['shot origin'] in so_dict[row['team']]:
                    so_dict[row['team']][row['shot origin']] += 1
                else:
                    so_dict[row['team']][row['shot origin']] = 1
            self.prints['shot origins'] = so_dict
        return self.prints['shot origins']

    def write_shot_origins(self) -> None:
        '''writes the shot origin info to output'''
        so_dict = self.shot_origins_dict()
        with open(self.out, 'a', encoding='utf-8') as f:
            f.write('Skottens ursprung\n')
            for team in so_dict:
                f.write(f'{team.title()}:\n')
                for so in so_dict[team]:
                    f.write(f'\t{so}: {so_dict[team][so]}\n')

    def add_shot_origins(self, other) -> dict:
        '''returns the shot origins of the added objects
            expects type to already have been checked'''
        return_dict = {team: dict() for team in self.teams}
        for team in self.prints['shot origins']:
            for shotorigin in self.prints['shot origins'][team]:
                if shotorigin in other.prints['shot origins'][team]:
                    return_dict[team][shotorigin] = self.prints['shot origins'][team][shotorigin] + other.prints['shot origins'][team][shotorigin]
                else:
                    return_dict[team][shotorigin] = self.prints['shot origins'][team][shotorigin] 
            for shotorigin in other.prints['shot origins'][team]:
                if shotorigin not in return_dict[team]:
                    return_dict[team][shotorigin] = other.prints['shot origins'][team][shotorigin]
        return return_dict

    def note_possession(self, row: pd.core.series.Series, index: int) -> None:
        '''updates the possession list based on row'''
        if row['event'] in Stats.possession_gained:
            if index == 0 or row['team'] != self.possession_list[-1][0]:
                self.possession_list.append((row['team'], row['time']))
        elif row['event'] in Stats.possession_lost:
            if index == 0 or self.opposite_team(row['team']) != self.possession_list[-1][0]:
                self.possession_list.append((self.opposite_team(row['team']), row['time']))
        elif row['event'] in Stats.await_next:
            if index != 0 and self.possession_list[-1][0] != None:
                self.possession_list.append((None, row['time']))
        else: # we should never get here?
            print(f"error in get_possession_list, event: {row['event']} not recognized by Stats")
            self.possession_list.append((None, None))
        return     
    
    def make_possession_list(self) -> None:
        '''returns the possession list'''
        if len(self.possession_list) == 0:
            for index, row in self.big_df.iterrows():
                self.note_possession(row, index)
        return 
        
    def get_shots_df(self) -> pd.core.frame.DataFrame:
        '''returns a df with only the outcome events from shots
            populates the df_dict if not already done'''
        if 'shots' not in self.df_dict:
            self.df_dict['shots'] = self.big_df.loc[self.big_df['event'].isin(['skott', 'mål'])]
        return self.df_dict['shots'] 

    def get_shottypes_df(self) -> pd.core.frame.DataFrame:
        '''returns a df with only the the shot types
            populates the df_dict if not already done'''
        if 'shot types' not in self.df_dict:
            self.df_dict['shot types'] = self.big_df.loc[self.big_df['event'] == 'skottyp']
        return self.df_dict['shot types'] 
    
    def get_score_df(self) -> pd.core.frame.DataFrame:
        '''returns a df with only the the goals
            populates the df_dict if not already done'''
        if 'goals' not in self.df_dict:
            self.df_dict['goals'] = self.big_df.loc[self.big_df['event'] == 'mål']
        return self.df_dict['goals'] 

    def get_duels_df(self) -> pd.core.frame.DataFrame:
        '''returns a df with only the the duels
            populates the df_dict if not already done'''
        if 'duels' not in self.df_dict:
            self.df_dict['duels'] = self.big_df.loc[self.big_df['event'].isin(['närkamp', 'brytning'])]
        return self.df_dict['duels'] 

    def opposite_team(self, team: str) -> str:
        '''returns the opposite team of input
            only works if input is correct'''
        return self.teams.difference(team).pop()