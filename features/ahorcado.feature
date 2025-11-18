Feature: Juego del Ahorcado - Interfaz Web
  
  Scenario: Gano la partida sin errores
    Given el servidor Flask está corriendo con la palabra "sol"
    When ingreso la palabra "sol" en el campo de intento y presiono el botón
    Then el juego debe estar ganado
    And las vidas deben ser 6
    And cierro el navegador
  

  Scenario: Gano la partida sin errores
    Given el servidor Flask está corriendo con la palabra "sol"
    When ingreso la letra "s" en el campo de intento y presiono el botón
    And ingreso la letra "o" en el campo de intento y presiono el botón
    And ingreso la letra "l" en el campo de intento y presiono el botón
    Then el juego debe estar ganado
    And las vidas deben ser 6
    And cierro el navegador


  Scenario: Pierdo la partida tras varios intentos fallidos
    Given el servidor Flask está corriendo con la palabra "sol" 
    When ingreso la letra "a" en el campo de intento y presiono el botón
    And ingreso la letra "b" en el campo de intento y presiono el botón
    And ingreso la letra "c" en el campo de intento y presiono el botón
    And ingreso la letra "d" en el campo de intento y presiono el botón
    And ingreso la letra "e" en el campo de intento y presiono el botón
    And ingreso la letra "f" en el campo de intento y presiono el botón
    Then el juego debe estar derrotado
    And las vidas deben ser 0
    And cierro el navegador


  Scenario: Gano la partida con algunos errores
    Given el servidor Flask está corriendo con la palabra "gato" 
    When ingreso la letra "g" en el campo de intento y presiono el botón
    And ingreso la letra "a" en el campo de intento y presiono el botón
    And ingreso la letra "z" en el campo de intento y presiono el botón
    And ingreso la letra "t" en el campo de intento y presiono el botón
    And ingreso la letra "o" en el campo de intento y presiono el botón
    Then el juego debe estar ganado
    And las vidas deben ser 5
    And cierro el navegador


  Scenario: Pierdo con algunos aciertos
    Given el servidor Flask está corriendo con la palabra "perro"
    When ingreso la letra "p" en el campo de intento y presiono el botón
    And ingreso la letra "e" en el campo de intento y presiono el botón
    And ingreso la letra "z" en el campo de intento y presiono el botón
    And ingreso la letra "q" en el campo de intento y presiono el botón
    And ingreso la letra "w" en el campo de intento y presiono el botón
    And ingreso la letra "r" en el campo de intento y presiono el botón
    And ingreso la letra "t" en el campo de intento y presiono el botón
    And ingreso la letra "x" en el campo de intento y presiono el botón
    And ingreso la letra "i" en el campo de intento y presiono el botón
    Then el juego debe estar derrotado
    And las vidas deben ser 0
    And cierro el navegador
