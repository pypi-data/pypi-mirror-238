"""Unittest für darlehen.py"""
import unittest
from src.darlehenpy import darlehen


class TestDarlehen(unittest.TestCase):
    """
    Tests für darlehen.py
    """

    def test_berechne_mit_monatsrate(self):
        """
        Test für berechne_mit_monatsrate
        """
        test_cases = [
            # format (Darlehenssumme, Zinssatz, Monatsrate, Laufzeit, Sondertilung,
            # (Restschuld, Gesamtaufwand, Tilgungsrate, Jahr_Fertig, Monat_Fertig))
            (400000, 4.2, 1500, 10, 10000, (0.3, 263476.89, 543476.89, None, None)),
            (200000, 5, 1500, 20, 5000, (4.0, 0, 264743.1, 12, 8)),
            (10000, 1, 50, 5, 0, (5.0, 7437.54, 10437.54, None, None)),
            (
                1000000,
                8,
                5000,
                15,
                10000,
                (-2.0, 1298786.37, 2348786.37, None, None),
            ),
            (1000000, 8, 10000, 15, 10000, (4, 0, 1565158.97, 13, 1)),
            (1000000, 8, 10000, 15, 10000, (4, 0, 1565158.97, 13, 1)),
            (100000.50, 4, 1000, 20, 10000, (8, 0, 111564.81, 6, 2)),
            (100000.50, 4, 1000, 20, 10000, (8, 0, 111564.81, 6, 2)),
            (100000.50, 4, 1000, 20, 10000.50, (8, 0, 111564.58, 6, 2)),
        ]

        # pylint: disable-next=invalid-name
        for P, r, M, n, S, expected in test_cases:
            with self.subTest(P=P, r=r, M=M, n=n, S=S, expected=expected):
                result = darlehen.berechne_mit_monatsrate(P, r, M, n, S)
                self.assertEqual(result, expected)

    def test_berechne_mit_tilgungsrate(self):
        """
        Test für berechne_mit_tilgungsrate
        """
        test_cases = [
            # format (Darlehenssume, Zinssatz, Tilgungsrate, Laufzeit, Sondertilung,
            # (Monatsrate, Restschuld, Gesamtaufwand, Jahr_Fertig, Monat_Fertig))
            (400000, 4.2, 1, 10, 10000, (1733.33, 228753.83, 536753.83, None, None)),
            (400000, 4.2, 2, 10, 10000, (2066.67, 179149.46, 527149.46, None, None)),
            (400000, 4, 1, 10, 10000, (1666.67, 230441.99, 530441.99, None, None)),
            (400000, 4, 2, 10, 10000, (2000.0, 181358.72, 521358.72, None, None)),
            (40000, 4, 0.5, 30, 0, (150, 28432.51, 82432.51, None, None)),
            (40000, 1, 4, 10, 0, (166.67, 23180.02, 43180.02, None, None)),
            (40000, 1, 10, 10, 0, (366.67, 0, 41953.99, 10, 7)),
            (40000.50, 1, 10, 10, 0, (366.67, 0, 41954.51, 10, 7)),
        ]

        # pylint: disable-next=invalid-name
        for P, r, t0, n, S, expected in test_cases:
            with self.subTest(P=P, r=r, t0=t0, n=n, S=S, expected=expected):
                result = darlehen.berechne_mit_tilgungsrate(P, r, t0, n, S)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()


# vim: foldmethod=indent
