#!/usr/bin/env python

import logging
import re
import sys

import attr

logging.basicConfig()
LOGGER = logging.getLogger()

VALID_HAIR_COLOR_RE = re.compile(r'^\#[0-9a-f]{6}')
VALID_EYE_COLOR_RE = re.compile(r'(?:amb|blu|brn|gry|grn|hzl|oth)')


@attr.s
class Passport:
    byr = attr.ib(type=str)
    iyr = attr.ib(type=str)
    eyr = attr.ib(type=str)
    hgt = attr.ib(type=str)
    hcl = attr.ib(type=str)
    ecl = attr.ib(type=str)
    pid = attr.ib(type=str)
    cid = attr.ib(type=str, default=None)

    @byr.validator
    def validate_birth_year(self, attribute, value):
        if not is_valid_year(value, 1920, 2002):
            raise ValueError('Invalid Birth Year')

    @iyr.validator
    def validate_issue_year(self, attribute, value):
        if not is_valid_year(value, 2010, 2020):
            raise ValueError('Invalid Issue Year')

    @eyr.validator
    def validate_expire_year(self, attribute, value):
        if not is_valid_year(value, 2020, 2030):
            raise ValueError('Invalid Expire Year')

    @hgt.validator
    def validate_height(self, attribute, value):
        height = int(value[:-2])
        unit = value[-2:]
        if unit == 'in':
            is_valid = 59 <= height <= 76
        elif unit == 'cm':
            is_valid = 150 <= height <= 193
        else:
            is_valid = False

        if not is_valid:
            raise ValueError('Invalid Height')

    @hcl.validator
    def validate_hair_color(self, attribute, value):
        if not VALID_HAIR_COLOR_RE.match(value):
            raise ValueError('Invalid Hair Color')

    @ecl.validator
    def validate_eye_color(self, attribute, value):
        if not VALID_EYE_COLOR_RE.match(value):
            raise ValueError('Invalid Eye Color')

    @pid.validator
    def validate_pid(self, attribute, value):
        if len(value) != 9 or not value.isdigit():
            raise ValueError('Invalid PID')


def is_valid_year(year, min_year, max_year):
    return all([
        len(year) == 4,
        int(min_year) <= int(year) <= int(max_year)
    ])


def read_input(input_path):
    with open(input_path, 'r') as f:
        row = ''
        lines = map(lambda l: l.strip(), f)
        for line in lines:
            if line:
                row += ' ' + line.strip()
            else:
                passport_vals = {}
                for key_pair in row.split():
                    key, _, val = key_pair.partition(':')
                    passport_vals[key] = val

                yield passport_vals
                row = ''

        if row:
            passport_vals = {}
            for key_pair in row.split():
                key, _, val = key_pair.partition(':')
                passport_vals[key] = val

            yield passport_vals


def main():
    input_path = sys.argv[1]
    passports = []
    for input_line in read_input(input_path):
        try:
            passports.append(Passport(**input_line))
        except (TypeError, ValueError) as e:
            LOGGER.warn(e)
            LOGGER.debug(input_line)
    print(len(passports))


if __name__ == '__main__':
    main()
