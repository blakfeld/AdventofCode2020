#!/usr/bin/env python

import sys

TARGET = 2020


def read_lines(input_path, func=None):
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            yield func(line) if func else line


def find_two_sum(nums, target):
    complements = {}
    for num in nums:
        complement = target - num
        if complement in complements:
            return complement * num

        complements[num] = complement

    raise RuntimeError('{} not found!'.format(target))


def find_three_sum(nums, target):
    nums = sorted(nums)
    for i in range(len(nums)):
        cur_target = target - nums[i]
        complements = set()
        for j in range(i + 1):
            complement = cur_target - nums[j]
            if complement in complements:
                return nums[i] * nums[j] * complement

            complements.add(nums[j])

    raise RuntimeError('{} not found!'.format(target))


def main():
    input_path = sys.argv[1]

    print 'Two Sum:'
    result = find_two_sum(
        read_lines(input_path, func=int),
        2020
    )
    print result
    print

    print 'Three Sum:'
    result = find_three_sum(
        read_lines(input_path, func=int),
        2020
    )
    print result
    print


if __name__ == '__main__':
    main()
