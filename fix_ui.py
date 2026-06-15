import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Fix Chronicles: Remove the patient images and center the quotes
old_chronicles_slider = re.search(r'<div data-reveal style="position:relative; min-height:460px; display:flex; align-items:center;">.*?</sc-for>\n    </div>', content, re.DOTALL).group(0)

new_chronicles_slider = """<div data-reveal style="position:relative; min-height:300px; display:flex; align-items:center; justify-content:center;">
      <sc-for list="{{ chronicles }}" as="c">
        <div style="position:absolute; top:0; left:0; width:100%; display:flex; align-items:center; justify-content:center; text-align:center; opacity:{{ $index === activeChronicle ? '1' : '0' }}; visibility:{{ $index === activeChronicle ? 'visible' : 'hidden' }}; transition:opacity 0.8s ease, visibility 0.8s ease; z-index:{{ $index === activeChronicle ? '5' : '1' }}; pointer-events:{{ $index === activeChronicle ? 'auto' : 'none' }};">
          
          <div style="max-width:900px; margin:0 auto;">
            <p style="margin:0 0 40px; font-family:'Cormorant Garamond', Georgia, serif; font-size:clamp(26px,3.5vw,52px); line-height:1.4; font-style:italic; font-weight:300; color:#1C1A17;">{{ c.quote }}</p>
            <span style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.2em; text-transform:uppercase; color:rgba(28,26,23,0.4);">&mdash; {{ c.author }}</span>
          </div>

        </div>
      </sc-for>
    </div>"""

content = content.replace(old_chronicles_slider, new_chronicles_slider)

# Also center the arrows
content = content.replace('<div style="display:flex; gap:16px; margin-top:24px; position:relative; z-index:10;">', '<div style="display:flex; gap:16px; margin-top:24px; position:relative; z-index:10; justify-content:center;">')

# 2. Fix Doctor Image Layout (remove aspect-ratio and object-fit)
old_doctor_img = """<div style="position:relative; width:100%; aspect-ratio:3/4; border-radius:12px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.1);">
          <img src="assets/dr_dipti.png" style="width:100%; height:100%; object-fit:cover;" alt="Dr. Dipti Mathias" />
        </div>"""

new_doctor_img = """<div style="position:relative; width:100%; border-radius:12px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.1);">
          <img src="assets/dr_dipti.jpg" style="width:100%; height:auto; display:block;" alt="Dr. Dipti Mathias" />
        </div>"""

content = content.replace(old_doctor_img, new_doctor_img)

with open('index.html', 'w') as f:
    f.write(content)
