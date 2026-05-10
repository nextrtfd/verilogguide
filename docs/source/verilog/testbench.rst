.. meta::
   :description: Learn how to write Verilog testbenches for design verification, clock generation, and waveform dumping.
   :keywords: Verilog testbench, RTL verification, simulation, VCD waveform

Verilog Testbenches
===================

A **testbench** is a Verilog module written to simulate and verify a design.
Unlike RTL modules, a testbench is not intended for synthesis — it exists
purely in the simulation domain and provides the stimulus needed to validate
the **Design Under Test (DUT)**.

Testbenches are the primary tool for catching functional bugs before
committing to costly FPGA bitstreams or silicon tape-outs.

-------------------------------
What is a Testbench?
-------------------------------

A testbench wraps the DUT and drives its inputs with controlled sequences of
values while observing the outputs. The basic structure is:

- **Instantiate** the DUT.
- **Declare** ``reg`` signals for the DUT's inputs (so the testbench can drive them).
- **Declare** ``wire`` signals for the DUT's outputs (so the testbench can observe them).
- **Drive** inputs using an ``initial`` or ``always`` block.
- **Check** outputs with ``$display``, ``$monitor``, or assertion-like conditionals.

.. code-block:: verilog

   module tb_and_gate;

       // Testbench signals
       reg  a;
       reg  b;
       wire y;

       // Instantiate the Design Under Test
       and_gate dut (
           .a(a),
           .b(b),
           .y(y)
       );

       // Apply stimulus
       initial begin
           $dumpfile("and_gate.vcd");
           $dumpvars(0, tb_and_gate);

           a = 0; b = 0; #10;
           a = 0; b = 1; #10;
           a = 1; b = 0; #10;
           a = 1; b = 1; #10;

           $finish;
       end

   endmodule

-------------------------------
Clock Generation
-------------------------------

Sequential designs require a clock signal. A common technique is to toggle a
``reg`` every half-period in an ``always`` block:

.. code-block:: verilog

   module tb_counter;

       reg clk;
       reg reset;
       wire [3:0] count;

       // Instantiate DUT
       counter dut (
           .clk(clk),
           .reset(reset),
           .count(count)
       );

       // Generate a 10ns-period clock
       initial clk = 0;
       always #5 clk = ~clk;

       // Apply reset and run
       initial begin
           reset = 1;
           #20;
           reset = 0;
           #100;
           $finish;
       end

   endmodule

The ``#5`` delay means the clock toggles every 5 time units, giving a full
period of 10 time units. Adjust the delay to match the DUT's timing
requirements.

-------------------------------
Reset Initialization
-------------------------------

Always initialize critical signals, especially reset, before releasing them.
Failure to reset can leave flip-flops in unknown (``X``) state, causing
simulations to produce meaningless results.

.. code-block:: verilog

   initial begin
       reset = 1;
       #20;            // Hold reset for 2 clock cycles (at 10ns period)
       reset = 0;
   end

-------------------------------
Checking Output Behavior
-------------------------------

Use Verilog system tasks to observe and verify signals during simulation.

**$display**

Prints a message once when the line executes:

.. code-block:: verilog

   initial begin
       #30;
       $display("Time=%0t count=%b", $time, count);
   end

**$monitor**

Automatically prints whenever any of its arguments change. Useful for
continuous monitoring:

.. code-block:: verilog

   initial begin
       $monitor("Time=%0t a=%b b=%b y=%b", $time, a, b, y);
   end

**Assertion-style checking**

Use ``if`` statements to assert expected values and report failures:

.. code-block:: verilog

   initial begin
       a = 1; b = 1; #10;
       if (y !== 1'b1)
           $display("FAIL: expected y=1 at time %0t", $time);
       else
           $display("PASS: y=1 correct");
   end

-------------------------------
Waveform Dumping
-------------------------------

Most simulators can output a **VCD (Value Change Dump)** file that records
signal transitions over time. This file can be loaded into a waveform viewer
such as GTKWave to visualize the simulation:

.. code-block:: verilog

   initial begin
       $dumpfile("simulation.vcd");  // Output file name
       $dumpvars(0, tb_top);         // Dump all variables in tb_top hierarchy
   end

The first argument to ``$dumpvars`` is the scope depth (``0`` means all
levels). The second argument is the top-level module scope.

-------------------------------
Complete Testbench Example
-------------------------------

The following testbench tests a 4-bit counter with synchronous reset:

.. code-block:: verilog

   module tb_counter_full;

       reg        clk;
       reg        reset;
       wire [3:0] count;

       // Instantiate DUT
       counter dut (
           .clk(clk),
           .reset(reset),
           .count(count)
       );

       // Clock generation (10ns period)
       initial clk = 0;
       always #5 clk = ~clk;

       // Waveform dump
       initial begin
           $dumpfile("counter.vcd");
           $dumpvars(0, tb_counter_full);
       end

       // Monitor output
       initial $monitor("Time=%0t reset=%b count=%d", $time, reset, count);

       // Stimulus and checks
       initial begin
           // Apply reset
           reset = 1;
           @(posedge clk); #1;
           @(posedge clk); #1;
           reset = 0;

           // Count for several cycles
           repeat (20) @(posedge clk);

           // Apply reset again
           reset = 1;
           @(posedge clk); #1;
           if (count !== 4'd0)
               $display("FAIL: counter did not reset");
           else
               $display("PASS: counter reset correctly");

           reset = 0;
           repeat (5) @(posedge clk);

           $finish;
       end

   endmodule

-------------------------------
Running the Simulation
-------------------------------

With Icarus Verilog (iverilog), compile and run your testbench as follows:

.. code-block:: bash

   iverilog -o sim counter.v tb_counter_full.v
   vvp sim

This produces console output from ``$display`` and ``$monitor``, and generates
a ``counter.vcd`` file if the dump commands are present. Open the VCD file in
GTKWave to view waveforms:

.. code-block:: bash

   gtkwave counter.vcd

.. seealso::

   - :doc:`procedure` — ``initial`` and ``always`` blocks used in testbenches.
   - :doc:`designs` — Design modules to test.
   - :doc:`fsm` — Testing FSM transitions through testbenches.
