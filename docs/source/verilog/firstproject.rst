.. meta::
   :description: Learn how to create your first Verilog project, from writing code to FPGA simulation and programming.
   :keywords: Verilog tutorial, FPGA project, LED blinker, Verilog simulation

First Verilog Project
=====================

This guide walks you through creating your first complete Verilog project, from
writing RTL code to running simulation and programming an FPGA board. The example
project is an **LED Blinker** — a counter that toggles an output LED at a
human-visible rate, driven by the FPGA's onboard clock.

-----------------------
Project Goal
-----------------------

Build a hardware module that:

1. Takes a clock and asynchronous reset as inputs.
2. Uses a 24-bit counter to divide the clock frequency.
3. Toggles an LED output every time the counter wraps around.

This demonstrates the core Verilog workflow: describing registers, combinational
logic, and a synchronous process inside an ``always`` block.

-----------------------
Required Tools
-----------------------

You can complete this project with any of the following toolchains:

- **Icarus Verilog** (free, open-source simulator) — recommended for beginners.
- **ModelSim / Questa** — industry-standard simulator from Siemens EDA.
- **Vivado** — Xilinx FPGA synthesis and implementation tool.
- **Quartus Prime** — Intel FPGA design suite.

For simulation only, install Icarus Verilog:

.. code-block:: bash

   # Linux / macOS
   sudo apt install iverilog   # Debian/Ubuntu
   brew install icarus-verilog # macOS

   # Windows: download installer from http://iverilog.icarus.com/

-----------------------
Create the Source File
-----------------------

Create a directory for your project and add a file named ``led_blinker.v``.

.. code-block:: bash

   mkdir blinker_project
   cd blinker_project
   touch led_blinker.v

-----------------------
Write the Verilog Module
-----------------------

Open ``led_blinker.v`` and enter the following code:

.. code-block:: verilog

   module led_blinker (
       input  wire clk,
       input  wire reset,
       output reg  led
   );

       reg [23:0] counter;

       always @(posedge clk or posedge reset) begin
           if (reset) begin
               counter <= 24'd0;
               led     <= 1'b0;
           end else begin
               counter <= counter + 1'b1;

               if (counter == 24'd0)
                   led <= ~led;
           end
       end

   endmodule

**How it works:**

- The ``always`` block triggers on the rising edge of ``clk`` or when ``reset`` goes
  high.
- On reset, both ``counter`` and ``led`` are cleared to zero.
- On every clock edge, the 24-bit counter increments.
- When ``counter`` overflows back to zero (after 16,777,216 cycles), the ``led``
  output is toggled.
- At a 50 MHz clock, the LED toggles approximately every 335 ms — clearly visible.

-----------------------
Create a Testbench
-----------------------

Create ``tb_led_blinker.v`` to simulate the design:

.. code-block:: verilog

   `timescale 1ns / 1ps

   module tb_led_blinker;

       reg  clk;
       reg  reset;
       wire led;

       led_blinker dut (
           .clk   (clk),
           .reset (reset),
           .led   (led)
       );

       // 10 ns clock period (100 MHz for fast simulation)
       initial clk = 0;
       always #5 clk = ~clk;

       initial begin
           $dumpfile("led_blinker.vcd");
           $dumpvars(0, tb_led_blinker);

           // Apply reset
           reset = 1;
           #20;
           reset = 0;

           // Run for enough cycles to see multiple toggles
           // (reduce counter width for simulation speed)
           #5000;
           $finish;
       end

   endmodule

-----------------------
Run Simulation
-----------------------

Compile and simulate using Icarus Verilog:

.. code-block:: bash

   iverilog -o sim_out led_blinker.v tb_led_blinker.v
   vvp sim_out

Open the waveform dump with GTKWave to inspect signal behavior:

.. code-block:: bash

   gtkwave led_blinker.vcd &

-----------------------
Synthesize and Program the FPGA
-----------------------

To target an FPGA board (e.g., Intel DE10-Lite or Xilinx Basys 3):

1. Create a new project in Quartus Prime or Vivado.
2. Add ``led_blinker.v`` as the top-level source file.
3. Create a pin constraints file mapping ``clk``, ``reset``, and ``led`` to physical
   board pins.
4. Run synthesis and implementation.
5. Generate the bitstream and program the FPGA.

Consult your board's user guide for the exact pin assignments.

-----------------------
Next Steps
-----------------------

Now that you have a working first project, continue learning:

- :doc:`datatype` — Understand the ``wire``, ``reg``, and vector types used here.
- :doc:`procedure` — Learn more about ``always`` blocks and blocking vs non-blocking.
- :doc:`testbench` — Build more advanced testbenches with self-checking logic.

-----------------------
Recommended Reading
-----------------------

- For broader technology insights and updates, visit **Technolati** at `Technolati.com <https://www.technolati.com/>`_.
