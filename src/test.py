import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_btflv_8bit_fp_adder(dut):
    dut._log.info("btflv_8bit_fp_adder start test")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")

    dut.rst_n.value = 0
    dut.ui_in.value = 67
    dut.uio_in.value = 200
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Checking 2.75 - 4")
    await ClockCycles(dut.clk, 10)
    assert int(dut.f_out.value) == 186

    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 75
    dut.uio_in.value = 99
    await ClockCycles(dut.clk, 10)

    dut._log.info("Checking 5.5 + 44")
    await ClockCycles(dut.clk, 10)
    assert int(dut.f_out.value) == 100
