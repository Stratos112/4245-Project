# CS 542 — Plan

## Strategy
Convert prosodic features (pitch → MIDI note, duration → note length, energy → velocity) into MIDI token sequences, then classify emotion from those sequences. The key framing: same transcript spoken in different emotions produces different "music" — the MIDI representation makes that learnable.

Primary path: use ESD's built-in word-level timestamps (no dependency on 545). Secondary path: pipe audio through the 545 aligner for finer-grained boundaries.

Classifier tiers:
1. **Baseline** — logistic regression on utterance-level summary stats (mean pitch, range, speaking rate)
2. **Main** — one HMM per emotion class (each HMM learns what that emotion's note sequences look like; classify by highest forward-algorithm score)
3. **Comparison** — BiLSTM over the same MIDI sequences

Also run the same classifiers on raw continuous pitch/energy to measure what MIDI quantization costs.

Dataset: ESD (same sentences per speaker per emotion → text can't leak the answer). Merge to 4 classes (angry, happy, sad, neutral) for class balance. Test on held-out speakers to guard against the speaker-identity shortcut.

## TODO
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

## Milestones
- **Nov 15** — ESD loaded, prosody pipeline + MIDI conversion working
- **Nov 26** — all three classifiers trained and scored
- **Dec 10** — report drafted
- **Dec 16** — final submission
