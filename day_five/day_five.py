#!/usr/bin/env python

import sys

import attr

UPPER_HALF = set(['B', 'R'])
LOWER_HALF = set(['F', 'L'])


@attr.s
class BoardingPass:
    row = attr.ib(type=int)
    column = attr.ib(type=int)
    seat_id = attr.ib(type=int)

    @staticmethod
    def of_record(record):
        row_bits = record[:7]
        available_rows = list(range(0, 128))
        for row_bit in row_bits:
            available_rows = take_specified_half(available_rows, row_bit)
        row = available_rows[0]

        col_bits = record[-3:]
        available_cols = list(range(0, 8))
        for col_bit in col_bits:
            available_cols = take_specified_half(available_cols, col_bit)
        col = available_cols[0]

        seat_id = (row * 8) + col

        return BoardingPass(row=row, column=col, seat_id=seat_id)


def take_specified_half(lst, take_half):
    mid = len(lst) // 2
    if take_half in UPPER_HALF:
        return lst[mid:]
    elif take_half in LOWER_HALF:
        return lst[:mid]
    else:
        return lst


def find_missing_seat(boarding_passes):
    prev = None
    for bp in sorted(boarding_passes, key=lambda bp: bp.seat_id):
        if prev and bp.seat_id - prev.seat_id != 1:
            return prev.seat_id + 1
        prev = bp


def main():
    input_path = sys.argv[1]

    boarding_passes = []
    with open(input_path, 'r') as f:
        records = map(lambda l: l.strip(), f.readlines())

    boarding_passes = [BoardingPass.of_record(r) for r in records]
    print('Largest Seat ID: ', max(bp.seat_id for bp in boarding_passes))
    print('Missing Seat ID: ', find_missing_seat(boarding_passes))


if __name__ == '__main__':
    main()
