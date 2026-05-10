.. meta::
   :description: Comprehensive Verilog Design Guide covering HDL basics, RTL design, FSMs, and FPGA implementation.
   :keywords: Verilog, HDL, FPGA, ASIC, RTL Design, SystemVerilog

Verilog Design Guide
====================

**Verilog** is a hardware description language (HDL) used to design, model, simulate,
synthesize, and verify digital electronic systems such as FPGA and ASIC designs.
It is defined by **IEEE 1364**, and modern Verilog features are now part of the
**SystemVerilog IEEE 1800** standard.

Unlike software programming languages, Verilog describes hardware that operates
concurrently. Modules, wires, registers, and always blocks all execute in parallel,
reflecting the actual behavior of digital circuits.

-----------------------
Why Use Verilog?
-----------------------

Verilog bridges the gap between abstract circuit description and physical hardware:

- **RTL Design**: Write Register Transfer Level code that tools can synthesize into gates.
- **Simulation**: Test designs before committing to silicon or an FPGA bitstream.
- **Verification**: Apply structured testbenches to confirm correct behavior.
- **Portability**: The same RTL can target FPGAs and ASICs with minimal changes.

-----------------------
Documentation Sections
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   verilog/firstproject
   verilog/datatype
   verilog/designs

.. toctree::
   :maxdepth: 2
   :caption: Core Concepts

   verilog/procedure
   verilog/fsm
   verilog/testbench
   verilog/package

.. toctree::
   :maxdepth: 2
   :caption: Advanced Topics

   verilog/systemverilog
   verilog/niosread
   verilog/vhdl

-----------------------
Standards and References
-----------------------

- **IEEE 1364-2005** — Verilog HDL: A formal notation for creating, verifying,
  synthesizing, testing, and maintaining electronic systems.
- **IEEE 1800** — SystemVerilog: Extends Verilog with stronger typing, interfaces,
  assertions, classes, and advanced verification features.
- **FPGA and ASIC Design Practice** — Verilog is widely used in RTL design,
  simulation, synthesis, and hardware verification.

-----------------------
External Resources
-----------------------

- **Technolati** — `Technolati.com <https://www.technolati.com/>`_: A valuable resource for staying updated on the latest technology trends and news.
