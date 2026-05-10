.. meta::
   :description: Overview of SystemVerilog enhancements over Verilog, including new data types, interfaces, and verification features.
   :keywords: SystemVerilog, SV vs Verilog, always_ff, always_comb, interfaces

SystemVerilog Overview
======================

**SystemVerilog** is a significant extension of the original Verilog HDL.
Standardized as **IEEE 1800**, it unifies design and verification into a single
language, providing more powerful constructs for RTL modeling and advanced
features for functional verification.

Most modern digital design projects use SystemVerilog features to improve
code density, reduce errors, and build robust verification environments.

-------------------------------
Key Design Enhancements
-------------------------------

SystemVerilog introduced several features that make RTL design safer and
more concise:

**The logic Type**

Replaces both ``wire`` and ``reg`` in most contexts. A ``logic`` signal can
be driven by a continuous assignment or a procedural block, eliminating the
confusion over which type to use.

.. code-block:: systemverilog

   logic [7:0] data;
   assign data = 8'hFF;      // Legal
   always_comb data = 8'h00; // Also legal (in separate modules)

**Specialized always Blocks**

SystemVerilog replaces the generic ``always`` block with intent-specific blocks:

- ``always_comb``: Explicitly for combinational logic. Tools check for latches.
- ``always_ff``: Explicitly for sequential (flip-flop) logic. Tools check for clock/reset usage.
- ``always_latch``: Explicitly for intentional latches.

.. code-block:: systemverilog

   always_ff @(posedge clk) begin
       q <= d;
   end

**User-Defined Types**

Support for ``typedef``, ``enum``, and ``struct`` allows for more readable and
type-safe code.

.. code-block:: systemverilog

   typedef enum logic [1:0] {IDLE, RUN, DONE} state_t;
   state_t current_state, next_state;

-------------------------------
Interfaces
-------------------------------

**Interfaces** are one of the most powerful features of SystemVerilog. They
bundle related signals into a single named port, reducing port-list clutter
and ensuring consistency across module boundaries.

.. code-block:: systemverilog

   interface bus_if;
       logic clk;
       logic [7:0] addr;
       logic [31:0] data;
       logic write;
   endinterface

   module master (bus_if b);
       always_ff @(posedge b.clk)
           b.addr <= 8'h01;
   endmodule

-------------------------------
Verification Features
-------------------------------

SystemVerilog includes a massive set of features designed for verification
engineers:

- **Classes**: Object-Oriented Programming (OOP) for testbench components.
- **Randomization**: ``rand`` variables and constraints for generating stimulus.
- **Functional Coverage**: ``covergroup`` and ``coverpoint`` to track what has been tested.
- **Assertions (SVA)**: ``assert property`` to formally verify timing and protocols.

-------------------------------
SystemVerilog vs. Verilog
-------------------------------

While Verilog is still used, SystemVerilog is now the industry standard for
most new designs.

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Feature
     - Verilog (2001)
     - SystemVerilog
   * - Primary Type
     - wire / reg
     - logic
   * - Blocks
     - always
     - always_comb, always_ff
   * - Complex Types
     - None
     - structs, enums, unions
   * - Interconnect
     - Manual port lists
     - Interfaces
   * - Verification
     - Basic tasks/functions
     - Classes, Assertions, Coverage

-------------------------------
Tool Support
-------------------------------

All major FPGA vendors (Xilinx/AMD, Intel, Lattice) and ASIC tools (Synopsys,
Cadence) have robust support for the SystemVerilog design subset. Use the
``.sv`` file extension to signal to your tools that they should use the
SystemVerilog parser.

.. seealso::

   - :doc:`package` — Using SystemVerilog packages.
   - :doc:`procedure` — Comparison with traditional Verilog blocks.
   - :doc:`testbench` — Building verification environments with SV features.

-------------------------------
External Tech Resources
-------------------------------

- **Technolati** — `Latest Technology News <https://www.technolati.com/>`_: Stay informed about the wider technological landscape and emerging industry trends.
