import pytest
from ahorcado import JuegoAhorcado


# --- INICIO DEL JUEGO ---
def test_inicio_juego_correctamente():
    juego = JuegoAhorcado("python")
    assert juego.palabra == "python"
    assert juego.vidas == 6
    assert juego.letras_acertadas == []
    assert juego.letras_erroneas == []
    assert juego.esta_ganado() is False
    assert juego.esta_derrotado() is False
    assert juego.esta_terminado() is False


def test_inicio_sin_palabra_toma_aleatoria(monkeypatch):
    # Simulamos random.choice para que siempre devuelva "azul"
    monkeypatch.setattr("ahorcado.random.choice", lambda lista: "azul")
    juego = JuegoAhorcado(None)
    assert juego.palabra == "azul"


def test_no_acepta_lista_vacia_de_palabras():
    with pytest.raises(
        ValueError, match="La lista de palabras no puede estar vacía."
    ):
        JuegoAhorcado.seleccionar_palabra_aleatoria([])


# --- ADIVINAR LETRAS ---
def test_adivino_letra_en_palabra():
    juego = JuegoAhorcado("python")
    resultado = juego.adivinar_letra("p")
    assert resultado is True
    assert "p" in juego.letras_acertadas


def test_adivino_letra_no_en_palabra():
    juego = JuegoAhorcado("python")
    resultado = juego.adivinar_letra("z")
    assert resultado is False
    assert "z" in juego.letras_erroneas


def test_no_se_puede_repetir_letra_correcta():
    juego = JuegoAhorcado("python")
    juego.adivinar_letra("p")
    with pytest.raises(ValueError, match="Ya intentaste esa letra."):
        juego.adivinar_letra("p")


def test_no_se_puede_repetir_letra_incorrecta():
    juego = JuegoAhorcado("python")
    juego.adivinar_letra("x")
    with pytest.raises(ValueError, match="Ya intentaste esa letra."):
        juego.adivinar_letra("x")


def test_adivinar_letra_mayuscula_funciona_igual():
    juego = JuegoAhorcado("python")
    assert juego.adivinar_letra("P") is True


def test_adivinar_letra_invalida_falla():
    """Cubre las validaciones de caracteres no alfabéticos o longitud > 1"""
    juego = JuegoAhorcado("python")
    # Caso: número
    with pytest.raises(
        ValueError, match="La letra debe ser un caracter alfabético único."
    ):
        juego.adivinar_letra("1")
    # Caso: dos letras
    with pytest.raises(
        ValueError, match="La letra debe ser un caracter alfabético único."
    ):
        juego.adivinar_letra("aa")


# --- ADIVINAR PALABRA ---
def test_adivinar_palabra_correcta():
    juego = JuegoAhorcado("python")
    assert juego.adivinar_palabra("python") is True
    assert juego.esta_ganado() is True
    assert juego.esta_terminado() is True


def test_adivinar_palabra_incorrecta():
    juego = JuegoAhorcado("python")
    assert juego.adivinar_palabra("java") is False
    assert juego.vidas == 5


def test_adivinar_palabra_vacia():
    juego = JuegoAhorcado("python")
    with pytest.raises(ValueError, match="La palabra no puede estar vacía."):
        juego.adivinar_palabra("")


def test_adivinar_palabra_con_espacios():
    juego = JuegoAhorcado("python")
    with pytest.raises(
        ValueError, match="La palabra no puede contener espacios."
    ):
        juego.adivinar_palabra("py thon")


def test_adivinar_palabra_con_caracteres_invalidos():
    juego = JuegoAhorcado("python")
    with pytest.raises(
        ValueError, match="La palabra solo puede contener letras."
    ):
        juego.adivinar_palabra("pyth0n")


# --- ESTADOS DEL JUEGO (GANAR/PERDER) ---
def test_no_se_puede_jugar_si_esta_ganado():
    juego = JuegoAhorcado("sol")
    juego.adivinar_palabra("sol")  # Ganamos
    with pytest.raises(RuntimeError, match="El juego ya terminó."):
        juego.adivinar_letra("a")
    with pytest.raises(RuntimeError, match="El juego ya terminó."):
        juego.adivinar_palabra("otra")


def test_no_se_puede_jugar_si_esta_derrotado():
    juego = JuegoAhorcado("test")
    juego.vidas = 0
    with pytest.raises(RuntimeError, match="El juego ya terminó."):
        juego.adivinar_letra("t")


def test_derrota_al_llegar_a_cero_vidas():
    juego = JuegoAhorcado("python")
    # Fallamos 6 veces
    for letra in ["a", "b", "c", "d", "e", "f"]:
        juego.adivinar_letra(letra)
    assert juego.vidas == 0
    assert juego.esta_derrotado() is True
    assert juego.esta_terminado() is True


# --- MOSTRAR LETRAS ---
def test_mostrar_letras_acertadas():
    juego = JuegoAhorcado("python")
    juego.adivinar_letra("p")
    juego.adivinar_letra("o")
    assert juego.mostrar_letras_acertadas() == ["p", "o"]


def test_mostrar_letras_erroneas():
    juego = JuegoAhorcado("python")
    juego.adivinar_letra("z")
    juego.adivinar_letra("q")
    assert juego.mostrar_letras_erroneas() == ["z", "q"]


# --- VALIDACIONES AUXILIARES ---
def test_valido_letra_alfabetica():
    juego = JuegoAhorcado("python")
    assert juego.validar_letra("a") is True
    assert juego.validar_letra("Z") is True


def test_no_valido_letra_no_alfabetica():
    juego = JuegoAhorcado("python")
    assert juego.validar_letra("1") is False
    assert juego.validar_letra("@") is False
    assert juego.validar_letra("ab") is False
    assert juego.validar_letra("") is False


# --- REINICIO DEL JUEGO ---
def test_reiniciar_con_nueva_palabra():
    juego = JuegoAhorcado("python")
    juego.adivinar_letra("y")  # Jugamos un poco
    juego.reiniciar_con_palabra("java")

    assert juego.palabra == "java"
    assert juego.vidas == 6
    assert juego.letras_acertadas == []
    assert juego.letras_erroneas == []
    assert juego.ganado is False


def test_reiniciar_con_palabra_invalida_falla():
    """
    Este test cubre los casos de validación en el reinicio.
    Como refactorizamos el código para usar validar_palabra,
    estos tests aseguran que la excepción sube correctamente.
    """
    juego = JuegoAhorcado("python")

    # Caso: Espacios (ya existía, pero reforzado)
    with pytest.raises(
        ValueError, match="La palabra no puede contener espacios."
    ):
        juego.reiniciar_con_palabra("ja va")

    # Caso: Vacía (NUEVO)
    with pytest.raises(ValueError, match="La palabra no puede estar vacía."):
        juego.reiniciar_con_palabra("")

    # Caso: Caracteres no alfabéticos (NUEVO)
    with pytest.raises(
        ValueError, match="La palabra solo puede contener letras."
    ):
        juego.reiniciar_con_palabra("jav4")
