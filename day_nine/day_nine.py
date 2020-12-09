#!/usr/bin/env python

import sys
from collections import deque

PREAMBLE_SIZE = 25


def _parse_xmas_chunks(nums, preamble_size):
    chunk = deque()
    for num in nums:
        if len(chunk) == preamble_size:
            yield list(chunk), num
            chunk.popleft()

        chunk.append(num)


def find_inconsistent_num(nums, preamble_size=PREAMBLE_SIZE):
    for chunk, target in _parse_xmas_chunks(nums, preamble_size):
        for i, num in enumerate(chunk):
            complement = target - num
            if complement in chunk and chunk.index(complement) != i:
                break
        else:
            return target


def find_contiguous_window(nums, target):
    left = 0
    right = 1
    total = nums[left] + nums[right]
    while left < right and right < len(nums):
        if total == target:
            return nums[left:right + 1]
        elif total < target:
            right += 1
            total += nums[right]
        else:
            total -= nums[left]
            left += 1


def main():
    input_path = sys.argv[1]
    with open(input_path, 'r') as f:
        nums = [int(l) for l in f.readlines()]

    print('Part One:')
    target = find_inconsistent_num(nums)
    print(target, '\n')

    print('Part Two:')
    window = find_contiguous_window(nums, target)
    min_max_window_sum = min(window) + max(window)
    print(min_max_window_sum)


if __name__ == '__main__':
    main()
