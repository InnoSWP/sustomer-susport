class TeamEntry:
    _team_name: str
    members: (set[int], set[str], set[int, str])

    def __init__(self, group_name: str, members: (set[int], set[str], set[int, str]) = None):
        if members is None:
            members = set()
        self._team_name = group_name
        self.members = members

    def __str__(self):
        return self._team_name

    @property
    def team_name(self):
        return self._team_name
