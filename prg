
@ factorial 0 = 1
@ factorial n =
    mul n (
        factorial (sub n 1)
        )






@ sub a b = add a ( neg b)