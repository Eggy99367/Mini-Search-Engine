# Mini Search Engine

A lightweight search engine implemented in **Python** as part of **CS121 Assignment 3**.  
The project demonstrates the core concepts of indexing and retrieval, building a functional prototype of a search engine.

## Features

- Reads and preprocesses input documents  
- Builds an inverted index for fast retrieval  
- Supports keyword and boolean-style queries  
- Returns ranked results based on relevance  
- Includes a simple test file (`TEST.txt`) and project report (`report.pdf`)  

## Project Structure

```
Mini-Search-Engine/
├── a3.py          # Main entry point
├── src/           # Core modules (indexing, searching, utilities)
├── TEST.txt       # Sample test file
├── report.pdf     # Project report
├── README.md
```

## Installation & Usage

1. Clone the repository:

```bash
git clone https://github.com/Eggy99367/Mini-Search-Engine.git
cd Mini-Search-Engine
```

2. Run the program:

```bash
python a3.py
```

3. Enter a query string when prompted.  
   The engine will return matching documents ranked by relevance.

## Technical Details

- **Language:** Python  
- **Core Data Structure:** Inverted Index (maps terms → documents)  
- **Query Processing:** Boolean and keyword matching  
- **Ranking:** Simple relevance scoring (e.g., based on term frequency)  

## License

This project is intended for **educational purposes** as part of CS121 coursework.  
