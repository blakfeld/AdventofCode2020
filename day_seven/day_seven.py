#!/usr/bin/env python

import re
import sys
from collections import defaultdict, deque

from functional import seq

RULE_RE = re.compile(r'^\s?(\d)\s(\w+\s\w+) bags?.?$')


def parse_rules(rules_path):
    with open(rules_path, 'r') as f:
        records = [l.rstrip('.').strip() for l in f]

    rules = {}
    for record in records:
        rule_match, _, rule_contents = record.partition(' bags contain ')

        rule_contents = seq(rule_contents.split(',')) \
            .map(lambda r: RULE_RE.match(r)) \
            .filter(lambda r: r) \
            .map(lambda r: (int(r.group(1)), r.group(2)))

        rules[rule_match] = list(rule_contents)

    return rules


def bags_can_contain_target(rules, target):
    inverse_rules = defaultdict(set)
    for bag, can_contain in rules.items():
        for bag_count, bag_type in can_contain:
            inverse_rules[bag_type].add(bag)

    bags = set()
    q = deque([target])
    while q:
        to_search = q.popleft()
        to_consider = inverse_rules[to_search]
        for tc in to_consider:
            bags.add(tc)
            q.append(tc)

    return bags


def how_many_bags(rules, bag):
    count = 0
    for bag_count, bag_type in rules.get(bag):
        count += bag_count * how_many_bags(rules, bag_type)

    return count + 1


def main():
    input_path = sys.argv[1]
    target_bag = 'shiny gold'

    print('Part One')
    rules = parse_rules(input_path)
    valid_bags = bags_can_contain_target(rules, target_bag)
    print(', '.join(valid_bags))
    print(len(valid_bags))
    print()

    print('Part Two')
    # -1 because the question asks not to include the "root" bag.
    print(how_many_bags(rules, target_bag) - 1)


if __name__ == '__main__':
    main()
