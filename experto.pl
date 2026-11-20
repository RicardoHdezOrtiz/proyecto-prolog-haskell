% ==========================================
% SISTEMA EXPERTO: Diagnóstico Dinámico de PC
% ==========================================
:- dynamic tiene_sintoma/1.

% 1. BASE DE CONOCIMIENTOS (Reglas de Diagnóstico y Solución)
diagnostico(falla_fuente_poder, 'Revisa el cable de corriente y prueba la fuente de poder con un puente o multimetro.') :- 
    tiene_sintoma(pc_no_enciende), 
    \+ tiene_sintoma(pitidos_al_arrancar),
    \+ tiene_sintoma(luces_encendidas).

diagnostico(falla_memoria_ram, 'Retira los modulos de RAM, limpia los contactos dorados con goma blanca y vuelvelos a insertar.') :- 
    tiene_sintoma(pantalla_negra), 
    tiene_sintoma(pitidos_al_arrancar).

diagnostico(sobrecalentamiento_cpu, 'Limpia el polvo de los ventiladores y cambia la pasta termica del procesador.') :- 
    tiene_sintoma(apagado_repentino), 
    tiene_sintoma(ventiladores_al_maximo).

diagnostico(falla_tarjeta_grafica, 'Verifica que el cable HDMI/DisplayPort este conectado a la GPU y revisa su alimentacion.') :- 
    tiene_sintoma(pantalla_negra), 
    tiene_sintoma(luces_encendidas),
    \+ tiene_sintoma(pitidos_al_arrancar).

diagnostico(disco_duro_danado, 'Respalda tu informacion de inmediato y ejecuta un analisis SMART o reemplaza la unidad.') :- 
    tiene_sintoma(pantalla_azul), 
    tiene_sintoma(ruidos_mecanicos).

% 2. MOTOR DE INFERENCIA DINÁMICO
% Carga los síntomas enviados desde Python como hechos temporales
cargar_sintomas([]).
cargar_sintomas([H|T]) :-
    assertz(tiene_sintoma(H)),
    cargar_sintomas(T).

% Punto de entrada principal que llamará Python
consultar :-
    current_prolog_flag(argv, Argv),
    cargar_sintomas(Argv),
    findall([Falla, Solucion], diagnostico(Falla, Solucion), Resultados),
    ( Resultados == [] ->
        write('DIAGNOSTICO: No se encontro una falla exacta para esa combinacion de sintomas.'), nl
    ;
        imprimir_resultados(Resultados)
    ),
    halt.

% Imprime limpiamente sin disparar errores al vaciar la lista
imprimir_resultados([]).
imprimir_resultados([[Falla, Solucion]|T]) :-
    format('FALLA DETECTADA: ~w | SOLUCION: ~w~n', [Falla, Solucion]),
    imprimir_resultados(T).