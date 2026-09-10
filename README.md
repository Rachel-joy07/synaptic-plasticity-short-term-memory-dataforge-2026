# Can a Connection Remember?
## DataForge 2026 — Explain the Frontier
### Topic: Synaptic Plasticity as Short-Term Memory

**Public artifact:** https://synaptic-memory-dataforge.streamlit.app
**Public source:** https://github.com/Rachel-joy07/synaptic-plasticity-short-term-memory-dataforge-2026

---

## 1. What this project teaches

This is an interactive educational experience about **synaptic plasticity as a short-term memory mechanism**.

### Central claim

> **Short-term synaptic plasticity can store recent information in changing synaptic states, but the persistence of those traces creates a trade-off between remembering recent information and being influenced by new or competing information.**

The artifact turns that claim into a live experiment. A learner teaches an `Apple → Red` association, lets the stored state decay, recalls it, then introduces `Apple → Green` and predicts which association will win at readout. The learner can then change persistence/decay and delay in the final challenge and test the prediction.

This claim is a **computational/educational claim about the toy model**, not a claim that this code reproduces human memory or all biological synaptic mechanisms.

---

## 2. Intended learner and prerequisites

**Audience:** undergraduate students and early-career data scientists/engineers who are comfortable with basic programming but have no specialized neuroscience background.

**Prerequisites:** basic familiarity with numbers, graphs, and the idea of a machine-learning model. No neuroscience or biophysics background is required.

---

## 3. Learning objectives

After the interaction, the learner should be able to:

1. Explain what a synapse is and what synaptic plasticity means.
2. Interpret a **weight** as the numerical state/strength of an association in this toy model.
3. Explain **decay** as the fading of the stored state over time.
4. Explain the simplified update rule:

   `w(t+1) = decay × w(t) + learning_rate × pre × post`

5. Explain why a changing synaptic state can act as a temporary computational memory trace.
6. Explain that, in this toy, Red and Green are separate traces and compete at **readout**, where the model selects the largest current weight.
7. Explore the stability–plasticity trade-off by changing persistence/decay and delay.
8. Explain how the toy provides intuition for synaptic-plasticity mechanisms used in the Dragon Hatchling (BDH) architecture.

---

## 4. 60-second learner journey

- **0–5 s:** Start with the question: *Can a connection remember?*
- **5–15 s:** Teach `Apple → Red`; observe the live synaptic state increase.
- **15–25 s:** Let time pass; observe the weight decay.
- **25–35 s:** Recall the strongest association.
- **35–50 s:** Teach `Apple → Green`; predict the readout winner and resolve the result.
- **50–60 s:** Change persistence and delay in the final challenge and test the prediction.

The point is not to watch a prerecorded animation. The learner changes the state/parameters and observes live consequences.

---

## 5. How the toy model works

### Weight

A **weight** is simply a number representing the current strength/state of an association in this educational model. For example, if `Apple → Red` has weight `0.80` and `Apple → Green` has weight `0.20`, Red is currently the stronger trace. The weight is not a probability and is not a biological measurement.

### Learning / plasticity

When the learner presents a concept-label pair, the model updates its associated weight. The simplified rule uses co-activation (`pre × post`) as a Hebbian-style learning term.

### Decay

When time passes without a new learning event, each stored weight is multiplied by the decay factor. With decay `δ`, after `n` passive time steps the toy gives `w(t+n) = δ^n w(t)`.

Higher decay values mean more of the old state survives each step; lower values make it fade faster. In the interface this is described intuitively as **persistence**.

### Recall

The toy reads all labels associated with a concept and selects the largest current weight (`argmax`).

### Competition

The current code does **not** make the Green trace erase the Red trace. They are stored as separate scalar traces. The competition in this experiment happens at readout when their current values are compared.

### Implementation detail

`learn()` caps an individual toy weight at `2.0`. This is an implementation choice for the educational substrate, not a biological constant.

---

## 6. Architecture

