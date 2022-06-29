class TeamEntry:
    _team_name: str
    members: (set[int], set[str], set[int, str])
    tg_group_id: int

    def __init__(self, group_name: str, group_id: int, members: (set[int], set[str], set[int, str]) = None):
        if members is None:
            members = set()
        self._team_name = group_name
        self.tg_group_id = group_id
        self.members = members

    def __str__(self):
        return self._team_name

    def __eq__(self, other):
        return (self.team_name == other.team_name) and\
               (self.tg_group_id == other.tg_group_id) and\
               (self.members == other.members)

    def to_dict(self):
        return {"team_name": self._team_name, "tg_group_id": self.tg_group_id, "members": list(self.members)}

    @property
    def team_name(self):
        return self._team_name
