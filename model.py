"""
model.py - Educational Synaptic Plasticity Toy Model
=====================================================
DataForge 2026 Hackathon - "Explain the Frontier" Pathway Track
Topic: Synaptic Plasticity as Short-Term Memory

IMPORTANT LABELS
----------------
This is an EDUCATIONAL TOY MODEL.
It is NOT the official BDH/BDH-CQ model.
It is NOT a biologically accurate spiking-neuron model.
It is NOT a large neural network.

The update rule below is a simplified educational rule chosen for
interpretability. It captures the qualitative behaviour of short-term
synaptic plasticity (STSP): Hebbian potentiation and exponential decay.
It does NOT reproduce the exact equations of BDH, the STP-neuron model of
Garcia Rodriguez et al. (2022), or any other specific published implementation.

Update rule (educational simplification):
    w(t+1) = decay * w(t) + learning_rate * pre * post

where:
  w      - synaptic weight between a concept neuron and a label neuron
  decay  - persistence factor in [0, 1]; controls how fast the trace fades
  lr     - learning_rate / plasticity strength in [0, 1]
  pre    - pre-synaptic activity (1.0 when the concept is presented)
  post   - post-synaptic activity (1.0 when the label is presented)

All displayed synaptic values come from this live computation.
No values are precomputed or scripted.
"""

from __future__ import annotations
import copy
from typing import Dict, Optional, Tuple


class SynapticMemoryModel:
    """
    A minimal toy model of short-term synaptic plasticity.

    Neurons are identified by string names (e.g. "apple", "red").
    Synaptic weights are stored in a dict keyed by (concept, label) pairs.
    Weights start at 0 and are updated by an explicit Hebbian rule with decay.
    """

    def __init__(self, decay: float = 0.85, learning_rate: float = 0.8) -> None:
        self.decay: float = float(decay)
        self.learning_rate: float = float(learning_rate)
        self._weights: Dict[Tuple[str, str], float] = {}
        self._history: list = []
        self._current_time: int = 0
        self._snapshot_history()

    def learn(self, concept: str, label: str) -> None:
        """
        Apply a Hebbian write for the association concept -> label.

        Update rule (educational simplification - NOT the BDH equation):
            w(t+1) = decay * w(t) + learning_rate * pre * post
        where pre = post = 1.0 (both neurons are co-activated).
        """
        key = (concept.lower(), label.lower())
        old_w = self._weights.get(key, 0.0)
        new_w = self.decay * old_w + self.learning_rate * 1.0 * 1.0
        self._weights[key] = min(new_w, 2.0)
        self._current_time += 1
        self._snapshot_history()

    def step_time(self, steps: int = 1) -> None:
        """
        Advance time by `steps` units without any learning event.
        Each step multiplies every synaptic weight by `decay`.

        Exponential decay: w(t + n) = decay^n * w(t)
        """
        for _ in range(steps):
            for key in list(self._weights.keys()):
                self._weights[key] *= self.decay
            self._current_time += 1
            self._snapshot_history()

    def recall(self, concept: str) -> Optional[str]:
        """
        Return the label with the strongest synaptic connection to `concept`.
        Returns None if no associations exist.
        """
        concept = concept.lower()
        candidates = {
            label: w
            for (c, label), w in self._weights.items()
            if c == concept
        }
        if not candidates:
            return None
        return max(candidates, key=candidates.__getitem__)

    def get_synaptic_state(self, concept: Optional[str] = None) -> Dict[Tuple[str, str], float]:
        """Return a snapshot of current synaptic weights (copy)."""
        if concept is None:
            return copy.deepcopy(self._weights)
        concept = concept.lower()
        return {(c, l): w for (c, l), w in self._weights.items() if c == concept}

    def reset(self) -> None:
        """Clear all synaptic weights and reset time."""
        self._weights.clear()
        self._current_time = 0
        self._history.clear()
        self._snapshot_history()

    def get_history(self) -> list:
        """Return copy of weight history for plotting."""
        return copy.deepcopy(self._history)

    @property
    def current_time(self) -> int:
        return self._current_time

    def weight_of(self, concept: str, label: str) -> float:
        """Return the synaptic weight for a specific (concept, label) pair."""
        return self._weights.get((concept.lower(), label.lower()), 0.0)

    def recall_scores(self, concept: str) -> Dict[str, float]:
        """Return {label: weight} for all associations from `concept`."""
        concept = concept.lower()
        return {label: w for (c, label), w in self._weights.items() if c == concept}

    def describe_update_rule(self) -> str:
        return (
            f"w(t+1) = {self.decay:.2f} x w(t)  +  {self.learning_rate:.2f} x pre x post"
        )

    @classmethod
    def simulate_scenario(
        cls,
        decay: float,
        learning_rate: float,
        red_reps: int = 5,
        delay: int = 20,
        green_reps: int = 1
    ) -> Dict[str, any]:
        """
        Simulate an educational sequence under specific decay and learning_rate:
          1. red_reps consecutive Hebbian writes for ('apple', 'red')
          2. delay discrete time steps of passive decay
          3. green_reps Hebbian writes for ('apple', 'green')

        Returns exact numeric dictionary of weights at each milestone and final readout.
        """
        sim = cls(decay=decay, learning_rate=learning_rate)
        for _ in range(red_reps):
            sim.learn('apple', 'red')
        w_red_learned = sim.weight_of('apple', 'red')

        sim.step_time(delay)
        w_red_decayed = sim.weight_of('apple', 'red')

        for _ in range(green_reps):
            sim.learn('apple', 'green')
        w_red_final = sim.weight_of('apple', 'red')
        w_green_final = sim.weight_of('apple', 'green')
        winner = sim.recall('apple')

        return {
            "w_red_after_learning": w_red_learned,
            "w_red_after_delay": w_red_decayed,
            "w_red_final": w_red_final,
            "w_green_final": w_green_final,
            "winner": winner,
            "scores": sim.recall_scores('apple'),
            "history": sim.get_history(),
        }

    def _snapshot_history(self) -> None:
        self._history.append({
            "t": self._current_time,
            "weights": copy.deepcopy(self._weights),
        })
