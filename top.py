from amaranth import Elaboratable, Signal, Module
from amaranth.build import Resource, Subsignal, Pins, Attrs
from amaranth_boards.ecpix5 import ECPIX585Platform
from timer import TwoSegmentClock

def dual_seven_segment(pmod0, pmod1):
    return [Resource("dual_seven_segment", 0,
        Subsignal("aa", Pins( "1", dir="o", conn=("pmod", pmod1))),
        Subsignal("ab", Pins( "2", dir="o", conn=("pmod", pmod1))),
        Subsignal("ac", Pins( "3", dir="o", conn=("pmod", pmod1))),
        Subsignal("ad", Pins( "4", dir="o", conn=("pmod", pmod1))),
        Subsignal("ae", Pins( "1", dir="o", conn=("pmod", pmod0))),
        Subsignal("af", Pins( "2", dir="o", conn=("pmod", pmod0))),
        Subsignal("ag", Pins( "3", dir="o", conn=("pmod", pmod0))),
        Subsignal("cat", Pins("4", dir="o", conn=("pmod", pmod0))),
        Attrs(IO_TYPE="LVCMOS33")
     )]


class Top(Elaboratable):

    def __init__(self, clk_freq, refresh_freq: float = 60.0):
        self.refresh_freq = refresh_freq
        self.clk_freq = clk_freq

    def elaborate(self, platform: ECPIX585Platform):
        m = Module()
        m.submodules.timer =  timer = TwoSegmentClock(self.clk_freq, refresh_freq=self.refresh_freq)

        rgb_led0 = platform.request("rgb_led", 0)
        rgb_led1 = platform.request("rgb_led", 1)
        rgb_led2 = platform.request("rgb_led", 2)
        rgb_led3 = platform.request("rgb_led", 3)
        display = platform.request("dual_seven_segment", 0)

        m.d.comb += [
            rgb_led0.r.o.eq(1),
            rgb_led0.g.o.eq(1),
            rgb_led0.b.o.eq(0),
            rgb_led1.r.o.eq(0),
            rgb_led1.g.o.eq(0),
            rgb_led1.b.o.eq(0),
            rgb_led2.r.o.eq(0),
            rgb_led2.g.o.eq(0),
            rgb_led2.b.o.eq(0),
            rgb_led3.r.o.eq(0),
            rgb_led3.g.o.eq(0),
            rgb_led3.b.o.eq(0),
        ]

        # Connect led segment signals
        m.d.comb += [
            display.aa.o.eq(timer.seven_segment.led_segments[6]),
            display.ab.o.eq(timer.seven_segment.led_segments[5]),
            display.ac.o.eq(timer.seven_segment.led_segments[4]),
            display.ad.o.eq(timer.seven_segment.led_segments[3]),
            display.ae.o.eq(timer.seven_segment.led_segments[2]),
            display.af.o.eq(timer.seven_segment.led_segments[1]),
            display.ag.o.eq(timer.seven_segment.led_segments[0]),
            display.cat.o.eq(timer.digit_sel)
        ]

        return m

if __name__ == "__main__":
    plat = ECPIX585Platform()
    plat.add_resources(dual_seven_segment(4, 5))
    plat.build(Top(clk_freq=int(100e6), refresh_freq=60.0), do_program=False)
