-- ==========================================
-- CALCULADORA ANALÍTICA EN HASKELL
-- ==========================================
import System.Environment (getArgs)
import Text.Read (readMaybe)
import Text.Printf (printf)

-- === [4. RECURSIVIDAD PURA, GUARDAS Y EVALUACION PEREZOSA] ===
-- Sin ciclos for/while: recursividad (Factorial/MCD), guardas (Primos) y lista infinita (Fibonacci)
-- 1. Factorial (Recursividad)
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- 2. Fibonacci (Evaluación perezosa con lista infinita)
fibonacci :: Int -> Integer
fibonacci n = fibs !! n
  where fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- 3. Verificar número primo
esPrimo :: Integer -> Bool
esPrimo n
    | n <= 1    = False
    | otherwise = null [x | x <- [2 .. floor (sqrt (fromIntegral n))], n `mod` x == 0]

-- 4. Listar primos hasta n (Función de orden superior: filter)
primosHasta :: Integer -> [Integer]
primosHasta n = filter esPrimo [2 .. n]

-- 5. Máximo Común Divisor (Algoritmo de Euclides)
mcd :: Integer -> Integer -> Integer
mcd a 0 = abs a
mcd a b = mcd b (a `mod` b)

-- 6. Estadísticas de lista (Función de orden superior: foldl)
estadisticas :: [Double] -> String
estadisticas xs =
    let suma     = foldl (+) 0 xs
        cantidad = fromIntegral (length xs) :: Double
        promedio = suma / cantidad
        minimo   = minimum xs
        maximo   = maximum xs
    in printf "Cantidad: %d | Suma: %.2f | Promedio: %.2f | Min: %.2f | Max: %.2f"
              (length xs) suma promedio minimo maximo

-- === [5. ENTRADA POR CONSOLA (getArgs) Y MANEJO SEGURO (Maybe)] ===
-- Si el usuario mete letras en vez de numeros, readMaybe devuelve Nothing sin tronar
evaluar :: [String] -> String
evaluar ["factorial", val] =
    case readMaybe val :: Maybe Integer of
        Just n | n >= 0 -> show (factorial n)
        _               -> "Error: Ingresa un entero mayor o igual a 0."

evaluar ["fibonacci", val] =
    case readMaybe val :: Maybe Int of
        Just n | n >= 0 -> show (fibonacci n)
        _               -> "Error: Ingresa una posicion entera mayor o igual a 0."

evaluar ["primo", val] =
    case readMaybe val :: Maybe Integer of
        Just n -> if esPrimo n then "Si, es primo" else "No es primo"
        _      -> "Error: Ingresa un numero entero valido."

evaluar ["primos_hasta", val] =
    case readMaybe val :: Maybe Integer of
        Just n | n >= 2 -> show (primosHasta n)
        Just _          -> "No hay numeros primos menores que 2."
        _               -> "Error: Ingresa un numero entero valido."

evaluar ["mcd", aStr, bStr] =
    case (readMaybe aStr :: Maybe Integer, readMaybe bStr :: Maybe Integer) of
        (Just a, Just b) -> show (mcd a b)
        _                -> "Error: Ingresa dos numeros enteros validos."

evaluar ("estadisticas":vals)
    | null vals = "Error: Ingresa al menos un numero."
    | otherwise =
        case mapM readMaybe vals :: Maybe [Double] of
            Just nums -> estadisticas nums
            Nothing   -> "Error: Todos los valores deben ser numericos."

evaluar _ = "Error: Operacion o cantidad de argumentos no valida."

-- Interfaz de E/S
main :: IO ()
main = do
    args <- getArgs
    putStrLn (evaluar args)