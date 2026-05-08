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
