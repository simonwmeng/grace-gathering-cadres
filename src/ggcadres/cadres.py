import itertools as it
import math
import random
from functools import cached_property, reduce
from typing import Collection

import networkx as nx


class CadreGenerator:
    def __init__(
        self,
        people: Collection[str],
        *,
        forbidden_groups: Collection[Collection[str]] | None,
        preferred_groups: Collection[Collection[str]] | None,
        num_groups: int,
        seed: int,
    ) -> None:
        self.people = set(people)
        self.forbidden_groups: set[frozenset[str]] = (
            {frozenset(group) for group in forbidden_groups}
            if forbidden_groups
            else set()
        )
        self.preferred_groups: set[frozenset[str]] = (
            {frozenset(group) for group in preferred_groups}
            if preferred_groups
            else set()
        )
        self.num_groups = num_groups
        self.seed = seed

    @property
    def _cadre_size(self) -> int:
        return math.ceil(len(self.people) / self.num_groups)

    @cached_property
    def _graph(self) -> nx.Graph:
        graph = nx.Graph()

        # Compute forbidden pairings.

        forbidden_pairs = {
            frozenset(pair)
            for group in self.forbidden_groups
            for pair in it.combinations(group, 2)
        }

        # Construct the graph.

        remaining_people = self.people - reduce(
            frozenset.union, self.preferred_groups, frozenset()
        )

        for p1, p2 in it.combinations(remaining_people, 2):
            if {p1, p2} not in forbidden_pairs:
                graph.add_edge(p1, p2)

        return graph

    def _get_clique(self, seed_person: str, num_people: int) -> list[str] | None:
        # find_cliques is non-deterministic. We need to make it so.

        candidate_cliques = sorted(
            sorted(clique)
            for clique in nx.find_cliques(self._graph, nodes=[seed_person])
            if len(clique) == num_people
        )

        if not candidate_cliques:
            return None

        clique = random.choice(candidate_cliques)
        return clique

    def generate(self) -> list[list[str]]:
        remaining_people = set(self.people)
        cadres = []

        # Immediately assign preferred groupings.

        for group in self.preferred_groups:
            cadres.append(sorted(group))
            remaining_people -= set(group)

        # Greedily match people with the lowest degrees to ensure we match everyone as
        # best as possible.

        random.seed(self.seed)

        while True:
            if len(self._graph) <= self._cadre_size:
                cadres.append(sorted(self._graph.nodes))
                break

            # Avoid splitting people into groups of 1.

            this_size = (
                self._cadre_size
                if len(self._graph) <= self._cadre_size
                else math.ceil(len(self._graph) / 2)
                if len(self._graph) < 2 * self._cadre_size
                else self._cadre_size
            )
            person_order = sorted((deg, person) for person, deg in self._graph.degree())
            _, seed_person = person_order[0]

            # With the seed person, attempt to determine a subgraph with this_size
            # people. If we can't identify a clique, try subsequently fewer numbers of
            # people. Randomly assign people to fill out the cadre.

            clique = []

            for k in range(this_size, 0, -1):
                if cand_clique := self._get_clique(seed_person, k):
                    clique = cand_clique
                    break

            self._graph.remove_nodes_from(clique)

            while len(clique) < this_size:
                next_person = random.choice(sorted(self._graph.nodes))
                self._graph.remove_node(next_person)
                clique.append(next_person)

            cadres.append(sorted(clique))

            # try:
            #     # find_cliques is non-deterministic. We need to make it so.

            #     candidate_cliques = sorted(
            #         sorted(clique)
            #         for clique in nx.find_cliques(self._graph, nodes=[seed_person])
            #         if len(clique) == this_size
            #     )
            #     clique = random.choice(candidate_cliques)
            #     cadres.append(clique)
            #     self._graph.remove_nodes_from(clique)

            # except StopIteration:
            #     1 / 0

        return cadres
