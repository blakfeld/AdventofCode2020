#!/usr/bin/env python

import re
import sys
from collections import Counter
from dataclasses import dataclass


@dataclass
class PasswordReq:
    req_char: str = None
    min_count: int = 0
    max_count: int = 0


def parse_input(input_path):
    parse_re = re.compile(r'(\d+)\-(\d+) (\w): (\w+)')
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            match = parse_re.match(line)
            if not match:
                continue

            min_count, max_count, req_char, password = match.groups()
            password_req = PasswordReq(
                req_char=req_char,
                min_count=int(min_count),
                max_count=int(max_count)
            )

            yield password, password_req


def is_valid_password_part_one(password, reqs_obj):
    char_counts = Counter(password)
    count = char_counts.get(reqs_obj.req_char, 0)

    return reqs_obj.min_count <= count <= reqs_obj.max_count


def is_valid_password_part_two(password, reqs_obj):
    pos_one = reqs_obj.min_count - 1
    pos_two = reqs_obj.max_count - 1
    req_char = reqs_obj.req_char

    match_one = password[pos_one] == req_char
    match_two = password[pos_two] == req_char

    if match_one and match_two:
        return False
    elif match_one or match_two:
        return True


def main():
    input_path = sys.argv[1]

    print('Part One')
    p1_result = filter(
        lambda p: is_valid_password_part_one(*p),
        parse_input(input_path)
    )
    p1_result = map(lambda x: x[0], p1_result)
    print(len(list(p1_result)))
    print()

    print('Part Two')
    p2_result = filter(
        lambda p: is_valid_password_part_two(*p),
        parse_input(input_path)
    )
    p2_result = map(lambda p: p[0], p2_result)
    print(len(list(p2_result)))


if __name__ == '__main__':
    main()
