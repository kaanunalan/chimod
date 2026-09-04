f1.
f2.
f3.

!na1 -> a1.
!a1 -> na1.

!na2 -> a2.
!a2 -> na2.

!na3 -> a3.
!a3 -> na3.

!b2&f1 -> b1.
!b1&f2 -> b2.
!c2&b1 -> c1.
!c1&b2 -> c2.

c1 -> d1.
c2&a1 -> d2.
d1&d2 -> d3.

e1 :- not f1, a2 -> e1.
e2 :- not e1, f2 -> e2.
e1&e2 -> g1.
g1&a3 -> g2.

h2&!h3 -> h1.
h3&!h1 -> h2.
h1&!h2 -> h3.


