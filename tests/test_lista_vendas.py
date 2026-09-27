import unittest

from src.estruturas import ListaVendas


class TestListaVendas(unittest.TestCase):

    def test_registar_e_totais(self):
        vendas = ListaVendas()
        vendas.registar_venda(1, "Pão de forma", 10, 80.0)
        vendas.registar_venda(3, "Pastel de nata", 5, 45.0)

        self.assertEqual(vendas.tamanho, 2)
        self.assertEqual([v.codigo_produto for v in vendas.listar_todas()], [1, 3])
        self.assertEqual(vendas.total_quantidade(), 15)
        self.assertEqual(vendas.total_vendas(), 1025.0)
        self.assertEqual(vendas.ultimo.codigo_produto, 3)
        self.assertEqual(vendas.ultimo.anterior.codigo_produto, 1)
        self.assertIsNone(vendas.primeiro.anterior)


if __name__ == "__main__":
    unittest.main()
