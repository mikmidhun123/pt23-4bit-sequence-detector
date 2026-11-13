import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_block_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), facecolor='white', dpi=200)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Main Module Box
    main_box = patches.FancyBboxPatch((3.0, 0.8), 4.2, 3.4, boxstyle="round,pad=0.2",
                                      facecolor='#eff6ff', edgecolor='#1e40af', linewidth=2.0)
    ax.add_patch(main_box)
    ax.text(5.1, 4.35, "seq_detector (Moore FSM)", fontsize=13, fontweight='bold',
            color='#1e3a8a', ha='center', va='center', fontfamily='sans-serif')

    # Internal Blocks
    # 1. State Register
    reg_box = patches.Rectangle((3.3, 1.2), 1.6, 1.5, facecolor='#dbeafe', edgecolor='#2563eb', linewidth=1.5)
    ax.add_patch(reg_box)
    ax.text(4.1, 2.0, "State Register\n(3x DFFs)\n[state]", fontsize=8.5, ha='center', va='center',
            color='#1e40af', fontweight='bold', fontfamily='sans-serif')

    # 2. Next-State Logic
    nsl_box = patches.Rectangle((3.3, 2.9), 1.6, 1.1, facecolor='#e0f2fe', edgecolor='#0284c7', linewidth=1.5)
    ax.add_patch(nsl_box)
    ax.text(4.1, 3.45, "Next-State\nLogic (case)", fontsize=8.5, ha='center', va='center',
            color='#0369a1', fontweight='bold', fontfamily='sans-serif')

    # 3. Moore Output Logic
    out_box = patches.Rectangle((5.3, 1.8), 1.6, 1.4, facecolor='#fef08a', edgecolor='#ca8a04', linewidth=1.5)
    ax.add_patch(out_box)
    ax.text(6.1, 2.5, "Moore Output\nLogic\n(state == S4)", fontsize=8.5, ha='center', va='center',
            color='#854d0e', fontweight='bold', fontfamily='sans-serif')

    # Internal Connections
    # NSL to Reg
    ax.annotate("", xy=(3.8, 2.7), xytext=(3.8, 2.9),
                arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.5))
    ax.text(3.7, 2.8, "next_state", fontsize=7.5, color="#1e40af", ha='right', va='center')

    # Reg to NSL feedback
    ax.annotate("", xy=(4.6, 2.9), xytext=(4.6, 2.7),
                arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.5))
    ax.text(4.7, 2.8, "state", fontsize=7.5, color="#1e40af", ha='left', va='center')

    # Reg to Output
    ax.annotate("", xy=(5.3, 2.5), xytext=(4.9, 2.0),
                arrowprops=dict(arrowstyle="->", color="#1e40af", lw=1.5))
    ax.text(5.05, 2.3, "state", fontsize=8, color="#1e40af", ha='center', va='bottom')

    # External Inputs
    # clk
    ax.annotate("", xy=(3.0, 1.6), xytext=(1.2, 1.6),
                arrowprops=dict(arrowstyle="->", color="#0f172a", lw=2.0))
    ax.text(1.1, 1.6, "clk (100MHz)", fontsize=10, fontweight='bold', color="#0f172a", ha='right', va='center')

    # rst
    ax.annotate("", xy=(3.0, 2.2), xytext=(1.2, 2.2),
                arrowprops=dict(arrowstyle="->", color="#e11d48", lw=2.0))
    ax.text(1.1, 2.2, "rst (Sync Active-High)", fontsize=10, fontweight='bold', color="#e11d48", ha='right', va='center')

    # din
    ax.annotate("", xy=(3.0, 3.45), xytext=(1.2, 3.45),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=2.0))
    ax.text(1.1, 3.45, "din (Serial Bit In)", fontsize=10, fontweight='bold', color="#d97706", ha='right', va='center')

    # External Output
    # detected
    ax.annotate("", xy=(8.8, 2.5), xytext=(7.2, 2.5),
                arrowprops=dict(arrowstyle="->", color="#15803d", lw=2.2))
    ax.text(8.9, 2.5, "detected\n(Active-High 1-bit)", fontsize=10, fontweight='bold', color="#15803d", ha='left', va='center')

    plt.tight_layout()
    plt.savefig('pt23-4bit-sequence-detector/images/block_diagram.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated block_diagram.png")

def draw_state_diagram():
    fig, ax = plt.subplots(figsize=(11, 4.5), facecolor='white', dpi=200)
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(-1.8, 2.2)
    ax.axis('off')

    states = [
        (0.8, 0.0, "S0\n000\nout=0"),
        (2.8, 0.0, "S1\n001\nout=0"),
        (4.8, 0.0, "S2\n010\nout=0"),
        (6.8, 0.0, "S3\n011\nout=0"),
        (8.8, 0.0, "S4\n100\nout=1"),
    ]

    r = 0.55
    for x, y, label in states:
        color = '#dcfce7' if 'out=1' in label else '#e0f2fe'
        border = '#16a34a' if 'out=1' in label else '#0284c7'
        circle = patches.Circle((x, y), r, facecolor=color, edgecolor=border, linewidth=2.0, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, label, ha='center', va='center', fontsize=8, fontweight='bold',
                color='#15803d' if 'out=1' in label else '#0369a1', zorder=4)

    # Reset arrow to S0
    ax.annotate("", xy=(0.8, r), xytext=(0.8, 1.4),
                arrowprops=dict(arrowstyle="->", color="#e11d48", lw=2.0))
    ax.text(0.8, 1.5, "rst=1", fontsize=9, fontweight='bold', color="#e11d48", ha='center', va='bottom')

    # Forward transitions:
    # S0 -> S1 (din=1)
    ax.annotate("", xy=(2.8 - r, 0.15), xytext=(0.8 + r, 0.15),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.8))
    ax.text(1.8, 0.35, "1", fontsize=10, fontweight='bold', color="#0284c7", ha='center')

    # S1 -> S2 (din=0)
    ax.annotate("", xy=(4.8 - r, 0.15), xytext=(2.8 + r, 0.15),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.8))
    ax.text(3.8, 0.35, "0", fontsize=10, fontweight='bold', color="#0284c7", ha='center')

    # S2 -> S3 (din=1)
    ax.annotate("", xy=(6.8 - r, 0.15), xytext=(4.8 + r, 0.15),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.8))
    ax.text(5.8, 0.35, "1", fontsize=10, fontweight='bold', color="#0284c7", ha='center')

    # S3 -> S4 (din=1)
    ax.annotate("", xy=(8.8 - r, 0.15), xytext=(6.8 + r, 0.15),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=2.0))
    ax.text(7.8, 0.35, "1", fontsize=10, fontweight='bold', color="#16a34a", ha='center')

    # Self-loops & Backward transitions:
    # S0 -> S0 (din=0) loop
    loop_s0 = patches.Arc((0.8, -r - 0.2), 0.5, 0.5, angle=0, theta1=20, theta2=340, color="#64748b", lw=1.5)
    ax.add_patch(loop_s0)
    ax.annotate("", xy=(0.8 + 0.15, -r), xytext=(0.8 + 0.25, -r - 0.2),
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5))
    ax.text(0.8, -r - 0.6, "0", fontsize=9.5, fontweight='bold', color="#64748b", ha='center')

    # S1 -> S1 (din=1) loop
    loop_s1 = patches.Arc((2.8, r + 0.2), 0.5, 0.5, angle=0, theta1=20, theta2=340, color="#64748b", lw=1.5)
    ax.add_patch(loop_s1)
    ax.annotate("", xy=(2.8 - 0.15, r), xytext=(2.8 - 0.25, r + 0.2),
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5))
    ax.text(2.8, r + 0.55, "1", fontsize=9.5, fontweight='bold', color="#64748b", ha='center')

    # S2 -> S0 (din=0) arc below
    ax.annotate("", xy=(0.8 + 0.2, -r), xytext=(4.8 - 0.2, -r),
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5,
                                connectionstyle="arc3,rad=0.35"))
    ax.text(2.8, -1.15, "din=0", fontsize=8.5, fontweight='bold', color="#64748b", ha='center')

    # S3 -> S2 (din=0) arc below
    ax.annotate("", xy=(4.8 + 0.2, -r), xytext=(6.8 - 0.2, -r),
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.5,
                                connectionstyle="arc3,rad=0.35"))
    ax.text(5.8, -0.9, "din=0", fontsize=8.5, fontweight='bold', color="#64748b", ha='center')

    # S4 -> S1 (din=1) Overlapping detection arc above!
    ax.annotate("", xy=(2.8 + 0.2, r), xytext=(8.8 - 0.2, r),
                arrowprops=dict(arrowstyle="->", color="#059669", lw=1.8,
                                connectionstyle="arc3,rad=-0.4"))
    ax.text(5.8, 1.45, "din=1 (Overlap: suffix '1' is prefix)", fontsize=8.5, fontweight='bold', color="#059669", ha='center')

    # S4 -> S2 (din=0) Overlapping detection arc below!
    ax.annotate("", xy=(4.8 + 0.35, -r), xytext=(8.8 - 0.2, -r),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.8,
                                connectionstyle="arc3,rad=0.45"))
    ax.text(6.8, -1.5, "din=0 (prefix '10' matched)", fontsize=8.5, fontweight='bold', color="#d97706", ha='center')

    plt.tight_layout()
    plt.savefig('pt23-4bit-sequence-detector/images/state_diagram.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("Generated state_diagram.png")

if __name__ == '__main__':
    draw_block_diagram()
    draw_state_diagram()
