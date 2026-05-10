.. meta::
   :description: Integrating custom Verilog peripherals with the Nios II soft processor via the Avalon Memory-Mapped interface.
   :keywords: Nios II, Avalon bus, Intel FPGA, soft processor, memory-mapped I/O

Nios II and Verilog
====================

The **Nios II** is a soft-core processor developed by Intel (formerly Altera)
for use within their FPGA devices. Unlike a hard-core processor, a soft
processor is implemented using the FPGA's programmable logic resources —
LUTs, registers, and block RAM — rather than being etched into dedicated
silicon.

This section explains how Nios II works, how it connects to custom Verilog
hardware, and the tools and workflow used to build Nios II-based systems.

-------------------------------
What is a Soft Processor?
-------------------------------

A **soft processor** is a processor design described in HDL that can be
implemented in any programmable logic device. The same processor that runs
in a Cyclone IV FPGA can be regenerated for an Arria 10 or a Stratix 10 by
recompiling the RTL.

Key characteristics of soft processors:

- **Flexible** — Peripherals, bus widths, and cache sizes are all configurable.
- **Customizable** — Custom instructions and hardware accelerators can be added.
- **Resource-intensive** — They consume FPGA logic and memory resources.
- **Slower** — Typically run at tens to hundreds of MHz, not the GHz range of hard cores.

**Nios II** was the primary Intel FPGA soft processor and supports a full
embedded software stack including Embedded Design Suite (EDS), C/C++
toolchain, and RTOS support.

.. note::

   Intel has introduced the **Nios V** processor as the modern successor to
   Nios II, based on the RISC-V ISA. Nios II remains widely documented and
   used in legacy systems.

-------------------------------
Processor System Architecture
-------------------------------

A Nios II system is not a standalone module — it is a **system-on-chip (SoC)**
built using **Platform Designer** (formerly Qsys). The typical system
includes:

- **Nios II/e, /f, or /s core** — Economy, Fast, or Standard variants.
- **On-chip memory** — Tightly coupled block RAM for instruction and data.
- **JTAG UART** — Serial communication for debugging.
- **Timer** — Periodic interrupt source.
- **GPIO** — General-purpose I/O mapped to FPGA pins.
- **Custom Verilog peripherals** — User-defined hardware connected via the Avalon bus.

.. code-block:: text

   +-------------------------------+
   |         Nios II Core          |
   +-------------------------------+
              |  Avalon-MM Master
   +----------+----------+---------+
   |          |          |         |
   On-Chip  Timer     JTAG UART  Custom
   Memory                        Verilog
                                 Peripheral

-------------------------------
The Avalon Memory-Mapped Interface
-------------------------------

Custom Verilog modules connect to the Nios II processor through the
**Avalon Memory-Mapped (Avalon-MM)** bus. This is a simple master/slave
interface where:

- The **Nios II core** is the master.
- **Peripherals** (including custom Verilog modules) are slaves.
- Each peripheral occupies a region of the **processor's address space**.

A minimal Avalon-MM slave peripheral responds to read and write transactions
from the processor:

