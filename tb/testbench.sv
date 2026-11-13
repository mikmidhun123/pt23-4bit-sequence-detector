`timescale 1ns/1ps

module tb_seq_detector;

    reg  clk, rst, din;
    wire detected;

    seq_detector dut (
        .clk(clk),
        .rst(rst),
        .din(din),
        .detected(detected)
    );

    // 10 ns clock
    initial clk = 0;
    always #5 clk = ~clk;

    // Test stream: contains 1011 five times (overlapping)
    reg [23:0] stream = 24'b0010_1101_1011_0101_1100_1011;
    integer i;

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, tb_seq_detector);

        rst = 1; din = 0;
        #12 rst = 0;

        for (i = 23; i >= 0; i = i - 1) begin
            din = stream[i];
            @(posedge clk);
            #1 $display("t=%0t  din=%b  detected=%b", $time, din, detected);
        end

        #20 $finish;
    end

endmodule
