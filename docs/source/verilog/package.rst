.. meta::
   :description: How to use Verilog packages to share constants, types, and functions across multiple design modules.
   :keywords: Verilog package, constants, shared types, RTL architecture

Verilog Packages
================

Verilog packages provide a way to share data types, constants, tasks, and
functions across different modules. They are particularly useful for defining
system-wide parameters, shared state encodings, and common utility functions.

By grouping related declarations into a package, you improve code
maintainability and reduce the risk of naming conflicts.

-------------------------------
Defining a Package
-------------------------------

A package is defined using the ``package`` and ``endpackage`` keywords.
Inside, you can declare ``parameter``, ``localparam``, ``typedef`` (in SystemVerilog),
tasks, and functions.

.. code-block:: verilog

   package my_design_pkg;

       // Shared constants
       parameter WIDTH = 32;
       parameter ADDR_WIDTH = 8;

       // Shared state encoding
       parameter IDLE = 2'b00;
       parameter BUSY = 2'b01;
       parameter DONE = 2'b10;

       // Shared utility function
       function [WIDTH-1:0] reverse_bits (input [WIDTH-1:0] data);
           integer i;
           for (i = 0; i < WIDTH; i = i + 1)
               reverse_bits[WIDTH-1-i] = data[i];
       endfunction

   endpackage

-------------------------------
Importing a Package
-------------------------------

To use the contents of a package in a module, you must **import** it. There
are two main ways to import:

**Explicit Import**

Import specific items into the module scope. This is the safest method as it
avoids namespace pollution.

.. code-block:: verilog

   module my_module (
       input wire [my_design_pkg::ADDR_WIDTH-1:0] addr
   );
       import my_design_pkg::WIDTH;
       import my_design_pkg::reverse_bits;

       wire [WIDTH-1:0] result = reverse_bits(32'hAAAA_BBBB);
   endmodule

**Wildcard Import**

Import all items from the package. This is convenient but can lead to
conflicts if multiple packages have items with the same name.

.. code-block:: verilog

   module my_other_module (
       input wire clk
   );
       import my_design_pkg::*;

       reg [1:0] state;

       always @(posedge clk) begin
           if (state == IDLE)
               state <= BUSY;
       end
   endmodule

-------------------------------
Package Use Cases
-------------------------------

1. **Protocol Definitions**: Define command codes, error types, and packet
   header sizes in a single place.
2. **Fixed-Point Math**: Store shared bit-widths and scale factors for
   arithmetic modules.
3. **FSM Encodings**: Share state names between a design module and its
   corresponding testbench or monitor.
4. **Utility Libraries**: Group common mathematical or conversion functions
   (like Gray-to-binary) for reuse.

-------------------------------
Synthesis Considerations
-------------------------------

Most modern synthesis tools (Vivado, Quartus, etc.) fully support Verilog
packages. However, ensure that the package file is included in your project
and compiled **before** any modules that import it.

.. note::

   While packages were introduced as a part of SystemVerilog (IEEE 1800),
   they are widely used in modern "Verilog" design flows and are supported
   by nearly all current FPGA and ASIC tools.

.. seealso::

   - :doc:`datatype` — Data types commonly used within packages.
   - :doc:`systemverilog` — SystemVerilog extensions that expand package capabilities.
   - :doc:`niosread` — Using packages to define memory-mapped register maps.
