# 7-Segment Minute Timer
This small project contains an HDL implementation of a 60-second timer, using a
a 2-digit 7-segment display written in Amaranth/nMigen HDL language, based in Python, written for my [ECPIX-5](https://shop.lambdaconcept.com/home/46-ecpix-5.html) development board by Lambda concept. The board features an **ECP5-5G LFE5UM5G-85F** FPGA, and is connected to a 2-digit 7-segment display, connected using two PMOD interfaces.

## Build
The HDL can be built into a bitstream for the ECP-5 using the fully open source [F4PGA toolchain](https://f4pga.org/), [Yosys](https://yosyshq.net/yosys/), [nextpnr](https://github.com/YosysHQ/nextpnr) and project Trellis to build the final bitstream.

## Simulation
To produce simulation waveform files, first install [Amaranth](https://github.com/amaranth-lang/amaranth.git)
```bash
python -m pip install amaranth
```
and then simply execute either the _timer.py_ or _seven_segment.py_ to produce waveform _.vcd_ files for the timer and seven-segment driver core respectively.

## Programming
Also included is a _.cfg_ file for the ECPIX-5 board that may be used to program the board using OpenOCD.
```bash
openocd -f openocd-ecpix5.cfg -c "init" -c "svf -quiet top.svf" -c "exit"
```

![Hardware Demo](fpga_timer.gif)
