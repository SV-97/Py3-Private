from enum import Enum, auto


class Team(Enum):
    # winners
    Bayern = auto()
    ManCity = auto()
    Liverpool = auto()
    Chelsea = auto()
    Bvb = auto()
    Juve = auto()
    Psg = auto()
    Real = auto()
    # seconds
    Porto = auto()
    Sevilla = auto()
    Lazio = auto()
    Barca = auto()
    Atletico = auto()
    Atalanta = auto()
    Rb = auto()
    Gladbach = auto()


class Country(Enum):
    De = auto()
    Gb = auto()
    It = auto()
    Fr = auto()
    Es = auto()
    Pt = auto()


firsts = {
    Team.Bayern: Country.De,
    Team.ManCity: Country.Gb,
    Team.Liverpool: Country.Gb,
    Team.Chelsea: Country.Gb,
    Team.Bvb: Country.De,
    Team.Juve: Country.It,
    Team.Psg: Country.Fr,
    Team.Real: Country.Es}

seconds = {
    Team.Porto: Country.Pt,
    Team.Sevilla: Country.Es,
    Team.Lazio: Country.It,
    Team.Barca: Country.Es,
    Team.Atletico: Country.Es,
    Team.Atalanta: Country.It,
    Team.Rb: Country.De,
    Team.Gladbach: Country.De}


pre_matches = {
    (Team.Bvb, Team.Lazio),
    (Team.Bayern, Team.Atletico),
    (Team.Real, Team.Gladbach),
    (Team.ManCity, Team.Porto),
    (Team.Liverpool, Team.Atalanta),
    (Team.Chelsea, Team.Sevilla),
    (Team.Juve, Team.Barca),
    (Team.Psg, Team.Rb)}

possible_edges = {(first, second) for first in firsts for second in seconds}
possible_edges = {
    edge for edge in possible_edges if firsts[edge[0]] != seconds[edge[1]]}
possible_edges = {edge for edge in possible_edges if edge not in pre_matches}


def possible_matches(team, allowed_matches):
    if len(allowed_matches) == 0:
        return set()
    edges_with_team = {edge for edge in allowed_matches if team in edge}
    to_ret = set()
    for edge in edges_with_team:
        opponent = edge[1]
        new_allowed = {
            edge for edge in allowed_matches if edge[1] != opponent and edge[0] != team}
        if len(new_allowed) == 0:
            to_ret.add(frozenset((edge, )))
            continue
        new_team = next(iter(new_allowed))[0]
        possible_configs = possible_matches(new_team, new_allowed)
        to_ret.update(frozenset((edge, *config))
                      for config in possible_configs)
    return to_ret


team_a = Team.Real
team_b = Team.Rb

# remove invalid combinations (those where there's an unmatched team)
omega = set(filter(lambda comb: len(comb) == len(firsts),
                   possible_matches(team_a, possible_edges)))
a = {config for config in omega if (team_a, team_b) in config}
print(len(a) / len(omega))
