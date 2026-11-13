import argparse
from collections import Counter
from itertools import combinations_with_replacement, product
import json
from pathlib import Path


def add(left, right):
    return left[0] | right[0], min(2, left[1] + right[1])


def sequence_sum(sequence):
    total = (0, 0)
    for term in sequence:
        total = add(total, term)
    return total


def multiply(left, right):
    result = Counter()
    for label_left, coefficient_left in left.items():
        for label_right, coefficient_right in right.items():
            result[add(label_left, label_right)] += coefficient_left * coefficient_right
    return {label: coefficient for label, coefficient in result.items() if coefficient}


def factor(term, coefficient):
    cyclic_idempotent = term[0], 0 if term[1] == 0 else 2
    result = Counter({term: 1})
    result[cyclic_idempotent] -= coefficient
    return {label: value for label, value in result.items() if value}


def irreducible(sequence):
    target = sequence_sum(sequence)
    for subset_mask in range((1 << len(sequence)) - 1):
        subsequence = tuple(term for index, term in enumerate(sequence)
                            if subset_mask & (1 << index))
        if sequence_sum(subsequence) == target:
            return False
    return True


def cyclic_is_group(term):
    elements = {term}
    current = add(term, term)
    while current not in elements:
        elements.add(current)
        current = add(current, term)
    return any(all(add(identity, member) == member for member in elements)
               and all(any(add(member, inverse) == identity for inverse in elements)
                       for member in elements) for identity in elements)


def verify_family(size):
    elements = tuple(product(range(1 << size), range(3)))
    for left, middle, right in product(elements, repeat=3):
        assert add(add(left, middle), right) == add(left, add(middle, right))
    ideals = {term: frozenset(add(term, other) for other in elements) for term in elements}
    for term in elements:
        assert add(term, (0, 0)) == term
        assert cyclic_is_group(term) == (term[1] != 1)
        expected = frozenset(other for other in elements
                             if term[0] | other[0] == other[0] and term[1] <= other[1])
        assert ideals[term] == expected
        for coefficient in (-3, -1, 1, 2, 5):
            if term[1] == 1:
                assert factor(term, coefficient)
        for modulus in (2, 3, 5, 7):
            for coefficient in range(1, modulus):
                if term[1] == 1:
                    assert any(value % modulus for value in factor(term, coefficient).values())
    assert len(set(ideals.values())) == len(elements)
    for left, right in product(elements, repeat=2):
        assert add(left, right) == add(right, left)
        assert not multiply(factor(left, 1), factor(right, 1))
        if left[1] == right[1] == 1:
            assert multiply(factor(left, 2), factor(right, 3)) == {add(left, right): 2}
    maxima = {term: -1 for term in elements}
    sequence_count = 0
    irreducible_count = 0
    counts_by_length = {}
    for length in range(size + 4):
        accepted = 0
        for sequence in combinations_with_replacement(elements, length):
            sequence_count += 1
            if irreducible(sequence):
                accepted += 1
                irreducible_count += 1
                target = sequence_sum(sequence)
                maxima[target] = max(maxima[target], length)
        counts_by_length[str(length)] = accepted
    for term, maximum in maxima.items():
        assert maximum == term[0].bit_count() + term[1], (term, maximum)
    assert counts_by_length[str(size + 3)] == 0
    for support, level in elements:
        witness = ((0, 1),) * level + tuple((1 << index, 0)
                                          for index in range(size) if support & (1 << index))
        assert sequence_sum(witness) == (support, level)
        assert irreducible(witness)
    result = {
        'm': size, 'elements': len(elements),
        'associativity_triples': len(elements) ** 3,
        'integer_annihilation_pairs': len(elements) ** 2,
        'sequences_exhaustively_checked': sequence_count,
        'maximum_enumerated_length': size + 3,
        'irreducible_sequences': irreducible_count,
        'irreducible_counts_by_length': counts_by_length,
        'relative_constants': [{'support_mask': support, 'level': level, 'D': maximum}
                               for (support, level), maximum in maxima.items()],
        'nongroup_relative_maximum': size + 1,
        'global_Davenport_threshold': size + 3,
        'all_checks_passed': True,
    }
    if size == 1:
        result['labels'] = [list(term) for term in elements]
        result['addition_table_label_indices'] = [[elements.index(add(left, right))
                                                  for right in elements] for left in elements]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {'schema_version': 1, 'arithmetic': 'exact integers and explicitly enumerated prime fields',
              'proof_scope': 'The universal formulas have written proofs; finite checks cover m=0,1,2.',
              'families': [verify_family(size) for size in range(3)]}
    rendered = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
