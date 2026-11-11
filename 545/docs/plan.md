# CS 545 — Plan

## Strategy
Reproduce Graves et al. (2006) using a biLSTM + CTC loss on TIMIT. The goal is a model that takes audio frames + a transcript and outputs ms-level word boundary timings. CTC handles alignment without needing frame-level labels — only the transcript is required.

Architecture: biLSTM → linear → softmax over phoneme vocabulary (+ blank token). CTC loss during training. Viterbi decode at inference to extract the best path → word boundaries.

Scoring: phone error rate (PER) and boundary error (ms) against TIMIT gold timings. Control group: same biLSTM trained with cross-entropy on TIMIT's frame-level labels (requires more supervision, makes CTC's advantage measurable).

Stretch goal: replace biLSTM with a Transformer encoder and compare on the same metrics. Expect data to be too small for Transformer to win, but that's a valid finding.

## TODO
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

## Milestones
- **Nov 8** — CTC verified on toy data, TIMIT pipeline ready
- **Nov 26** — biLSTM + CTC vs. cross-entropy scored on both metrics
- **Nov 30** — core notebook drafted
- **Dec 16** — final submission
