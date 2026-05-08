# Devlog

## 2026-05-08 00:44

### Initial Thoughts

Currently trying to understand the bigger picture on how the B-Tree will be structured on disk and how the file I/O will work with the 512 byte block system. Read through the spec and looked at the test.idx binary file to get a feel for how the header and nodes are laid out. The big endian integer requirement and the 3 node memory limit are the two things I'm still wrapping my head around.

### Overall Plan

I'm thinking of using Python since it has clean support for big endian byte packing with to_bytes and from_bytes. Will start with getting the file creation and header reading working first then move into the node structure and eventually the full B-Tree insert with splitting. Going to validate each piece against the provided test.idx before moving on to the next command.

### Open Questions

I'm not totally sure how to handle the 3 node memory limit when doing inserts that cause splits propagating up multiple levels. Will definitely need to rethink the approach as I get deeper into the insert logic.

---
