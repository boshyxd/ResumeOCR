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
- google-generativeai
- Pillow (PIL)

## Usage

1. Place resume image files (PNG, JPG, JPEG) in `~/Documents/ResumePng/`
2. Create a .env file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Run the script
4. Find the combined results in `~/Documents/ResumeDump/combined_results.txt`
