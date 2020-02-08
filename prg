
@ factorial 0 = 1
@ factorial n = mul n (factorial (sub n 1))

@ true = 1
@ false = 0

@ sub a b = add a ( neg b )

@ if 1 a b = a
@ if 0 a b = b

@ id a = a

@ lul x = List x 0

@ head (List x xs) = x

@ tail (List x xs) = xs

@ main = head (lul 1)
