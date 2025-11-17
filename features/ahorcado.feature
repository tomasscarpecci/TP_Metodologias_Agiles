Feature: Juego del Ahorcado - Interfaz Web

  Scenario: Iniciar sin palabra
    Given el servidor Flask está corriendo con la palabra ""
    Then cierro el navegador
  
  Scenario: Gano la partida sin errores
    Given el servidor Flask está corriendo con la palabra "sol"
    When ingreso "sol" en el campo de intento y presiono el botón
    Then el juego debe estar ganado
    And las vidas deben ser 6
    And cierro el navegador
  

  Scenario: Gano la partida sin errores
    Given el servidor Flask está corriendo con la palabra "sol"
    When ingreso "s" en el campo de intento y presiono el botón
    And ingreso "o" en el campo de intento y presiono el botón
    And ingreso "l" en el campo de intento y presiono el botón
    Then el juego debe estar ganado
    And las vidas deben ser 6
    And cierro el navegador


  Scenario: Pierdo la partida tras varios intentos fallidos
    Given el servidor Flask está corriendo con la palabra "sol" 
    When ingreso "a" en el campo de intento y presiono el botón
    And ingreso "b" en el campo de intento y presiono el botón
    And ingreso "c" en el campo de intento y presiono el botón
    And ingreso "d" en el campo de intento y presiono el botón
    And ingreso "e" en el campo de intento y presiono el botón
    And ingreso "f" en el campo de intento y presiono el botón
    Then el juego debe estar derrotado
    And las vidas deben ser 0
    And cierro el navegador


  Scenario: Gano la partida con algunos errores
    Given el servidor Flask está corriendo con la palabra "gato" 
    When ingreso "g" en el campo de intento y presiono el botón
    And ingreso "a" en el campo de intento y presiono el botón
    And ingreso "z" en el campo de intento y presiono el botón
    And ingreso "t" en el campo de intento y presiono el botón
    And ingreso "o" en el campo de intento y presiono el botón
    Then el juego debe estar ganado
    And las vidas deben ser 5
    And cierro el navegador


  Scenario: Pierdo con algunos aciertos
    Given el servidor Flask está corriendo con la palabra "perro"
    When ingreso "p" en el campo de intento y presiono el botón
    And ingreso "e" en el campo de intento y presiono el botón
    And ingreso "z" en el campo de intento y presiono el botón
    And ingreso "q" en el campo de intento y presiono el botón
    And ingreso "w" en el campo de intento y presiono el botón
    And ingreso "r" en el campo de intento y presiono el botón
    And ingreso "t" en el campo de intento y presiono el botón
    And ingreso "x" en el campo de intento y presiono el botón
    And ingreso "i" en el campo de intento y presiono el botón
    Then el juego debe estar derrotado
    And las vidas deben ser 0
    And cierro el navegador

  Scenario: Ejecución del step ingreso las letras en CSV
    Given el servidor Flask está corriendo con la palabra "sol"
    When ingreso las letras "s, o, l"
    Then el juego debe estar ganado
    And cierro el navegador