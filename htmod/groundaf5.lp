
arg_a1.
arg_a2.
att_a1_a2.
att_a2_a1.

!in_a1 -> out_a1.
!in_a2 -> out_a2.


!out_a1 -> in_a1.
!out_a2 -> in_a2.




in_a1 -> defeated_a2.
in_a2 -> defeated_a1.

out_a1&!defeated_a1 -> 0.
out_a2&!defeated_a2 -> 0.



in_a2&in_a1 -> 0.
in_a1&in_a2 -> 0.
