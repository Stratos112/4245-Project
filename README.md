# Speech Prosody Projects — CS545 + CS542

Two connected school projects. One builds the speech alignment pipeline; the other uses it for emotion classification.

---

## CS 545 — Forced Alignment with CTC
**Class:** Deep Learning | **Due:** Dec 16, 2026

Train a bidirectional LSTM on the [TIMIT](https://catalog.ldc.upenn.edu/LDC93S1) dataset to find **where each word starts and ends in audio**, using a loss function called **CTC (Connectionist Temporal Classification)**.

- CTC lets the model learn timing without needing every audio frame pre-labeled — it figures out the alignment on its own.
- The output is a matrix of per-frame phoneme probabilities; a Viterbi search over it gives exact word boundaries.
- Reproduces the approach from Graves et al. (2006), scored against TIMIT's hand-labeled gold timings.
- Stretch goal: compare the biLSTM to a Transformer on the same task.

**Deliverable:** Jupyter notebook explaining CTC, the architecture, and results.

---

## CS 542 — Emotion Classification via MIDI Prosody
**Class:** NLP | **Due:** Dec 16, 2026

Take word-boundary timings (from the 545 aligner, or from pre-labeled data in the [ESD dataset](https://github.com/HLTSingapore/Emotional-Speech-Data)) and convert **pitch, duration, and timing into MIDI notation**. Then classify the emotion category from those MIDI sequences.

- MIDI is used as a "musical" tokenization of speech prosody — same words, different emotions → different note patterns.
- Classifier options: one HMM per emotion class, or a BiLSTM over the note sequence.
- Comparison: MIDI-only vs. raw continuous pitch/energy features, to measure what quantization costs.
- Dataset: ESD has the same sentences spoken in multiple emotions, so text alone can't cheat the classifier.

**Deliverable:** Written report + code.

---

## How They Fit Together

```
Raw audio + transcript
        |
   [ CS 545 ]  BiLSTM + CTC → word/phoneme boundaries (ms-level)
        |
   Convert to MIDI tokens (pitch → notes, duration → note length)
        |
   [ CS 542 ]  Classifier → emotion label (angry, happy, sad, neutral)
```

The 545 project is the **upstream pipeline** — it solves the hard problem of *when* each sound happens. The 542 project is the **downstream consumer** — it asks *what that timing pattern means* emotionally. The 542 project can run independently using ESD's built-in labels as a fallback if the 545 aligner isn't ready.

All Rights Reserved Sky Vercauteren November-December 2026
