.. meta::
   :description: Comprehensive guide to Finite State Machines (FSM) in Verilog, covering Moore and Mealy architectures.
   :keywords: Verilog FSM, Moore machine, Mealy machine, state transition logic

Finite State Machines in Verilog
=================================

A **Finite State Machine (FSM)** is a digital circuit that moves between a finite
number of predefined states in response to inputs. FSMs are the backbone of
control logic in nearly every digital system.

-----------------------
What is an FSM?
-----------------------

An FSM consists of:

- A finite set of **states** (e.g., IDLE, RUN, DONE).
- **Transitions** between states, triggered by input conditions.
- **Outputs** that depend on the current state (and optionally the inputs).

In hardware, an FSM is implemented using:

1. A **state register** — holds the current state.
2. **Next-state logic** — combinational logic that determines the next state.
3. **Output logic** — combinational or registered logic that generates outputs.

-----------------------
Moore vs Mealy Machines
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Property
     - Moore Machine
     - Mealy Machine
   * - Outputs depend on
     - Current state only
     - Current state **and** current inputs
   * - Output stability
     - Stable between clock edges
     - Can change as inputs change
   * - Typical use
     - Simpler to design and debug
     - Fewer states needed for same function

-----------------------
State Encoding
-----------------------

State values must be encoded as binary numbers stored in the state register.
Three common encoding styles:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Encoding
     - Description
   * - **Binary**
     - Minimum bits. 4 states → 2-bit encoding. Dense but slower decode.
   * - **One-hot**
     - One bit per state; only one bit is high at a time. Faster decode on FPGAs.
   * - **Gray code**
     - Adjacent states differ by only one bit. Reduces glitches in output.

FPGAs typically benefit from one-hot encoding because they have abundant flip-flops
and fast local logic.

-----------------------
3-Block FSM Template
-----------------------

The industry-standard Verilog FSM template separates concerns into three always
blocks:

1. **State register** (sequential) — clocked, stores current state.
2. **Next-state logic** (combinational) — determines the next state.
3. **Output logic** (combinational or registered) — generates outputs.

.. code-block:: verilog

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

       // ── Block 1: State Register ────────────────────────────────
       always @(posedge clk or posedge reset) begin
           if (reset)
               state <= IDLE;
           else
               state <= next_state;
       end

       // ── Block 2: Next-State Logic ──────────────────────────────
       always @(*) begin
           next_state = state;  // Default: stay in current state

           case (state)
               IDLE: begin
                   if (start)
                       next_state = RUN;
               end

               RUN: begin
                   next_state = DONE;
               end

               DONE: begin
                   next_state = IDLE;
               end

               default: begin
                   next_state = IDLE;
               end
           endcase
       end

       // ── Block 3: Output Logic ──────────────────────────────────
       always @(*) begin
           done = 1'b0;  // Default output

           case (state)
               DONE: done = 1'b1;
               default: done = 1'b0;
           endcase
       end

   endmodule

-----------------------
Example: Traffic Light Controller
-----------------------

A classic FSM example: a simple two-direction traffic light with timed transitions.

.. code-block:: verilog

   module traffic_light (
       input  wire       clk,
       input  wire       reset,
       output reg  [1:0] ns_light,  // North-South: 00=RED, 01=YELLOW, 10=GREEN
       output reg  [1:0] ew_light   // East-West:   same encoding
   );

       localparam NS_GREEN  = 2'd0;
       localparam NS_YELLOW = 2'd1;
       localparam EW_GREEN  = 2'd2;
       localparam EW_YELLOW = 2'd3;

       localparam GREEN  = 2'b10;
       localparam YELLOW = 2'b01;
       localparam RED    = 2'b00;

       reg [1:0] state;
       reg [1:0] next_state;
       reg [4:0] timer;

       // State Register
       always @(posedge clk or posedge reset) begin
           if (reset) begin
               state <= NS_GREEN;
               timer <= 5'd0;
           end else begin
               if (timer == 5'd0)
                   state <= next_state;
               timer <= (timer == 5'd0) ? 5'd30 : timer - 1'b1;
           end
       end

       // Next-State Logic
       always @(*) begin
           case (state)
               NS_GREEN:  next_state = NS_YELLOW;
               NS_YELLOW: next_state = EW_GREEN;
               EW_GREEN:  next_state = EW_YELLOW;
               EW_YELLOW: next_state = NS_GREEN;
               default:   next_state = NS_GREEN;
           endcase
       end

       // Output Logic (Moore)
       always @(*) begin
           case (state)
               NS_GREEN:  begin ns_light = GREEN;  ew_light = RED;    end
               NS_YELLOW: begin ns_light = YELLOW; ew_light = RED;    end
               EW_GREEN:  begin ns_light = RED;    ew_light = GREEN;  end
               EW_YELLOW: begin ns_light = RED;    ew_light = YELLOW; end
               default:   begin ns_light = RED;    ew_light = RED;    end
           endcase
       end

   endmodule

-----------------------
Common Mistakes
-----------------------

- **Forgetting a default assignment** — outputs left unassigned in some states
  will infer latches.
- **Using blocking assignments in the state register** — use ``<=`` for all
  clocked assignments.
- **No default case** — missing a default in ``case`` statements can create
  unreachable states with undefined behavior.

-----------------------
See Also
-----------------------

- :doc:`procedure` — ``always`` blocks and non-blocking assignments.
- :doc:`designs` — Simpler sequential patterns like counters and flip-flops.
- :doc:`testbench` — How to verify FSM behavior in simulation.
