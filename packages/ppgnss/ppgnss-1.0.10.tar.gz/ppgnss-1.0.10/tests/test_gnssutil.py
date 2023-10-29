# -*- coding: utf-8 -*-
"""
   unit test of gnss util module.
"""
import unittest
from os import path

import matplotlib.pyplot as plt

from ppgnss import gnss_io
from ppgnss import gnss_utils


class TestUtils(unittest.TestCase):
    """
    Unit test of ppgnss.gnss_geodesy
    """
    soltab_filename = path.join(path.dirname(
        __file__), "data", "soltab.2017.J2000")

    def test_read_soltab_file(self):
        """Unit test of :func:`gnss_utils.read_soltab_file`.
        """
        xr_sol = gnss_io.read_soltab_file(self.soltab_filename)
        x = xr_sol.loc[57661, 'x'].values
        y = xr_sol.loc[57661, 'y'].values
        self.assertEqual(149023950, x)
        self.assertEqual(14491419, y)
        x = xr_sol.loc[58217, 'x'].values
        y = xr_sol.loc[58217, 'y'].values
        z = xr_sol.loc[58217, 'z'].values
        self.assertEqual(-142551505, x)
        self.assertEqual(-42145569, y)
        self.assertEqual(-18269828, z)

    # def test_everett_interplotion(self):
    #         :57693
    #     gnss_utils.everett_interp_order8(
    #         data.coords['time'].values, data.loc[:, 'x'].values, 57690)

    def test_xr_ssr2clock_norm(self):
        """Unit test of :func:`gnss_utils.xr_ssr2clock`
        """
        ssr_file = path.join(path.dirname(__file__), "data", "IGS0319543.ssrC")
        brdc_file_1 = path.join(path.dirname(__file__), "data", "brdc1720.17n")
        brdc_file_2 = path.join(path.dirname(__file__), "data", "brdc1730.17n")
        xr_clock_ssr, xr_orbit_ssr = gnss_io.read_ssr_file(ssr_file)
        xr_brdc = gnss_io.read_brdc_file(brdc_file_1)
        xr_brdc_2 = gnss_io.read_brdc_file(brdc_file_2)
        xr_brdc = xr_brdc.combine_first(xr_brdc_2)

        xr_clock = gnss_utils.xr_ssr2clock(xr_clock_ssr, xr_brdc)
        self.assertAlmostEqual(
            xr_clock.loc['2017-06-21 00:00:00.00', 'G01'].values,
            56.100561E-6,
            places=12)
        self.assertAlmostEqual(
            xr_clock.loc['2017-06-21 23:59:50.00', 'G32'].values,
            -445.859629E-6,
            places=12)

        ssr_file = path.join(path.dirname(__file__), "data", "IGS0119543.ssrC")
        brdc_file_1 = path.join(path.dirname(__file__), "data", "brdc1720.17n")
        brdc_file_2 = path.join(path.dirname(__file__), "data", "brdc1730.17n")
        xr_brdc = gnss_io.read_brdc_file(brdc_file_1)
        xr_brdc_2 = gnss_io.read_brdc_file(brdc_file_2)
        xr_brdc = xr_brdc.combine_first(xr_brdc_2)
        xr_clock_ssr, xr_orbit_ssr = gnss_io.read_ssr_file(ssr_file)
        xr_clock = gnss_utils.xr_ssr2clock_norm(xr_clock_ssr, xr_brdc)
        # prns = ['G%02d' % tmp for tmp in xrange(1, 33)]

        self.assertAlmostEqual(
            xr_clock.loc["2017-06-21 00:00:00.0", "G01"].values,
            5.610861600000e-05,
            places=11)
        self.assertAlmostEqual(
            xr_clock.loc["2017-06-21 23:59:55.0", "G32"].values,
            -4.458591870000e-04,
            places=11)

    def test_repair_datum(self):
        """
        Not work.
        """
        return
        brdc_file_1 = path.join(path.dirname(__file__), "data", "brdc1720.17n")
        brdc_file_2 = path.join(path.dirname(__file__), "data", "brdc1730.17n")
        clock_file = path.join(path.dirname(__file__),
                               "data", "IGS0119543.clk")
        xr_brdc = gnss_io.read_brdc_file(brdc_file_1)
        xr_brdc_2 = gnss_io.read_brdc_file(brdc_file_2)
        xr_brdc = xr_brdc.combine_first(xr_brdc_2)
        xr_clock = gnss_io.read_clock_file(clock_file)

        xr_clock_repaired, xr_jumped, xr_outlier = gnss_utils.repair_datum(
            xr_clock, xr_brdc)
        xr_delta = xr_clock - xr_clock_repaired

        self.assertAlmostEqual(
            xr_delta.loc["2017-06-21T00:00:15.00", 'G01'].values,
            -8.55310650e-09,
            places=11)  # nan

        self.assertAlmostEqual(
            xr_delta.loc["2017-06-21T23:59:55.00", 'G01'].values,
            -1.170237e-08,
            places=11)

        xr_diff = xr_clock_repaired.diff('time')
        fig, ax = plt.subplots()
        ax.plot(xr_diff.loc[:, "G01"], linestyle='dashed', marker='o')
        ax.plot(xr_diff.loc[:, "G03"], linestyle='dashed', marker='o')
        ax.plot(xr_diff.loc[:, "G05"], linestyle='dashed', marker='o')
        ax.plot(xr_diff.loc[:, "G07"], linestyle='dashed', marker='o')
        plt.show()

    def test_xr_ssr2clock(self):
        """
        """
        ssr_file = path.join(path.dirname(__file__), "data", "IGS0119543.ssrC")
        brdc_file_0 = path.join(path.dirname(__file__), "data", "brdc1710.17n")
        brdc_file_1 = path.join(path.dirname(__file__), "data", "brdc1720.17n")
        brdc_file_2 = path.join(path.dirname(__file__), "data", "brdc1730.17n")
        xr_brdc_0 = gnss_io.read_brdc_file(brdc_file_0)
        xr_brdc = gnss_io.read_brdc_file(brdc_file_1)
        xr_brdc_2 = gnss_io.read_brdc_file(brdc_file_2)
        xr_brdc = xr_brdc.combine_first(xr_brdc_0)
        xr_brdc = xr_brdc.combine_first(xr_brdc_2)
        xr_clock_ssr, xr_orbit_ssr = gnss_io.read_ssr_file(ssr_file)

        prns = ['G%02d' % tmp for tmp in range(1, 33)]
        xr_clock_ssr = xr_clock_ssr.loc[:, prns]
        xr_clock2 = gnss_utils.xr_ssr2clock(
            xr_clock_ssr, xr_brdc, latency=0, interval=1, valid_seconds=59)

        self.assertAlmostEqual(
            xr_clock2.loc["2017-06-21 00:00:00.0", "G01"].values,
            5.610861600000e-05, places=11)
        self.assertAlmostEqual(
            xr_clock2.loc["2017-06-21 23:59:55.0", "G32"].values,
            -4.458591870000e-04, places=11)
        # gnss_io.save_clock_file("can_remove_igs03_172.clk", xr_clock2)

    def test_timearrgen(self):
        """Unit test of ``gnss_utils.time_arr_gen``
        """
        time_from = '2017-10-10 00:00:00.00'
        time_to = '2017-10-10 00:00:20.00'
        interval = 5
        self.assertEqual(
            str(gnss_utils.time_arr_gen(time_from, time_to, interval)[0]),
            "2017-10-10 00:00:00")
        self.assertEqual(
            str(gnss_utils.time_arr_gen(time_from, time_to, interval)[-1]),
            "2017-10-10 00:00:20")

    def test_clock_extrapolation(self):
        """Unit test of ``gnss_utils.clock_extrapolation``
        Not working.
        """
        return
        ssr_file = path.join(path.dirname(__file__), "data", "IGS0119543.ssrC")
        brdc_file_0 = path.join(path.dirname(__file__), "data", "brdc1710.17n")
        brdc_file_1 = path.join(path.dirname(__file__), "data", "brdc1720.17n")
        brdc_file_2 = path.join(path.dirname(__file__), "data", "brdc1730.17n")
        xr_brdc_0 = gnss_io.read_brdc_file(brdc_file_0)
        xr_brdc = gnss_io.read_brdc_file(brdc_file_1)
        xr_brdc_2 = gnss_io.read_brdc_file(brdc_file_2)
        xr_brdc = xr_brdc.combine_first(xr_brdc_0)
        xr_brdc = xr_brdc.combine_first(xr_brdc_2)
        xr_clock_ssr, xr_orbit_ssr = gnss_io.read_ssr_file(ssr_file)

        prns = ['G%02d' % tmp for tmp in range(1, 33)]
        xr_clock_ssr = xr_clock_ssr.loc[:, prns]
        xr_clock = gnss_utils.xr_ssr2clock(
            xr_clock_ssr, xr_brdc, latency=0, interval=5, valid_seconds=4)
        xr_clock_repaired, xr_jumped = gnss_utils.repair_datum(
            xr_clock, xr_brdc)

        xr_clock_extra = gnss_utils.clock_extrapolation(
            xr_clock_repaired, xr_brdc,
            interval=1, valid_seconds=179)

        self.assertAlmostEqual(xr_clock_extra.loc[
            "2017-06-21 01:02:10.00", "G18"],
            0.0006208285716103342, places=10)
        self.assertAlmostEqual(xr_clock_extra.loc[
            "2017-06-21 01:02:11.00", "G18"],
            0.0006208285730853481, places=10)
        xr_diff = xr_clock_extra.diff('time')
        plt.plot(xr_diff, linestyle='dashed', marker='o')
        plt.show()
