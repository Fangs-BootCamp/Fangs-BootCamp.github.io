`timescale 1ns / 1ps

module SevSegDriver(
    input clk,
    input rst,
    input [7:0] byte0,
    input [7:0] byte1,
    output reg[6:0] seg,
    output reg[3:0] an
    );

reg slowRst;
reg rstClear;
wire sclk;

wire [3:0] disp0 = byte0[3:0];
wire [3:0] disp1 = byte0[7:4];
wire [3:0] disp2 = byte1[3:0];
wire [3:0] disp3 = byte1[7:4];
reg [3:0] currDisp;

//slwclk
reg [16:0] q;
    //positive-edge triggered, synchronous reset flip flop
    always @(posedge clk)
   begin
        if (rst)  q <= 16'h0;
        else      q <= q + 1;
    end
assign sclk = q[16]; //slow for simulation

//catch the high-speed reset, 
// generate a  slow-speed reset
// hold until cleared
always@(posedge clk) begin
    if (rst) 
        slowRst <= 1'h1;
    else if (rstClear)
        slowRst <= 1'h0;
end

always@(posedge sclk) begin
    if (slowRst) begin
        an <=  4'b1110;
        rstClear = 1'h1;
    end else  begin
        an <= {an[2:0],an[3]};
        rstClear = 1'h0;
    end
end
    
        
always @(*) begin
    currDisp = disp0; //default
    seg = 7'b1111111; //default

    case(an)
      4'b1110: 
          currDisp=disp0;
      4'b1101:
          currDisp=disp1;
      4'b1011:
          currDisp=disp2;
      4'b0111:
          currDisp=disp3;
    endcase

    case(currDisp)
        4'b0000: seg = 7'b1000000; // "0"  
        4'b0001: seg = 7'b1111001; // "1" 
        4'b0010: seg = 7'b0100100; // "2" 
        4'b0011: seg = 7'b0110000; // "3" 
        4'b0100: seg = 7'b0011001; // "4" 
        4'b0101: seg = 7'b0010010; // "5" 
        4'b0110: seg = 7'b0000010; // "6" 
        4'b0111: seg = 7'b1111000; // "7" 
        4'b1000: seg = 7'b0000000; // "8"  
        4'b1001: seg = 7'b0010000; // "9" 
        4'b1010: seg = 7'b0001000; // "A"
        4'b1011: seg = 7'b0000011; // "b"
        4'b1100: seg = 7'b0100111; // "c"
        4'b1101: seg = 7'b0100001; // "d"
        4'b1110: seg = 7'b0000110; // "E"
        4'b1111: seg = 7'b0001110;
        default:  seg = 7'b1111111;
    endcase
      
end


endmodule