.. code-block:: verilog

   module my_led_peripheral (
       // Avalon-MM slave interface
       input  wire        clk,
       input  wire        reset,
       input  wire        chipselect,
       input  wire        write,
       input  wire        read,
       input  wire [31:0] writedata,
       output reg  [31:0] readdata,

       // Hardware output
       output reg  [7:0]  leds
   );

       // Write: processor stores a value into this peripheral
       always @(posedge clk or posedge reset) begin
           if (reset)
               leds <= 8'h00;
           else if (chipselect && write)
               leds <= writedata[7:0];
       end

       // Read: processor loads a value from this peripheral
       always @(posedge clk) begin
           if (chipselect && read)
               readdata <= {24'b0, leds};
       end

   endmodule

-------------------------------
Connecting Custom Verilog Logic
-------------------------------

To integrate a custom Verilog module into a Nios II system:

1. **Describe the module** as an Avalon-MM slave (or other Avalon interface).
2. **Register it in Platform Designer** by adding it as a custom component.
3. **Connect it to the bus** in Platform Designer and assign it an address range.
4. **Export external signals** (e.g., ``leds``) through the top-level wrapper
   to FPGA I/O pins.

The Platform Designer tool generates the interconnect logic that connects all
components, leaving you to focus on the custom hardware behavior.

-------------------------------
Nios II Workflow
-------------------------------

Building a complete Nios II application follows these stages:

**Step 1: Create the Quartus Project**

Open Intel Quartus Prime and create a new project for the target FPGA device.

**Step 2: Build the Processor System in Platform Designer**

Launch Platform Designer from the Tools menu. Add the Nios II core, memory,
JTAG UART, and any custom peripherals. Assign base addresses and interrupt
numbers to each component, then click *Generate HDL*.

**Step 3: Add Top-Level Verilog Wrapper**

Platform Designer generates a system module. Instantiate this in a top-level
Verilog file that maps signals to physical FPGA pins:

.. code-block:: verilog

   module top (
       input  wire       clk_50mhz,
       input  wire       reset_n,
       output wire [7:0] leds
   );

       // Instantiate the Platform Designer generated system
       nios_system u0 (
           .clk_clk         (clk_50mhz),
           .reset_reset_n   (reset_n),
           .led_export      (leds)
       );

   endmodule

**Step 4: Compile and Program the FPGA**

Run full compilation in Quartus to synthesize, place, route, and generate the
bitstream. Use the Programmer tool to load the bitstream into the FPGA.

**Step 5: Write and Run Embedded Software**

Open the **Nios II Software Build Tools (SBT)** or **Eclipse-based EDS**:

.. code-block:: c

   #include "system.h"
   #include "io.h"

   int main(void) {
       // Write 0xFF to the LED peripheral base address
       IOWR_32DIRECT(LED_BASE, 0, 0xFF);
       return 0;
   }

The macros ``IOWR_32DIRECT`` and ``LED_BASE`` are generated automatically
by the BSP (Board Support Package) from your Platform Designer system.

-------------------------------
Memory-Mapped Peripheral Access
-------------------------------

From the software perspective, all hardware peripherals appear as memory
addresses. Writing to an address triggers the corresponding hardware write
operation. Reading from an address returns the current hardware state.

Platform Designer automatically generates C header files (``system.h``) that
define base addresses and span constants for all peripherals:

.. code-block:: c

   // From generated system.h
   #define LED_BASE   0x00001000
   #define LED_SPAN   16

   // Direct write to peripheral
   IOWR_32DIRECT(LED_BASE, 0, 0xFF);

   // Direct read from peripheral
   uint32_t val = IORD_32DIRECT(LED_BASE, 0);

-------------------------------
Custom Instruction Acceleration
-------------------------------

For computationally intensive tasks, Nios II supports **custom instructions** —
user-defined hardware operations that appear as single-cycle (or multi-cycle)
instructions in the processor's instruction set.

A custom instruction is described in Verilog and registered with the Nios II
core in Platform Designer. The C compiler can then call the hardware operation
using a built-in intrinsic function, bypassing the general-purpose ALU for
that operation.

-------------------------------
Summary
-------------------------------

The Nios II workflow brings together Verilog, Platform Designer, and embedded
C to create a complete SoC system on an Intel FPGA:

- **Verilog** describes the custom hardware peripherals.
- **Platform Designer** assembles the processor system and generates the interconnect.
- **Quartus** synthesizes the hardware and programs the FPGA.
- **Embedded software** controls the hardware through memory-mapped registers.

This architecture allows hardware designers and software engineers to divide
work clearly, while the Avalon bus protocol serves as a well-defined interface
between the two domains.

.. seealso::

   - :doc:`designs` — Common Verilog module examples useful as peripherals.
   - :doc:`procedure` — ``always`` blocks and clocked logic patterns used in peripherals.
   - :doc:`systemverilog` — SystemVerilog enhancements relevant to SoC interfaces.
