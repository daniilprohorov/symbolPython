
@ factorial 0 = 1
@ factorial n = mul n (factorial (sub n 1))


@ sub a b = add a ( neg b)

@ if 1 a b = a
@ if 0 a b = b

@ main = print ( factorial 9 )