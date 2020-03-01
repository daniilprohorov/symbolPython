@ factorial Const = Const
@ factorial 0 = 1
@ factorial n = mul n (factorial (sub n 1))

@ sub Const Const = Const
@ sub a b = add a ( neg b )

@ if Const Symbol Symbol = Symbol
@ if 1 a b = a
@ if 0 a b = b

@ List Symbol Symbol = Symbol
@ List a b = a

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

@ filter Symbol Function = Function
@ filter f (List 0 0) = List 0 0
@ filter f (List x xs) = if (f x) (List x (filter f xs)) (List 8 (filter f xs))


@ main = Symbol
@ main = filter isZero (prepend 0 (prepend 1 (listCreate 0)))
