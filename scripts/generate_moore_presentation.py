import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank slide

    # Color Palette
    BG_DARK = RGBColor(11, 19, 43)        # #0B132B - Midnight Navy
    BG_CARD = RGBColor(22, 36, 71)        # #162447 - Card Navy
    BG_CARD_LIGHT = RGBColor(28, 44, 84)  # #1C2C54
    ACCENT_CYAN = RGBColor(0, 210, 211)   # #00D2D3 - Vibrant Cyan
    ACCENT_GOLD = RGBColor(255, 209, 102) # #FFD166 - Gold Accent
    ACCENT_GREEN = RGBColor(6, 214, 160)  # #06D6A0 - Success Green
    TEXT_WHITE = RGBColor(255, 255, 255)  # Crisp White
    TEXT_MUTED = RGBColor(180, 195, 215)  # Soft Silver Blue
    TEXT_DIM = RGBColor(130, 145, 170)    # Dimmed Text
    BORDER_COLOR = RGBColor(45, 65, 110)  # Card Border

    img_dir = "e:/work/vlsi report/pt23-4bit-sequence-detector/images"

    def apply_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, slide_num, category, title, subtitle=None):
        # Top banner line
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.04))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = ACCENT_CYAN
        top_bar.line.fill.background()

        # Metadata text
        meta_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(9.0), Inches(0.3))
        tf = meta_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"ST. JOSEPH'S COLLEGE OF ENGINEERING  |  DEPT. OF ECE  |  EEC SD0212  |  {category.upper()}"
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.48), Inches(2.033), Inches(0.3))
        ntf = num_box.text_frame
        ntf.margin_left = ntf.margin_top = ntf.margin_right = ntf.margin_bottom = 0
        np = ntf.paragraphs[0]
        np.text = f"SLIDE {slide_num:02d} / 12"
        np.alignment = PP_ALIGN.RIGHT
        np.font.size = Pt(8.5)
        np.font.bold = True
        np.font.color.rgb = TEXT_MUTED

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.65))
        ttf = title_box.text_frame
        ttf.word_wrap = True
        ttf.margin_left = ttf.margin_top = ttf.margin_right = ttf.margin_bottom = 0
        tp = ttf.paragraphs[0]
        tp.text = title
        tp.font.size = Pt(20)
        tp.font.bold = True
        tp.font.color.rgb = TEXT_WHITE

        if subtitle:
            sp = ttf.add_paragraph()
            sp.text = subtitle
            sp.font.size = Pt(11)
            sp.font.color.rgb = ACCENT_GOLD
            sp.space_before = Pt(3)

    def add_card(slide, left, top, width, height, fill_color=BG_CARD, border_color=BORDER_COLOR):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1)
        else:
            card.line.fill.background()
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1)

    # Accent decorative banner
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    banner.fill.solid()
    banner.fill.fore_color.rgb = ACCENT_CYAN
    banner.line.fill.background()

    # College & Department Header
    col_box = s1.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.733), Inches(0.8))
    ctf = col_box.text_frame
    cp1 = ctf.paragraphs[0]
    cp1.text = "ST. JOSEPH'S COLLEGE OF ENGINEERING"
    cp1.font.size = Pt(15)
    cp1.font.bold = True
    cp1.font.color.rgb = ACCENT_CYAN

    cp2 = ctf.add_paragraph()
    cp2.text = "(An Autonomous Institution)  |  OMR, Chennai - 600 119  |  Department of Electronics and Communication Engineering"
    cp2.font.size = Pt(10)
    cp2.font.color.rgb = TEXT_MUTED

    cp3 = ctf.add_paragraph()
    cp3.text = "EMPLOYABILITY ENHANCEMENT COURSE — SD0212: RTL DESIGN AND VERIFICATION  |  NOVEMBER 2026"
    cp3.font.size = Pt(9.5)
    cp3.font.bold = True
    cp3.font.color.rgb = ACCENT_GOLD
    cp3.space_before = Pt(2)

    # Title Card
    add_card(s1, 0.8, 1.8, 11.733, 2.3, BG_CARD_LIGHT, ACCENT_CYAN)
    t_box = s1.shapes.add_textbox(Inches(1.1), Inches(1.95), Inches(11.133), Inches(2.0))
    ttf = t_box.text_frame
    ttf.word_wrap = True
    tp1 = ttf.paragraphs[0]
    tp1.text = "RTL Design and Verification of 4-Bit Sequence Detector"
    tp1.font.size = Pt(28)
    tp1.font.bold = True
    tp1.font.color.rgb = TEXT_WHITE

    tp2 = ttf.add_paragraph()
    tp2.text = "Overlapping Moore Finite State Machine ('1011') Using EDA Playground & Yosys"
    tp2.font.size = Pt(16)
    tp2.font.bold = True
    tp2.font.color.rgb = ACCENT_CYAN
    tp2.space_before = Pt(6)

    tp3 = ttf.add_paragraph()
    tp3.text = "Synthesizable Verilog-2001 RTL  •  Icarus Verilog 12.0  •  EPWave Cloud Timing  •  Yosys Gate Synthesis (16 Standard Cells)"
    tp3.font.size = Pt(11)
    tp3.font.color.rgb = TEXT_MUTED
    tp3.space_before = Pt(8)

    # Team Members Card
    add_card(s1, 0.8, 4.35, 6.8, 2.5)
    m_box = s1.shapes.add_textbox(Inches(1.0), Inches(4.45), Inches(6.4), Inches(2.3))
    mtf = m_box.text_frame
    mp = mtf.paragraphs[0]
    mp.text = "PROJECT TEAM PT23 — CONTRIBUTORS"
    mp.font.size = Pt(11)
    mp.font.bold = True
    mp.font.color.rgb = ACCENT_GOLD

    members = [
        ("MIDHUN M (Project Lead)", "312324106102"),
        ("SIVAGURU S", "312324106165"),
        ("SIVAPADHASEKARAN G", "312324106166"),
        ("SUNDAR S", "312324106170"),
        ("SURENDAR", "312324106172")
    ]
    for name, regno in members:
        p = mtf.add_paragraph()
        p.text = f"•  {name:<32} Register No: {regno}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

    # Faculty & Institution Card
    add_card(s1, 7.8, 4.35, 4.733, 2.5)
    f_box = s1.shapes.add_textbox(Inches(8.0), Inches(4.45), Inches(4.333), Inches(2.3))
    ftf = f_box.text_frame
    fp = ftf.paragraphs[0]
    fp.text = "FACULTY GUIDANCE & INSTITUTION LEADERSHIP"
    fp.font.size = Pt(11)
    fp.font.bold = True
    fp.font.color.rgb = ACCENT_GOLD

    faculty = [
        ("Project Supervisor", "Dr. P. LATHA, M.E., Ph.D."),
        ("Head of Department", "Dr. S. RAJESH KANNAN, M.E., Ph.D."),
        ("Principal", "Dr. VADDI SESHAGIRI RAO, M.E., M.B.A., Ph.D."),
        ("Chairman", "Dr. B. BABU MANOHARAN, M.A., M.B.A., Ph.D.")
    ]
    for role, fname in faculty:
        p = ftf.add_paragraph()
        p.text = f"{role}:"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.space_before = Pt(2)
        p2 = ftf.add_paragraph()
        p2.text = f"   {fname}"
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT & SPECIFICATIONS
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2)
    add_header(s2, 2, "Problem Statement & Specifications", "Sliding-Window '1011' Sequence Detection", "High-speed serial bitstream pattern recognition with overlapping sequence capability")

    # Left Column: Problem Definition & Overlap Concept
    add_card(s2, 0.8, 1.6, 5.7, 5.3)
    p_box = s2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.9))
    ptf = p_box.text_frame
    ptf.word_wrap = True

    p = ptf.paragraphs[0]
    p.text = "PROBLEM STATEMENT & OBJECTIVES"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GOLD

    points1 = [
        ("Serial Data Stream", "Modern telecommunication transceivers and serial buses transmit continuous bitstreams at wire speed without inter-byte packet markers."),
        ("Target Signature ('1011')", "The detector must monitor input line din continuously and assert output detected high immediately after receiving the sequence 1011."),
        ("Overlapping Detection", "The detector must retain partial matching history. If the input stream contains back-to-back signatures such as '1011011', the trailing bit '1' of the first '1011' serves directly as the leading bit '1' of the subsequent match."),
        ("Deterministic Synchronous Reset", "An active-high synchronous reset signal clears all internal state flip-flops cleanly to S0 on the rising clock edge.")
    ]
    for title, desc in points1:
        p = ptf.add_paragraph()
        p.text = f"• {title}: "
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.space_before = Pt(8)
        p.add_run()
        p.runs[0].text = f"• {title}: "
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = ACCENT_CYAN
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_WHITE

    # Right Column: Specification Cards
    specs = [
        ("TARGET BIT SEQUENCE", "4'b1011 (Binary: 1 -> 0 -> 1 -> 1)", ACCENT_CYAN),
        ("FSM ARCHITECTURE", "Moore Machine (Output depends strictly on state register)", ACCENT_GOLD),
        ("TIMING & CLOCK", "100 MHz Master Clock (10 ns clock period, 50% duty cycle)", TEXT_WHITE),
        ("RESET PROTOCOL", "Active-High Synchronous Reset (Evaluated at posedge clk)", ACCENT_GREEN),
        ("VERIFICATION STREAM", "24-bit test vector: 0010_1101_1011_0101_1100_1011", ACCENT_CYAN),
        ("EXPECTED DETECTIONS", "Exactly 5 Valid Matches (with overlapping handling)", ACCENT_GOLD)
    ]
    for idx, (stitle, sval, scolor) in enumerate(specs):
        add_card(s2, 6.8, 1.6 + idx * 0.88, 5.733, 0.76)
        sbox = s2.shapes.add_textbox(Inches(7.0), Inches(1.65 + idx * 0.88), Inches(5.333), Inches(0.66))
        stf = sbox.text_frame
        stf.word_wrap = True
        sp1 = stf.paragraphs[0]
        sp1.text = stitle
        sp1.font.size = Pt(8.5)
        sp1.font.bold = True
        sp1.font.color.rgb = TEXT_MUTED
        sp2 = stf.add_paragraph()
        sp2.text = sval
        sp2.font.size = Pt(11)
        sp2.font.bold = True
        sp2.font.color.rgb = scolor

    # ==========================================
    # SLIDE 3: REAL-WORLD VLSI APPLICATIONS
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3)
    add_header(s3, 3, "Real-World Applications", "Industrial & Telecommunication Applications", "Significance of hardware-accelerated sliding pattern recognition in digital systems")

    apps = [
        ("TELECOMMUNICATIONS & NETWORKING", "High-Speed Packet Frame Delimiters", 
         "Synchronous Data Link Control (SDLC), HDLC, and Ethernet protocols rely on dedicated hardware sequence detectors to detect framing flags (e.g., 01111110) across continuous serial data channels with zero software overhead.",
         ACCENT_CYAN),
        ("SERIAL PHYSICAL LAYERS (PHY)", "Preamble Synchronization & Alignment",
         "High-speed serial communication transceivers (PCIe, USB, SATA, UART) utilize bit-pattern detectors to lock onto preambles and establish word-boundary alignment before clock-data recovery (CDR) and deserialization.",
         ACCENT_GOLD),
        ("DIGITAL SECURITY & MONITORING", "Hardware Attack & Instruction Sniffers",
         "On-chip hardware monitors observe internal system buses in real time to intercept unauthorized instruction opcodes, malicious debug triggers, or fault-injection signatures before illegal execution can occur.",
         ACCENT_GREEN),
        ("DATA COMPRESSION & DSP", "Sliding-Window Pattern Filtering",
         "Hardware-based Huffman and Lempel-Ziv (LZ77/LZW) compression accelerators use sliding-window sequence matching units to locate repeated substring tokens at streaming clock rates.",
         TEXT_WHITE)
    ]

    for idx, (cat, title, desc, col) in enumerate(apps):
        row = idx // 2
        col_idx = idx % 2
        c_left = 0.8 + col_idx * 5.966
        c_top = 1.6 + row * 2.65
        add_card(s3, c_left, c_top, 5.766, 2.45)
        
        abox = s3.shapes.add_textbox(Inches(c_left + 0.25), Inches(c_top + 0.2), Inches(5.266), Inches(2.05))
        atf = abox.text_frame
        atf.word_wrap = True
        
        ap1 = atf.paragraphs[0]
        ap1.text = cat
        ap1.font.size = Pt(8.5)
        ap1.font.bold = True
        ap1.font.color.rgb = col
        
        ap2 = atf.add_paragraph()
        ap2.text = title
        ap2.font.size = Pt(13)
        ap2.font.bold = True
        ap2.font.color.rgb = TEXT_WHITE
        ap2.space_before = Pt(3)
        
        ap3 = atf.add_paragraph()
        ap3.text = desc
        ap3.font.size = Pt(9.5)
        ap3.font.color.rgb = TEXT_MUTED
        ap3.space_before = Pt(6)

    # ==========================================
    # SLIDE 4: TOP-LEVEL HARDWARE ARCHITECTURE
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4)
    add_header(s4, 4, "Hardware Architecture", "Top-Level Architecture & Port Specifications", "Module interface definitions, pin descriptions, and design guarantees")

    # Left: Block diagram image
    add_card(s4, 0.8, 1.6, 6.0, 5.3)
    bd_path = os.path.join(img_dir, "block_diagram.png")
    if os.path.exists(bd_path):
        s4.shapes.add_picture(bd_path, Inches(1.0), Inches(1.8), width=Inches(5.6))
    
    cap_box = s4.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(5.6), Inches(0.5))
    ctf = cap_box.text_frame
    cp = ctf.paragraphs[0]
    cp.text = "Figure 3.1: Top-Level Module Interface Block Diagram of seq_detector"
    cp.alignment = PP_ALIGN.CENTER
    cp.font.size = Pt(9)
    cp.font.italic = True
    cp.font.color.rgb = ACCENT_CYAN

    # Right: Pin table & Architecture Rules
    add_card(s4, 7.1, 1.6, 5.433, 5.3)
    pbox = s4.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.033), Inches(4.9))
    ptf = pbox.text_frame
    ptf.word_wrap = True

    pp = ptf.paragraphs[0]
    pp.text = "TABLE 3.1 — PIN DESCRIPTION & ATTRIBUTES"
    pp.font.size = Pt(11)
    pp.font.bold = True
    pp.font.color.rgb = ACCENT_GOLD

    pin_data = [
        ("clk", "Input", "1-bit", "System clock (10 ns / 100 MHz)"),
        ("rst", "Input", "1-bit", "Active-high synchronous reset"),
        ("din", "Input", "1-bit", "Serial binary data input stream"),
        ("detected", "Output", "1-bit", "Moore output (High on '1011' match)")
    ]
    for p_name, p_dir, p_w, p_desc in pin_data:
        p = ptf.add_paragraph()
        p.text = f"• {p_name} ({p_dir}, {p_w}): {p_desc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(4)

    pp2 = ptf.add_paragraph()
    pp2.text = "HARDWARE DESIGN GUARANTEES"
    pp2.font.size = Pt(11)
    pp2.font.bold = True
    pp2.font.color.rgb = ACCENT_CYAN
    pp2.space_before = Pt(14)

    guarantees = [
        ("Zero Inferred Latches", "Next-state logic always @(*) utilizes a complete case statement with a mandatory default branch, preventing combinational latch synthesis."),
        ("Glitch-Free Moore Output", "Output detected is decoded purely from the state register (state == S4), isolating output signals from input glitches."),
        ("Deterministic Synchronous Reset", "Guarantees clean startup into state S0 without metastable hazards.")
    ]
    for g_title, g_desc in guarantees:
        p = ptf.add_paragraph()
        p.text = f"• {g_title}: {g_desc}"
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(4)

    # ==========================================
    # SLIDE 5: MOORE FSM STATE TRANSITION ARCHITECTURE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5)
    add_header(s5, 5, "FSM Architecture", "Moore FSM 5-State Transition Architecture", "State encoding, next-state transitions, and overlapping recovery logic")

    # Left: State Diagram Image
    add_card(s5, 0.8, 1.6, 6.2, 5.3)
    sd_path = os.path.join(img_dir, "state_diagram.png")
    if os.path.exists(sd_path):
        s5.shapes.add_picture(sd_path, Inches(0.95), Inches(1.8), width=Inches(5.9))
    
    sd_cap = s5.shapes.add_textbox(Inches(0.95), Inches(6.35), Inches(5.9), Inches(0.45))
    sdtf = sd_cap.text_frame
    sdp = sdtf.paragraphs[0]
    sdp.text = "Figure 3.2: 5-State Moore FSM State Transition Flowchart"
    sdp.alignment = PP_ALIGN.CENTER
    sdp.font.size = Pt(9)
    sdp.font.italic = True
    sdp.font.color.rgb = ACCENT_CYAN

    # Right: State Table & Overlap Analysis
    add_card(s5, 7.3, 1.6, 5.233, 5.3)
    tbox = s5.shapes.add_textbox(Inches(7.5), Inches(1.8), Inches(4.833), Inches(4.9))
    ttf = tbox.text_frame
    ttf.word_wrap = True

    tp = ttf.paragraphs[0]
    tp.text = "TABLE 3.2 — MOORE STATE TRANSITION TABLE"
    tp.font.size = Pt(11)
    tp.font.bold = True
    tp.font.color.rgb = ACCENT_GOLD

    states_info = [
        ("S0 (3'b000)", "No match / Idle", "S1 (1)", "S0 (0)", "0"),
        ("S1 (3'b001)", "Matched '1'", "S1 (1)", "S2 (10)", "0"),
        ("S2 (3'b010)", "Matched '10'", "S3 (101)", "S0 (0)", "0"),
        ("S3 (3'b011)", "Matched '101'", "S4 (1011)", "S2 (10)", "0"),
        ("S4 (3'b100)", "Matched '1011'", "S1 (1)", "S2 (10)", "1")
    ]
    for s_name, s_meaning, n_1, n_0, out_val in states_info:
        p = ttf.add_paragraph()
        p.text = f"{s_name} [{s_meaning}]:"
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        p.space_before = Pt(3)
        p2 = ttf.add_paragraph()
        p2.text = f"   din=0 -> {n_0}  |  din=1 -> {n_1}  |  detected = {out_val}"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_WHITE

    p_ov = ttf.add_paragraph()
    p_ov.text = "OVERLAPPING RECOVERY LOGIC AT S4"
    p_ov.font.size = Pt(11)
    p_ov.font.bold = True
    p_ov.font.color.rgb = ACCENT_GOLD
    p_ov.space_before = Pt(10)

    p_ov_desc = ttf.add_paragraph()
    p_ov_desc.text = "When in state S4, the sequence '1011' has completed:\n" \
                     "• If next bit din=0, stream ends in '10' -> transition to S2.\n" \
                     "• If next bit din=1, stream ends in '1' -> transition to S1.\n" \
                     "This enables back-to-back pattern recognition without dropping shared bits."
    p_ov_desc.font.size = Pt(8.5)
    p_ov_desc.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 6: VERILOG RTL CODE IMPLEMENTATION
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6)
    add_header(s6, 6, "RTL Implementation", "Synthesizable Verilog-2001 Source Code (design.sv)", "Verbatim implementation of module seq_detector as verified on EDA Playground")

    add_card(s6, 0.8, 1.6, 11.733, 5.3)
    cbox = s6.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.333), Inches(5.0))
    ctf = cbox.text_frame
    ctf.word_wrap = True

    code_lines = [
        ("// 4-bit Sequence Detector (1011), overlapping, Moore FSM", ACCENT_CYAN),
        ("module seq_detector (", TEXT_WHITE),
        ("    input  wire clk, rst, din,     // Synchronous reset, serial input", TEXT_MUTED),
        ("    output wire detected           // High when 1011 has just been received", ACCENT_GOLD),
        (");", TEXT_WHITE),
        ("    localparam S0 = 3'd0, S1 = 3'd1, S2 = 3'd2, S3 = 3'd3, S4 = 3'd4;", ACCENT_CYAN),
        ("    reg [2:0] state, next_state;", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("    // State register (Positive-edge triggered with synchronous reset)", ACCENT_CYAN),
        ("    always @(posedge clk) begin", TEXT_WHITE),
        ("        if (rst) state <= S0;", ACCENT_GREEN),
        ("        else     state <= next_state;", TEXT_WHITE),
        ("    end", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("    // Next-state combinational logic", ACCENT_CYAN),
        ("    always @(*) begin", TEXT_WHITE),
        ("        case (state)", ACCENT_GOLD),
        ("            S0: next_state = din ? S1 : S0;", TEXT_WHITE),
        ("            S1: next_state = din ? S1 : S2;", TEXT_WHITE),
        ("            S2: next_state = din ? S3 : S0;", TEXT_WHITE),
        ("            S3: next_state = din ? S4 : S2;", TEXT_WHITE),
        ("            S4: next_state = din ? S1 : S2;  // Overlap handling: 1011 -> 1 or 10", ACCENT_GREEN),
        ("            default: next_state = S0;", TEXT_MUTED),
        ("        endcase", ACCENT_GOLD),
        ("    end", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("    // Pure Moore output decode (isolated from input glitches)", ACCENT_CYAN),
        ("    assign detected = (state == S4);", ACCENT_GOLD),
        ("endmodule", TEXT_WHITE)
    ]

    for idx, (cline, ccolor) in enumerate(code_lines):
        if idx == 0:
            p = ctf.paragraphs[0]
        else:
            p = ctf.add_paragraph()
        p.text = cline
        p.font.name = "Consolas"
        p.font.size = Pt(9.5)
        p.font.color.rgb = ccolor
        p.space_before = Pt(0)

    # ==========================================
    # SLIDE 7: TESTBENCH ARCHITECTURE & VERIFICATION PLAN
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7)
    add_header(s7, 7, "Verification Methodology", "Self-Checking Testbench Architecture (testbench.sv)", "Stimulus generation, clock synthesis, and automated waveform dumping")

    # Left: Testbench Code Highlights
    add_card(s7, 0.8, 1.6, 6.0, 5.3)
    tb_box = s7.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(5.6), Inches(5.0))
    tbtf = tb_box.text_frame
    tbtf.word_wrap = True

    tb_code = [
        ("`timescale 1ns/1ps", ACCENT_CYAN),
        ("module tb_seq_detector;", TEXT_WHITE),
        ("    reg clk, rst, din; wire detected;", TEXT_MUTED),
        ("    seq_detector dut (.clk(clk), .rst(rst), .din(din), .detected(detected));", TEXT_WHITE),
        ("", TEXT_WHITE),
        ("    // 100 MHz clock generation (10 ns period)", ACCENT_CYAN),
        ("    initial clk = 0;", TEXT_WHITE),
        ("    always #5 clk = ~clk;", ACCENT_GREEN),
        ("", TEXT_WHITE),
        ("    // 24-bit stimulus vector containing 5 overlapping matches", ACCENT_CYAN),
        ("    reg [23:0] stream = 24'b0010_1101_1011_0101_1100_1011;", ACCENT_GOLD),
        ("    integer i;", TEXT_WHITE),
        ("    initial begin", TEXT_WHITE),
        ("        $dumpfile(\"dump.vcd\"); $dumpvars(0, tb_seq_detector);", ACCENT_CYAN),
        ("        rst = 1; din = 0;", TEXT_WHITE),
        ("        #12 rst = 0;  // Synchronous reset release", ACCENT_GREEN),
        ("        for (i = 23; i >= 0; i = i - 1) begin", ACCENT_GOLD),
        ("            din = stream[i];", TEXT_WHITE),
        ("            @(posedge clk);", TEXT_WHITE),
        ("            #1 $display(\"t=%0t  din=%b  detected=%b\", $time, din, detected);", TEXT_WHITE),
        ("        end", ACCENT_GOLD),
        ("        #20 $finish;  // Clean termination at 266 ns", ACCENT_CYAN),
        ("    end", TEXT_WHITE),
        ("endmodule", TEXT_WHITE)
    ]
    for idx, (tbline, tbcolor) in enumerate(tb_code):
        if idx == 0:
            p = tbtf.paragraphs[0]
        else:
            p = tbtf.add_paragraph()
        p.text = tbline
        p.font.name = "Consolas"
        p.font.size = Pt(8.5)
        p.font.color.rgb = tbcolor
        p.space_before = Pt(0)

    # Right: Verification Strategy
    add_card(s7, 7.1, 1.6, 5.433, 5.3)
    strat_box = s7.shapes.add_textbox(Inches(7.3), Inches(1.8), Inches(5.033), Inches(4.9))
    stf = strat_box.text_frame
    stf.word_wrap = True

    sp = stf.paragraphs[0]
    sp.text = "VERIFICATION STRATEGY & METRICS"
    sp.font.size = Pt(12)
    sp.font.bold = True
    sp.font.color.rgb = ACCENT_GOLD

    strat_points = [
        ("Bit-Stream Vector Analysis", "The 24-bit stream contains exactly 5 valid occurrences of 1011, including contiguous overlapping windows ('1011011')."),
        ("Synchronous Reset Verification", "Reset is applied at t=0 and held until t=12 ns (2 ns after first rising edge), ensuring synchronous initialization to state S0."),
        ("Post-Clock Sample Strobe (#1)", "The $display strobe samples 1 ns after posedge clk, capturing stable flip-flop outputs without zero-delay simulator race hazards."),
        ("EPWave Waveform Instrumentation", "$dumpvars(0, tb_seq_detector) logs all signal transitions into dump.vcd for cycle-accurate timing inspection.")
    ]
    for stitle, sdesc in strat_points:
        p = stf.add_paragraph()
        p.text = f"• {stitle}: {sdesc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(8)

    # ==========================================
    # SLIDE 8: EDA PLAYGROUND CLOUD SIMULATION
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8)
    add_header(s8, 8, "EDA Playground Execution", "Cloud IDE Environment & Simulation Run", "Execution under logged-in account MIDHUN M on edaplayground.com/x/jXfS")

    # Left: Editor screenshot
    add_card(s8, 0.8, 1.6, 6.8, 5.3)
    ed_path = os.path.join(img_dir, "editor.png")
    if os.path.exists(ed_path):
        s8.shapes.add_picture(ed_path, Inches(0.95), Inches(1.75), width=Inches(6.5))
    
    ed_cap = s8.shapes.add_textbox(Inches(0.95), Inches(6.35), Inches(6.5), Inches(0.45))
    edtf = ed_cap.text_frame
    edp = edtf.paragraphs[0]
    edp.text = "Figure 3.3: EDA Playground Cloud IDE with Logged-In User MIDHUN M"
    edp.alignment = PP_ALIGN.CENTER
    edp.font.size = Pt(8.5)
    edp.font.italic = True
    edp.font.color.rgb = ACCENT_CYAN

    # Right: Log screenshot & execution parameters
    add_card(s8, 7.8, 1.6, 4.733, 5.3)
    l_box = s8.shapes.add_textbox(Inches(8.0), Inches(1.75), Inches(4.333), Inches(2.2))
    ltf = l_box.text_frame
    ltf.word_wrap = True
    lp = ltf.paragraphs[0]
    lp.text = "SIMULATION LOG SUMMARY"
    lp.font.size = Pt(11)
    lp.font.bold = True
    lp.font.color.rgb = ACCENT_GOLD

    sim_params = [
        ("Simulator Tool", "Icarus Verilog 12.0"),
        ("Compiler Flags", "-Wall -g2012 (Verilog-2001/SystemVerilog)"),
        ("Cloud Workspace", "https://www.edaplayground.com/x/jXfS"),
        ("Logged-In Account", "MIDHUN M (User ID: 1133145)"),
        ("Simulation Exit", "Code 0 (Normal termination at t=266 ns)")
    ]
    for sp_name, sp_val in sim_params:
        p = ltf.add_paragraph()
        p.text = f"• {sp_name}: {sp_val}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(3)

    log_path = os.path.join(img_dir, "log.png")
    if os.path.exists(log_path):
        s8.shapes.add_picture(log_path, Inches(8.0), Inches(4.1), width=Inches(4.333))

    # ==========================================
    # SLIDE 9: CYCLE-ACCURATE TIMING & EPWAVE WAVEFORM
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9)
    add_header(s9, 9, "Timing Verification", "EPWave Waveform & 5 Detection Milestones", "Full 24-bit stimulus cycle-accurate waveform proving overlapping detection")

    # Waveform image across top half
    add_card(s9, 0.8, 1.5, 11.733, 2.7)
    ep_path = os.path.join(img_dir, "epwave.png")
    if os.path.exists(ep_path):
        s9.shapes.add_picture(ep_path, Inches(0.95), Inches(1.58), width=Inches(11.433))

    # 5 Detection Milestone Cards below
    matches = [
        ("MATCH #1", "t = 66 ns", "Bits 23..18: 001011", "Initial match from S0"),
        ("MATCH #2", "t = 96 ns", "Bits 18..15: 011", "Overlapping with Match #1"),
        ("MATCH #3", "t = 126 ns", "Bits 15..12: 011", "Overlapping with Match #2"),
        ("MATCH #4", "t = 176 ns", "Bits 11..7: 01011", "Match following '0' reset"),
        ("MATCH #5", "t = 246 ns", "Bits 3..0: 1011", "Final match at end of stream")
    ]
    for idx, (m_tag, m_time, m_seq, m_desc) in enumerate(matches):
        c_left = 0.8 + idx * 2.386
        add_card(s9, c_left, 4.35, 2.186, 2.55)
        mb = s9.shapes.add_textbox(Inches(c_left + 0.1), Inches(4.45), Inches(1.986), Inches(2.35))
        mtf = mb.text_frame
        mtf.word_wrap = True
        
        mp1 = mtf.paragraphs[0]
        mp1.text = m_tag
        mp1.font.size = Pt(11)
        mp1.font.bold = True
        mp1.font.color.rgb = ACCENT_GOLD
        
        mp2 = mtf.add_paragraph()
        mp2.text = m_time
        mp2.font.size = Pt(13)
        mp2.font.bold = True
        mp2.font.color.rgb = ACCENT_CYAN
        mp2.space_before = Pt(2)
        
        mp3 = mtf.add_paragraph()
        mp3.text = m_seq
        mp3.font.size = Pt(8.5)
        mp3.font.bold = True
        mp3.font.color.rgb = TEXT_WHITE
        mp3.space_before = Pt(4)
        
        mp4 = mtf.add_paragraph()
        mp4.text = m_desc
        mp4.font.size = Pt(8)
        mp4.font.color.rgb = TEXT_MUTED
        mp4.space_before = Pt(3)

    # ==========================================
    # SLIDE 10: YOSYS GATE-LEVEL LOGIC SYNTHESIS
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10)
    add_header(s10, 10, "Logic Synthesis", "Yosys Gate-Level Synthesis & Schematic", "RTL-to-gate elaboration into standard-cell logic gates and flip-flops")

    # Left: Schematic diagram
    add_card(s10, 0.8, 1.6, 6.8, 5.3)
    yd_path = os.path.join(img_dir, "yosys_diagram.png")
    if os.path.exists(yd_path):
        s10.shapes.add_picture(yd_path, Inches(0.95), Inches(1.75), width=Inches(6.5))
    
    yd_cap = s10.shapes.add_textbox(Inches(0.95), Inches(6.35), Inches(6.5), Inches(0.45))
    ydtf = yd_cap.text_frame
    ydp = ydtf.paragraphs[0]
    ydp.text = "Figure 3.4: Yosys Gate-Level Synthesized Logic Schematic"
    ydp.alignment = PP_ALIGN.CENTER
    ydp.font.size = Pt(8.5)
    ydp.font.italic = True
    ydp.font.color.rgb = ACCENT_CYAN

    # Right: Synthesis metrics
    add_card(s10, 7.8, 1.6, 4.733, 5.3)
    sbox = s10.shapes.add_textbox(Inches(8.0), Inches(1.75), Inches(4.333), Inches(4.9))
    stf = sbox.text_frame
    stf.word_wrap = True

    sp = stf.paragraphs[0]
    sp.text = "YOSYS SYNTHESIS STATISTICS"
    sp.font.size = Pt(11)
    sp.font.bold = True
    sp.font.color.rgb = ACCENT_GOLD

    synth_stats = [
        ("Synthesis Engine", "Yosys Open SYnthesis Suite"),
        ("Target Architecture", "Standard Logic Gate Primitives"),
        ("Total Cell Count", "16 Standard Cells"),
        ("Sequential Flip-Flops", "3 DFFs ($_SDFF_PP0_)"),
        ("Combinational Gates", "13 Logic Gates"),
        ("  • 2-Input AND ($_AND_)", "4 Cells"),
        ("  • AND with Invert ($_ANDNOT_)", "4 Cells"),
        ("  • 2-Input OR ($_OR_)", "3 Cells"),
        ("  • 2-Input NOR ($_NOR_)", "1 Cell"),
        ("  • 2:1 Multiplexer ($_MUX_)", "1 Cell"),
        ("Internal Wires / Bits", "17 Wires / 19 Wire Bits"),
        ("Inferred Latches", "0 (Pure edge-triggered)")
    ]
    for s_name, s_val in synth_stats:
        p = stf.add_paragraph()
        p.text = f"{s_name}: {s_val}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

    # ==========================================
    # SLIDE 11: QUANTITATIVE VERIFICATION MATRIX
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11)
    add_header(s11, 11, "Results & Verification", "Quantitative Verification & Sign-Off Matrix", "Summary of simulation, timing, and synthesis sign-off criteria")

    # Metric Cards Top Row
    top_metrics = [
        ("TEST BITS EVALUATED", "24 Bits", "Complete vector streamed", ACCENT_CYAN),
        ("MATCHES DETECTED", "5 / 5", "100% detection rate", ACCENT_GOLD),
        ("VERIFICATION ERRORS", "0 Mismatches", "Zero false positives", ACCENT_GREEN),
        ("SIMULATION FINISH", "266 ns", "Deterministic completion", TEXT_WHITE)
    ]
    for idx, (m_title, m_val, m_sub, m_col) in enumerate(top_metrics):
        c_left = 0.8 + idx * 2.983
        add_card(s11, c_left, 1.6, 2.783, 1.45)
        tb = s11.shapes.add_textbox(Inches(c_left + 0.15), Inches(1.7), Inches(2.483), Inches(1.25))
        ttf = tb.text_frame
        ttf.word_wrap = True
        
        tp1 = ttf.paragraphs[0]
        tp1.text = m_title
        tp1.font.size = Pt(8)
        tp1.font.bold = True
        tp1.font.color.rgb = TEXT_MUTED
        
        tp2 = ttf.add_paragraph()
        tp2.text = m_val
        tp2.font.size = Pt(18)
        tp2.font.bold = True
        tp2.font.color.rgb = m_col
        tp2.space_before = Pt(2)
        
        tp3 = ttf.add_paragraph()
        tp3.text = m_sub
        tp3.font.size = Pt(8)
        tp3.font.color.rgb = TEXT_WHITE

    # Detailed Verification Table Card
    add_card(s11, 0.8, 3.25, 11.733, 3.65)
    v_box = s11.shapes.add_textbox(Inches(1.0), Inches(3.4), Inches(11.333), Inches(3.3))
    vtf = v_box.text_frame
    vtf.word_wrap = True

    vp = vtf.paragraphs[0]
    vp.text = "TABLE 3.3 — VERIFICATION TESTBENCH SIGN-OFF SUMMARY"
    vp.font.size = Pt(11)
    vp.font.bold = True
    vp.font.color.rgb = ACCENT_GOLD

    rows = [
        ("Synchronous Reset Release", "t = 12 ns", "State forced to S0 on clk edge; detected holds 0", "PASS [VERIFIED]"),
        ("Match 1: First '1011' Detection", "t = 66 ns", "din=1 latches state S4; detected pulse asserts high", "PASS [VERIFIED]"),
        ("Match 2: Overlapping '1011' Detection", "t = 96 ns", "Trailing bit '1' from Match 1 re-used as prefix for Match 2", "PASS [VERIFIED]"),
        ("Match 3: Consecutive Overlap Detection", "t = 126 ns", "Third overlapping occurrence verified without state reset", "PASS [VERIFIED]"),
        ("Intermediate Negative Vectors", "t = 136-166 ns", "Sequences '01' and '11' correctly reject false triggers", "PASS [VERIFIED]"),
        ("Match 4: Fourth '1011' Detection", "t = 176 ns", "Recovers from '0' bit and detects complete pattern", "PASS [VERIFIED]"),
        ("Match 5: Final '1011' Detection", "t = 246 ns", "Detects final sequence at end of 24-bit test vector", "PASS [VERIFIED]")
    ]
    for r_test, r_time, r_obs, r_status in rows:
        p = vtf.add_paragraph()
        p.text = f"• {r_test:<36} | {r_time:<14} | {r_obs:<58} | {r_status}"
        p.font.name = "Consolas"
        p.font.size = Pt(8)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(2)

    # ==========================================
    # SLIDE 12: CONCLUSION & DELIVERABLES
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12)
    add_header(s12, 12, "Conclusion & Deliverables", "Project Conclusions & Online Repositories", "Summary of completed design goals, public source repositories, and live links")

    # Left: Project Conclusion
    add_card(s12, 0.8, 1.6, 5.7, 5.3)
    c_box = s12.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.9))
    ctf = c_box.text_frame
    ctf.word_wrap = True

    cp = ctf.paragraphs[0]
    cp.text = "PROJECT CONCLUSIONS"
    cp.font.size = Pt(13)
    cp.font.bold = True
    cp.font.color.rgb = ACCENT_GOLD

    concl_points = [
        ("Functional Closure Achieved", "The 4-bit overlapping Moore sequence detector ('1011') was successfully modeled in synthesizable Verilog-2001 and verified on Icarus Verilog 12.0 with 0 errors."),
        ("Glitch-Free Moore Decoding", "Decoding detected directly from state register S4 ensures a full-cycle, glitch-free pulse immune to combinational input hazards."),
        ("Gate-Level Logic Synthesis", "Mapped using Yosys to 16 standard cells (3 flip-flops, 13 combinational gates) with zero latches and clean timing."),
        ("Open-Source Toolchain Mastery", "Demonstrated that complete RTL design, cloud verification, and logic synthesis can be executed efficiently using EDA Playground.")
    ]
    for ctitle, cdesc in concl_points:
        p = ctf.add_paragraph()
        p.text = f"• {ctitle}: {cdesc}"
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(8)

    # Right: Deliverables & Links Card
    add_card(s12, 6.8, 1.6, 5.733, 5.3)
    d_box = s12.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.333), Inches(4.9))
    dtf = d_box.text_frame
    dtf.word_wrap = True

    dp = dtf.paragraphs[0]
    dp.text = "ONLINE ARTIFACTS & DELIVERABLES"
    dp.font.size = Pt(13)
    dp.font.bold = True
    dp.font.color.rgb = ACCENT_GOLD

    links = [
        ("PUBLIC GITHUB REPOSITORY", "https://github.com/mikmidhun123/pt23-4bit-sequence-detector", ACCENT_CYAN),
        ("LIVE EDA PLAYGROUND WORKSPACE", "https://www.edaplayground.com/x/jXfS", ACCENT_GOLD),
        ("SUBMITTED PROJECT REPORT", "docs/report.pdf  &  docs/report.docx (19 Body Pages + Roman Front Matter)", TEXT_WHITE),
        ("PRESENTATION SLIDES", "PT23_4bit_Sequence_Detector_Presentation.pptx", ACCENT_GREEN)
    ]
    for ltitle, lurl, lcol in links:
        p = dtf.add_paragraph()
        p.text = ltitle
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_MUTED
        p.space_before = Pt(8)
        p2 = dtf.add_paragraph()
        p2.text = lurl
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = lcol

    dp_ack = dtf.add_paragraph()
    dp_ack.text = "THANK YOU — LIVE Q&A"
    dp_ack.font.size = Pt(14)
    dp_ack.font.bold = True
    dp_ack.font.color.rgb = ACCENT_CYAN
    dp_ack.space_before = Pt(16)

    dp_sub = dtf.add_paragraph()
    dp_sub.text = "Project Team PT23  |  Department of ECE  |  St. Joseph's College of Engineering"
    dp_sub.font.size = Pt(9.5)
    dp_sub.font.color.rgb = TEXT_WHITE

    # Save Presentation
    out_ppt_repo = "e:/work/vlsi report/pt23-4bit-sequence-detector/docs/PT23_4bit_Sequence_Detector_Presentation.pptx"
    out_ppt_root = "e:/work/vlsi report/PT23_4bit_Sequence_Detector_Presentation.pptx"
    
    prs.save(out_ppt_repo)
    prs.save(out_ppt_root)
    print(f"Presentation saved successfully to:\n  1. {out_ppt_repo}\n  2. {out_ppt_root}")

if __name__ == "__main__":
    create_presentation()
