'''App for splitting the cost on a receipt.
Pass in a CSV file where each row has the format:
    <item name>,<item cost>,<payer list>,<payee list>
where <payer list> is a space-separated list of people to split the cost of this item with,
and, optionally, <payee list> is a space-separated list of the people who paid for this item'''
from argparse import ArgumentParser
from decimal import Decimal
from pathlib import Path
import sys


def main():
    parser = ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        'file',
        help='The filename of the bill CSV file'
    )
    parser.add_argument(
        '--default-payee',
        default='DEFAULT',
        help='Payee name to use when no name is provided'
    )
    args = parser.parse_args()
    file = Path(args.file)
    if not file.is_file():
        print(args.file, 'is not a file', file=sys.stderr)
        return
    csv = file.read_text(encoding='utf-8').split('\n')
    people = {}
    for line in csv:
        item = line.split(',')
        if len(item) < 3:
            continue
        payers = item[2].split(' ')
        if not payers:
            print('No payers for item', line)
            continue
        amount = Decimal(item[1])
        payer_amount = amount / len(payers)
        for person in payers:
            people[person] = people.get(person, 0) + payer_amount
        payees = item[3].split(' ') if len(
            item) >= 4 else (args.default_payee,)
        payee_amount = amount / len(payees)
        for person in payees:
            people[person] = people.get(person, 0) - payee_amount
    print('Person,Amount')
    for person, amount in people.items():
        print(f'{person},{amount:.3f}')


if __name__ == '__main__':
    main()
