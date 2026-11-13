import os
import sys
import time
from playwright.sync_api import sync_playwright

WORKSPACE = r"e:\work\vlsi report\pt23-4bit-sequence-detector"
DESIGN_FILE = os.path.join(WORKSPACE, "rtl", "design.sv")
TB_FILE = os.path.join(WORKSPACE, "tb", "testbench.sv")
SCREENSHOTS_DIR = os.path.join(WORKSPACE, "images")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

with open(DESIGN_FILE, "r", encoding="utf-8") as f:
    design_code = f.read()

with open(TB_FILE, "r", encoding="utf-8") as f:
    tb_code = f.read()

print("Launching browser...", flush=True)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1600, "height": 950})
    page = context.new_page()

    print("Navigating to https://www.edaplayground.com ...", flush=True)
    page.goto("https://www.edaplayground.com", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    # Set content of CodeMirror editors
    page.evaluate("""([ds, tb]) => {
        const dEd = document.querySelector('#design-editor .CodeMirror');
        if (dEd && dEd.CodeMirror) {
            dEd.CodeMirror.setValue(ds);
        } else {
            const el = document.getElementById('design');
            if (el) el.value = ds;
        }

        const tEd = document.querySelector('#testbench-editor .CodeMirror');
        if (tEd && tEd.CodeMirror) {
            tEd.CodeMirror.setValue(tb);
        } else {
            const el = document.getElementById('testbench');
            if (el) el.value = tb;
        }
    }""", [design_code, tb_code])
    print("Set design and testbench code.", flush=True)

    # Select Icarus Verilog 12.0 (value '7') directly via JS
    page.evaluate("""() => {
        const sel = document.getElementById('simulator');
        if (sel) {
            sel.value = '7';
            sel.dispatchEvent(new Event('change', { bubbles: true }));
        }
        // Check "Open EPWave after run"
        const cb = document.getElementById('waves') || document.querySelector('input[name="waves"]');
        if (cb) {
            cb.checked = true;
            cb.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""")
    print("Configured Icarus Verilog 12.0 and Open EPWave.", flush=True)
    page.wait_for_timeout(1000)

    # Take screenshot of editor
    page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "editor.png"))
    print("Saved editor.png", flush=True)

    # Click Run
    print("Clicking Run button...", flush=True)
    page.evaluate("""() => {
        const btn = document.getElementById('runButton') || document.querySelector('button[title*="Run"]');
        if (btn) btn.click();
    }""")

    # Wait up to 15 seconds for simulation to finish
    for sec in range(15):
        page.wait_for_timeout(1000)
        log_text = page.evaluate("""() => {
            const l = document.getElementById('log');
            return l ? l.innerText : '';
        }""")
        if "$finish" in log_text or "Exit code expected: 0" in log_text or "Done" in log_text:
            print(f"Simulation finished at {sec+1}s!", flush=True)
            break
        # Also check for modal
        modal_txt = page.evaluate("""() => {
            const m = document.querySelector('.modal.in, #loginModal.in');
            return m ? m.innerText : '';
        }""")
        if modal_txt:
            print(f"Modal appeared: {modal_txt[:100]}", flush=True)
            break

    log_text = page.evaluate("""() => {
        const l = document.getElementById('log');
        return l ? l.innerText : '';
    }""")
    print("Log text length:", len(log_text), flush=True)
    print("Log content:\n" + log_text, flush=True)
    with open(os.path.join(SCREENSHOTS_DIR, "simulation.log"), "w", encoding="utf-8") as f:
        f.write(log_text)

    # Capture log area screenshot
    page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "log.png"))
    print("Saved log.png", flush=True)

    # Check for EPWave
    page.wait_for_timeout(3000)
    frames = page.frames
    print("Total frames:", len(frames), flush=True)
    for f in frames:
        print("Frame URL:", f.url, flush=True)

    browser.close()
