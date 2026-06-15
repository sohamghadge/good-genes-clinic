import re

with open('index.html', 'r') as f:
    content = f.read()

# Replace the entire chronicles section
old_chronicles_section = re.search(r'<section id="chronicles".*?</section>', content, re.DOTALL).group(0)

new_chronicles_section = """
  <section id="chronicles" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px); position:relative; overflow:hidden;">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px); position:relative; z-index:10;">
      <div>
        <span data-reveal style="display:block; font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.3em; text-transform:uppercase; color:rgba(28,26,23,0.45); margin-bottom:12px;">Chronicles</span>
        <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(40px,5vw,72px); line-height:1.0; letter-spacing:-0.018em;">The <span style="font-style:italic;">Patina</span> of Trust</h2>
      </div>
      <div data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; color:rgba(28,26,23,0.45);">
        0{{ activeChronicle + 1 }} / 0{{ chronicles.length }}
      </div>
    </div>

    <div data-reveal style="position:relative; min-height:460px; display:flex; align-items:center;">
      <sc-for list="{{ chronicles }}" as="c">
        <div style="position:absolute; top:0; left:0; width:100%; display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap; opacity:{{ $index === activeChronicle ? '1' : '0' }}; visibility:{{ $index === activeChronicle ? 'visible' : 'hidden' }}; transition:opacity 0.8s ease, visibility 0.8s ease; z-index:{{ $index === activeChronicle ? '5' : '1' }}; pointer-events:{{ $index === activeChronicle ? 'auto' : 'none' }};">
          
          <div style="flex:1 1 400px; max-width:750px;">
            <p style="margin:0 0 40px; font-family:'Cormorant Garamond', Georgia, serif; font-size:clamp(26px,3vw,46px); line-height:1.4; font-style:italic; font-weight:300; color:#1C1A17;">{{ c.quote }}</p>
            <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; text-transform:uppercase; color:rgba(28,26,23,0.4);">&mdash; {{ c.author }}</span>
          </div>

          <div style="flex:0 1 360px; width:100%;">
            <div style="width:100%; aspect-ratio:3/4; border-radius:12px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.08);">
              <img src="{{ c.img }}" style="width:100%; height:100%; object-fit:cover;" alt="Patient" />
            </div>
          </div>
          
        </div>
      </sc-for>
    </div>

    <div style="display:flex; gap:16px; margin-top:24px; position:relative; z-index:10;">
      <button onClick="{{ prevChronicle }}" style="background:none; border:1px solid rgba(28,26,23,0.2); width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; transition:border-color 0.3s ease; color:#1C1A17;" style-hover="border-color:#1C1A17;">
        <span style="font-family:serif; font-size:20px;">&#8592;</span>
      </button>
      <button onClick="{{ nextChronicle }}" style="background:none; border:1px solid rgba(28,26,23,0.2); width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; cursor:pointer; transition:border-color 0.3s ease; color:#1C1A17;" style-hover="border-color:#1C1A17;">
        <span style="font-family:serif; font-size:20px;">&#8594;</span>
      </button>
    </div>
  </section>
"""

content = content.replace(old_chronicles_section, new_chronicles_section)

# Update State
content = content.replace("state = { openMod: 0, openFaq: 0, name: '', concern: '', submitted: false, waOpen: false };", "state = { openMod: 0, openFaq: 0, name: '', concern: '', submitted: false, waOpen: false, activeChronicle: 0 };")

# Add Chronicles Data to renderVals
render_vals_injection = """
    const chroniclesData = [
      { quote: "“I have sat in many chairs across many cities. This is the first where the doctor seemed more interested in the decade ahead than the appointment in front of her.”", author: "VERIFIED PATIENT RECORD VIA PRACTO", img: "assets/patient-1.png" },
      { quote: "“The clinic atmosphere is incredibly calming, and Dr. Dipti's approach to youth preservation is meticulous. I felt completely informed throughout the entire protocol.”", author: "VERIFIED PATIENT RECORD VIA GOOGLE", img: "assets/patient-2.png" },
      { quote: "“A true boutique experience. It’s rare to find a practitioner who listens this closely and executes with such exactitude. My results are balanced and entirely natural.”", author: "VERIFIED PATIENT RECORD VIA GOOGLE", img: "assets/patient-3.png" }
    ];
    const chronicles = chroniclesData;

    this._syncMod();
"""
content = content.replace("this._syncMod();", render_vals_injection, 1)

# Add logic to return
return_injection = """      faqs,
      chronicles,
      activeChronicle: this.state.activeChronicle,
      nextChronicle: () => this.setState((s) => ({ activeChronicle: (s.activeChronicle + 1) % chronicles.length })),
      prevChronicle: () => this.setState((s) => ({ activeChronicle: (s.activeChronicle - 1 + chronicles.length) % chronicles.length })),
"""
content = content.replace("faqs,", return_injection)

with open('index.html', 'w') as f:
    f.write(content)
