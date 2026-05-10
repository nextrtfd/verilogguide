.. meta::
   :description: Common Verilog design examples including combinational logic, counters, and parameterized modules.
   :keywords: Verilog examples, multiplexer, counter, RTL patterns

Common Verilog Design Examples
==============================

This section presents common Verilog building blocks that appear frequently in
RTL design. These examples demonstrate both **combinational** and **sequential**
logic patterns, as well as **parameterized** modules for reuse.

-----------------------
Combinational Logic
-----------------------

Combinational logic produces outputs that depend only on the current inputs —
there is no state or memory. In Verilog, combinational logic is modeled with
``assign`` statements or ``always @(*)`` blocks.

AND Gate
~~~~~~~~

.. code-block:: verilog

   module and_gate (
       input  wire a,
       input  wire b,
       output wire y
   );
       assign y = a & b;
   endmodule

2-to-1 Multiplexer
~~~~~~~~~~~~~~~~~~

A multiplexer selects between two inputs based on a select signal.

.. code-block:: verilog

   module mux2 (
       input  wire a,
       input  wire b,
       input  wire sel,
       output wire y
   );
       assign y = sel ? b : a;
   endmodule

4-to-1 Multiplexer
~~~~~~~~~~~~~~~~~~

.. code-block:: verilog

   module mux4 (
       input  wire [3:0] d,
       input  wire [1:0] sel,
       output reg        y
   );
       always @(*) begin
           case (sel)
               2'b00: y = d[0];
               2'b01: y = d[1];
               2'b10: y = d[2];
               2'b11: y = d[3];
               default: y = 1'bx;
           endcase
       end
   endmodule

Half Adder
~~~~~~~~~~

.. code-block:: verilog

   module half_adder (
       input  wire a,
       input  wire b,
       output wire sum,
       output wire carry
   );
       assign sum   = a ^ b;
       assign carry = a & b;
   endmodule

Full Adder
~~~~~~~~~~

.. code-block:: verilog

   module full_adder (
       input  wire a,
       input  wire b,
       input  wire cin,
       output wire sum,
       output wire cout
   );
       assign {cout, sum} = a + b + cin;
   endmodule

-----------------------
Sequential Logic
-----------------------

Sequential logic produces outputs that depend on current inputs **and** past
state. Sequential elements are clocked; use non-blocking assignments (``<=``)
inside clocked ``always`` blocks.

D Flip-Flop
~~~~~~~~~~~

.. code-block:: verilog

   module d_ff (
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

4-bit Counter
~~~~~~~~~~~~~

.. code-block:: verilog

   module counter (
       input  wire       clk,
       input  wire       reset,
       output reg [3:0]  count
   );
       always @(posedge clk or posedge reset) begin
           if (reset)
               count <= 4'd0;
           else
               count <= count + 1'b1;
       end
   endmodule

4-bit Shift Register
~~~~~~~~~~~~~~~~~~~~

.. code-block:: verilog

   module shift_register (
       input  wire       clk,
       input  wire       reset,
       input  wire       d,
       output reg [3:0]  q
   );
       always @(posedge clk or posedge reset) begin
           if (reset)
               q <= 4'b0000;
           else
               q <= {q[2:0], d};  // Shift left, insert d at LSB
       end
   endmodule

-----------------------
Parameterized Modules
-----------------------

Parameterized modules can be customized at instantiation time, avoiding
code duplication.

N-bit Counter
~~~~~~~~~~~~~

.. code-block:: verilog

   module counter_n #(
       parameter N = 8
   ) (
       input  wire       clk,
       input  wire       reset,
       output reg [N-1:0] count
   );
       always @(posedge clk or posedge reset) begin
           if (reset)
               count <= {N{1'b0}};
           else
               count <= count + 1'b1;
       end
   endmodule

   // Instantiate as 16-bit counter
   counter_n #(.N(16)) u_cnt (.clk(clk), .reset(rst), .count(cnt));

N-bit Adder
~~~~~~~~~~~

.. code-block:: verilog

   module adder_n #(
       parameter N = 8
   ) (
       input  wire [N-1:0] a,
       input  wire [N-1:0] b,
       input  wire         cin,
       output wire [N-1:0] sum,
       output wire         cout
   );
       assign {cout, sum} = a + b + cin;
   endmodule

-----------------------
Synthesis-Friendly Style
-----------------------

Follow these coding guidelines for reliable synthesis results:

- Use **non-blocking** ``<=`` in clocked ``always`` blocks (sequential).
- Use **blocking** ``=`` in combinational ``always @(*)`` blocks.
- Always include a ``default`` case in ``case`` statements.
- Do not use ``#delay`` in synthesizable code — delays are simulation-only.
- Declare all outputs of combinational blocks in the sensitivity list (use ``@(*)``).

.. code-block:: verilog

   // BAD: incomplete sensitivity list (may not synthesize correctly)
   always @(a) begin
       y = a & b;   // b is missing from sensitivity list
   end

   // GOOD: use @(*) for combinational logic
   always @(*) begin
       y = a & b;
   end

-----------------------
See Also
-----------------------

- :doc:`datatype` — Data types used in these examples.
- :doc:`procedure` — How ``initial`` and ``always`` blocks work.
- :doc:`fsm` — State machine design as an advanced sequential pattern.
