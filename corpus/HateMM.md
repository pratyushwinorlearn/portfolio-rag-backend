# HateMM

# HateMM — Multimodal Harmful Content Classifier

A production-ready deep learning system that classifies hateful social media content using **three modalities**: image (ViT), text caption (RoBERTa), and OCR text extracted from images (EasyOCR + RoBERTa).

---

## Architecture Overview

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  ViT-B/16    │  │ RoBERTa-base │  │ RoBERTa-base │
│  (Image)     │  │ (Caption)    │  │ (OCR Text)   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
  Projection        Projection        Projection
  Head (768)        Head (768)        Head (768)
       │                 │                 │
       └────────┬────────┴────────┬────────┘
                │                 │
         Modality-Gated     Missing Modality
         Attention (MGA)    Mask Tokens
                │
     ┌──────────┴──────────┐
     │  Cross-Modal         │
     │  Transformer (6L)    │
     │  8 heads, 2048 FFN   │
     └──────────┬──────────┘
                │
          Mean Pooling
                │
     ┌──────────┴──────────┐
     │  Classifier Head     │
     │  768→256→64→2        │
     └─────────────────────┘
```

## Key Features

- **Three-phase training**: Contrastive pretraining → Full fine-tuning → Hard negative mining
- **Missing modality robustness**: Learned mask tokens replace absent modalities
- **Modality-Gated Attention**: Adaptive weighting with interpretable gate values
- **Hardware-optimised**: Mixed precision (fp16), gradient accumulation, frozen encoder layers, `torch.compile()`
- **Full evaluation suite**: AUROC, F1, confusion matrix, ROC/PR curves, modality ablation

---

## Hardware Requirements

| Component | Specification |
|-----------|---------------|
| GPU | NVIDIA RTX 4060 Laptop (8 GB VRAM) or equivalent |
| CUDA | 12.1+ |
| RAM | 16 GB+ recommended |
| OS | Windows 11 / Linux |

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Data

See [`data/README.md`](data/README.md) for detailed instructions on downloading MMHS150K or Hateful Memes.

Your final CSV (`data/dataset.csv`) must have columns: `image_path`, `text`, `label`.

### 3. Verify Pipeline (Dry Run)

```bash
python train.py --config config.yaml --dry-run
```

This runs 2 batches per training phase to verify everything works before committing to a full run.

### 4. Train

```bash
python train.py --config config.yaml
```

Training runs three phases:
1. **Phase 1** (5 epochs): Contrastive pretraining — aligns image and text embeddings
2. **Phase 2** (15 epochs): Full fine-tuning — all components with early stopping
3. **Phase 3** (3 epochs): Hard negative mining — re-trains on low-confidence samples

Best model is saved to `checkpoints/best_model.pt`.

### 5. Evaluate

```bash
python evaluate.py --config config.yaml --checkpoint checkpoints/best_model.pt
```

Generates:
- `results/test_metrics.json` — AUROC, F1, Precision, Recall, Accuracy
- `results/roc_curve.png` — ROC curve
- `results/pr_curve.png` — Precision-Recall curve
- `results/confusion_matrix.png` — Confusion matrix
- `results/ablation_results.json` — Missing-modality comparison
- `results/modality_importance.json` — Gate weight averages

---

## Project Structure

```
hatemm/
├── data/
│   └── README.md                  ← instructions to download datasets
├── models/
│   ├── __init__.py
│   └── hatemm.py                  ← full model architecture
├── dataset.py                     ← dataset class, OCR extraction, augmentation
├── train.py                       ← 3-phase training loop
├── evaluate.py                    ← metrics, plots, ablation
├── config.yaml                    ← all hyperparameters
├── requirements.txt               ← pip dependencies
└── README.md                      ← this file
```

---

## Configuration

All hyperparameters are centralised in `config.yaml`. Key settings:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `batch_size` | 32 | Per-GPU batch size |
| `grad_accumulation_steps` | 2 | Effective batch = 64 |
| `learning_rate` | 2e-5 | AdamW learning rate |
| `phase1_epochs` | 5 | Contrastive pretraining epochs |
| `phase2_epochs` | 15 | Fine-tuning epochs |
| `phase3_epochs` | 3 | Hard negative mining epochs |
| `freeze_encoder_layers` | 8 | Frozen ViT/RoBERTa layers |
| `fp16` | true | Mixed precision training |
| `missing_image_prob` | 0.15 | Image dropout probability |
| `missing_text_prob` | 0.10 | Text dropout probability |
| `missing_ocr_prob` | 0.20 | OCR dropout probability |

---

## Weights & Biases

Training logs to [Weights & Biases](https://wandb.ai/) automatically. Set your project name in `config.yaml`:

```yaml
wandb:
  project: hatemm
  entity: your-username  # or null for default
```

Logged metrics include: train/val loss, AUROC, F1, modality gate weights, learning rate, GPU memory.

---

## Citation

If you use this code, please cite the relevant datasets:

```bibtex
@inproceedings{gomez2020mmhs150k,
  title={Exploring Hate Speech Detection in Multi-Modal Publications},
  author={Gomez, Raul and Gibert, Jaume and Gomez, Lluis and Karatzas, Dimosthenis},
  booktitle={WACV},
  year={2020}
}

@inproceedings{kiela2020hateful,
  title={The Hateful Memes Challenge: Detecting Hate Speech in Multi-Modal Memes},
  author={Kiela, Douwe and Firooz, Hamed and others},
  booktitle={NeurIPS},
  year={2020}
}
```

---

## License

This project is for research and educational purposes.
