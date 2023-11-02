########################################
# UNIT TESTS
########################################


from textkernel import *

import unittest


class Test_VALUE(unittest.TestCase):

    def runTest(self):

        parser = VALUE + StringEnd()

        self.assertEqual(parser.parseString("  1234 ")[0],  1234)
        self.assertEqual(parser.parseString(" -1234 ")[0], -1234)
        self.assertEqual(parser.parseString(" +1234 ")[0],  1234)

        self.assertEqual(parser.parseString("  1234.      ")[0],  1234.)
        self.assertEqual(parser.parseString("  12340.e-01 ")[0],  1234.)
        self.assertEqual(parser.parseString("  12340e-1   ")[0],  1234.)
        self.assertEqual(parser.parseString("  234.5e+01  ")[0],  2345.)
        self.assertEqual(parser.parseString("  234.5D1    ")[0],  2345.)
        self.assertEqual(parser.parseString("  234.5d1    ")[0],  2345.)
        self.assertEqual(parser.parseString("  234.5E+001 ")[0],  2345.)
        self.assertEqual(parser.parseString(" +1234.      ")[0],  1234.)
        self.assertEqual(parser.parseString(" +12340.e-01 ")[0],  1234.)
        self.assertEqual(parser.parseString(" +12340e-1   ")[0],  1234.)
        self.assertEqual(parser.parseString(" +234.5e+01  ")[0],  2345.)
        self.assertEqual(parser.parseString(" +234.5D1    ")[0],  2345.)
        self.assertEqual(parser.parseString(" +234.5d1    ")[0],  2345.)
        self.assertEqual(parser.parseString(" +234.5E+001 ")[0],  2345.)
        self.assertEqual(parser.parseString(" -1234.0     ")[0], -1234.)
        self.assertEqual(parser.parseString(" -12340.e-01 ")[0], -1234.)
        self.assertEqual(parser.parseString(" -12340e-1   ")[0], -1234.)
        self.assertEqual(parser.parseString(" -234.5e+01  ")[0], -2345.)
        self.assertEqual(parser.parseString(" -234.5D1    ")[0], -2345.)
        self.assertEqual(parser.parseString(" -234.5d1    ")[0], -2345.)
        self.assertEqual(parser.parseString(" -234.5E+001 ")[0], -2345.)

        self.assertEqual(parser.parseString(" '  1234 '")[0], "  1234 ")
        self.assertEqual(parser.parseString("''' 1234 '")[0], "' 1234 ")
        self.assertEqual(parser.parseString("' 1234 '''")[0], " 1234 '")
        self.assertEqual(parser.parseString("' 12''34 '")[0], " 12'34 ")
        self.assertEqual(parser.parseString("''")[0],         "")
        self.assertEqual(parser.parseString("''''")[0],       "'")

        self.assertEqual(parser.parseString("@2001-Jan-01")[0],
            dt.datetime(2001,1,1))
        self.assertEqual(parser.parseString("@2001-Jan-01:12:34:56.789")[0],
            dt.datetime(2001,1,1,12,34,56,789000))

        self.assertEqual(parser.parseString("(1,2,3)")[0],    [1,2,3])
        self.assertEqual(parser.parseString("(1)")[0],        1)
        self.assertEqual(parser.parseString("(1,2, \n3)")[0], [1,2,3])
        self.assertEqual(parser.parseString("('1','2')")[0],  ["1","2"])
        self.assertEqual(parser.parseString("('1''','2')")[0],["1'","2"])
        self.assertEqual(parser.parseString("(1, @Jul-4-1776)")[0],
            [1, dt.datetime(1776,7,4)])

        # Doesn't recognize...
        self.assertRaises(ParseException, parser.parseString, "  1234 .  ")
        self.assertRaises(ParseException, parser.parseString, "- 12340e-1")
        self.assertRaises(ParseException, parser.parseString, "-12340 e-1")
        self.assertRaises(ParseException, parser.parseString, "-12340e -1")
        self.assertRaises(ParseException, parser.parseString, "-12340e- 1")

        self.assertRaises(ParseException, parser.parseString, "@ 2001-Jan-01")
        self.assertRaises(ParseException, parser.parseString, "@2001 -Jan-01")
        self.assertRaises(ParseException, parser.parseString, "@2001- Jan-01")

        # A tab character is not supposed to be treated as whitespace
        # self.assertRaises(ParseException, parser.parseString, "\t1")
        # self.assertRaises(ParseException, parser.parseString, "1\t")


