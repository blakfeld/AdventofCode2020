#!/usr/bin/env python

import sys
from enum import Enum

import attr
from functional import seq


class Operation(Enum):
    NOP = 'nop'
    ACC = 'acc'
    JMP = 'jmp'


@attr.s
class Instruction:
    op = attr.ib(type=Operation)
    arg = attr.ib(type=int)

    def execute(self, context):
        context.update({
            'op': str(self.op),
            'arg': self.arg,
            'ptr_jmp': 1,
        })

        if self.op == Operation.ACC:
            context['accumulator'] = context.get('accumulator', 0) + self.arg

        elif self.op == Operation.JMP:
            context['ptr_jmp'] = self.arg

        return context

    @staticmethod
    def of_str(s):
        op, _, arg = s.partition(' ')
        return Instruction(op=Operation[op.upper()], arg=int(arg))


def call_stack_from_input(input_path):
    with open(input_path, 'r') as f:
        return seq(f) \
            .map(lambda l: l.strip()) \
            .filter(lambda l: l) \
            .map(Instruction.of_str) \
            .to_list()


def execute_program(call_stack):
    ptr = 0
    context = {}
    seen = set()
    while ptr not in seen and ptr < len(call_stack):
        seen.add(ptr)
        context = call_stack[ptr].execute(context)
        ptr += context.get('ptr_jmp', 0)

    completed_execution = ptr == len(call_stack)
    return context, completed_execution


def fix_corrupted_inst(call_stack):
    for i in range(len(call_stack)):
        inst = call_stack[i]
        if inst.op != Operation.JMP:
            continue

        new_inst = Instruction(op=Operation.NOP, arg=inst.arg)
        call_stack[i] = new_inst

        context, completed = execute_program(call_stack)
        if completed:
            return call_stack, context

        call_stack[i] = inst

    raise RuntimeError('Unable to correct program!')


def main():
    input_path = sys.argv[1]
    call_stack = call_stack_from_input(input_path)

    print('Part One:')
    p1_ctx, p1_completed = execute_program(call_stack)
    print(p1_ctx['accumulator'], '\n')

    print('Part Two:')
    fixed_call_stack, p2_ctx = fix_corrupted_inst(call_stack)
    print(p2_ctx['accumulator'], '\n')


if __name__ == '__main__':
    main()
