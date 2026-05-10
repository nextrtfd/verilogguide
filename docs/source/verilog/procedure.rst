.. meta::
   :description: Understanding procedural blocks in Verilog, including initial and always blocks, and blocking vs non-blocking assignments.
   :keywords: Verilog procedure, always block, blocking vs non-blocking, RTL behavior

Procedural Blocks in Verilog
=============================

Procedural blocks are the primary mechanism for describing behavior in Verilog.
They contain sequential statements that execute in order, unlike continuous
assignments which are always active.

Verilog has two procedural block types: ``initial`` and ``always``.

-----------------------
initial Block
-----------------------

An ``initial`` block executes **once** at simulation time zero and then terminates.
It is used in testbenches to set up initial conditions and apply stimulus. Initial
blocks are **not synthesizable** and should not appear in RTL design files.

.. code-block:: verilog

   module tb_example;

       reg a;
       reg b;

       initial begin
           a = 0;
           b = 0;
           #10 a = 1;
           #10 b = 1;
           #10 $finish;
       end

   endmodule

Multiple ``initial`` blocks can coexist in a module; they all start at time zero
and execute concurrently.

-----------------------
always Block
-----------------------

An ``always`` block executes **repeatedly** whenever its sensitivity list is
triggered. If there is no sensitivity list, it runs forever (useful for clock
generation in testbenches, not in RTL).

.. code-block:: verilog

   // Clock generator (testbench only)
   reg clk = 0;
   always #5 clk = ~clk;  // Toggle every 5 ns → 10 ns period

-----------------------
Sensitivity Lists
-----------------------

The sensitivity list after ``@`` specifies what triggers the ``always`` block.

**Edge-sensitive** — triggers on a signal transition:

.. code-block:: verilog

   always @(posedge clk)           // Rising edge of clk
   always @(negedge clk)           // Falling edge of clk
   always @(posedge clk or posedge reset)  // Either event

**Level-sensitive (combinational)** — triggers when any listed signal changes:

.. code-block:: verilog

   always @(a or b or sel)   // Explicit list
   always @(*)               // Implicit: all signals read in the block

Using ``@(*)`` for combinational logic is strongly preferred — it is less
error-prone because you cannot accidentally omit a signal.

-----------------------
Blocking Assignment (=)
-----------------------

A blocking assignment executes immediately and **blocks** the next statement
until it completes. Statements execute one after another, like software.

.. code-block:: verilog

   always @(*) begin
       temp = a & b;   // Executes first
       y    = temp | c; // Executes after temp is updated
   end

Use blocking assignments in **combinational** logic blocks.

.. warning::
   Using blocking assignments inside a clocked ``always`` block can cause
   simulation mismatches with synthesized hardware. Avoid this pattern.

-----------------------
Non-Blocking Assignment (<=)
-----------------------

A non-blocking assignment **schedules** an update to happen at the end of the
current time step. All right-hand sides are evaluated first, then all left-hand
sides are updated simultaneously.

.. code-block:: verilog

   always @(posedge clk) begin
       a <= b;   // Both right-hand sides evaluated first
       b <= a;   // Then both left-hand sides updated → swap without temp
   end

Use non-blocking assignments in **clocked (sequential)** logic blocks.

-----------------------
Combinational Logic with always
-----------------------

An ``always @(*)`` block models combinational logic when every output is assigned
under every possible condition (no latches inferred).

.. code-block:: verilog

   reg y;

   always @(*) begin
       case (sel)
           2'b00: y = d0;
           2'b01: y = d1;
           2'b10: y = d2;
           2'b11: y = d3;
           default: y = 1'bx;
       endcase
   end

.. warning::
   If a signal is not assigned in all branches of an ``always @(*)`` block, the
   synthesizer infers a **latch**. Always include a ``default`` case or assign
   default values at the top of the block.

-----------------------
Sequential Logic with always
-----------------------

A clocked ``always`` block captures state — it synthesizes to flip-flops.

.. code-block:: verilog

   module d_flip_flop (
       input  wire clk,
       input  wire reset,
       input  wire d,
       output reg  q
   );
       always @(posedge clk or posedge reset) begin
           if (reset)
               q <= 1'b0;
           else
               q <= d;
       end
   endmodule

The structure above is the standard pattern for an asynchronous active-high
reset D flip-flop.

-----------------------
Assignment Rule Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Context
     - Use
     - Reason
   * - Combinational ``always @(*)``
     - Blocking ``=``
     - Executes sequentially like software logic
   * - Clocked ``always @(posedge clk)``
     - Non-blocking ``<=``
     - Models flip-flop sampling correctly
   * - Testbench ``initial``
     - Either (blocking is common)
     - Simulation only; no synthesis concern

-----------------------
See Also
-----------------------

- :doc:`datatype` — ``wire`` and ``reg`` type rules.
- :doc:`fsm` — Applying procedural blocks to state machine design.
- :doc:`testbench` — Using ``initial`` and ``always`` in simulation.
