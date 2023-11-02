module tt_um_btflv_8bit_fp_adder (
	input  wire [7:0] ui_in,    // Dedicated inputs
	output wire [7:0] uo_out,   // Dedicated outputs
	input  wire [7:0] uio_in,   // IOs: Input path
	output wire [7:0] uio_out,  // IOs: Output path
	output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
	input  wire       ena,      // will go high when the design is enabled
	input  wire       clk,      // clock
	input  wire       rst_n     // reset_n - low to reset
);

assign uio_oe = 8'b00000000;

wire       a_sign;
wire       b_sign;
wire [3:0] a_expo;
wire [3:0] b_expo;
wire [2:0] a_mant;
wire [2:0] b_mant;

reg [3:0] l_expo;
reg [3:0] s_expo;
reg [2:0] l_mant;
reg [2:0] s_mant;
reg [3:0] c_mant;
reg [4:0] g_mant;
reg [3:0] o_expo;
reg [2:0] o_mant;
reg       o_sign;
reg [7:0] o_floa;

assign a_sign = ui_in[7];
assign b_sign = uio_in[7];
assign a_expo = ui_in[6:3];
assign b_expo = uio_in[6:3];
assign a_mant = ui_in[2:0];
assign b_mant = uio_in[2:0];

assign uo_out = o_floa;

always @*
begin
	if (a_expo > b_expo)
	begin
		l_expo = a_expo;
		s_expo = b_expo;
		l_mant = a_mant;
		s_mant = b_mant >> (l_expo - s_expo);
		o_sign = a_sign;
	end
	else if (a_expo < b_expo)
	begin
		l_expo = b_expo;
		s_expo = a_expo;
		l_mant = b_mant;
		s_mant = a_mant >> (l_expo - s_expo);
		o_sign = b_sign;
	end
	else
	begin
		if(a_mant > b_mant)
		begin
			l_expo = a_expo;
			s_expo = b_expo;
			l_mant = a_mant;
			s_mant = b_mant;
			o_sign = a_sign;
		end
		else
		begin
			l_expo = b_expo;
			s_expo = a_expo;
			l_mant = b_mant;
			s_mant = a_mant;
			o_sign = b_sign;
		end
	end
	
	c_mant = (a_sign ^ b_sign) ? l_mant - s_mant : l_mant + s_mant;
	g_mant = c_mant + 5;
	
	if (c_mant[3])
	begin
		if (g_mant[4])
		begin
			if (g_mant < 4'b1101)
			begin
				o_mant = g_mant[4:2];
				o_expo = l_expo + 2;
			end
			else
			begin
				o_mant = 3'b000;
				o_expo = 4'b1111;
			end
		end
		else
		begin
			if (g_mant < 4'b1110)
			begin
				o_mant = g_mant[3:1];
				o_expo = l_expo + 1;
			end
			else
			begin
				o_mant = 3'b000;
				o_expo = 4'b1111;
			end
			o_mant = c_mant[2:0];
			o_expo = l_expo;
		end
	end
	else
	begin
		o_mant = c_mant[2:0];
		o_expo = l_expo;
	end
end

always @(posedge clk)
begin
	if (rst_n)
	begin
		o_floa <= 8'd0;
	end
	else if (ena)
	begin
		o_floa[6:3] <= o_expo;
		o_floa[2:0] <= o_mant;
		o_floa[7]   <= o_sign;
	end
	else
	begin
		o_floa <= 8'd0;
	end
end

endmodule
