# ResumeOCR

ResumeOCR is a Python script that automates the process of converting multiple resume images (PNG format) to text files using Optical Character Recognition (OCR).

## Description

This tool scans a specified input folder for PNG images of resumes, uses OCR to extract the text content, and saves each result as a separate text file in an output folder. It's designed to help streamline the process of digitizing and managing large numbers of resume images.

## Features

- Batch processing of multiple PNG files
- Automatic naming of output text files
- Configurable input and output directories

## Requirements

- Python 3.x
- pytesseract
- Pillow (PIL)
- Tesseract OCR engine

## Usage

1. Place resume PNG files in `~/Documents/ResumePng/`
2. Run the script
3. Find converted text files in `~/Documents/ResumeDump/`
