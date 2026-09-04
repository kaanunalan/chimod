% --- Facts ---
f1.
f2.
f3.

% --- Emulated choice rules ---
a1 :- not na1.
na1 :- not a1.

a2 :- not na2.
na2 :- not a2.

a3 :- not na3.
na3 :- not a3.

% --- Independent atoms (choice-like) rewritten as implications from facts ---
a1 :- f1.
a2 :- f2.
a3 :- f3.

% --- Cycles / mutual dependencies rewritten to preserve answer sets ---
b1 :- f1, not b2.
b2 :- f2, not b1.

c1 :- b1, not c2.
c2 :- b2, not c1.

% --- Chains / dependencies ---
d1 :- c1.
d2 :- c2, a1.
d3 :- d1, d2.

% --- Mixed negation rules rewritten as implications ---
e1 :- a2, not f1.
e2 :- f2, not e1.
g1 :- e1, e2.
g2 :- g1, a3.

% --- Cyclic dependencies rewritten using only implication ---
h1 :- h2, not h3.
h2 :- h3, not h1.
h3 :- h1, not h2.
