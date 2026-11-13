# Counterexamples to Wang's Conjectures 3.26 and 5.3

## Contents and build

`note.tex` is the only main document. Its bibliography is inline; no external
figures, bibliography database, network-fetched TeX inputs or data files are
required once the TeX distribution's standard packages are available.

Build with **Tectonic 0.17.0**:

```sh
tectonic --untrusted --keep-logs note.tex
```

Alternatively, with a standard LaTeX distribution containing `amsmath`, `amsthm`,
`amssymb`, `geometry`, `lmodern`, `microtype` and `hyperref`:

```sh
pdflatex -interaction=nonstopmode -halt-on-error note.tex
pdflatex -interaction=nonstopmode -halt-on-error note.tex
```

BibTeX is unnecessary because references are embedded in `note.tex`.
The source archive contains `note.tex`, `verify.py`, `metadata.json` and this
README.

## Mathematical scope

The note proves, for every set U and every nonzero commutative unitary ring R,
that S_U = P_fin(U) × {0,1,2}, with union and addition capped at two, satisfies
d(S_U,R)=1, Green H=equality, and D_(A,k)(S_U)=|A|+k. All Schützenberger groups
are trivial. U=N refutes Wang's Conjecture 3.26; finite U of size m>=1 gives
d=1 while the expression in Conjecture 5.3 is m+1. A six-element member suffices.
No global minimality claim is made for that member.

The interpretation of Remark 3.27 is handled explicitly: its literal printed
word is “group”; only its intended semigroup interpretation is contradicted.

## Exact finite reproduction

Only Python's standard library is needed:

```sh
python3 verify.py --output verification.json
sha256sum verification.json
```

Expected SHA256:
`ba0dcb687b6923e0eb21805ef290e04ddf23f068348d883fe7d616f5299f5935`.

The verifier uses exact integer convolution with every basis label retained.
For m=0,1,2 it checks all associativity triples, principal ideals, cyclic group
classification, all coefficient-one factor pairs, prime-field singleton
nonvanishing, and every sequence multiset through length m+3. It checks every
proper subsequence, including the empty one. The respective numbers of sequence
multisets are 20, 210 and 6,188. The absence of an irreducible sequence of length
m+3, together with reducibility being preserved when adjoining terms, also
excludes longer irreducibles in these finite models. The universal formulas
are proved in the note, not inferred from finite tests. Regenerable output is
not duplicated in the source ZIP.

## Sources and proof coverage

The posing source is Guoqing Wang, arXiv:2509.18724v1, Definition 2.1 p.8,
Definition D p.9, Conjecture 3.26 and Remark 3.27 p.23, and Conjecture 5.3 p.27:
https://arxiv.org/abs/2509.18724v1 .

The existing formal source for the infinite refutation is:
https://github.com/the-omega-institute/trureturing/blob/d1876cfbbef8c13023311126691b180eefa69569/D5/S0/Certificates/Algebra/WangConjecture326Refutation.lean .

That pinned source's theorem `D5.S0.Certificates.Algebra.WangConjecture326Refutation.result`
negates the universal implication of Conjecture 3.26 using Q, with an algebraic
upper bound of one and an unbounded nongroup relative supremum.
The exact equality for arbitrary nonzero R, the all-level relative formulas,
and the finite Conjecture 5.3 consequence have written proofs. The finite
checker covers m=0,1,2, with the ranges and arithmetic described above.

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

The note and accompanying original verification materials are licensed under
Creative Commons Attribution 4.0 International (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/ .
Original sources retain their respective rights and attribution.
