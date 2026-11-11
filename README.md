# Speech Prosody Projects — CS545 + CS542

Two connected school projects. CS545 builds a forced aligner that finds word boundaries in audio using CTC loss. CS542 takes those boundaries, converts prosody to MIDI notation, and classifies emotion from the resulting sequences.

```
Raw audio + transcript
        |
   [ CS 545 ]  BiLSTM + CTC → word/phoneme boundaries (ms-level)
        |
   Convert to MIDI tokens (pitch → notes, duration → note length)
        |
   [ CS 542 ]  Classifier → emotion label (angry, happy, sad, neutral)
```

See `plan.md` for strategy and TODOs.

---

## Running

> Instructions will be filled in as the projects are built.

**CS 545**
```bash
# cd 545/
# jupyter notebook forced_alignment.ipynb
```

**CS 542**
```bash
# cd 542/
# jupyter notebook emotion_classification.ipynb
```

---

All Rights Reserved Sky Vercauteren November-December 2026
