#!/usr/bin/env python3
import sys
import os

BLOCK_SIZE = 512
MAGIC = b'4348PRJ3'


def read_block(f, block_id):
    f.seek(block_id * BLOCK_SIZE)
    data = f.read(BLOCK_SIZE)
    if len(data) < BLOCK_SIZE:
        data = data + b'\x00' * (BLOCK_SIZE - len(data))
    return data


def write_block(f, block_id, data):
    padded = data + b'\x00' * (BLOCK_SIZE - len(data))
    f.seek(block_id * BLOCK_SIZE)
    f.write(padded)


def read_header(f):
    data = read_block(f, 0)
    if data[0:8] != MAGIC:
        print("Error: not a valid index file", file=sys.stderr)
        sys.exit(1)
    root_id = int.from_bytes(data[8:16], 'big')
    next_block_id = int.from_bytes(data[16:24], 'big')
    return root_id, next_block_id


def write_header(f, root_id, next_block_id):
    data = bytearray(BLOCK_SIZE)
    data[0:8] = MAGIC
    data[8:16] = root_id.to_bytes(8, 'big')
    data[16:24] = next_block_id.to_bytes(8, 'big')
    write_block(f, 0, bytes(data))


MAX_KEYS = 19
MAX_CHILDREN = 20


class Node:
    def __init__(self, block_id, parent_id=0):
        self.block_id = block_id
        self.parent_id = parent_id
        self.num_keys = 0
        self.keys = [0] * MAX_KEYS
        self.values = [0] * MAX_KEYS
        self.children = [0] * MAX_CHILDREN

    @staticmethod
    def from_block(data):
        def rd(offset):
            return int.from_bytes(data[offset:offset + 8], 'big')

        node = Node(rd(0), rd(8))
        node.num_keys = rd(16)
        for i in range(MAX_KEYS):
            node.keys[i] = rd(24 + i * 8)
        for i in range(MAX_KEYS):
            node.values[i] = rd(176 + i * 8)
        for i in range(MAX_CHILDREN):
            node.children[i] = rd(328 + i * 8)
        return node

    def to_block(self):
        data = bytearray(BLOCK_SIZE)

        def wr(offset, val):
            data[offset:offset + 8] = val.to_bytes(8, 'big')

        wr(0, self.block_id)
        wr(8, self.parent_id)
        wr(16, self.num_keys)
        for i in range(MAX_KEYS):
            wr(24 + i * 8, self.keys[i])
        for i in range(MAX_KEYS):
            wr(176 + i * 8, self.values[i])
        for i in range(MAX_CHILDREN):
            wr(328 + i * 8, self.children[i])
        return bytes(data)

    def is_leaf(self):
        return self.children[0] == 0


def read_node(f, block_id):
    return Node.from_block(read_block(f, block_id))


def write_node(f, node):
    write_block(f, node.block_id, node.to_block())


def open_index(filename):
    if not os.path.exists(filename):
        print(f"Error: file '{filename}' does not exist", file=sys.stderr)
        sys.exit(1)
    f = open(filename, 'r+b')
    data = read_block(f, 0)
    if data[0:8] != MAGIC:
        print(f"Error: '{filename}' is not a valid index file", file=sys.stderr)
        f.close()
        sys.exit(1)
    return f


def cmd_create(args):
    if len(args) < 1:
        print("Usage: project3 create <filename>", file=sys.stderr)
        sys.exit(1)
    filename = args[0]
    if os.path.exists(filename):
        print(f"Error: file '{filename}' already exists", file=sys.stderr)
        sys.exit(1)
    with open(filename, 'wb') as f:
        write_header(f, 0, 1)


def main():
    if len(sys.argv) < 2:
        print("Usage: project3 <command> [args...]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    if cmd == 'create':
        cmd_create(args)
    else:
        print(f"Error: unknown command '{cmd}'", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