class Test_STATEMENT(unittest.TestCase):

    def runTest(self):

        DICTIONARY.clear()
        parser = STATEMENT + StringEnd()

        # Tests of simple definitions and augmentations
        parser.parseString(" A = 1 \n")
        self.assertEqual(DICTIONARY["A"], 1)

        parser.parseString(" A = 2 \n")
        self.assertEqual(DICTIONARY["A"], 2)

        parser.parseString(" A += 3 \n")
        self.assertEqual(DICTIONARY["A"], [2,3])

        parser.parseString(" B += 4 \n")
        self.assertEqual(DICTIONARY["B"], 4)

        # Tests of expanding lists
        parser.parseString("D = (1.)\n")
        self.assertEqual(DICTIONARY["D"], 1.)
        parser.parseString("D += 2.\n")
        self.assertEqual(DICTIONARY["D"], [1.,2.])

        parser.parseString("D = 3.\n")
        parser.parseString("D += 4.\n")
        self.assertEqual(DICTIONARY["D"], [3.,4.])

        parser.parseString("D = 5.\n")
        parser.parseString("D += (6.)\n")
        self.assertEqual(DICTIONARY["D"], [5.,6.])

        parser.parseString("D = (7.)\n")
        parser.parseString("D += (8.)\n")
        self.assertEqual(DICTIONARY["D"], [7.,8.])

        parser.parseString("D = (9.,10.)\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.])
        parser.parseString("D += 11.\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.,11.])
        parser.parseString("D += (12.)\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.,11.,12.])
        parser.parseString("D += (13.,14.)\n")
        self.assertEqual(DICTIONARY["D"], [9.,10.,11.,12.,13.,14.])

        # Tests of string concatenation
        parser.parseString("E = ('Antidis// ','establish// ','mentarianism')\n")
        self.assertEqual(DICTIONARY["E"], ["Antidisestablishmentarianism"])

        parser.parseString("E = 'T''was brillig and //  '\n")
        parser.parseString("E += 'the slithy toves'\n")
        self.assertEqual(DICTIONARY["E"], "T'was brillig and the slithy toves")

        parser.parseString("E += 'Did gyre and //  '\n")
        parser.parseString("E += 'gimble in the wabe'  \n")
        self.assertEqual(DICTIONARY["E"], ["T'was brillig and the slithy toves",
                                           "Did gyre and gimble in the wabe"])

        parser.parseString("F += 'Four score //  '\n")
        parser.parseString("F += '//'  \n")
        parser.parseString("F += 'and seven //'  \n")
        self.assertEqual(DICTIONARY["F"], "Four score and seven //")

        parser.parseString("F += ('years //  ')  \n")
        self.assertEqual(DICTIONARY["F"], "Four score and seven years //  ")

        parser.parseString("F += ('ago','our fathers //', 'brought forth')\n")
        self.assertEqual(DICTIONARY["F"], ["Four score and seven years ago",
                                           "our fathers brought forth"])

        # Tests of prefixed definitions and augmentations
        parser.parseString(" B/C = 5 \n")
        self.assertEqual(DICTIONARY["B"]["C"], 5)

        parser.parseString(" B/C/D = 6 \n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], 6)

        parser.parseString(" B/C/D += 7 \n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], [6,7])

        parser.parseString(" B/C/D += (8) \n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], [6,7,8])

        parser.parseString(" B/C/D += (9,10,11)\n")
        self.assertEqual(DICTIONARY["B"]["C"]["D"], [6,7,8,9,10,11])

        # Tests of BODY codes and names
        parser.parseString(" NAIF_BODY_CODE += ( 698 )\n")
        parser.parseString(" NAIF_BODY_NAME += ( 'TEST' )\n")
        self.assertEqual(DICTIONARY["BODY"][698], DICTIONARY["BODY"]["TEST"])
        self.assertEqual(DICTIONARY["BODY"][698]["ID"], 698)
        self.assertEqual(DICTIONARY["BODY"][698]["NAME"], "TEST")

        parser.parseString(" BODY698_RADII = (100., 90., 80.)\n")
        self.assertEqual(DICTIONARY["BODY"][698]["RADII"][2], 80.)
        self.assertEqual(DICTIONARY["BODY"][698], DICTIONARY["BODY"]["TEST"])

        parser.parseString("BODY699_RADII = (60330.)\n")
        self.assertEqual(DICTIONARY["BODY"][699]["RADII"], 60330.)
        self.assertEqual(DICTIONARY["BODY"]["SATURN"]["RADII"], 60330.)

        # Tests of FRAME codes, names and centers
        parser.parseString("FRAME_1698_NAME = 'IAU_TEST'\n")
        self.assertEqual(DICTIONARY["FRAME"][1698]["NAME"], "IAU_TEST")
        self.assertEqual(DICTIONARY["FRAME"][1698]["ID"], 1698)
        self.assertEqual(DICTIONARY["FRAME"][1698],
                         DICTIONARY["FRAME"]["IAU_TEST"])

        parser.parseString("FRAME_1698_CENTER = 698\n")
        self.assertEqual(DICTIONARY["FRAME"][698], DICTIONARY["FRAME"][1698])

        parser.parseString("FRAME_1697_NAME = 'INERTIAL'\n")
        self.assertEqual(DICTIONARY["FRAME"][1697]["NAME"], "INERTIAL")
        self.assertEqual(DICTIONARY["FRAME"][1697]["ID"], 1697)
        self.assertEqual(DICTIONARY["FRAME"][1697],
                         DICTIONARY["FRAME"]["INERTIAL"])

        parser.parseString("FRAME_1697_CENTER = 698\n")
        self.assertEqual(DICTIONARY["FRAME"][698], DICTIONARY["FRAME"][1698])

        parser.parseString("FRAME_618_CLASS =  2 \n")
        self.assertEqual(DICTIONARY["FRAME"][618]["CLASS"], 2)
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["CLASS"], 2)
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["NAME"], "IAU_PAN")
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["CENTER"], 618)
        self.assertEqual(DICTIONARY["FRAME"]["IAU_PAN"]["ID"], 10082)
        self.assertEqual(DICTIONARY["FRAME"][618], DICTIONARY["FRAME"][10082])

        # Tests of general names
        parser.parseString("FRAME_IAU_S7_2004 = 65035\n")
        self.assertEqual(DICTIONARY["FRAME_IAU_S7_2004"], 65035)


class Test_FromFile(unittest.TestCase):

  def runTest(self):

    import os.path

    # Test DefaultBodies()
    dict = default_bodies(clear=True)
    self.assertEqual(dict["BODY"][618], dict["BODY"]["PAN"])
    self.assertEqual(dict["BODY"][618]["NAME"], "PAN")
    self.assertEqual(dict["BODY"][618]["ID"],     618)

    # ... make sure it does not replace a pre-existing definition
    DICTIONARY.clear()
    DICTIONARY["BODY"] = {618: {"ID":618, "NAME":"ALIAS"}}
    DICTIONARY["BODY"]["ALIAS"] = DICTIONARY["BODY"][618]

    dict = default_bodies(clear=False)

    self.assertEqual(dict["BODY"][618],   dict["BODY"]["ALIAS"])
    self.assertEqual(dict["BODY"]["PAN"], dict["BODY"]["ALIAS"])
    self.assertEqual(dict["BODY"]["PAN"]["NAME"], "ALIAS")
    self.assertEqual(dict["BODY"]["PAN"]["ID"],      618)

    # Test DefaultFrames()
    dict = default_frames(clear=True)
    self.assertEqual(dict["FRAME"][618], dict["FRAME"]["IAU_PAN"])
    self.assertEqual(dict["FRAME"][618], dict["FRAME"][10082])
    self.assertEqual(dict["FRAME"][618]["ID"],       10082)
    self.assertEqual(dict["FRAME"][618]["NAME"], "IAU_PAN")
    self.assertEqual(dict["FRAME"][618]["CENTER"],     618)

    self.assertEqual(dict["FRAME"][399]["NAME"], "IAU_EARTH")
    self.assertEqual(dict["FRAME"]["IAU_EARTH"]["CENTER"], 399)
    self.assertEqual(dict["FRAME"]["ITRF93"]["CENTER"],    399)

    # ... make sure it does not replace a pre-existing definition
    DICTIONARY.clear()
    DICTIONARY["FRAME"] = {618: {"CENTER":618, "NAME":"NOT_IAU", "ID":11111}}

    dict = default_frames(clear=False)

    self.assertEqual(dict["FRAME"][10082], dict["FRAME"]["IAU_PAN"])
    self.assertEqual(dict["FRAME"][10082]["ID"],       10082)
    self.assertEqual(dict["FRAME"][10082]["NAME"], "IAU_PAN")
    self.assertEqual(dict["FRAME"][10082]["CENTER"],     618)

    self.assertEqual(dict["FRAME"][618]["ID"],       11111)
    self.assertEqual(dict["FRAME"][618]["NAME"], "NOT_IAU")
    self.assertEqual(dict["FRAME"][618]["CENTER"],     618)

    # Test FromFile() by attempting to parse every text kernel
    filenames = ["cas_iss_v10.ti",
                 "cas_rocks_v18.tf",
                 "cas_status_v04.tf",
                 "cas_v40.tf",
                 "cas00149.tsc",
                 "cpck_rock_21Jan2011_merged.tpc",
                 "cpck14Oct2011.tpc",
                 "earth_topo_050714.tf",
                 "juno_jiram_v00.ti",
                 "juno_v02.tf",
                 "mars_iau2000_v0.tpc",
                 "mk00062a.tsc",
                 "naif0009.tls",
                 "new_horizons_295.tsc",
                 "nh_lorri_v100.ti",
                 "nh_v110.tf",
                 "pck00010.tpc",
                 "vg2_isswa_v01.ti",
                 "vg2_v02.tf",
                 "vg200011.tsc"]

    for file in filenames:
        print(file)
        d = from_file(os.path.join('test_files', file))
