from amaranth import Elaboratable, Signal, Module
from amaranth.sim import Simulator, Settle, Delay
# Constants based on common Anode,
# i.e for a segment to be on low
ZERO = 0b0000001
ONE = 0b1001111
TWO = 0b0010010
THREE = 0b0000110
FOUR = 0b1001100
FIVE = 0b0100100
SIX = 0b0100000
SEVEN = 0b0001111
EIGHT = 0b0000000
NINE = 0b0000100

DIGITS = [ZERO, ONE, TWO, THREE, FOUR,
          FIVE, SIX, SEVEN, EIGHT, NINE]


class SevenSegmentDisplay(Elaboratable):

    def __init__(
        self,
        common_anode: bool = False,
    ):
        # Reset signal
        self.digit = Signal(4)
        self.common_anode = common_anode
        if common_anode:
            self.digit_segments = DIGITS
            self.disp_off = 0b1111111
        else:
            self.disp_off = 0b0000000
            self.digit_segments = [(~d) & 0b1111111 for d in DIGITS]

        self.led_segments = Signal(7, reset=self.disp_off)

    def elaborate(self, platform) -> Module:
        # Digit cathode pins
        m = Module()

        with m.Switch(self.digit):
            with m.Case(0):
                m.d.comb += self.led_segments.eq(self.digit_segments[0])
            with m.Case(1):
                m.d.comb += self.led_segments.eq(self.digit_segments[1])
            with m.Case(2):
                m.d.comb += self.led_segments.eq(self.digit_segments[2])
            with m.Case(3):
                m.d.comb += self.led_segments.eq(self.digit_segments[3])
            with m.Case(4):
                m.d.comb += self.led_segments.eq(self.digit_segments[4])
            with m.Case(5):
                m.d.comb += self.led_segments.eq(self.digit_segments[5])
            with m.Case(6):
                m.d.comb += self.led_segments.eq(self.digit_segments[6])
            with m.Case(7):
                m.d.comb += self.led_segments.eq(self.digit_segments[7])
            with m.Case(8):
                m.d.comb += self.led_segments.eq(self.digit_segments[8])
            with m.Case(9):
                m.d.comb += self.led_segments.eq(self.digit_segments[9])
            with m.Default():
                m.d.comb += self.led_segments.eq(self.disp_off)

        return m


if __name__ == "__main__":
    dut = SevenSegmentDisplay()

    def process():
        yield dut.digit.eq(8)
        yield dut.en.eq(0)
        yield Delay(10e-9)
        yield Settle()
        yield Delay(10e-9)
        yield dut.en.eq(1)
        yield Settle()
        for d in range(10):
            yield dut.digit.eq(d)
            yield Delay(10e-9)
            yield Settle()
            assert (yield dut.led_segments) == DIGITS[d]

    sim = Simulator(dut)
    sim.add_process(process)
    with sim.write_vcd("seven_segment.py".vcd"):
        sim.run_until(1000e-9)
