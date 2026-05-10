documentation:
  title: "Verilog Documentation"
  subtitle: "Standard Hardware Description Language for Digital Design"
  description: >
    Verilog is a hardware description language used to design, model, simulate,
    synthesize, and verify digital electronic systems such as FPGA and ASIC designs.
    It is defined by IEEE 1364, and modern Verilog features are now part of the
    SystemVerilog IEEE 1800 standard.

  references:
    - title: "IEEE 1364-2005 Verilog HDL Standard"
      note: "Defines Verilog HDL as a formal notation for creating, verifying, synthesizing, testing, and maintaining electronic systems."
    - title: "IEEE 1800 SystemVerilog Standard"
      note: "SystemVerilog extends Verilog with stronger typing, interfaces, assertions, classes, and verification features."
    - title: "FPGA and ASIC Design Practice"
      note: "Verilog is widely used in RTL design, simulation, synthesis, and hardware verification."

  topics:
    - id: 01
      slug: "introduction"
      title: "Introduction to Verilog"
      source_url: "https://verilogguide.readthedocs.io/"
      status: "rewrite_required"
      reason: "Provided page currently contains unrelated banking/API content."
      learning_objectives:
        - "Understand what Verilog is."
        - "Explain the difference between HDL and software programming languages."
        - "Identify where Verilog is used: FPGA, ASIC, simulation, and verification."
      key_points:
        - "Verilog describes hardware structure and behavior."
        - "Unlike software code, Verilog models circuits that operate concurrently."
        - "Verilog is commonly used at the RTL, or Register Transfer Level."
        - "Designs are written as modules with inputs, outputs, wires, registers, and logic behavior."
      suggested_sections:
        - "What is Verilog?"
        - "Why use Verilog?"
        - "Verilog vs software programming"
        - "FPGA and ASIC design flow"
        - "Basic module example"
      example_code: |
        module and_gate (
            input  wire a,
            input  wire b,
            output wire y
        );

            assign y = a & b;

        endmodule

    - id: 02
      slug: "testbench"
      title: "Verilog Testbench"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/testbench.html"
      status: "rewrite_required"
      reason: "Provided page returned 404."
      learning_objectives:
        - "Understand the purpose of a testbench."
        - "Create stimulus for a Verilog design."
        - "Use simulation output to verify correctness."
      key_points:
        - "A testbench is not usually synthesized into hardware."
        - "It instantiates the design under test, also called DUT."
        - "It drives inputs and checks outputs."
        - "Common simulation tasks include $display, $monitor, $dumpfile, and $dumpvars."
      suggested_sections:
        - "What is a testbench?"
        - "Design Under Test"
        - "Generating input stimulus"
        - "Clock and reset generation"
        - "Checking output behavior"
        - "Waveform dumping"
      example_code: |
        module tb_and_gate;

            reg a;
            reg b;
            wire y;

            and_gate dut (
                .a(a),
                .b(b),
                .y(y)
            );

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

    - id: 03
      slug: "systemverilog"
      title: "SystemVerilog Overview"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/systemverilog.html"
      status: "rewrite_required"
      reason: "Provided page currently contains unrelated banking/payment-system content."
      learning_objectives:
        - "Understand how SystemVerilog extends Verilog."
        - "Identify design and verification features added by SystemVerilog."
        - "Compare Verilog and SystemVerilog coding styles."
      key_points:
        - "SystemVerilog extends Verilog for both RTL design and verification."
        - "It adds logic, always_comb, always_ff, interfaces, packages, enums, structs, assertions, and classes."
        - "Modern digital design often uses SystemVerilog instead of pure Verilog."
      suggested_sections:
        - "What is SystemVerilog?"
        - "Verilog vs SystemVerilog"
        - "New data types"
        - "always_comb and always_ff"
        - "Assertions"
        - "Interfaces and packages"
      example_code: |
        module dff_sv (
            input  logic clk,
            input  logic reset,
            input  logic d,
            output logic q
        );

            always_ff @(posedge clk or posedge reset) begin
                if (reset)
                    q <= 1'b0;
                else
                    q <= d;
            end

        endmodule

    - id: 04
      slug: "procedural-blocks"
      title: "Procedural Blocks in Verilog"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/procedure.html"
      status: "rewrite_required"
      reason: "Provided page currently contains unrelated bank-account content."
      learning_objectives:
        - "Understand initial and always blocks."
        - "Use blocking and non-blocking assignments correctly."
        - "Write combinational and sequential logic."
      key_points:
        - "initial blocks run once at the start of simulation."
        - "always blocks run repeatedly when triggered by their sensitivity list."
        - "Blocking assignment uses = and executes immediately."
        - "Non-blocking assignment uses <= and is preferred for clocked sequential logic."
      suggested_sections:
        - "initial block"
        - "always block"
        - "Sensitivity lists"
        - "Blocking assignment"
        - "Non-blocking assignment"
        - "Combinational vs sequential logic"
      example_code: |
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

    - id: 05
      slug: "verilog-vs-vhdl"
      title: "Verilog vs VHDL"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/vhdl.html"
      status: "rewrite_required"
      reason: "Provided page returned 404."
      learning_objectives:
        - "Compare Verilog and VHDL."
        - "Understand syntax and design-style differences."
        - "Know when each HDL may be used."
      key_points:
        - "Both Verilog and VHDL are hardware description languages."
        - "Verilog syntax is more C-like."
        - "VHDL is more strongly typed and verbose."
        - "Both can be used for FPGA and ASIC design."
      suggested_sections:
        - "What is VHDL?"
        - "Syntax comparison"
        - "Typing differences"
        - "Design flow similarities"
        - "When to choose Verilog"
        - "When to choose VHDL"
      comparison_table:
        - feature: "Syntax style"
          verilog: "C-like and compact"
          vhdl: "Ada-like and verbose"
        - feature: "Typing"
          verilog: "Weak/static typing"
          vhdl: "Strong typing"
        - feature: "Common use"
          verilog: "ASIC, FPGA, verification"
          vhdl: "FPGA, aerospace, defense, education"
        - feature: "Learning curve"
          verilog: "Usually easier for C programmers"
          vhdl: "More strict, often more verbose"

    - id: 06
      slug: "fsm"
      title: "Finite State Machines in Verilog"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/fsm.html"
      status: "rewrite_required"
      reason: "Provided page currently contains unrelated RTA bus-fare content."
      learning_objectives:
        - "Understand finite state machines."
        - "Design Moore and Mealy FSMs."
        - "Implement FSMs in Verilog using state registers and next-state logic."
      key_points:
        - "An FSM has a finite number of states."
        - "FSMs are useful for control logic."
        - "A typical FSM contains state register, next-state logic, and output logic."
        - "State encoding may be binary, one-hot, or gray-coded."
      suggested_sections:
        - "What is an FSM?"
        - "Moore vs Mealy machines"
        - "State encoding"
        - "FSM design template"
        - "Example: traffic light controller"
      example_code: |
        module simple_fsm (
            input  wire clk,
            input  wire reset,
            input  wire start,
            output reg  done
        );

            localparam IDLE = 2'b00;
            localparam RUN  = 2'b01;
            localparam DONE = 2'b10;

            reg [1:0] state;
            reg [1:0] next_state;

            always @(posedge clk or posedge reset) begin
                if (reset)
                    state <= IDLE;
                else
                    state <= next_state;
            end

            always @(*) begin
                next_state = state;
                done = 1'b0;

                case (state)
                    IDLE: begin
                        if (start)
                            next_state = RUN;
                    end

                    RUN: begin
                        next_state = DONE;
                    end

                    DONE: begin
                        done = 1'b1;
                        next_state = IDLE;
                    end

                    default: begin
                        next_state = IDLE;
                    end
                endcase
            end

        endmodule

    - id: 07
      slug: "nios-ii"
      title: "Nios II and Verilog"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/niosread.html"
      status: "rewrite_required"
      reason: "Provided page failed to fetch."
      learning_objectives:
        - "Understand what the Nios II processor is."
        - "Learn how a soft processor can be implemented in FPGA fabric."
        - "Understand how custom Verilog modules can connect to processor systems."
      key_points:
        - "Nios II is a soft processor historically used in Intel/Altera FPGA systems."
        - "A soft processor is implemented using programmable logic resources."
        - "Custom Verilog hardware can communicate with a processor through memory-mapped interfaces."
        - "Typical tools include Quartus, Platform Designer, and embedded software tools."
      suggested_sections:
        - "What is Nios II?"
        - "Soft processor concept"
        - "Processor system architecture"
        - "Memory-mapped peripherals"
        - "Connecting custom Verilog logic"
        - "Basic workflow"
      workflow:
        - "Create Quartus project."
        - "Build processor system in Platform Designer."
        - "Add clock, reset, memory, and I/O peripherals."
        - "Connect custom Verilog module as a peripheral."
        - "Generate HDL system."
        - "Compile FPGA design."
        - "Write and run embedded software."

    - id: 08
      slug: "first-project"
      title: "First Verilog Project"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/firstproject.html"
      status: "rewrite_required"
      reason: "Provided page failed to fetch."
      learning_objectives:
        - "Create a simple Verilog project."
        - "Write, simulate, and synthesize a basic design."
        - "Understand the basic FPGA development workflow."
      key_points:
        - "A first Verilog project should be simple and observable."
        - "Good examples include AND gate, LED blinker, counter, or multiplexer."
        - "The workflow usually includes writing RTL, creating constraints, simulating, synthesizing, and programming the FPGA."
      suggested_sections:
        - "Project goal"
        - "Required tools"
        - "Create source file"
        - "Write Verilog module"
        - "Create testbench"
        - "Run simulation"
        - "Synthesize and program FPGA"
      example_project:
        name: "LED Blinker"
        description: "Toggle an LED using a counter driven by the FPGA clock."
      example_code: |
        module led_blinker (
            input  wire clk,
            input  wire reset,
            output reg  led
        );

            reg [23:0] counter;

            always @(posedge clk or posedge reset) begin
                if (reset) begin
                    counter <= 24'd0;
                    led <= 1'b0;
                end else begin
                    counter <= counter + 1'b1;

                    if (counter == 24'd0)
                        led <= ~led;
                end
            end

        endmodule

    - id: 09
      slug: "design-examples"
      title: "Common Verilog Design Examples"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/designs.html"
      status: "rewrite_required"
      reason: "Provided page currently contains unrelated current-vs-savings-account content."
      learning_objectives:
        - "Study common Verilog building blocks."
        - "Recognize combinational and sequential design patterns."
        - "Reuse basic modules in larger systems."
      key_points:
        - "Common combinational designs include gates, multiplexers, decoders, encoders, adders, and comparators."
        - "Common sequential designs include flip-flops, counters, shift registers, and FSMs."
        - "Reusable modules should have clear ports, parameters, and predictable timing behavior."
      suggested_sections:
        - "Combinational examples"
        - "Sequential examples"
        - "Parameterized modules"
        - "Reusable design patterns"
        - "Synthesis-friendly coding style"
      examples:
        - name: "2-to-1 Multiplexer"
          code: |
            module mux2 (
                input  wire a,
                input  wire b,
                input  wire sel,
                output wire y
            );

                assign y = sel ? b : a;

            endmodule

        - name: "Counter"
          code: |
            module counter (
                input  wire clk,
                input  wire reset,
                output reg [3:0] count
            );

                always @(posedge clk or posedge reset) begin
                    if (reset)
                        count <= 4'd0;
                    else
                        count <= count + 1'b1;
                end

            endmodule

    - id: 10
      slug: "data-types"
      title: "Verilog Data Types"
      source_url: "https://verilogguide.readthedocs.io/en/latest/verilog/datatype.html"
      status: "rewrite_required"
      reason: "Provided page failed to fetch."
      learning_objectives:
        - "Understand Verilog net and variable data types."
        - "Use wire, reg, integer, parameter, and vector types correctly."
        - "Understand 4-state logic: 0, 1, X, and Z."
      key_points:
        - "wire represents a net driven by continuous assignment or module output."
        - "reg stores a value assigned inside procedural blocks."
        - "Despite the name, reg does not always infer a physical register."
        - "Vectors represent multi-bit signals."
        - "Verilog supports unknown X and high-impedance Z states."
      suggested_sections:
        - "wire"
        - "reg"
        - "vectors"
        - "integer"
        - "parameter and localparam"
        - "arrays and memories"
        - "4-state logic"
      example_code: |
        module data_type_example;

            wire single_bit_wire;
            reg single_bit_reg;

            wire [7:0] data_bus;
            reg  [3:0] counter;

            parameter WIDTH = 8;
            localparam IDLE = 2'b00;

            reg [7:0] memory [0:15];

        endmodule