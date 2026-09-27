import unittest

from src.estruturas import ListaLigada


class TestListaLigada(unittest.TestCase):

    def setUp(self):
        self.lista = ListaLigada()
        self.lista.cadastrar(1, "Pão de forma", "Pão", 80.0, 50, "15/09/2026")
        self.lista.cadastrar(2, "Bolo de chocolate", "Bolo", 350.0, 10, "12/09/2026")
        self.lista.cadastrar(3, "Pão careca", "Pão", 15.0, 100, "14/09/2026")

    def codigos(self, produtos):
        return [p.codigo for p in produtos]

    def test_cadastrar_adiciona_no_fim(self):
        self.assertEqual(self.lista.tamanho, 3)
        self.assertEqual(self.codigos(self.lista.listar_todos()), [1, 2, 3])

    def test_cadastrar_codigo_repetido_falha(self):
        with self.assertRaises(ValueError):
            self.lista.cadastrar(1, "Outro", "Pão", 1.0, 1, "")

    def test_buscar_por_codigo(self):
        self.assertEqual(self.lista.buscar_por_codigo(2).nome, "Bolo de chocolate")
        self.assertIsNone(self.lista.buscar_por_codigo(99))

    def test_buscar_por_um_atributo_ignora_maiusculas(self):
        self.assertEqual(self.codigos(self.lista.buscar_por_um_atributo("categoria", "pão")), [1, 3])

    def test_buscar_por_dois_atributos(self):
        resultado = self.lista.buscar_por_dois_atributos("categoria", "Pão", "preco", "15.0")
        self.assertEqual(self.codigos(resultado), [3])

    def test_alterar_ignora_campos_vazios(self):
        self.lista.alterar_por_codigo(1, {"nome": "", "preco": 90.0})
        produto = self.lista.buscar_por_codigo(1)
        self.assertEqual(produto.nome, "Pão de forma")
        self.assertEqual(produto.preco, 90.0)

    def test_eliminar_por_posicao(self):
        self.assertEqual(self.lista.eliminar_por_posicao(2).codigo, 2)
        self.assertEqual(self.codigos(self.lista.listar_todos()), [1, 3])
        self.assertEqual(self.lista.eliminar_por_posicao(1).codigo, 1)
        self.assertEqual(self.lista.tamanho, 1)

    def test_eliminar_por_posicao_invalida(self):
        with self.assertRaises(IndexError):
            self.lista.eliminar_por_posicao(4)

    def test_eliminar_por_codigo(self):
        self.lista.eliminar_por_codigo(3)
        self.assertEqual(self.codigos(self.lista.listar_todos()), [1, 2])
        with self.assertRaises(ValueError):
            self.lista.eliminar_por_codigo(3)

    def test_listar_ordenado(self):
        self.assertEqual(self.codigos(self.lista.listar_ordenado("preco")), [3, 1, 2])
        self.assertEqual(self.codigos(self.lista.listar_ordenado("preco", decrescente=True)), [2, 1, 3])


if __name__ == "__main__":
    unittest.main()
