
import time
import math
import enum
import datetime
import logging

LOG = logging.getLogger(__name__)

class DL24M:
    class Query(enum.IntEnum):
        ISON        = 0x10
        MILLIVOLTS  = 0x11
        MILLIAMPS   = 0x12
        TIME        = 0x13
        MAH         = 0x14
        MWH         = 0x15
        TEMP        = 0x16
        LIMIT_VAL   = 0x17
        LIMIT_VOLTS = 0x18
        LIMIT_TIME  = 0x19
        CLEAR       = 0x20
        MODE        = 0x21
        TEST_DATA   = 0x22
        TEMP2       = 0x36

    class Command(enum.IntEnum):
        POWER               = 0x01
        SET_LIMIT_VAL       = 0x02
        SET_LIMIT_VOLTS     = 0x03
        SET_LIMIT_TIME      = 0x04
        RESET               = 0x05
        MODE                = 0x06
        BATTERY_SIZE        = 0x08

    class Power(enum.IntEnum):
        ENABLED     = 0x01
        DISABLED    = 0x00

    class Mode(enum.IntEnum):
        CURRENT     = 0x00
        VOLTAGE     = 0x01
        RESISTANCE  = 0x02
        POWER       = 0x03
        BATTERY     = 0x04
        POWER_SUPPLY= 0x05
        CABLE       = 0x06

    class BatterySize(enum.IntEnum):
        BIG     = 0x00
        SMALL   = 0x01

    def __init__(self, ser):
        self.ser = ser

    @staticmethod
    def query(q, a=0, b=0, c=0, d=0, e=0):
        return bytes(
            (0xb1, 0xb2, q, a, b, c, d, e, 0xb6)
        )

    def read(self, n=0, t=0):
        b = self.ser.read_all()
        if len(b) >= n or t == 0:
            return b
        self.ser.timeout = t
        b += self.ser.read(n - len(b))
        return b


    def flush(self):
        self.ser.timeout = 0
        b = self.ser.read(128)
        if b:
            LOG.info(f'extra bytes: {b.hex(" ", 4)}')
        return b

    def get_value(self, que, **qs):
        # self.flush()
        q = self.query(que, **qs)
        n = self.ser.write(q)
        assert n == 9
        self.ser.flush()
        r = b''
        for i in range(4):
            # self.ser.timeout = 0.1
            r += self.read(10, .1)
            # r += self.ser.read_until('\0\0\xCE\xCF')
            n1 = r.find(b'\xCA\xCB')
            n2 = r.find(b'\0\0\xCE\xCF')
            if (0 <= n1 < n2 < len(r)):
               break
            LOG.debug(f'read: {r.hex(" ", 4)}')
        else:
            raise RuntimeError(repr(r.hex(' ', 4)))
        if n1:
            LOG.info(f'ectra bytes: {r[:n1].hex(" ", 4)}')
        v = r[n1+2:n2]
        assert v[0] == que
        LOG.debug(f'got: {r.hex(" ", 4)}')
        LOG.debug(f'got val {que:02x}: {v[1:].hex(" ", 4)}')
        return v[1:]

    def get_state(self):
        v = self.get_value(DL24M.Query.ISON)
        p = int.from_bytes(v)
        return DL24M.Power(p)

    def get_millivolts(self):
        v = self.get_value(DL24M.Query.MILLIVOLTS)
        return int.from_bytes(v)

    def get_clear(self):
        v = self.get_value(DL24M.Query.CLEAR)
        return int.from_bytes(v)

    def get_milliamps(self):
        v = self.get_value(DL24M.Query.MILLIAMPS)
        return int.from_bytes(v)

    def get_time(self):
        v = self.get_value(DL24M.Query.TIME)
        return datetime.timedelta(
            hours=v[0],
            minutes=v[1],
            seconds=v[2],
        )

    def get_milliamphours(self):
        v = self.get_value(DL24M.Query.MAH)
        return int.from_bytes(v)

    def get_milliwatthours(self):
        v = self.get_value(DL24M.Query.MWH)
        return int.from_bytes(v)

    def get_temp(self):
        v = self.get_value(DL24M.Query.TEMP)
        return int.from_bytes(v) / 10

    def get_temp2(self):
        v = self.get_value(DL24M.Query.TEMP2)
        return int.from_bytes(v) / 100.

    def get_limit_value(self):
        v = self.get_value(DL24M.Query.LIMIT_VAL)
        LOG.info(v.hex(' ', 4))
        return int.from_bytes(v)

    def get_min_voltage(self):
        v = self.get_value(DL24M.Query.LIMIT_VOLTS)
        return int.from_bytes(v) / 100.

    def get_max_time(self):
        v = self.get_value(DL24M.Query.LIMIT_TIME)
        LOG.debug(v.hex(' ', 4))
        return datetime.timedelta(
            hours=v[0],
            minutes=v[1],
            seconds=v[2],
        )

    def get_mode(self):
        v = self.get_value(DL24M.Query.MODE)
        m = int.from_bytes(v)
        return DL24M.Mode(m)

    def get_test_data(self):
        v = self.get_value(DL24M.Query.TEST_DATA, b=1, c=1, d=1, e=1)
        x = int.from_bytes(v)
        return x

    def get_all(self):
        return dict(
            state = self.get_state(),
            mode = self.get_mode(),
            voltage_mv = self.get_millivolts(),
            current_ma = self.get_milliamps(),
            capacity_mah = self.get_milliamphours(),
            energy_mwh = self.get_milliwatthours(),
            temp_c = self.get_temp2(),
            duration_s = self.get_time().total_seconds(),
            # test_data = self.get_test_data(),
        )

    def parse_msg(self, bytes):
        '''
  ca cb 22 00 00 00 00 00 ce cf

  b1 b2 22 00 00 00 00 00 b6
  ca cb 22 00 00 00 00 00 ce cf
  ca cb 61 01 00 00 00 00 01 ff 00 00 05 00 00 ff 00 00 00 ce cf
  ca cb 62 01 00 00 03 00 01 f9 00 00 0a 00 01 f5 00 00 00 ce cf
  ca cb 63 01 00 00 14 00 01 e7 00 00 14 00 03 ce 00 00 00 ce cf
  ca cb 64 01 00 00 2b 00 01 d0 00 00 1e 00 05 6f 00 00 00 ce cf
  ca cb 65 01 00 00 ca 00 01 31 00 00 22 00 04 33 00 00 00 ce cf
  ca cb 66 01 00 00 ff 00 00 fc 00 00 23 00 03 a8 00 00 00 ce cf
        -n    -volts-- -volts-- -amps--- -watts--
                /100     /100     /10      /100
                                         -mOhm---        ^ err

        '''
        pass

    def set_cmd(self, cmd, *val, **kv):
        q = self.query(cmd, *val, **kv)
        n = self.ser.write(q)
        assert n == 9
        self.ser.flush()
        LOG.info(f'write: {q.hex(" ",3)}')

    def set_power_on(self):
        self.set_cmd(DL24M.Command.POWER, DL24M.Power.ENABLED)

    def set_power_off(self):
        self.set_cmd(DL24M.Command.POWER, DL24M.Power.DISABLED)

    def set_mode(self, mode):
        self.set_cmd(DL24M.Command.MODE, 0, 0, mode)
        time.sleep(1)
        self.flush()
        m = self.get_mode()
        assert m == mode, (m, mode)

    def set_limit(self, lim):
        v = round(lim * 1000.).to_bytes(3)
        LOG.info(v.hex())
        self.set_cmd(DL24M.Command.SET_LIMIT_VAL, v[0], v[1], v[2])
        self.flush()
        time.sleep(0.2)
        lv = self.get_limit_value() / 1000.
        LOG.info(f'set: {lim!r} check: {lv!r}')
        assert lim == lv

    def set_min_voltage(self, lim):
        v = round(lim * 10.).to_bytes(3)
        LOG.info(v.hex())
        self.set_cmd(DL24M.Command.SET_LIMIT_VOLTS, v[0], v[1], v[2])
        self.flush()
        time.sleep(0.2)
        lv = self.get_min_voltage()
        LOG.info(f'set: {lim!r} check: {lv!r}')
        assert lim == lv

    def set_max_time(self, dur=datetime.timedelta()):
        v = round(dur.total_seconds()).to_bytes(3)
        LOG.info(v.hex())
        self.set_cmd(DL24M.Command.SET_LIMIT_TIME, v[0], v[1], v[2])
        self.flush()
        time.sleep(0.5)
        tv = self.get_max_time()
        LOG.info(f'set: {dur!r} check: {tv!r}')
        assert dur == tv

    def reset_counters(self):
        self.set_cmd(DL24M.Command.RESET)
        self.flush()
        time.sleep(0.2)
        mah = self.get_milliamphours()
        assert mah == 0



