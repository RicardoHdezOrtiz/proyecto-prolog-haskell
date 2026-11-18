import System.Environment (getArgs)

-- ==========================================
-- CALCULADORA ANALÍTICA EN HASKELL
-- ==========================================

-- 1. FUNCIONES MATEMÁTICAS PURAS
-- Factorial clásico usando recursividad
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Fibonacci usando evaluación perezosa (listas infinitas)
fibonacci :: Int -> Integer
fibonacci n = fibs !! n
  where fibs = 0 : 1 : zipWith (+) fibs (tail fibs)


-- 2. MANEJO DE ENTRADA/SALIDA (Lo que conecta con Python)
main :: IO ()
main = do
    -- Leer los argumentos que Python enviará por la terminal
    args <- getArgs
    if length args < 2
        then putStrLn "Error: Faltan argumentos. Esperado: <operacion> <numero>"
        else do
            let operacion = args !! 0
                numero = read (args !! 1) :: Int
            
            -- Evaluar qué operación se pidió
            case operacion of
                "factorial" -> print (factorial (toInteger numero))
                "fibonacci" -> print (fibonacci numero)
                _           -> putStrLn "Error: Operacion no reconocida."