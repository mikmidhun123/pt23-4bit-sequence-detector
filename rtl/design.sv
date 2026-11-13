// 4-bit Sequence Detector (1011), overlapping, Moore FSM
module seq_detector (
    input  wire clk,
    input  wire rst,      // synchronous, active high
    input  wire din,      // serial input bit
    output wire detected  // high when 1011 has just been received
);

    localparam S0 = 3'd0,  // no match
               S1 = 3'd1,  // "1"
               S2 = 3'd2,  // "10"
               S3 = 3'd3,  // "101"
               S4 = 3'd4;  // "1011" -> detected

    reg [2:0] state, next_state;

    // State register
    always @(posedge clk) begin
        if (rst) state <= S0;
        else     state <= next_state;
    end

    // Next-state logic
    always @(*) begin
        case (state)
            S0: next_state = din ? S1 : S0;
            S1: next_state = din ? S1 : S2;
            S2: next_state = din ? S3 : S0;
            S3: next_state = din ? S4 : S2;
            S4: next_state = din ? S1 : S2;  // overlap handling
            default: next_state = S0;
        endcase
    end

    // Moore output
    assign detected = (state == S4);

endmodule
