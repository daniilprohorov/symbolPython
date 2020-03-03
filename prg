@ factorial Const = Const
@ factorial 0 = 1
@ factorial n = mul n (factorial (sub n 1))

@ sub Const Const = Const
@ sub a b = add a ( neg b )

@ if Const Symbol Symbol = Symbol
@ if 1 a b = a
@ if 0 a b = b

@ Mul Symbol Symbol = Symbol
@ Mul a b = a

@ Add Symbol Symbol = Symbol
@ Add a b = a

@ head Function = Const
@ head (List a b) = a

@ tail Function = Symbol
@ tail (List a b) = b

@ lol Symbol Symbol = Function
@ lol a l = List a l

@ listCreate Symbol = Function
@ listCreate a = List a (List 0 0)


@ prepend Symbol Symbol = Function
@ prepend x xs = List x xs

@ headSnd Function = Symbol
@ headSnd (List a (List b c)) = b


@ operation Function = Const
@ operation (Mul a b) = 5
@ operation (Add a b) = 6

@ isZero Const = Const
@ isZero 0 = 1
@ isZero a = 0

@ equal Const Const = Const
@ equal a b = isZero (sub a b)

@ id Function = Function
@ id a = a

@ Tuple Symbol Symbol = Symbol
@ Tuple a b = a

@ tCreate Symbol Symbol = Function
@ tCreate a b = Tuple a b

@ headThird Function = Symbol
@ headThird (List a (List b (List c d))) = c

@ fst Function = Symbol
@ fst (Tuple a b) = a

@ snd Function = Symbol
@ snd (Tuple a b) = b

@ map Symbol Function = Function
@ map f (List 0 0) = List 0 0
@ map f (List x xs) = List (f x) (map f xs)

@ mapNeg Function = Function
@ mapNeg (List 0 0) = List 0 0
@ mapNeg (List x xs) = List (neg x) (mapNeg xs)

@ len Function Const = Const
@ len (List 0 0) = 0
@ len (List x xs) = add 1 (len xs)

@ transform Function = Function
@ transform (Mul (Add a b) (Add c d)) = transform (Add (Add (Mul a c) (Mul a d)) (Add (Mul b c) (Mul b d)))
@ transform (Mul 0 x) = 0
@ transform (Mul x 0) = 0
@ transform (Mul 1 x) = transform x
@ transform (Mul x 1) = transform x
@ transform (Add 0 x) = transform x
@ transform (Add x 0) = transform x
@ transform (Mul a (Add b c)) = transform (Add (Mul a b) (Mul a c))
@ transform (Mul (Add b c) a) = transform (Add (Mul a b) (Mul a c))
@ transform (Mul a b) = Mul (transform a) (transform b)
@ transform (Add a b) = Add (transform a) (transform b)
@ transform x = x


@ main = Symbol
@ main = A 1
