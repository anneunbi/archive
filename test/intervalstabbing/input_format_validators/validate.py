#!/usr/bin/env python3
import sys,re

INT_MIN, INT_MAX = -10**9, 10**9
N_MIN, N_MAX = 200000

def die(msg):
    print(f"invalid: {msg}", file=sys.stderr)
    sys.exit(1)

def read_all():
    data = sys.stdin.read()
    if not data.endswith("\n"):
        die("file must end with newline")
    return data

def main():
    data = read_all()
    lines = data.strip("\n").split("\n")
    if not lines:
        die("empty file")

    def parse_line(line):
        toks = line.strip().split()
        if not toks:
            die("blank line not allowed")
        return toks

    # first line: n
    toks0 = parse_line(lines[0])
    if len(toks0) != 1 or not re.fullmatch(r"-?\d+", toks0[0]):
        die("first line must contain a single integer n")
    try:
        n = int(toks0[0])
    except:
        die("n not an integer")
    if not (1 <= n <= N_MAX):
        die(f"n out of range [1,{N_MAX}]")

    if len(lines) != 1 + n:
        die(f"expected {n} interval lines, got {len(lines)-1}")

    for i in range(n):
        toks = parse_line(lines[1+i])
        if len(toks) != 2:
            die(f"line {i+2}: expected two integers l r")
        if not all(re.fullmatch(r"-?\d+", t) for t in toks):
            die(f"line {i+2}: non-integer token")
        l, r = map(int, toks)
        if l > r:
            die(f"line {i+2}: requires l <= r")
        if not (INT_MIN <= l <= INT_MAX and INT_MIN <= r <= INT_MAX):
            die(f"line {i+2}: endpoint out of range [{INT_MIN},{INT_MAX}]")

    # no extra content beyond the n+1 lines (we already enforced last char newline)
    sys.exit(0)

if __name__ == "__main__":
    main()
