import itertools
from typing import TypeAlias, Iterable


class Participant:
    name: str
    pid: int
    tid: int
    introduced_in: int

    def __init__(self,
                 pid: int,
                 name: str,
                 tid: int | str,
                 introduced_in: int):
        self.name = name
        self.pid = pid
        self.tid = tid if type(tid) is int else tid.upper()[0] == 'A'
        self.introduced_in = introduced_in

    def __str__(self):
        return 'Participant(pid=%d, tid=%d, name=\'%s\', introduced_in=%d)' % (
            self.pid, self.tid, self.name, self.introduced_in)


class EventMatchBox:
    participants: tuple[Participant, Participant]
    match: bool

    def __init__(self,
                 participants: tuple[Participant, Participant],
                 match: bool):
        self.participants = participants
        self.match = match

    def filter_func(self,
                    permutations: Iterable[list[list[Participant]]]) -> Iterable[list[list[Participant]]]:
        return filter(lambda perm: self.match is (self.participants[1] in perm[self.participants[0].pid]),
                      permutations)


class EventMatchNight:
    arrangement: list[Participant]
    lights: int

    def __init__(self,
                 arrangement: list[tuple[Participant, Participant]],
                 lights: int):
        self.arrangement = list(map(lambda tup: tup[1],
                                    sorted(arrangement, key=lambda tup: tup[0].pid)))
        self.lights = lights

    def filter_func(self,
                    permutations) -> Iterable[list[list[Participant]]]:
        return filter(lambda perm:
                      sum(x[0] in x[1] for x in zip(self.arrangement, perm)) == self.lights,
                      permutations)


class EventAddParticipant:
    participant: Participant

    def __init__(self,
                 participant: Participant):
        self.participant = participant

    def filter_func(self,
                    permutations) -> Iterable[list[list[Participant]]]:
        for perm in permutations:
            for i in range(len(perm)):
                yield perm[:i] + [perm[i] + [self.participant]] + perm[i + 1:]


# TODO: Add decorator class vor Events
Event: TypeAlias = EventMatchBox | EventMatchNight | EventAddParticipant


class InstructionSet:
    participants: tuple[list[Participant],
                        list[Participant]]

    episode_names: list[str]
    episode_events: list[list[Event]]

    def __init__(self):
        self.episode_names = []
        self.episode_events = []

    def participant_by_name(self,
                            name: str):
        for participant in [participant for team in self.participants for participant in team]:
            if participant.name.upper() == name.upper():
                return participant
        raise Exception('Name not found: %s' % name)

    def gen_base_permutations(self,
                              base_size: int = 10):
        for perm in itertools.permutations(self.participants[1][:base_size]):
            yield [[participant] for participant in perm]  # TODO: I think this is correct. IDE says no.

    def print_config(self):
        for team in self.participants:
            for name in team:
                print(name)
        for ep in zip(self.episode_names, self.episode_events):
            print(ep)


def _split_names(line: str, sep=';') -> list[str]:
    return list(filter(lambda x: x,
                       [name.strip() for name in line.split(sep=sep)]))


def instructions_from_txt(instruction_file_path: str):
    with open(instruction_file_path, 'r') as fp:
        i_set = InstructionSet()
        ep_counter = -1
        lines = iter(filter(lambda s: s, map(lambda s: s.strip(), fp.readlines())))
        for line in lines:
            if line[0] == '$':
                line = line.upper()

                if 'SEASON' in line:
                    i_set.participants = tuple([Participant(pid=id_name[0],
                                                            name=id_name[1],
                                                            tid=tid,
                                                            introduced_in=0)
                                                for id_name in zip(itertools.count(), _split_names(line=next(lines)))]
                                               for tid in [0, 1])

                elif 'EPISODE' in line:
                    ep_counter += 1
                    i_set.episode_names += [next(lines)]
                    i_set.episode_events += [[]]

                elif 'MATCH BOX' in line:
                    vals = _split_names(line=next(lines))
                    i_set.episode_events[-1] += [EventMatchBox(participants=(i_set.participant_by_name(name=vals[0]),
                                                                             i_set.participant_by_name(name=vals[1])),
                                                               match=bool(int(vals[2])) if len(vals) > 2 else False)]

                elif 'MATCH NIGHT' in line:
                    arrangement = []
                    for _ in range(10):
                        arrangement += [tuple(i_set.participant_by_name(name) for name in _split_names(next(lines)))]
                    i_set.episode_events[-1] += [EventMatchNight(arrangement=arrangement,
                                                                 lights=int(next(lines)))]

                elif 'PARTICIPANT' in line:
                    participant = Participant(pid=len(i_set.participants[1]),
                                              name=next(lines),
                                              tid=1,
                                              introduced_in=ep_counter)
                    i_set.participants[1].append(participant)
                    i_set.episode_events[-1] += [EventAddParticipant(participant=participant)]
    return i_set
