# LINGUANA
## Linguistics Analyser
* Application designed for analyzing various forms of text
* Builds fingerprints for classified text to associate authorship
* Can do comparitive analysis on text, compare and contrast if two structures align

## Setup
1. Install dependencies
```
pip install -r requirements.txt
```

## Usage
1. Fingerprint style of document
```
python3 ./main.py --input <PATH TO TEXT FILE>
```
2. Fingerprint style of document and output results
```
python3 ./main.py --input <PATH> --output <PATH>
```
3. Launch collaborative web server
```
python3 ./server.py
```

## Features
* N-gram factorial style pairing
* Spelling mistake tracking
* Word frequency and usage
* Words per line hits tracking
* Characters per word hits tracking

## Future Plans
* Create OCR features for picking apart non-text data
* Llama Guard v2 integration for categorizing text