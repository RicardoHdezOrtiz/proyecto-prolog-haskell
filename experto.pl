% ==========================================
% SISTEMA EXPERTO: Diagnóstico Básico de PC
% ==========================================

% 1. HECHOS (Base de conocimientos estática)
tiene_sintoma(pc_no_enciende).
tiene_sintoma(pantalla_negra).
tiene_sintoma(pitidos_al_arrancar).

% 2. REGLAS (Lógica de diagnóstico)
% Si se cumplen ciertos síntomas, se infiere una falla.
diagnostico(falla_fuente_poder) :- 
    tiene_sintoma(pc_no_enciende), 
    \+ tiene_sintoma(pitidos_al_arrancar).

diagnostico(falla_memoria_ram) :- 
    tiene_sintoma(pantalla_negra), 
    tiene_sintoma(pitidos_al_arrancar).

% 3. MOTOR DE INFERENCIA (Función que Python llamará)
% Busca todos los diagnósticos posibles y los imprime.
analizar_sistema :-
    findall(D, diagnostico(D), Resultados),
    ( Resultados \= [] ->
        format('Diagnosticos encontrados: ~w~n', [Resultados])
    ;
        write('No se pudo determinar el problema con los sintomas actuales.'), nl
    ).