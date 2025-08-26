<!---
This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.
You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

# NanoCalc - 4-bit ALU

**NanoCalc** is a compact 4-bit Arithmetic Logic Unit (ALU) that performs eight essential digital operations. This educational project demonstrates fundamental computer architecture concepts including arithmetic operations, logical operations, and flag generation.

## How it works

NanoCalc implements a combinational logic circuit that takes two 4-bit operands (A and B) and performs one of eight operations based on a 3-bit control signal. The design uses a case statement in Verilog to select between operations and includes flag generation for carry/overflow and zero detection.

### Operation Table

| Control (uio[2:0]) | Operation | Description | Example |
|-------------------|-----------|-------------|---------|
| 000 | A + B | Addition with carry | 5 + 3 = 8, carry=0 |
| 001 | A - B | Subtraction with borrow | 5 - 3 = 2, carry=0 |
| 010 | A & B | Bitwise AND | 1100 & 1010 = 1000 |
| 011 | A \| B | Bitwise OR | 1100 \| 1010 = 1110 |
| 100 | A ^ B | Bitwise XOR | 1100 ^ 1010 = 0110 |
| 101 | ~A | Bitwise NOT of A | ~1100 = 0011 |
| 110 | A << 1 | Left shift A by 1 | 0110 << 1 = 1100, carry=0 |
| 111 | A == B | Equality check | Returns 0001 if equal, 0000 if not |

### Internal Architecture

The ALU consists of:
- **Input Decoders**: Parse the 4-bit operands from ui_in pins
- **Operation Selector**: 3-bit control logic using uio_in pins
- **Arithmetic Unit**: Handles addition and subtraction with carry propagation
- **Logic Unit**: Performs bitwise operations (AND, OR, XOR, NOT)
- **Shift Unit**: Implements left shift with carry output
- **Comparator**: Equality checking logic
- **Flag Generator**: Produces carry and zero flags

## How to test

### Basic Testing Procedure

1. **Set Operand A**: Use switches/inputs connected to ui_in[3:0] to set the first 4-bit number
2. **Set Operand B**: Use switches/inputs connected to ui_in[7:4] to set the second 4-bit number
3. **Select Operation**: Use switches/inputs connected to uio_in[2:0] to choose the operation
4. **Read Result**: Observe the 4-bit result on uo_out[3:0] (displayed on LEDs or 7-segment display)
5. **Check Flags**: Monitor uo_out[4] for carry flag and uo_out[5] for zero flag

### Test Cases

#### Addition Test (000)
- A = 0101 (5), B = 0011 (3) → Result = 1000 (8), Carry = 0
- A = 1111 (15), B = 0001 (1) → Result = 0000 (0), Carry = 1

#### Subtraction Test (001)  
- A = 1010 (10), B = 0110 (6) → Result = 0100 (4), Carry = 0
- A = 0011 (3), B = 0101 (5) → Result = 1110 (14), Carry = 1

#### Logic Tests (010-101)
- AND: 1100 & 1010 = 1000
- OR: 1100 | 0011 = 1111  
- XOR: 1010 ^ 0101 = 1111
- NOT: ~1010 = 0101

#### Shift Test (110)
- A = 0110 (6) → Result = 1100 (12), Carry = 0
- A = 1001 (9) → Result = 0010 (2), Carry = 1

#### Equality Test (111)
- A = 0101, B = 0101 → Result = 0001, Carry = 1
- A = 1010, B = 0101 → Result = 0000, Carry = 0

## External hardware

### Required Components

1. **Input Switches/DIP Switches**
   - 8-bit DIP switch for operands A and B (ui_in[7:0])
   - 3-bit DIP switch or toggle switches for operation selection (uio_in[2:0])

2. **Output Display**
   - **Option 1**: 4 LEDs to show binary result (uo_out[3:0])
   - **Option 2**: 7-segment display to show hexadecimal result (0-F)
   - 2 additional LEDs for carry flag (uo_out[4]) and zero flag (uo_out[5])

3. **Power Supply**
   - Standard TinyTapeout development board power (1.8V digital)

### Recommended Setup

