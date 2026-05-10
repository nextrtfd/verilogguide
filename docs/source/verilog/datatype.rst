.. meta::
   :description: Deep dive into Verilog data types including nets, variables, vectors, and 4-state logic for RTL design.
   :keywords: Verilog data types, wire vs reg, logic states, Verilog vectors

Verilog Data Types
==================

Verilog provides two fundamental categories of data types: **nets** and
**variables**. Choosing the correct type is essential for writing code that both
simulates correctly and synthesizes into the intended hardware.

Verilog uses a **4-state logic** system where every signal can hold one of four
values: ``0``, ``1``, ``X`` (unknown), or ``Z`` (high-impedance).

-----------------------
4-State Logic Values
-----------------------

.. list-table:: Logic States
   :header-rows: 1
   :widths: 15 85

   * - Value
     - Meaning
   * - ``0``
     - Logic low / false / ground
   * - ``1``
     - Logic high / true / VDD
   * - ``X``
     - Unknown — the simulator cannot determine the value (e.g., uninitialized reg)
   * - ``Z``
     - High-impedance — the signal is not driven (e.g., tri-state bus)

-----------------------
wire
-----------------------

A ``wire`` is a **net** type. It models a physical wire in a circuit.

- Must be driven continuously by an ``assign`` statement or a module output port.
- Cannot hold a value on its own.
- Default value is ``Z``.

.. code-block:: verilog

   wire  enable;            // 1-bit wire
   wire  [7:0] data_bus;    // 8-bit wire (vector)
   wire  [31:0] addr;       // 32-bit address bus

   assign enable = a & b;   // Continuously driven

-----------------------
reg
-----------------------

A ``reg`` is a **variable** type that holds a value across simulation time steps.

- Assigned inside ``initial`` or ``always`` procedural blocks.
- Despite the name, ``reg`` does **not** always infer a hardware flip-flop. A ``reg``
  assigned in a combinational ``always`` block synthesizes to combinational logic.
- Default value at the start of simulation is ``X``.

.. code-block:: verilog

   reg  q;            // Single-bit register
   reg  [3:0] count;  // 4-bit register (e.g., counter output)
   reg  [7:0] byte;   // 8-bit register

   always @(posedge clk) begin
       q <= d;        // Infers a D flip-flop
   end

-----------------------
Vectors
-----------------------

Both ``wire`` and ``reg`` can be declared as multi-bit vectors using the
``[MSB:LSB]`` notation.

.. code-block:: verilog

   wire [7:0]  data;    // 8-bit vector, MSB is bit 7
   reg  [15:0] result;  // 16-bit vector

   // Bit-select
   wire msb = data[7];

   // Part-select
   wire [3:0] nibble = data[7:4];

By convention, Verilog vectors are declared ``[n-1:0]`` (e.g., ``[7:0]`` for a
byte), making index 0 the least significant bit.

-----------------------
integer
-----------------------

``integer`` is a signed 32-bit variable, primarily used in simulation for loop
counters and general arithmetic. It is **not** recommended for synthesizable RTL.

.. code-block:: verilog

   integer i;

   initial begin
       for (i = 0; i < 16; i = i + 1) begin
           $display("i = %0d", i);
       end
   end

-----------------------
parameter and localparam
-----------------------

Parameters allow you to write reusable, configurable modules.

- ``parameter`` — A compile-time constant that can be overridden when the module
  is instantiated.
- ``localparam`` — A local constant that cannot be overridden from outside. Use it
  for internal constants like state encodings.

.. code-block:: verilog

   module adder #(
       parameter WIDTH = 8
   ) (
       input  wire [WIDTH-1:0] a,
       input  wire [WIDTH-1:0] b,
       output wire [WIDTH:0]   sum
   );
       assign sum = a + b;
   endmodule

   // Instantiate with a different width
   adder #(.WIDTH(16)) u_adder (.a(x), .b(y), .sum(s));

.. code-block:: verilog

   // Internal constants
   localparam IDLE = 2'b00;
   localparam RUN  = 2'b01;
   localparam DONE = 2'b10;

-----------------------
Arrays and Memories
-----------------------

Verilog supports arrays of ``reg`` to model memories.

.. code-block:: verilog

   reg [7:0]  memory [0:255];   // 256 x 8-bit memory (RAM model)
   reg [31:0] rom    [0:15];    // 16 x 32-bit ROM

   // Write
   memory[0] = 8'hAB;

   // Read
   wire [7:0] data_out = memory[addr];

-----------------------
Complete Data Type Example
-----------------------

The following module demonstrates all major data types together:

.. code-block:: verilog

   module data_type_example;

       wire        single_bit_wire;
       reg         single_bit_reg;

       wire [7:0]  data_bus;
       reg  [3:0]  counter;

       parameter   WIDTH = 8;
       localparam  IDLE  = 2'b00;

       reg  [7:0]  memory [0:15];

   endmodule

-----------------------
Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - Type
     - Category
     - Key Rule
   * - ``wire``
     - Net
     - Driven by ``assign`` or module output; cannot be assigned in ``always``
   * - ``reg``
     - Variable
     - Assigned in ``initial`` or ``always``; does not always mean flip-flop
   * - ``integer``
     - Variable
     - Use for simulation loops only
   * - ``parameter``
     - Constant
     - Module-level, overridable at instantiation
   * - ``localparam``
     - Constant
     - Module-level, NOT overridable

-----------------------
See Also
-----------------------

- :doc:`procedure` — How ``wire`` and ``reg`` behave inside procedural blocks.
- :doc:`designs` — Examples of combinational and sequential designs using these types.
