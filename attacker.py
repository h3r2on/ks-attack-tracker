class Attacker():
    def __init__(self, member, opponent_th_list):
        self.tag = member["tag"]
        self.name = member["name"]
        self.townhallLevel= member["townhallLevel"]
        self.wars = 1
        self.attacks_v_11 = []
        self.attacks_v_10 = []
        self.attacks_v_9 = []
        if member.get("attacks"): 
            self.parse_attacks(member["attacks"], opponent_th_list)
    
    def __repr__(self):
        return repr((self.name, self.townhallLevel, self.hit_rate(11)))
    
    def parse_attacks(self, attacks, opponent_th):
        for attack in attacks:
            op_th = opponent_th.get(attack["defenderTag"])
            if op_th == 11:
                self.attacks_v_11.append(attack["stars"])
            if op_th == 10:
                self.attacks_v_10.append(attack["stars"])
            if op_th == 9:
                self.attacks_v_9.append(attack["stars"])
    
    def add_war(self, attacks, op_th): 
        self.wars += 1
        if attacks:
            self.parse_attacks(attacks, op_th)

    def three_stars(self, attacks, op_th):
        if op_th > self.townhallLevel:
            return len([x for x in attacks if x >= 2])
        else: 
            return len([x for x in attacks if x == 3])
    
    def num_of_attacks(self, th_level):
        """Return the number of attacks against the given town hall level.
        
        Arguments:
            th_level (int): The town hall level of the opponent TH.
        
        Returns:
            int: Number of attacks made.
        """
        if th_level == 9:
            return len(self.attacks_v_9)
        elif th_level == 10:
            return len(self.attacks_v_10)
        elif th_level == 11:
            return len(self.attacks_v_11)
    
    def hit_rate(self, th_level):
        if th_level == 11 and self.attacks_v_11:
            return round(self.three_stars(self.attacks_v_11, 11)/len(self.attacks_v_11), 2)
        elif th_level == 10 and self.attacks_v_10:
            return round(self.three_stars(self.attacks_v_10, 10)/len(self.attacks_v_10), 2)
        elif th_level == 9 and self.attacks_v_9: 
            return round(self.three_stars(self.attacks_v_9, 9)/len(self.attacks_v_9), 2)
        else: 
            return ""
    
    def average_stars(self, th_level):
        if th_level == 11 and self.attacks_v_11:
            return round(sum(self.attacks_v_11)/len(self.attacks_v_11), 1)
        elif th_level == 10 and self.attacks_v_10:
            return round(sum(self.attacks_v_10)/len(self.attacks_v_10), 1)
        elif th_level == 9 and self.attacks_v_9: 
            return round(sum(self.attacks_v_9)/len(self.attacks_v_9), 1)
        else: 
            return ""

    def share(self):
        return {"tag": self.tag, "name": self.name, "TH": self.townhallLevel, "wars": self.wars, 
                "v11": "{}/{}/{}".format(self.attacks_v_11, sum(self.attacks_v_11), self.three_stars(self.attacks_v_11, 11)),
                "v10": "{}/{}/{}".format(self.attacks_v_10, sum(self.attacks_v_10), self.three_stars(self.attacks_v_10, 10)),
                "v9": "{}/{}/{}".format(self.attacks_v_9, sum(self.attacks_v_9), self.three_stars(self.attacks_v_9, 9))
        }
        
    def spreadsheet_list(self):
        return [self.tag, self.name,
                self.hit_rate(11), 
                self.hit_rate(10), 
                self.hit_rate(9), 
                self.average_stars(11), 
                self.average_stars(10), 
                self.average_stars(9),
                len(self.attacks_v_11),
                len(self.attacks_v_10),
                len(self.attacks_v_9),
                sum(self.attacks_v_11),
                sum(self.attacks_v_10),
                sum(self.attacks_v_9),
                self.three_stars(self.attacks_v_11, 11),
                self.three_stars(self.attacks_v_10, 10),
                self.three_stars(self.attacks_v_9, 9),
                self.wars]