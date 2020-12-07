#!/usr/bin/env python

import sys
from collections import Counter


def parse_records(input_path):
    with open(input_path, 'r') as f:
        for line in map(lambda l: l.strip(), f):
            if line:
                yield line
            else:
                yield None


def all_answers_for_group(records):
    group_answers = set()
    for record in records:
        if record:
            group_answers.update(list(record))
        else:
            yield group_answers
            group_answers = set()

    yield group_answers


def matching_answers_for_group(records):
    member_count = 0
    group_answers = Counter()
    for record in records:
        if record:
            member_count += 1
            for char in record:
                group_answers[char] += 1
        else:
            yield [a for a, c in group_answers.items() if c == member_count]
            group_answers = Counter()
            member_count = 0

    yield [a for a, c in group_answers.items() if c == member_count]


def main():
    input_path = sys.argv[1]

    print('Part One:')
    p1_total = 0
    for record in all_answers_for_group(parse_records(input_path)):
        p1_total += len(record)
    print(p1_total, '\n')

    print('Part Two:')
    p2_total = 0
    for record in matching_answers_for_group(parse_records(input_path)):
        p2_total += len(record)
    print(p2_total, '\n')


if __name__ == '__main__':
    main()
