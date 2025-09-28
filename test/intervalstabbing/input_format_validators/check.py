#!/usr/bin/env python3
# Usage (Polygon-style): check.py input.txt output.txt
# Accepts any optimal solution: covers all intervals and k equals greedy optimum.
import sys,re

def die(code, msg):
    print(msg)
    sys.exit(code)

def read_intervals(inp_path):
    with open(inp_path, "r", encoding="utf-8") as f:
        data = f.read()
    if not data.endswith("\n"):
        die(1, "Wrong answer: input missing terminal newline")
    it = iter(data.strip("\n").splitlines())
    try:
        n = int(next(it).strip())
    except:
        die(1, "Internal error: bad input header")
    intervals = []
    for i in range(n):
        try:
            l, r = map(int, next(it).split())
        except:
            die(1, f"Internal error: bad interval line {i+2}")
        intervals.append((l, r))
    return intervals

def parse_output(out_path):
    with open(out_path, "r", encoding="utf-8") as f:
        data = f.read()
    data = data.strip()
    if data == "":
        die(1, "Wrong answer: empty output")
    lines = data.splitlines()
    if len(lines) < 1:
        die(1, "Wrong answer: missing k")
    # allow extra empty lines at end but require 1 or 2 non-empty lines
    lines = [ln.strip() for ln in lines if ln.strip() != ""]
    if not lines:
        die(1, "Wrong answer: empty output")
    # first line: k
    try:
        k = int(lines[0])
    except:
        die(1, "Wrong answer: first line must be an integer k")
    if k < 0:
        die(1, "Wrong answer: k must be nonnegative")
    if len(lines) == 1:
        if k != 0:
            die(1, "Wrong answer: missing point list")
        points = []
    else:
        # parse exactly k integers on second line
        toks = lines[1].split()
        if len(toks) != k:
            die(1, f"Wrong answer: expected {k} integers on second line, got {len(toks)}")
        try:
            points = list(map(int, toks))
        except:
            die(1, "Wrong answer: non-integer in points list")
        # must be nondecreasing
        if any(points[i] > points[i+1] for i in range(len(points)-1)):
            die(1, "Wrong answer: points must be in nondecreasing order")
    # no further constraints; returning
    return k, points

def covers_all(intervals, points):
    # intervals are closed; integers suffice
    i = 0
    j = 0
    n = len(intervals)
    m = len(points)
    while i < n:
        l, r = intervals[i]
        # advance j until point >= l
        while j < m and points[j] < l:
            j += 1
        if j == m or points[j] > r:
            return False
        i += 1
    return True

def greedy_opt(intervals):
    # classic: sort by r, pick r, skip covered
    intervals = sorted(intervals, key=lambda x: x[1])
    points = []
    i = 0
    n = len(intervals)
    while i < n:
        _, r = intervals[i]
        points.append(r)
        i += 1
        while i < n and intervals[i][0] <= r <= intervals[i][1]:
            i += 1
    return len(points)

def main():
    if len(sys.argv) < 3:
        print("Checker usage: check.py <input> <output>")
        sys.exit(1)

    intervals = read_intervals(sys.argv[1])
    # normalize intervals: closed, sort by l then r for coverage check
    intervals_sorted = sorted(intervals, key=lambda x: (x[0], x[1]))

    k, pts = parse_output(sys.argv[2])

    # coverage check
    if not covers_all(intervals_sorted, pts):
        die(1, "Wrong answer: not all intervals are covered")

    # optimality check
    k_opt = greedy_opt(intervals_sorted)
    if k != k_opt:
        die(1, f"Wrong answer: k={k} but optimal is {k_opt}")

    die(0, "OK")

if __name__ == "__main__":
    main()
