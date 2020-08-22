import log

from bisect import insort
from dataclasses import dataclass
from typing import Dict, List, Set

from datafiles import datafile

@datafile("{self.key}.yaml")
class Fact:
    key: str
    description: str
    reasons: List[str] # Set[Fact.key]


@dataclass
class DagNavigator:
    fact: Fact

    def new_consequence(self, key, description):
        return self.add_consequence(Fact(key, description, []))

    def add_consequence(self, fact):
        return DagNavigator(fact).add_reason(self.fact)

    def new_reason(self, key, description):
        return self.add_reason(Fact(key, description, []))

    def add_reason(self, fact):
        if fact.key not in self.fact.reasons:
            insort(self.fact.reasons, fact.key)

        return self

    @property
    def consequences(self):
        return list(DagNavigator(fact) for fact in Fact.objects.all() if self.fact.key in fact.reasons)

    @property
    def reasons(self):
        return list(DagNavigator(fact) for fact in Fact.objects.all() if fact.key in self.fact.reasons)

    def __repr__(self):
        consequences = "\n  - ".join(n.fact.description for n in self.consequences)
        reasons = "\n  - ".join(n.fact.description for n in self.reasons)
        return f"fact: {self.fact.description}\nconsequences:\n  - {consequences}\nreasons:\n  - {reasons}"


@dataclass
class Dag:
    roots: List[DagNavigator]

    def __repr__(self):
        roots = "\n  - ".join(n.fact.description for n in self.roots)
        return f"roots:\n  - {roots}"


def dag():
    return Dag(list(DagNavigator(fact) for fact in Fact.objects.all() if fact.reasons == []))


log.silence('datafiles')
print("Inspect facts:")
print("- dag()")
