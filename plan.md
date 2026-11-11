# Project Plan

## CS 545 — Forced Alignment with CTC

### Strategy
Reproduce Graves et al. (2006) using a biLSTM + CTC loss on TIMIT. The goal is a model that takes audio frames + a transcript and outputs ms-level word boundary timings. CTC handles alignment without needing frame-level labels — only the transcript is required.

Architecture: biLSTM → linear → softmax over phoneme vocabulary (+ blank token). CTC loss during training. Viterbi decode at inference to extract the best path → word boundaries.

Scoring: phone error rate (PER) and boundary error (ms) against TIMIT gold timings. Control group: same biLSTM trained with cross-entropy on TIMIT's frame-level labels (requires more supervision, makes CTC's advantage measurable).

Stretch goal: replace biLSTM with a Transformer encoder and compare on the same metrics. Expect data to be too small for Transformer to win, but that's a valid finding.

### TODO
- [ ] Verify CTC loss implementation on toy data against `torch.nn.CTCLoss`
- [ ] Load and clean TIMIT (deduplicate, normalize audio, encode phoneme labels)
- [ ] Build MFCC feature extraction pipeline (frame step, window size)
- [ ] Implement biLSTM + CTC training loop with configurable hyperparameters
- [ ] Implement Viterbi decode over CTC output matrix
- [ ] Implement boundary error metric (ms) and PER
- [ ] Run controlled hyperparameter sweep (learning rate, hidden size, layers)
- [ ] Run control group: cross-entropy on frame-level labels, same architecture
- [ ] Write notebook: explain CTC, compare results, discuss failure cases
- [ ] (Stretch) Swap biLSTM for Transformer encoder, retrain, compare

### Milestones
- **Nov 8** — CTC verified on toy data, TIMIT pipeline ready
- **Nov 26** — biLSTM + CTC vs. cross-entropy scored on both metrics
- **Nov 30** — core notebook drafted
- **Dec 16** — final submission

---

## CS 542 — Emotion Classification via MIDI Prosody

### Strategy
Convert prosodic features (pitch → MIDI note, duration → note length, energy → velocity) into MIDI token sequences, then classify emotion from those sequences. The key framing: same transcript spoken in different emotions produces different "music" — the MIDI representation makes that learnable.

Primary path: use ESD's built-in word-level timestamps (no dependency on 545). Secondary path: pipe audio through the 545 aligner for finer-grained boundaries.

Classifier tiers:
1. **Baseline** — logistic regression on utterance-level summary stats (mean pitch, range, speaking rate)
2. **Main** — one HMM per emotion class (each HMM learns what that emotion's note sequences look like; classify by highest forward-algorithm score)
3. **Comparison** — BiLSTM over the same MIDI sequences

Also run the same classifiers on raw continuous pitch/energy to measure what MIDI quantization costs.

Dataset: ESD (same sentences per speaker per emotion → text can't leak the answer). Merge to 4 classes (angry, happy, sad, neutral) for class balance. Test on held-out speakers to guard against the speaker-identity shortcut.

### TODO
- [ ] Request IEMOCAP license from USC (if using IEMOCAP as supplement)
- [ ] Download and explore ESD; confirm timestamp format and emotion labels
- [ ] Build prosody extraction pipeline: pitch (YIN or Praat), energy, duration per word/syllable
- [ ] Build MIDI conversion: pitch → nearest semitone, duration → grid quantization, energy → velocity
- [ ] Implement baseline (logistic regression on summary stats)
- [ ] Implement HMM-per-class classifier (Gaussian emissions over pitch/duration/velocity)
- [ ] Implement BiLSTM classifier with padding/masking
- [ ] Run all three classifiers on MIDI features and on raw continuous features
- [ ] Analyze: where does each model fail? (quiet emotions, short utterances, speaker outliers?)
- [ ] Write report: questions, hypotheses, results, discussion

### Milestones
- **Nov 15** — ESD loaded, prosody pipeline + MIDI conversion working
- **Nov 26** — all three classifiers trained and scored
- **Dec 10** — report drafted
- **Dec 16** — final submission

---

## Shared / Cross-Project

- [ ] Decide on shared data directory structure (`data/timit/`, `data/esd/`)
- [ ] Export word boundary timings from 545 in a format 542 can consume (CSV: `file, word, start_ms, end_ms`)
- [ ] Confirm with both instructors that sharing one pipeline across two classes is OK