```text
DataForge/
├── app.py             # Streamlit interactive editorial experience
├── model.py           # Authoritative educational toy model
├── requirements.txt   # Python dependencies
├── README.md          # Documentation and disclosures
├── LICENSE            # Project code license
└── docs/
    ├── blog.pdf
    └── concept-summary.pdf
```

### `model.py`

Contains the computational substrate:

- `SynapticMemoryModel`: stores toy synaptic weights and history.
- `learn(concept, label)`: applies the simplified Hebbian update.
- `step_time(steps)`: applies passive decay.
- `recall(concept)`: selects the strongest association.
- `simulate_scenario(...)`: runs the final challenge sequence and returns live milestone values.
- `get_history()`, `weight_of()`, and `recall_scores()`: expose current state for the interface.

### `app.py`

Contains the narrative/editorial interface, learner controls, live SVG visualization, Plotly trajectory, explanations, research evidence, limitations, and final challenge.

---

## 7. What is live, synthetic, precomputed, or animated?

### Live

The following are computed from the current model state:

- synaptic weights
- weight trajectory
- displayed numerical values
- recall/readout
- final challenge results
- explanatory text tied to the selected state
- visualization geometry driven by weights

### Synthetic

`Apple → Red` and `Apple → Green` are synthetic pedagogical examples. No external dataset is required.

### Precomputed

There are **no precomputed experimental results** used to determine the learner's outcome. The final challenge runs the toy model with the selected conditions.

### Animated / visualized

The synapse SVG uses the current weights to control connection thickness, opacity, node size, and signal-particle activity. These are visual representations of the live toy state, not simulations of literal biological synaptic geometry.

---

## 8. Scientific boundaries and limitations

This project is deliberately small and interpretable.

It is **not**:

- a biologically accurate simulation of a brain;
- an exact implementation of STPN;
- an exact implementation of BDH or BDH-CQ;
- a spiking-neuron/biophysical simulator;
- evidence that human short-term memory is implemented exactly this way.

The toy uses scalar association weights, a simplified Hebbian-style update, multiplicative decay, and a simple maximum-weight readout. Real synaptic plasticity includes many mechanisms and timescales that are outside the scope of this artifact.

The conflict experiment is also intentionally limited: Red and Green remain separate traces. The educational experiment studies how their **current strengths affect readout**, rather than claiming to model all biological forms of interference.

---

## 9. Research evidence

The project is grounded in recent primary research. The papers are used for context and motivation; our toy is not presented as a reproduction of their exact models.

