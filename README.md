# Project 3 — B-Tree Index File Manager
CS4348 Operating Systems Concepts | Spring 2026

## Requirements
- Python 3

## Running

All commands follow the pattern:
```
python3 btree_index.py <command> [args...]
```

---

### create
Create a new empty index file.
```bash
python3 btree_index.py create test.idx
```

---

### insert
Insert a key/value pair into the index. If the key already exists, its value is updated.
```bash
python3 btree_index.py insert test.idx 15 100
```

---

### search
Search for a key. Prints `key,value` if found, otherwise prints an error.
```bash
python3 btree_index.py search test.idx 15
```

---

### load
Bulk-insert key/value pairs from a CSV file. Each line should be `key,value`.
```bash
python3 btree_index.py load test.idx input.csv
```

Example `input.csv`:
```
1,10
2,20
3,30
```

---

### print
Print every key/value pair in the index in sorted order.
```bash
python3 btree_index.py print test.idx
```

---

### extract
Save every key/value pair to a CSV file in sorted order. Fails if the output file already exists.
```bash
python3 btree_index.py extract test.idx output.csv
```

---

## Quick Verification

```bash
python3 btree_index.py create test.idx
python3 btree_index.py insert test.idx 10 100
python3 btree_index.py insert test.idx 5 50
python3 btree_index.py insert test.idx 20 200
python3 btree_index.py print test.idx
# Expected output:
# 5,50
# 10,100
# 20,200
python3 btree_index.py search test.idx 10
# Expected output:
# 10,100
python3 btree_index.py search test.idx 99
# Expected output:
# Error: key 99 not found
```
