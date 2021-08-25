// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.2 (lin64) Build 2258646 Thu Jun 14 20:02:38 MDT 2018
// Date        : Fri Apr  5 11:23:34 2019
// Host        : hognose.sice.indiana.edu running 64-bit Red Hat Enterprise Linux Workstation release 7.6 (Maipo)
// Command     : write_verilog -mode synth_stub uart_stub.v
// Design      : uart
// Purpose     : Stub declaration of top-level module interface
// Device      : xc7a35ticpg236-1L
// --------------------------------------------------------------------------------

// This empty module with port declaration file causes synthesis tools to infer a black box for IP.
// The synthesis directives are for Synopsys Synplify support to prevent IO buffer insertion.
// Please paste the declaration into a Verilog source file or add the file as an additional source.
module uart(clk, rst, uart_rx_in, uart_tx_out, tx_data, tx_req, 
  tx_empty, tx_err, rx_data, rx_ready)
/* synthesis syn_black_box black_box_pad_pin="clk,rst,uart_rx_in,uart_tx_out,tx_data[7:0],tx_req,tx_empty,tx_err,rx_data[7:0],rx_ready" */;
  input clk;
  input rst;
  input uart_rx_in;
  output uart_tx_out;
  input [7:0]tx_data;
  input tx_req;
  output tx_empty;
  output tx_err;
  output [7:0]rx_data;
  output rx_ready;
endmodule