1. **Garcia Rodriguez, H., Guo, Q., & Moraitis, T. (2022).** *Short-Term Plasticity Neurons Learning to Learn and Forget.* ICML 2022, PMLR 162:18704–18722. The paper introduces STP Neurons whose synapses have state propagated through time and evaluates learning/forgetting behavior across several tasks. [Official paper](https://proceedings.mlr.press/v162/rodriguez22b.html)

2. **Kozachkov, L. et al. (2022).** *Robust and brain-like working memory through short-term synaptic plasticity.* PLOS Computational Biology 18(12): e1010776. In their RNN experiments, models with STSP maintained working memories, showed more brain-like activity, and were more robust to network degradation than the corresponding models without STSP. [Primary paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010776)

3. **Chrysanthidis, N. et al. (2025).** *Short-term plasticity influences episodic memory recall: an interplay of synaptic traces in a spiking neural network model.* Scientific Reports 15:28164. The study models interactions between episodic memory and short-term recency effects using synaptic plasticity mechanisms. Our Red/Green conflict is an educational simplification inspired by this broader question. [Primary paper](https://www.nature.com/articles/s41598-025-12611-5)

4. **Kosowski, A. et al. (2025).** *The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain.* arXiv:2509.26507. The paper presents BDH and describes its working memory during inference as relying on synaptic plasticity with Hebbian learning using spiking neurons. [Primary paper](https://arxiv.org/abs/2509.26507)

### What the evidence does and does not establish

These papers provide computational and/or modeling evidence that dynamic synaptic mechanisms can support learning, forgetting, working-memory behavior, or recency-related effects in their respective systems. They do **not** establish that our simplified scalar equation is a complete model of biological memory.

---

## 10. BDH and BDH-CQ

### BDH

BDH (The Dragon Hatchling) is directly relevant. Its 2025 paper describes a brain-inspired language-model architecture in which working memory during inference relies on synaptic plasticity with Hebbian learning using spiking neurons. Our artifact isolates the intuition of a changing synaptic state and makes it manipulable in a tiny educational substrate. It is **not** an implementation of BDH.

### BDH-CQ

BDH-CQ (2026) extends the BDH family toward in-context learning with recurrent latent reasoning. Its relevance to this submission is **contextual rather than a direct implementation claim**: it builds on the BDH family and uses evolving recurrent memory during inference. We do not claim that our scalar toy reproduces BDH-CQ's latent reasoning mechanism. See the primary BDH-CQ paper: https://arxiv.org/abs/2608.09888

---

## 11. Reproduction / setup

### Local setup

Python 3.10+ is recommended.

```bash
git clone <PUBLIC-REPOSITORY-URL>
cd DataForge
python -m venv venv
```

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, normally `http://localhost:8501`.

### Reproducing the final challenge

The final challenge is computed by `SynapticMemoryModel.simulate_scenario()` from the selected decay/persistence, learning rate, Red repetitions, delay, and Green repetitions. It returns the learned Red weight, decayed Red weight, final Red and Green weights, winner, scores, and history.

---

## 12. Source, data, weights, graphics, fonts, and licenses

| Component | Source / origin | License / status |
|---|---|---|
| Project Python code | DataForge 2026 team | MIT; see `LICENSE` |
| Synthetic Apple/Red/Green examples | Generated by the project | Original/synthetic; no external dataset |
| Model weights | No pretrained weights | None used/distributed |
| Synapse visualization | Programmatically generated in `app.py` | Original project code; MIT |
| Plotly charts | Plotly library | MIT |
| Streamlit | Streamlit | Apache-2.0 |
| NumPy | NumPy project | BSD-3-Clause |
| Pandas | pandas project | BSD-3-Clause |
| Matplotlib | Matplotlib project | PSF-based license |
| Newsreader font | Google Fonts | SIL Open Font License 1.1 |
| Plus Jakarta Sans font | Google Fonts | SIL Open Font License 1.1 |
| JetBrains Mono font | JetBrains / Google Fonts | SIL Open Font License 1.1 |
| Research papers | Original authors/publishers | Linked/cited at source; no paper figures are embedded in the artifact |

The application loads the listed fonts from Google Fonts at runtime. If the network is unavailable, the CSS includes system-font fallbacks.

---

## 13. AI assistance disclosure

Generative AI tools, including Google Antigravity/Gemini and ChatGPT, were used for selected coding assistance, UI/CSS refinement, debugging support, documentation drafting, and explanation refinement. The DataForge team reviewed and tested the implementation and is responsible for the final code, scientific claims, citations, model design, and submitted materials.

---

## 14. Team ownership

The team must be able to explain every major component during a live defense, including the weight representation, update rule, decay, readout, final challenge, visualization-to-state binding, research boundaries, and BDH connection.

---

## 15. Credits and further learning

- Garcia Rodriguez et al. (2022), PMLR / ICML: https://proceedings.mlr.press/v162/rodriguez22b.html
- Kozachkov et al. (2022), PLOS Computational Biology: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1010776
- Chrysanthidis et al. (2025), Scientific Reports: https://www.nature.com/articles/s41598-025-12611-5
- Kosowski et al. (2025), BDH: https://arxiv.org/abs/2509.26507
- Engdahl et al. (2026), BDH-CQ: https://arxiv.org/abs/2608.09888
