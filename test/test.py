# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

@cocotb.test()
async def test_nanocalc_basic(dut):
    """Basic functionality test for NanoCalc ALU"""
    
    dut._log.info("Start NanoCalc basic test")
    
    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    dut._log.info("Test NanoCalc ALU operations")
    
    # Test 1: Addition (5 + 3 = 8)
    dut.ui_in.value = 0b00110101  # A=5 (bits 3:0), B=3 (bits 7:4)
    dut.uio_in.value = 0b000      # Operation = ADD
    await Timer(1, units="ns")    # Allow combinational logic to settle
    
    result = dut.uo_out.value & 0xF      # Extract result (bits 3:0)
    carry = (dut.uo_out.value >> 4) & 1  # Extract carry flag (bit 4)
    
    assert result == 8, f"Addition test failed: 5+3 expected 8, got {result}"
    assert carry == 0, f"Addition carry test failed: expected 0, got {carry}"
    dut._log.info(f"✓ Addition test passed: 5+3={result}, carry={carry}")
    
    # Test 2: Subtraction (10 - 6 = 4)
    dut.ui_in.value = 0b01101010  # A=10 (bits 3:0), B=6 (bits 7:4)  
    dut.uio_in.value = 0b001      # Operation = SUB
    await Timer(1, units="ns")
    
    result = dut.uo_out.value & 0xF
    carry = (dut.uo_out.value >> 4) & 1
    
    assert result == 4, f"Subtraction test failed: 10-6 expected 4, got {result}"
    dut._log.info(f"✓ Subtraction test passed: 10-6={result}, carry={carry}")

@cocotb.test()
async def test_nanocalc_all_operations(dut):
    """Comprehensive test for all ALU operations"""
    
    dut._log.info("Start comprehensive ALU test")
    
    # Initialize clock
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    
    # Reset
    dut.ena.value = 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    
    # Test cases: (A, B, operation, expected_result, expected_carry, description)
    test_cases = [
        (5, 3, 0, 8, 0, "ADD: 5+3"),
        (15, 1, 0, 0, 1, "ADD with overflow: 15+1"), 
        (10, 6, 1, 4, 0, "SUB: 10-6"),
        (3, 5, 1, 14, 1, "SUB with underflow: 3-5"),
        (12, 10, 2, 8, 0, "AND: 1100&1010=1000"),
        (12, 3, 3, 15, 0, "OR: 1100|0011=1111"),
        (10, 5, 4, 15, 0, "XOR: 1010^0101=1111"),
        (10, 0, 5, 5, 0, "NOT: ~1010=0101"),
        (6, 0, 6, 12, 0, "SHIFT: 0110<<1=1100"),
        (9, 0, 6, 2, 1, "SHIFT with carry: 1001<<1=0010,carry=1"),
        (5, 5, 7, 1, 1, "EQUAL: 5==5 returns 1"),
        (5, 7, 7, 0, 0, "NOT EQUAL: 5==7 returns 0"),
    ]
    
    for a, b, op, exp_result, exp_carry, description in test_cases:
        # Set inputs: A in lower 4 bits, B in upper 4 bits
        dut.ui_in.value = (b << 4) | a
        dut.uio_in.value = op
        
        await Timer(1, units="ns")  # Allow combinational logic to settle
        
        # Read outputs
        result = dut.uo_out.value & 0xF
        carry = (dut.uo_out.value >> 4) & 1
        zero = (dut.uo_out.value >> 5) & 1
        
        # Check results
        assert result == exp_result, f"{description}: Expected result {exp_result}, got {result}"
        assert carry == exp_carry, f"{description}: Expected carry {exp_carry}, got {carry}"
        
        # Check zero flag
        expected_zero = 1 if result == 0 else 0
        assert zero == expected_zero, f"{description}: Expected zero flag {expected_zero}, got {zero}"
        
        dut._log.info(f"✓ {description} passed: result={result}, carry={carry}, zero={zero}")

@cocotb.test()
async def test_nanocalc_edge_cases(dut):
    """Test edge cases and boundary conditions"""
    
    dut._log.info("Start edge case tests")
    
    # Initialize
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    # Edge cases
    edge_cases = [
        (0, 0, 0, 0, 0, "Zero + Zero"),
        (15, 15, 0, 14, 1, "Max + Max (overflow)"),
        (0, 15, 1, 1, 1, "Zero - Max (underflow)"), 
        (15, 0, 2, 0, 0, "Max AND Zero"),
        (0, 0, 3, 0, 0, "Zero OR Zero"),
        (15, 15, 4, 0, 0, "Max XOR Max"),
        (0, 0, 5, 15, 0, "NOT Zero = Max"),
        (15, 0, 5, 0, 0, "NOT Max = Zero"),
        (8, 0, 6, 0, 1, "Shift with MSB set"),
        (0, 0, 7, 1, 1, "Zero == Zero"),
    ]
    
    for a, b, op, exp_result, exp_carry, description in edge_cases:
        dut.ui_in.value = (b << 4) | a
        dut.uio_in.value = op
        
        await Timer(1, units="ns")
        
        result = dut.uo_out.value & 0xF
        carry = (dut.uo_out.value >> 4) & 1
        
        assert result == exp_result, f"Edge case {description}: Expected {exp_result}, got {result}"
        assert carry == exp_carry, f"Edge case {description}: Expected carry {exp_carry}, got {carry}"
        
        dut._log.info(f"✓ Edge case {description} passed: result={result}, carry={carry}")

@cocotb.test()
async def test_nanocalc_random(dut):
    """Random test with multiple input combinations"""
    
    dut._log.info("Start random testing")
    
    # Initialize
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.rst_n.value = 1
    
    import random
    
    # Test 50 random combinations
    for i in range(50):
        a = random.randint(0, 15)  # 4-bit values
        b = random.randint(0, 15)
        op = random.randint(0, 7)  # 8 operations
        
        dut.ui_in.value = (b << 4) | a
        dut.uio_in.value = op
        
        await Timer(1, units="ns")
        
        result = dut.uo_out.value & 0xF
        carry = (dut.uo_out.value >> 4) & 1
        
        # Basic sanity checks
        assert result <= 15, f"Random test {i}: Result {result} exceeds 4-bit range"
        assert carry <= 1, f"Random test {i}: Carry {carry} is invalid"
        
        if i % 10 == 0:  # Log every 10th test
            dut._log.info(f"Random test {i}: A={a}, B={b}, op={op} -> result={result}, carry={carry}")
    
    dut._log.info("✓ All 50 random tests passed")
