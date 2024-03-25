from amaranth import Elaboratable, Signal, Module
from amaranth.sim import Simulator, Tick
from seven_segment import SevenSegmentDisplay


class TwoSegmentClock(Elaboratable):

    def __init__(self, clk_freq: int, refresh_freq: float = 60.0):
        self.clk_freq = clk_freq
        # Selects which digit to enable
        self.digit_sel = Signal(1)
        self.refresh_freq = refresh_freq
        self.seven_segment = SevenSegmentDisplay()

    def elaborate(self, platform) -> Module:
        m = Module()
        # Counter for the number of clock cycles
        clk_counter = Signal(32)
        # Counter for the number of cycles since last refresh cycle start
        refresh_counter = Signal(32)
        # Number of clock cylces per digit refresh cycle
        refresh_cycle = round(self.clk_freq / (self.refresh_freq * 2))
        digit_hi = Signal(4)
        digit_lo = Signal(4)

        m.submodules.seven_segment = seven_segment = self.seven_segment

        # Enables the digits one by one periodically
        # since they share the same bus for which digit is to
        # be displayed, when enabling a particular digit,
        # we also set the digit bus-line equal to the corresponding
        # time digit
        with m.If(refresh_counter == refresh_cycle - 1):
            m.d.sync += [
                refresh_counter.eq(0),
                self.digit_sel.eq(~self.digit_sel),
            ]
        with m.Else():
            m.d.sync += refresh_counter.eq(refresh_counter + 1)

        with m.If(self.digit_sel == 1):
            m.d.comb += seven_segment.digit.eq(digit_hi)
        with m.Else():
            m.d.comb += seven_segment.digit.eq(digit_lo)

        # Every second we update which digits should
        # show on the seven segment display
        with m.If(clk_counter == self.clk_freq - 1):
            m.d.sync += clk_counter.eq(0)

            # Every 10 seconds bring the low digit
            # back to 0
            with m.If(digit_lo == 9):
                m.d.sync += digit_lo.eq(0)
                # Wraps the time from 59 back to 00
                with m.If(digit_hi == 5):
                    m.d.sync += digit_hi.eq(0)
                with m.Else():
                    m.d.sync += digit_hi.eq(digit_hi + 1)
            with m.Else():
                m.d.sync += digit_lo.eq(digit_lo + 1)
        with m.Else():
            m.d.sync += clk_counter.eq(clk_counter + 1)

        return m


if __name__ == "__main__":
    clk_freq = 60
    refresh_freq = 1.0
    dut = TwoSegmentClock(clk_freq, refresh_freq=refresh_freq)
    sim = Simulator(dut)

    def process():
        for _ in range(clk_freq * (60 + 2)):
            yield Tick()

    sim.add_clock(1 / clk_freq)
    sim.add_sync_process(process)
    with sim.write_vcd("timer.vcd"):
        sim.run()
