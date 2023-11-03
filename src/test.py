import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_btflv_8bit_fp_adder(dut):
    dut._log.info("btflv_8bit_fp_adder start test")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1

    dut._log.info("reset")

    dut.rst_n.value = 0
    dut.ui_in.value = 67
    dut.uio_in.value = 200
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Checking 2.75 + -4 (0 100 0011 + 1 1001 000)")
    await ClockCycles(dut.clk, 10)
    dut._log.info(dut.uo_out.value)
    assert int(dut.uo_out.value) == 186

    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 75
    dut.uio_in.value = 99
    await ClockCycles(dut.clk, 10)

    dut._log.info("Checking 5.5 + 44 (0 1001 011 + 0 1100 011)")
    await ClockCycles(dut.clk, 10)
    dut._log.info(dut.uo_out.value)
    assert int(dut.uo_out.value) == 100

    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 65
    dut.uio_in.value = 66
    await ClockCycles(dut.clk, 10)

    dut._log.info("Checking 2.25 + 2.5 (0 1000 001 + 0 1000 010)")
    await ClockCycles(dut.clk, 10)
    dut._log.info(dut.uo_out.value)
    assert int(dut.uo_out.value) == 74

    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 250
    dut.uio_in.value = 247
    await ClockCycles(dut.clk, 10)

    dut._log.info("Checking NaN + -240 (1 1111 010 + 1 1110 111)")
    await ClockCycles(dut.clk, 10)
    dut._log.info(dut.uo_out.value)
    assert int(dut.uo_out.value) == 127

    await ClockCycles(dut.clk, 10)
    dut.ui_in.value = 248
    dut.uio_in.value = 81
    await ClockCycles(dut.clk, 10)

    dut._log.info("Checking -Inf + 9 (1 1111 000 + 0 1010 001)")
    await ClockCycles(dut.clk, 10)
    dut._log.info(dut.uo_out.value)
    assert int(dut.uo_out.value) == 248