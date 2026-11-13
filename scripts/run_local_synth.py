import os
import sys
import yowasp_yosys

WORKSPACE = r"e:\work\vlsi report\pt23-4bit-sequence-detector"
SYNTH_DIR = os.path.join(WORKSPACE, "synth")
os.makedirs(SYNTH_DIR, exist_ok=True)

ys_script = """
read_verilog rtl/design.sv
hierarchy -check -top seq_detector
proc; opt; fsm; opt; memory; opt; techmap; opt; abc; opt_clean; stat
write_verilog -noattr synth/seq_detector_netlist.v
show -format dot -prefix synth/seq_detector_schematic
"""

with open(os.path.join(SYNTH_DIR, "synth.ys"), "w", encoding="utf-8") as f:
    f.write(ys_script.strip() + "\n")

print("Running Yosys...")
cwd = os.getcwd()
os.chdir(WORKSPACE)
rc = yowasp_yosys.run_yosys(["-l", "synth/yosys_synthesis.log", "-s", "synth/synth.ys"])
os.chdir(cwd)
print("Yosys exit code:", rc)
