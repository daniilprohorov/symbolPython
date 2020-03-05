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

@ concat Function Function = Function
@ concat (List 0 0) lst = lst
@ concat (List x xs) lst = List x (concat xs lst)

@ operation Function = Const
@ operation (Mul a b) = 5
@ operation (Add a b) = 6

@ isZero Const = Const
@ isZero 0 = 1
@ isZero a = 0

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

@ map Symbol Function = Function
@ map f (List 0 0) = List 0 0
@ map f (List x xs) = if (f x) (List x (filter f xs)) (filter f xs)

@ mapNeg Function = Function
@ mapNeg (List 0 0) = List 0 0
@ mapNeg (List x xs) = List (neg x) (mapNeg xs)

@ len Function Const = Const
@ len (List 0 0) = 0
@ len (List x xs) = add 1 (len xs)

@ transform Function = Function
@ transform (Sub a b) = trOrReturn ( Add a (Mul b (Val (-1))))
@ transform (Add a (Val 0)) = trOrReturn a
@ transform (Add (Val 0) a) = trOrReturn a
@ transform (Mul a (Val 1)) = trOrReturn a
@ transform (Mul (Val 1) a) = trOrReturn a
@ transform (Pow (Val 1) a) = trOrReturn a
@ transform (Pow (S s) a) = Pow (S s) (trOrReturn a)
@ transform (Pow n a) = trOrReturn ( Mul a (Pow (evaluate ( Sub n (Val 1))) a))
@ transform (Mul (Add a b) (Add c d)) =
    trOrReturn (
        Add
        (trOrReturn (
            Add
            (trOrReturn ( Mul (trOrReturn a) (trOrReturn c)))
            (trOrReturn ( Mul (trOrReturn a) (trOrReturn d)))))
        (trOrReturn (
            Add
            (trOrReturn ( Mul (trOrReturn b) (trOrReturn c)))
            (trOrReturn ( Mul (trOrReturn b) (trOrReturn d))))))
@ transform (Mul a (Add b c)) = trOrReturn (
    Add
    (trOrReturn ( Mul (trOrReturn a) (trOrReturn b)))
    (trOrReturn ( Mul (trOrReturn a) (trOrReturn c))))
@ transform (Mul (Add a b) c) = trOrReturn (
    Add
    (trOrReturn ( Mul (trOrReturn a) (trOrReturn c)))
    (trOrReturn ( Mul (trOrReturn b) (trOrReturn c))))

@ transform (Add a b) = Add (trOrReturn a) (trOrReturn b)
@ transform (Sub a b) = Sub (trOrReturn a) (trOrReturn b)
@ transform (Mul a b) = Mul (trOrReturn a) (trOrReturn b)
@ transform (Val n) = Val n
@ transform x = x

@ tryTransform Const Symbol = Symbol
@ tryTransform 0 expr = expr
@ tryTransform n expr = tryTransform (sub n 1) (transform expr)

@ and Const Const = Const
@ and 0 x = 0
@ and x 0 = 0
@ and 1 1 = 1

@ equal Function Function = Const
@ equal (Add a b) (Add c d) = and (equal a c) (equal b d)
@ equal (Mul a b) (Add c d) = and (equal a c) (equal b d)
@ equal (Pow a b) (Pow c d) = and (equal a c) (equal b d)
@ equal (Val a) (Val c) = equalBuildInConst a c
@ equal (S a) (S c) = equalBuildInS a c
@ equal x y = 0

@ trOrReturn Function = Function
@ trOrReturn expr = if (equal expr (transform expr)) expr (transform expr)

@ evaluate Function = Function
@ evaluate (Add a b) = evAdd (evaluate a) (evaluate b)
@ evaluate (Sub a b) = evSub (evaluate a) (evaluate b)
@ evaluate (Mul a b) = evMul (evaluate a) (evaluate b)
@ evaluate x = x

@ evAdd Function Function = Function
@ evAdd (Val a) (Val b) = Val (add a b)
@ evAdd a b = Add a b

@ evSub Function Function = Function
@ evSub (Val a) (Val b) = Val (sub a b)
@ evSub a b = Sub a b

@ evMul Function Function = Function
@ evMul (Val a) (Val b) = Val (mul a b)
@ evMul a b = Mul a b

@ mulToList Function = Function
@ mulToList (Mul (S a) (S b)) = prepend (S a) (listCreate (S b))
@ mulToList (Mul (S a) (Val b)) = prepend (S a) (listCreate (Val b))
@ mulToList (Mul (Val a) (S b)) = prepend (Val a) (listCreate (S b))
@ mulToList (Mul (Val a) (Val b)) = listCreate (evaluate (Mul (Val a)(Val b)))
@ mulToList (Mul a b) = concat (mulToList a) (mulToList b)
@ mulToList x = listCreate x

@ toFlat Function = Function
@ toFlat (Mul a b) = listCreate (mulToList (Mul a b))
@ toFlat (Add a b) = concat (toFlat a) (toFlat b)
@ toFlat x = listCreate (listCreate x)


@ isVal Function = Const
@ isVal (Val x) = 1
@ isVal n = 0


@ getVal Function = Const
@ getVal (Val x) = x


@ isS Function = Const
@ isS (S s) = 1
@ isS n = 0

@ product Function = Const
@ product (List 0 0) = 1
@ product (List x xs) = mul x (product xs)

@ getS Function = Symbol
@ getS (S s) = s

@ toSumm Symbol = Function
@ toSumm lst = Tuple (product ( map getVal ( filter (isVal) lst))) (map getS ( filter isS lst))

@ smm Symbol = Symbol
@ smm flat = map toSumm flat

@ isPatternC Function Symbol = Const
@ isPatternC (List 0 0) pattern = 0
@ isPatternC (List (Tuple c lst) xs) pattern = if ((snd pattern) == lst) (add c (isPatternC xs pattern)) (isPatternC xs pattern)

@ patternConcat_ Function Symbol = Function
@ patternConcat_ (List 0 0) smm = List 0 0
@ patternConcat_ (List x xs) smm = List (Tuple (isPatternC smm x) (snd x)) (patternConcat_ xs smm)

@ notZero Function = Const
@ notZero (Tuple 0 x) = 0
@ notZero n = 1

@ sameConcat Symbol = Symbol
@ sameConcat sm = patternConcat_ sm sm

@ not Const = Const
@ not 1 = 0
@ not 0 = 1

@ isNotEqual Symbol Symbol = Symbol
@ isNotEqual a b =  not (equalBuildInSymbol a b)

@ deleteDuplicates_ Function Function = Symbol
@ deleteDuplicates_ (List 0 0) b = b
@ deleteDuplicates_ (List x xs) b = deleteDuplicates_ xs (List x (filter (isNotEqual x) b))

@ clear Function = Function
@ clear exprs = filter notZero exprs

@ deleteDuplicates Function = Function
@ deleteDuplicates exprs = deleteDuplicates_ (clear exprs) (clear exprs)

@ eval Function = Function
@ eval expr = deleteDuplicates (sameConcat (smm (toFlat (tryTransform 10 expr))))

@ main = Symbol
@ main = tryTransform 10 (Add 3 4)

