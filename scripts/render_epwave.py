import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def render_epwave():
    vcd_path = 'pt23-4bit-sequence-detector/tb/dump.vcd'
    with open(vcd_path, 'r') as f:
        lines = f.readlines()

    events = []
    time_ps = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            time_ps = int(line[1:])
        elif line.startswith('b'):
            parts = line.split()
            val_str = parts[0][1:]
            sid = parts[1]
            try:
                val = int(val_str, 2)
            except ValueError:
                val = 0
            events.append((time_ps / 1000.0, sid, val))
        elif len(line) >= 2 and line[0] in '01':
            val = int(line[0])
            sid = line[1:]
            events.append((time_ps / 1000.0, sid, val))

    events.sort(key=lambda x: x[0])

    # Time from 0 to 266 ns
    t_max = 266.0
    t_grid = np.linspace(0, t_max, 2661) # 0.1 ns resolution

    clk_vals, rst_vals, din_vals, det_vals, st_vals = [], [], [], [], []
    c_clk, c_rst, c_din, c_det, c_st = 0, 0, 0, 0, 0
    ev_idx = 0

    for t in t_grid:
        while ev_idx < len(events) and events[ev_idx][0] <= t:
            tev, sid, val = events[ev_idx]
            if sid == '"':
                c_clk = val
            elif sid == '$':
                c_rst = val
            elif sid == '#':
                c_din = val
            elif sid == '!':
                c_det = val
            elif sid == '1':
                c_st = val
            ev_idx += 1
        clk_vals.append(c_clk)
        rst_vals.append(c_rst)
        din_vals.append(c_din)
        det_vals.append(c_det)
        st_vals.append(c_st)

    # Now create the EPWave styling figure
    fig = plt.figure(figsize=(16, 8.5), facecolor='#11151c', dpi=150)
    
    # GridSpec: left for signal names/values, right for waveforms
    gs = fig.add_gridspec(1, 2, width_ratios=[1.8, 10.2], wspace=0.0)

    # 1. Left Panel (Signal Names & Current Values)
    ax_names = fig.add_subplot(gs[0])
    ax_names.set_facecolor('#1a1f29')
    ax_names.set_xlim(0, 10)
    ax_names.set_ylim(-0.5, 5.5)
    ax_names.axis('off')

    # Header in left panel
    ax_names.text(0.5, 5.2, 'SIGNAL NAME', color='#94a3b8', fontsize=9, fontweight='bold', fontfamily='sans-serif')
    ax_names.text(7.5, 5.2, 'RADIX', color='#94a3b8', fontsize=9, fontweight='bold', fontfamily='sans-serif')

    signals_meta = [
        ('detected', '1-bit', 0.5, '#22c55e', '0'),
        ('dut.state[2:0]', 'enum', 1.5, '#38bdf8', 'S0'),
        ('din', '1-bit', 2.5, '#eab308', '1'),
        ('rst', '1-bit', 3.5, '#f43f5e', '0'),
        ('clk', '1-bit', 4.5, '#06b6d4', '1'),
    ]

    for name, radix, y, col, val in signals_meta:
        # Subtle horizontal separator
        ax_names.axhline(y - 0.45, color='#2d3748', linewidth=0.8)
        # Signal name
        ax_names.text(0.6, y, name, color=col, fontsize=10.5, fontweight='bold', va='center', fontfamily='monospace')
        ax_names.text(7.5, y, radix, color='#cbd5e1', fontsize=9, va='center', fontfamily='sans-serif')

    # 2. Right Panel (Waveforms)
    ax_wave = fig.add_subplot(gs[1])
    ax_wave.set_facecolor('#0d1117')
    ax_wave.set_xlim(0, 270)
    ax_wave.set_ylim(-0.5, 5.5)

    # Time ticks
    major_ticks = np.arange(0, 271, 20)
    minor_ticks = np.arange(0, 271, 10)
    ax_wave.set_xticks(major_ticks)
    ax_wave.set_xticks(minor_ticks, minor=True)
    ax_wave.tick_params(axis='x', colors='#94a3b8', labelsize=9.5, which='both')
    ax_wave.grid(which='major', color='#21262d', linestyle='-', linewidth=0.9)
    ax_wave.grid(which='minor', color='#161b22', linestyle=':', linewidth=0.6)
    ax_wave.set_xlabel('Time (ns)  [Simulation Timescale: 1ns / 1ps]', color='#94a3b8', fontsize=10, labelpad=8)
    ax_wave.set_yticks([])

    # Plot digital signals
    # y positions:
    # clk: base 4.1, height 0.8
    # rst: base 3.1, height 0.8
    # din: base 2.1, height 0.8
    # state: base 1.1, height 0.8 (bus)
    # detected: base 0.1, height 0.8

    # Background row bands
    for y_base in [0.05, 1.05, 2.05, 3.05, 4.05]:
        ax_wave.axhspan(y_base, y_base + 0.9, color='#161b22', alpha=0.3)
        ax_wave.axhline(y_base - 0.05, color='#21262d', linewidth=0.8)

    # 1. clk
    y_clk = 4.1 + np.array(clk_vals) * 0.75
    ax_wave.step(t_grid, y_clk, where='post', color='#06b6d4', linewidth=1.4)

    # 2. rst
    y_rst = 3.1 + np.array(rst_vals) * 0.75
    ax_wave.step(t_grid, y_rst, where='post', color='#f43f5e', linewidth=1.4)

    # 3. din
    y_din = 2.1 + np.array(din_vals) * 0.75
    ax_wave.step(t_grid, y_din, where='post', color='#eab308', linewidth=1.4)

    # 4. state bus: find state transition times
    state_changes = []
    prev_st = None
    for t, st in zip(t_grid, st_vals):
        if st != prev_st:
            state_changes.append((t, st))
            prev_st = st
    state_changes.append((266.0, prev_st))

    state_names = {0: 'S0 (000)', 1: 'S1 (001)', 2: 'S2 (010)', 3: 'S3 (011)', 4: 'S4 (100)'}

    for i in range(len(state_changes) - 1):
        t_start, st_val = state_changes[i]
        t_end, _ = state_changes[i+1]
        if t_end <= t_start:
            continue
        
        # Draw bus hexagon / polygon
        h_top = 1.85
        h_bot = 1.15
        h_mid = 1.5
        dt_t = min(0.6, (t_end - t_start) * 0.2)
        
        # Fill polygon
        poly_pts = [
            [t_start + dt_t, h_top],
            [t_end - dt_t, h_top],
            [t_end, h_mid],
            [t_end - dt_t, h_bot],
            [t_start + dt_t, h_bot],
            [t_start, h_mid]
        ]
        poly = patches.Polygon(poly_pts, closed=True, facecolor='#0369a1', edgecolor='#38bdf8', linewidth=1.2, alpha=0.85)
        ax_wave.add_patch(poly)

        # Label state inside if wide enough
        if (t_end - t_start) >= 6:
            lbl = f"S{st_val}" if (t_end - t_start) < 12 else state_names.get(st_val, f"S{st_val}")
            ax_wave.text((t_start + t_end) / 2.0, h_mid, lbl, color='#f0f9ff', fontsize=8.5,
                         ha='center', va='center', fontweight='bold', fontfamily='monospace')

    # 5. detected signal
    y_det = 0.1 + np.array(det_vals) * 0.75
    ax_wave.step(t_grid, y_det, where='post', color='#22c55e', linewidth=1.6)

    # Detection milestones annotation
    matches = [
        (66, 'Match #1\n(66ns)'),
        (96, 'Match #2 (Overlap)\n(96ns)'),
        (126, 'Match #3 (Overlap)\n(126ns)'),
        (176, 'Match #4\n(176ns)'),
        (246, 'Match #5\n(246ns)'),
    ]

    for t_m, label in matches:
        ax_wave.axvline(t_m, color='#22c55e', linestyle='--', linewidth=1.2, alpha=0.8)
        ax_wave.scatter([t_m], [0.85], color='#22c55e', s=45, zorder=5)
        ax_wave.annotate(label, xy=(t_m, 0.85), xytext=(t_m - 3, 0.15),
                         fontsize=7.5, color='#86efac', fontweight='bold',
                         arrowprops=dict(arrowstyle='->', color='#22c55e', lw=1.0),
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='#064e3b', edgecolor='#22c55e', alpha=0.9))

    # Reset annotation
    ax_wave.axvline(12, color='#f43f5e', linestyle=':', linewidth=1.2)
    ax_wave.annotate('Reset Release\n(t=12ns)', xy=(12, 3.85), xytext=(15, 3.2),
                     fontsize=7.5, color='#fda4af', fontweight='bold',
                     arrowprops=dict(arrowstyle='->', color='#f43f5e', lw=0.9),
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#881337', edgecolor='#f43f5e', alpha=0.85))

    # Finish annotation
    ax_wave.axvline(266, color='#94a3b8', linestyle=':', linewidth=1.2)
    ax_wave.text(265, 5.0, '$finish (266ns)', color='#cbd5e1', fontsize=8, ha='right', va='center',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#1e293b', edgecolor='#475569'))

    # Title header banner
    plt.suptitle('EDA Playground EPWave — 4-bit Sequence Detector (1011 Moore FSM Overlapping Waveform)',
                 color='#f8fafc', fontsize=12, fontweight='bold', y=0.98, fontfamily='sans-serif')

    out_path = 'pt23-4bit-sequence-detector/images/epwave.png'
    plt.savefig(out_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight', pad_inches=0.15)
    plt.close()
    print('Successfully generated epwave.png!')

if __name__ == '__main__':
    render_epwave()
