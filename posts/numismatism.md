---
title: "Coin Analysis"
date: "2026-01-19 06:10"
tags: ["coin", "coins", "machine learning", "computer vision", "numismatist", "numismatism", "collecting", "python"]
blurb: "Coin ML Tool"
one_liner: "Computer-vision and ML experiments for recognising, identifying and cataloguing coins from images."
image: /static/images/numismatism.png
social_image: /static/images/numismatism.png
---

[Coin Analysis](https://github.com/oernster/coin-analysis) 🪙

## Problem → Solution → Impact

**Problem:** Few modern computer vision tools exist for identifying collectible coins.  
**Solution:** This app uses machine learning and CV to recognize years and mint marks.  
**Impact:** A working educational prototype for ML use cases in a niche hobby.

---

## Rationale

A couple of friends in the US were manually identifying 1¢ coins under microscopes. This tool streamlines that: a desktop application that recognises years and mint marks on US cents using ML + CV.  

> **Note:** Data availability remains poor, so model accuracy is limited. It's a personal prototype, a fossil of fast coding, and I'm okay with that.

---

## Features at a Glance

| 🖼️ Image Handling              | 🤖 Machine Learning             |
|------------------------------|--------------------------------|
| Image preprocessing tools    | Basic classification model     |
| Batch image processing       | Option to train your own model |
| Format support: PNG, JPG...  | OCR planned (future)           |

| 💻 Desktop App UI             | 📦 Export / Integration         |
|------------------------------|--------------------------------|
| Built with PySide6 (Qt)      | Export results as CSV or JSON  |
| Tabs for single/batch input  |                                |
| Inline preview of results    |                                |

---

## How It Works

### Single Image Processing

1. Click **"Open Image"** to load
2. Tweak enhancement settings
3. Click **"Process"**
4. View the output in results panel

### Batch Mode

1. Switch to the **Batch** tab  
2. Choose multiple images or a folder  
3. Process them all at once  
4. Export results if needed

---

## Image Requirements

| Condition                        | Details                                  |
|----------------------------------|------------------------------------------|
| **Side of coin**                 | Right side preferred                     |
| **What must be visible**        | Year and mint mark                       |
| **Image coverage**              | Partial coins are OK                     |
| **Formats supported**           | PNG, JPG, JPEG, BMP, TIF, TIFF           |

---

## Training a Custom Model

You can improve results by training on your own dataset.

1. Collect labelled coin images
2. Place them in `data/raw`
3. Use the **Train Model** tool in-app
4. Follow the wizard to generate your new model

---

## Future Improvements

- Transfer learning via deeper networks  
- Text-based OCR for better year/mint detection  
- Support for coins outside the US  
- Lightweight mobile version  

---
