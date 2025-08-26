/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_nanocalc (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // Input assignments
    wire [3:0] A = ui_in[3:0];      // First 4-bit operand
    wire [3:0] B = ui_in[7:4];      // Second 4-bit operand
    wire [2:0] operation = uio_in[2:0];  // 3-bit operation selector
    
    // ALU result and flags
    reg [3:0] result;
    reg carry_flag;
    reg zero_flag;
    
    // ALU Logic - Combinational
    always @(*) begin
        carry_flag = 1'b0;  // Default no carry
        zero_flag = 1'b0;   // Default not zero
        
        case (operation)
            3'b000: begin  // Addition
                {carry_flag, result} = A + B;
            end
            
            3'b001: begin  // Subtraction  
                {carry_flag, result} = A - B;
            end
            
            3'b010: begin  // Bitwise AND
                result = A & B;
                carry_flag = 1'b0;
            end
            
            3'b011: begin  // Bitwise OR
                result = A | B;
                carry_flag = 1'b0;
            end
            
            3'b100: begin  // Bitwise XOR
                result = A ^ B;
                carry_flag = 1'b0;
            end
            
            3'b101: begin  // Bitwise NOT A
                result = ~A;
                carry_flag = 1'b0;
            end
            
            3'b110: begin  // Left Shift A by 1
                {carry_flag, result} = {A, 1'b0};
            end
            
            3'b111: begin  // Equality Check (A == B)
                result = (A == B) ? 4'b0001 : 4'b0000;
                carry_flag = (A == B) ? 1'b1 : 1'b0;
            end
            
            default: begin
                result = 4'b0000;
                carry_flag = 1'b0;
            end
        endcase
        
        // Set zero flag if result is zero
        zero_flag = (result == 4'b0000) ? 1'b1 : 1'b0;
    end
    
    // Output assignments
    assign uo_out[3:0] = result;        // 4-bit ALU result
    assign uo_out[4] = carry_flag;      // Carry/overflow flag
    assign uo_out[5] = zero_flag;       // Zero flag
    assign uo_out[7:6] = 2'b00;         // Unused outputs
    
    // Bidirectional pins - not used, set as inputs
    assign uio_out = 8'b0;
    assign uio_oe = 8'b0;
    
    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, uio_in[7:3], 1'b0};

endmodule
