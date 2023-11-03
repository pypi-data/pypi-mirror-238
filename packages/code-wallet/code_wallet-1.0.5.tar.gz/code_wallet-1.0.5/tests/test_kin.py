import unittest
from code_wallet.library.kin import Kin

class TestKinAndQuarksConversion(unittest.TestCase):

    def test_from_quarks(self):
        self.assertEqual(Kin.from_quarks(100000).whole, 1)
        self.assertEqual(Kin.from_quarks(500000).whole, 5)
        self.assertEqual(Kin.from_quarks(10000).whole, 0)
        self.assertEqual(Kin.from_quarks(0).whole, 0)

        self.assertEqual(Kin.from_quarks(99999).whole, 0)
        self.assertEqual(Kin.from_quarks(100001).whole, 1)

    def test_to_quarks(self):
        self.assertEqual(Kin(1).to_quarks(), 100000)
        self.assertEqual(Kin(5).to_quarks(), 500000)
        self.assertEqual(Kin(0).to_quarks(), 0)

        self.assertEqual(Kin(-1).to_quarks(), -100000)

    def test_from_decimal(self):
        kin = Kin.from_decimal(1.23456)
        self.assertEqual(kin.to_quarks(), 123456)

    def test_to_decimal(self):
        kin = Kin(1, 23456)
        self.assertAlmostEqual(kin.to_decimal(), 1.23456, places=5)

    def test_arithmetic_operations(self):
        kin1 = Kin.from_decimal(1.23456)
        kin2 = Kin.from_decimal(2.34567)

        sum_kin = kin1.add(kin2)
        self.assertEqual(sum_kin.to_quarks(), 358023)

        difference = kin1.subtract(kin2)
        self.assertEqual(difference.to_quarks(), -111111)

        product = kin1.multiply(2)
        self.assertEqual(product.to_quarks(), 246912)

        quotient = kin1.divide(2)
        self.assertEqual(quotient.to_quarks(), 61728)

if __name__ == "__main__":
    unittest.main()