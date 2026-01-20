---
title: "Coin Analysis"
date: "2026-01-19 06:10"
tags: ["coin", "coins", "machine learning", "computer vision", "numismatist", "numismatism", "collecting", "python"]
blurb: "Coin ML Tool"
one_liner: "Computer-vision and ML experiments for recognising, identifying, and cataloguing coins from images."

# Used by the site as the cover image AND by the RSS feed thumbnail.
# It will NOT be duplicated in the post body (the renderer strips a matching standalone image paragraph).
image: /static/images/numismatism.png
social_image: /static/images/numismatism.png
---
[Coin Analysis](https://github.com/oernster/coin-analysis)  🪙

## Problem → Solution → Impact

**Problem:** There are few modern computer vision solutions tailored for identifying and sorting collectible coins.

**Solution:** This project explores ML classification for coins using custom-trained models and image recognition.

**Impact:** A helpful educational prototype in vision + classification for niche ML use cases.

# Rationale
A US friend of mine (well 2 of them actually) are really into collecting 1 cent coins and manually identifying each one
using simple desktop scopes.  I wanted to make their life a little easier for processing coins.

This is a desktop application for recognising years and mint marks on US cents using computer vision and machine learning 
techniques.

# Challenges along the way
This was very hard to get the machine learning and computer vision algorithms to work as I desired.
Even now, the source data sets I was able to find on the internet are really insufficient to properly test the app.
I'd love to train it on better data sets to prove it more but I can't find any good data sources anywhere apart from what 
I'm already using.  Full disclosure, I _did_ to be fully honest, use AI to create the code since I wanted something quick 
for my friends to work with.

I'm not particularly proud of the maintainability of the code but since I can't find any good data sources online for 
Machine Learning material.  Therefore, I feel it's not worth investing any more time into this little project.

Basically this is now my personally curated fossil. I'll keep it in a jar.

# Coin Recognition Application

## Overview

This application is designed to analyze images of US cents and identify the year and mint mark on the right side of the coin. It works with partial coin images and can process both individual images and batches of images.

## Features

- **Image Processing**: Preprocess coin images to enhance features for recognition
- **Feature Extraction**: Extract relevant features from coin images
- **Machine Learning**: Recognize years and mint marks using trained models
- **User Interface**: Intuitive desktop interface built with PySide6
- **Batch Processing**: Process multiple images at once
- **Result Export**: Export recognition results to CSV or JSON formats
- **Image Enhancement**: Tools for adjusting image preprocessing parameters

### Single Image Processing

1. Click "Open Image" to load a coin image
2. Adjust enhancement parameters if needed
3. Click "Process" to recognize the year and mint mark
4. View results in the results panel

### Batch Processing

1. Switch to the "Batch Processing" tab
2. Click "Select Folder" or "Select Files" to choose images
3. Click "Process" to start batch processing
4. View results in the results table
5. Export results to CSV or JSON if needed

## Image Requirements

- Images should show the right side of US cents
- The year and mint mark should be visible
- Images can be partial (don't need to show the entire coin)
- Supported formats: PNG, JPG, JPEG, BMP, TIF, TIFF

## Training Your Own Model

The application comes with a basic model, but you can train your own model using your own dataset:

1. Collect images of US cents with visible years and mint marks
2. Place the images in the `data/raw` directory
3. Use the "Train Model" option in the Tools menu
4. Follow the training wizard to create and train your model

## Future Improvements

- Transfer learning with deep neural networks for improved accuracy
- OCR integration for direct text recognition
- Support for other coin types
- Mobile application version
