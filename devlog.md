# Devlog

## 2026-05-08 00:44

### Initial Thoughts

Currently trying to understand the bigger picture on how the B-Tree will be structured on disk and how the file I/O will work with the 512 byte block system. Read through the spec and looked at the test.idx binary file to get a feel for how the header and nodes are laid out. The big endian integer requirement and the 3 node memory limit are the two things I'm still wrapping my head around.

### Overall Plan

I'm thinking of using Python since it has clean support for big endian byte packing with to_bytes and from_bytes. Will start with getting the file creation and header reading working first then move into the node structure and eventually the full B-Tree insert with splitting. Going to validate each piece against the provided test.idx before moving on to the next command.

### Open Questions

I'm not totally sure how to handle the 3 node memory limit when doing inserts that cause splits propagating up multiple levels. Will definitely need to rethink the approach as I get deeper into the insert logic.

---

## 2026-05-08 (session 2)

### What Was Done

Implemented the three remaining commands to complete the project:

**`load`** — reads a CSV file line by line, splits on comma, and calls `btree_insert` for each key/value pair. Handles missing file error and skips blank lines.

**`print`** — traverses the B-tree in sorted order and prints each pair as `key,value` to stdout.

**`extract`** — same traversal as print but writes to a file. Errors if the output file already exists (per spec).

The traversal for both `print` and `extract` uses `btree_inorder_pairs`, an iterative generator that uses the parent pointers already stored in each node. Starting from the leftmost leaf, it:
1. Yields all keys in the current leaf
2. Climbs to the parent using `parent_id`, finds which child slot it came from by scanning `parent.children`
3. Emits the separator key at that slot, then descends to the leftmost leaf of the next child
4. Repeats until the root has been exhausted as the last child at some level

At most 2 nodes are in memory at any point during traversal (current + parent), well within the 3-node limit.

### Tested Against

- `test.idx` from the course: `print` outputs all 32 pairs in sorted order (1–31, then 50→100)
- Fresh index loaded from a CSV, then extracted — round-trips correctly
- 50 randomly-ordered inserts (forcing splits), then `print` — output is fully sorted

### Status

All 6 commands implemented: `create`, `insert`, `search`, `load`, `print`, `extract`.

---
