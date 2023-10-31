# dicttowddx

This is a python script that converts a python dictionary to a wddx string. This is useful when you want to exchange with endpoints that support WDDX format.

## Installation

```bash
pip install dicttowddx
```

## Supported data types
The following datatypes are supported:

| Python   | WDDX Type               |
|----------|-------------------------|
| None     | null                    |
| int      | number                  |
| float    | number                  |
| str      | string                  |
| bytes    | binary (base64 encoded) |
| datetime | dateTime                |
| bool     | boolean                 |

## Usage

```python
import datetime
from dicttowddx import DictToWDDX

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

wddx = DictToWDDX(c).to_wddx()
```
The value of `wddx` should be:
```text
<wddxPacket version='1.0'><header/><data><struct><var name="a"><string>ab</string></var><var name="b"><null/></var><var name="c"><string>1</string></var><var name="d"><array length="7"><null/><string>True</string><string>1.8</string><string>1</string><string>1</string><string>2021-09-15 14:30:00+00:00</string><string>as</string></array></var><var name="e"><string>2021-09-15 14:30:00+00:00</string></var><var name="f"><null/></var><var name="g"><string>1.1</string></var><var name="h"><string>True</string></var><var name="i"><string>1</string></var></struct></data></wddxPacket>
```

By default, all data types are converted to string. If you want to keep the original data type, you can use the `force_type` parameter:
```python
wddx = DictToWDDX(c, force_type=True).to_wddx()
```
The value of `wddx` should be:
```text
<wddxPacket version='1.0'><header/><data><struct><var name="a"><binary>YWI=</binary></var><var name="b"><null/></var><var name="c"><number>1</number></var><var name="d"><array length="7"><null/><boolean>True</boolean><number>1.8</number><number>1</number><string>1</string><dateTime>2021-09-15 14:30:00+00:00</dateTime><binary>YXM=</binary></array></var><var name="e"><dateTime>2021-09-15 14:30:00+00:00</dateTime></var><var name="f"><null/></var><var name="g"><number>1.1</number></var><var name="h"><boolean>True</boolean></var><var name="i"><string>1</string></var></struct></data></wddxPacket>
```

To format the output, you can use pass `format_output` arg with `True` and `display_indent` to any integer greater than `0`, default is `4`
```python
wddx = DictToWDDX(c, format_output=True, display_indent=2).to_wddx()
```
The value of `wddx` should be:
```text
<wddxPacket version='1.0'>
    <header/>
    <data>
        <struct>
            <var name="a">
                <binary>YWI=</binary>
            </var>
            <var name="b">
                <null/>
            </var>
            <var name="c">
                <number>1</number>
            </var>
            <var name="d">
                <array length="7">
                    <null/>
                    <boolean>True</boolean>
                    <number>1.8</number>
                    <number>1</number>
                    <string>1</string>
                    <dateTime>2021-09-15 14:30:00+00:00</dateTime>
                    <binary>YXM=</binary>
                </array>
            </var>
            <var name="e">
                <dateTime>2021-09-15 14:30:00+00:00</dateTime>
            </var>
            <var name="f">
                <null/>
            </var>
            <var name="g">
                <number>1.1</number>
            </var>
            <var name="h">
                <boolean>True</boolean>
            </var>
            <var name="i">
                <string>1</string>
            </var>
        </struct>
    </data>
</wddxPacket>
```
## Running tests

```bash
python -m pytest tests
```