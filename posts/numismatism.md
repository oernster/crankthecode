---
blurb: Coin ML Tool
date: 2026-01-19 06:10
type: project
image: /static/images/numismatism.png
thumb_image: /static/images/coin-analysis-icon.svg
one_liner: Computer-vision and ML experiments for recognising, identifying and cataloguing
  coins from images.
social_image: /static/images/numismatism.png
tags:
- cat:Data / Ml
- coin
- coins
- machine learning
- computer vision
- numismatist
- numismatism
- collecting
- python
title: Coin Analysis
---

[Coin Analysis](https://ernster.dev/coin-analysis/) is a computer-vision and machine-learning tool for recognising, identifying and cataloguing coins from images.

## Problem → System → Outcome

**Problem.** Few modern computer vision tools exist for identifying collectible coins.  
**System.** This app uses machine learning and CV to recognise years and mint marks.  
**Outcome.** Collectors could identify coins from imperfect photos without needing specialist knowledge or manual cross-referencing.

---

## Rationale

A couple of friends in the US were manually identifying 1¢ coins under microscopes. This tool streamlines that: a desktop application that recognises years and mint marks on US cents using ML + CV.  

> **Note:** Data availability remains poor, so model accuracy is limited. It's a personal prototype, a fossil of fast coding and I'm okay with that.

---

## What it does

A PySide6 desktop application over OpenCV, scikit-learn and Tesseract that reads the year and mint mark off US cent photographs: a machine-learning classifier and an OCR reader each read the coin independently and a confidence-scored hybrid decides between them, cross-checked against historically valid mint-and-year combinations. Single images or whole folders in batch, partial coins accepted, results exported to CSV or JSON, all local. The full rundown lives on the product site: [ernster.dev/coin-analysis](https://ernster.dev/coin-analysis/).
