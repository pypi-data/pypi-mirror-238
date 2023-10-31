import datetime
import unittest

from dicttowddx.main import DictToWDDX


class TestDictToWDDX(unittest.TestCase):
    a = {
        "a": [
            None,
            True,
            1.8,
            1,
            "1",
            datetime.datetime(2021, 9, 15, 14, 30, 0, tzinfo=datetime.timezone.utc),
            b"as",
        ]
    }
    b = {
        "a": b"ab",
        "c": None,
        "d": 1,
        "e": datetime.datetime(2021, 9, 15, 14, 30, 0, tzinfo=datetime.timezone.utc),
    }
    c = {
        "a": b"ab",
        "b": None,
        "c": 1,
        "d": [
            None,
            True,
            1.8,
            1,
            "1",
            datetime.datetime(2021, 9, 15, 14, 30, 0, tzinfo=datetime.timezone.utc),
            b"as",
        ],
        "e": datetime.datetime(2021, 9, 15, 14, 30, 0, tzinfo=datetime.timezone.utc),
        "f": None,
        "g": 1.1,
        "h": True,
        "i": "1",
    }
    d = {
        "a": b"ab",
    }

    def test_invalid_data(self):
        with self.assertRaises(TypeError):
            DictToWDDX(1)

    def test_valid_data_nested(self):
        wddx = """<wddxPacket version='1.0'><header/><data><struct><var name="a"><array length="7"><null/><boolean>True</boolean><number>1.8</number><number>1</number><string>1</string><dateTime>2021-09-15 14:30:00+00:00</dateTime><binary>YXM=</binary></array></var></struct></data></wddxPacket>"""  # noqa
        dtw = DictToWDDX(self.a, force_type=True, format_output=False)
        self.assertEqual(dtw.to_wddx(), wddx)

        wddx2 = """<wddxPacket version='1.0'><header/><data><struct><var name="a"><binary>YWI=</binary></var><var name="b"><null/></var><var name="c"><number>1</number></var><var name="d"><array length="7"><null/><boolean>True</boolean><number>1.8</number><number>1</number><string>1</string><dateTime>2021-09-15 14:30:00+00:00</dateTime><binary>YXM=</binary></array></var><var name="e"><dateTime>2021-09-15 14:30:00+00:00</dateTime></var><var name="f"><null/></var><var name="g"><number>1.1</number></var><var name="h"><boolean>True</boolean></var><var name="i"><string>1</string></var></struct></data></wddxPacket>"""  # noqa
        dtw2 = DictToWDDX(self.c, force_type=True, format_output=False)
        self.assertEqual(dtw2.to_wddx(), wddx2)

    def test_valid_data_not_nested(self):
        wddx = """<wddxPacket version='1.0'><header/><data><struct><var name="a"><binary>YWI=</binary></var><var name="c"><null/></var><var name="d"><number>1</number></var><var name="e"><dateTime>2021-09-15 14:30:00+00:00</dateTime></var></struct></data></wddxPacket>"""  # noqa
        dtw = DictToWDDX(self.b, force_type=True, format_output=False)
        self.assertEqual(dtw.to_wddx(), wddx)

        wddx3 = """<wddxPacket version='1.0'><header/><data><struct><var name="a"><string>ab</string></var></struct></data></wddxPacket>"""  # noqa
        dtw3 = DictToWDDX(self.d, force_type=False, format_output=False)
        self.assertEqual(dtw3.to_wddx(), wddx3)

    def test_invalid_data_none_key(self):
        with self.assertRaises(KeyError):
            DictToWDDX({None: 1}).to_wddx()

    def test_type_force(self):
        self.assertEqual(DictToWDDX(self.a, force_type=True).wddx_type(1), "number")
        self.assertEqual(DictToWDDX(self.a, force_type=True).wddx_type(1.8), "number")
        self.assertEqual(DictToWDDX(self.a, force_type=True).wddx_type(True), "boolean")
        self.assertEqual(
            DictToWDDX(self.a, force_type=True).wddx_type(False), "boolean"
        )
        self.assertEqual(
            DictToWDDX(self.a, force_type=True).wddx_type(b"test"), "binary"
        )
        self.assertEqual(DictToWDDX(self.a, force_type=True).wddx_type("1"), "string")

        self.assertEqual(DictToWDDX(self.a).wddx_type(1), "string")
        self.assertEqual(DictToWDDX(self.a).wddx_type(1.8), "string")
        self.assertEqual(DictToWDDX(self.a).wddx_type(True), "string")
        self.assertEqual(DictToWDDX(self.a).wddx_type(False), "string")
        self.assertEqual(DictToWDDX(self.a).wddx_type(b"test"), "string")

    def test_to_type(self):
        self.assertEqual(DictToWDDX(self.a, force_type=True).to_type(1), "number")
        self.assertEqual(DictToWDDX(self.a, force_type=True).to_type(1.8), "number")
        self.assertEqual(DictToWDDX(self.a, force_type=True).to_type(True), "boolean")
        self.assertEqual(DictToWDDX(self.a, force_type=True).to_type(False), "boolean")
        self.assertEqual(DictToWDDX(self.a, force_type=True).to_type(b"test"), "binary")
        self.assertEqual(DictToWDDX(self.a, force_type=True).to_type("1"), "string")
        self.assertEqual(
            DictToWDDX(self.a, force_type=True).to_type(
                datetime.datetime(2021, 9, 15, 14, 30, 0, tzinfo=datetime.timezone.utc)
            ),
            "dateTime",
        )
        self.assertEqual(
            DictToWDDX(self.a, force_type=True).to_type("2021-09-15T15:40:36.000Z"),
            "string",
        )


if __name__ == "__main__":
    unittest.main()
