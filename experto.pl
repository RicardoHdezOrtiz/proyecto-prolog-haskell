:- dynamic tiene_sintoma/1.


diagnostico(falla_fuente_poder, 'CRITICA', 'Revisa el cable de corriente y prueba la fuente de poder con un puente o multimetro.') :-
    tiene_sintoma(pc_no_enciende),
    \+ tiene_sintoma(pitidos_al_arrancar),
    \+ tiene_sintoma(luces_encendidas).

diagnostico(falla_placa_madre, 'CRITICA', 'Desconecta perifericos innecesarios, revisa capacitores inflados y prueba un reinicio de BIOS.') :-
    tiene_sintoma(pc_no_enciende),
    tiene_sintoma(luces_encendidas),
    \+ tiene_sintoma(pitidos_al_arrancar).

diagnostico(disco_duro_danado, 'CRITICA', 'Respalda tu informacion de inmediato, ejecuta un analisis SMART y reemplaza la unidad.') :-
    tiene_sintoma(pantalla_azul),
    tiene_sintoma(ruidos_mecanicos).

diagnostico(falla_memoria_ram, 'ALTA', 'Retira los modulos de RAM, limpia los contactos dorados con goma blanca y vuelvelos a insertar.') :-
    tiene_sintoma(pantalla_negra),
    tiene_sintoma(pitidos_al_arrancar).

diagnostico(sobrecalentamiento_cpu, 'ALTA', 'Limpia el polvo de los ventiladores y cambia la pasta termica del procesador.') :-
    tiene_sintoma(apagado_repentino),
    tiene_sintoma(ventiladores_al_maximo).

diagnostico(falla_tarjeta_grafica, 'ALTA', 'Verifica que el cable HDMI/DisplayPort este conectado a la GPU y revisa su alimentacion.') :-
    tiene_sintoma(pantalla_negra),
    tiene_sintoma(luces_encendidas),
    \+ tiene_sintoma(pitidos_al_arrancar).

diagnostico(gpu_danada_o_driver, 'MEDIA', 'Reinstala los drivers de video desde cero con DDU y monitorea temperaturas de la GPU.') :-
    tiene_sintoma(artefactos_en_pantalla).

diagnostico(cuello_botella_almacenamiento, 'MEDIA', 'Desactiva programas de inicio, libera espacio en disco o considera migrar el sistema a un SSD.') :-
    tiene_sintoma(lentitud_extrema),
    tiene_sintoma(alto_uso_disco).

diagnostico(falla_tarjeta_red, 'BAJA', 'Reinicia el adaptador de red, actualiza el driver Wi-Fi/Ethernet o prueba con otro cable.') :-
    tiene_sintoma(sin_internet),
    tiene_sintoma(icono_red_rojo).

diagnostico(bateria_cmos_agotada, 'BAJA', 'Reemplaza la pila de boton CR2032 de la placa madre y vuelve a ajustar fecha y hora en BIOS.') :-
    tiene_sintoma(hora_desconfigurada).

% 2. MOTOR DE INFERENCIA DINÁMICO
cargar_sintomas([]).
cargar_sintomas([H|T]) :-
    assertz(tiene_sintoma(H)),
    cargar_sintomas(T).

consultar :-
    current_prolog_flag(argv, Argv),
    cargar_sintomas(Argv),
    findall([Falla, Urgencia, Solucion], diagnostico(Falla, Urgencia, Solucion), Resultados),
    ( Resultados == [] ->
        write('SIN_COINCIDENCIA'), nl
    ;
        imprimir_resultados(Resultados)
    ),
    halt.

imprimir_resultados([]).
imprimir_resultados([[Falla, Urgencia, Solucion]|T]) :-
    format('~w|~w|~w~n', [Falla, Urgencia, Solucion]),
    imprimir_resultados(T).