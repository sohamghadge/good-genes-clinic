import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update Navbar
old_nav = """<div style="max-width:1440px; margin:0 auto; padding:18px clamp(24px,6vw,120px); display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;">
      <a href="#top" style="text-decoration:none; display:flex; align-items:center;">
        <img src="assets/logo.png" alt="Good Genes Clinic" style="height:120px; margin:-36px 0; mix-blend-mode: multiply;" />
      </a>"""

new_nav = """<div style="max-width:1440px; margin:0 auto; padding:0 clamp(24px,6vw,120px); min-height:84px; display:flex; align-items:center; justify-content:space-between; gap:24px; flex-wrap:wrap;">
      <a href="#top" style="text-decoration:none; display:flex; align-items:center; background:#fff; padding:24px 28px; margin-bottom:-24px; align-self:flex-start; box-shadow:0 12px 30px rgba(0,0,0,0.06); position:relative; z-index:10; border-radius:0 0 8px 8px;">
        <img src="assets/logo.png" alt="Good Genes Clinic" style="height:56px;" />
      </a>"""

content = content.replace(old_nav, new_nav)

# 2. Insert Featured In below Hero
featured_in = """
  <section id="featured-in" style="border-top:1px solid rgba(28,26,23,0.15); padding:40px 0; overflow:hidden; background:rgba(255,255,255,0.4);">
    <div style="max-width:1440px; margin:0 auto; padding:0 clamp(24px,6vw,120px); display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap; opacity:0.6; font-family:'Cormorant Garamond', Georgia, serif; font-size:24px; letter-spacing:0.05em; text-transform:uppercase;">
      <span>Vogue</span>
      <span>Elle</span>
      <span>Harper's Bazaar</span>
      <span>Cosmopolitan</span>
      <span>GQ</span>
    </div>
  </section>
"""
content = content.replace('  </section>\n\n  <section id="clinic"', '  </section>\n' + featured_in + '\n  <section id="clinic"')

# 3. Insert Intro Video below Clinic Atmosphere
intro_video = """
  <section id="intro-video" style="max-width:1440px; margin:0 auto; padding:clamp(80px,12vw,160px) clamp(24px,6vw,120px);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(40px,6vw,80px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">The <span style="font-style:italic;">Philosophy</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">Introductory Film</span>
    </div>
    <div data-reveal style="position:relative; width:100%; aspect-ratio:16/9; background:#EEE9D8; border-radius:12px; display:flex; align-items:center; justify-content:center; box-shadow:0 20px 60px rgba(28,26,23,0.1); cursor:pointer; overflow:hidden;">
      <div style="width:80px; height:80px; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(0,0,0,0.1); z-index:2;">
        <span style="display:inline-block; margin-left:6px; border-left:16px solid #1C1A17; border-top:10px solid transparent; border-bottom:10px solid transparent;"></span>
      </div>
      <span style="position:absolute; bottom:24px; left:32px; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.2em; text-transform:uppercase; color:rgba(28,26,23,0.45); z-index:2;">[ Placeholder: Embed YouTube Video Here ]</span>
    </div>
  </section>
"""
content = content.replace('  </section>\n\n  <section id="curations"', '  </section>\n' + intro_video + '\n  <section id="curations"')

# 4. Replace Chronicles with Before/After, Reviews, Insta, and FAQs
old_chronicles_regex = re.compile(r'  <section id="chronicles".*?</section>\n', re.DOTALL)

new_sections = """
  <section id="before-after" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">Clinical <span style="font-style:italic;">Efficacy</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">Before &amp; After Samples</span>
    </div>
    
    <div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:60px;">
      <!-- Pair 1 -->
      <div style="display:flex; gap:16px; flex-direction:column;">
        <div style="display:flex; gap:16px;">
          <div style="flex:1; aspect-ratio:4/5; background:#E5E2D8; border-radius:8px; display:flex; align-items:center; justify-content:center;">
             <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; opacity:0.4;">BEFORE</span>
          </div>
          <div style="flex:1; aspect-ratio:4/5; background:#D9D6CB; border-radius:8px; display:flex; align-items:center; justify-content:center;">
             <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; opacity:0.4;">AFTER</span>
          </div>
        </div>
        <p style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-size:22px; font-style:italic; text-align:center;">Case 01 &mdash; Facial Contouring</p>
      </div>
      <!-- Pair 2 -->
      <div style="display:flex; gap:16px; flex-direction:column;">
        <div style="display:flex; gap:16px;">
          <div style="flex:1; aspect-ratio:4/5; background:#E5E2D8; border-radius:8px; display:flex; align-items:center; justify-content:center;">
             <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; opacity:0.4;">BEFORE</span>
          </div>
          <div style="flex:1; aspect-ratio:4/5; background:#D9D6CB; border-radius:8px; display:flex; align-items:center; justify-content:center;">
             <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; opacity:0.4;">AFTER</span>
          </div>
        </div>
        <p style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-size:22px; font-style:italic; text-align:center;">Case 02 &mdash; Hair Regrowth</p>
      </div>
    </div>
  </section>

  <section id="reviews" data-screen-label="Reviews" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px); background:rgba(255,255,255,0.4);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">Patient <span style="font-style:italic;">Experiences</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">Google &middot; Practo</span>
    </div>

    <div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px;">
      <!-- Review 1 -->
      <div style="background:#fff; border:1px solid rgba(28,26,23,0.08); border-radius:12px; padding:32px; box-shadow:0 10px 30px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <div style="display:flex; gap:4px; color:#E3B505;">
            &starf;&starf;&starf;&starf;&starf;
          </div>
          <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; font-weight:500; letter-spacing:0.1em; color:rgba(28,26,23,0.5);">GOOGLE</span>
        </div>
        <p style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:22px; line-height:1.45; font-style:italic;">"I have sat in many chairs across many cities. This is the first where the doctor seemed more interested in the decade ahead than the appointment in front of her."</p>
        <p style="margin:0; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">&mdash; Anjali D.</p>
      </div>
      <!-- Review 2 -->
      <div style="background:#fff; border:1px solid rgba(28,26,23,0.08); border-radius:12px; padding:32px; box-shadow:0 10px 30px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <div style="display:flex; gap:4px; color:#E3B505;">
            &starf;&starf;&starf;&starf;&starf;
          </div>
          <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; font-weight:500; letter-spacing:0.1em; color:rgba(28,26,23,0.5);">PRACTO</span>
        </div>
        <p style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:22px; line-height:1.45; font-style:italic;">"Nothing here is sold to you. A protocol is proposed, explained, and then quietly, exactly executed. The restraint is the luxury. Highly recommend Dr. Dipti."</p>
        <p style="margin:0; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">&mdash; Rahul M.</p>
      </div>
      <!-- Review 3 -->
      <div style="background:#fff; border:1px solid rgba(28,26,23,0.08); border-radius:12px; padding:32px; box-shadow:0 10px 30px rgba(0,0,0,0.03);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
          <div style="display:flex; gap:4px; color:#E3B505;">
            &starf;&starf;&starf;&starf;&starf;
          </div>
          <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; font-weight:500; letter-spacing:0.1em; color:rgba(28,26,23,0.5);">GOOGLE</span>
        </div>
        <p style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:22px; line-height:1.45; font-style:italic;">"Six months on, no one can name what changed — only that I look unmistakably, calmly like myself. That, I am told, was the entire point of the contouring."</p>
        <p style="margin:0; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase;">&mdash; Sneha K.</p>
      </div>
    </div>
  </section>

  <section id="instagram" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">The <span style="font-style:italic;">Journal</span></h2>
      <a href="#" data-reveal style="text-decoration:none; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:#1C1A17; border-bottom:1px solid #1C1A17; padding-bottom:4px; transition:opacity 0.3s ease;" style-hover="opacity:0.6;">@goodgenesclinic</a>
    </div>

    <div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px;">
      <div style="aspect-ratio:1/1; overflow:hidden; border-radius:8px;">
        <img src="assets/carousel-1.png" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s ease;" style-hover="transform:scale(1.05);" />
      </div>
      <div style="aspect-ratio:1/1; overflow:hidden; border-radius:8px;">
        <img src="assets/carousel-2.png" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s ease;" style-hover="transform:scale(1.05);" />
      </div>
      <div style="aspect-ratio:1/1; overflow:hidden; border-radius:8px;">
        <img src="assets/carousel-3.png" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s ease;" style-hover="transform:scale(1.05);" />
      </div>
      <div style="aspect-ratio:1/1; overflow:hidden; border-radius:8px;">
        <img src="assets/carousel-4.png" style="width:100%; height:100%; object-fit:cover; transition:transform 0.5s ease;" style-hover="transform:scale(1.05);" />
      </div>
    </div>
  </section>

  <section id="faqs" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">Patient <span style="font-style:italic;">Inquiries</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">F.A.Q.</span>
    </div>

    <div data-reveal style="max-width:800px;">
      <sc-for list="{{ faqs }}" as="f">
        <div onClick="{{ f.onClick }}" style="border-top:1px solid rgba(28,26,23,0.15); padding:clamp(20px,3vw,32px) 0; cursor:pointer;">
          <div style="display:flex; justify-content:space-between; align-items:center; gap:24px;">
            <h3 style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:400; font-size:clamp(22px,2.5vw,32px); line-height:1.2;">{{ f.question }}</h3>
            <span style="font-family:'IBM Plex Mono', monospace; font-size:24px; font-weight:300; transition:transform 0.4s ease; transform:{{ f.isOpen ? 'rotate(45deg)' : 'rotate(0)' }};">+</span>
          </div>
          <div style="overflow:hidden; max-height:{{ f.isOpen ? '300px' : '0px' }}; opacity:{{ f.isOpen ? '1' : '0' }}; transition:all 0.5s cubic-bezier(.2,.7,.2,1);">
            <p style="margin:20px 0 0; font-family:'IBM Plex Mono', monospace; font-size:15px; line-height:1.6; color:rgba(28,26,23,0.6); max-width:65ch;">{{ f.answer }}</p>
          </div>
        </div>
      </sc-for>
      <div style="border-top:1px solid rgba(28,26,23,0.15);"></div>
    </div>
  </section>
"""
content = old_chronicles_regex.sub(new_sections, content)

# 5. Update Script Data
old_state = "  state = { openMod: 0, activeT: 0, name: '', concern: '', submitted: false };"
new_state = "  state = { openMod: 0, openFaq: -1, name: '', concern: '', submitted: false };"
content = content.replace(old_state, new_state)

# Remove testimonial specific script and insert FAQ data
old_script_block = re.compile(r'    const tData = \[\n.*?const n = tData\.length;\n', re.DOTALL)
new_script_block = """    const faqData = [
      { question: 'What is the consultation process like?', answer: 'Your initial consultation is an unhurried, comprehensive assessment of your skin architecture, concerns, and aesthetic goals. We do not rush this process. Expect a detailed discussion resulting in a bespoke protocol.' },
      { question: 'Is there downtime associated with treatments?', answer: 'Downtime varies heavily depending on the specific modality used. Many of our non-invasive skin boosters and injectables have zero to minimal downtime, while deeper laser therapies may require a few days of social downtime.' },
      { question: 'How often should I schedule an appointment?', answer: 'This is entirely dependent on your bespoke protocol. For youth preservation, we generally recommend quarterly visits, while active treatments like hair regrowth may require monthly sessions initially.' },
      { question: 'Do you offer virtual consultations?', answer: 'We believe aesthetic dermatology requires precise, in-person assessment of skin quality, laxity, and structural anatomy. Therefore, we only consult in-clinic.' }
    ];
    const faqs = faqData.map((f, i) => ({
      question: f.question,
      answer: f.answer,
      isOpen: this.state.openFaq === i,
      onClick: () => this.setState((s) => ({ openFaq: s.openFaq === i ? -1 : i }))
    }));

    this._syncMod();

"""
content = old_script_block.sub(new_script_block, content)

# Also update the `return { ... }` block
return_block_old = """    return {
      setRoot: (el) => { this.rootEl = el; },
      timeline,
      modalities,
      testimonials,
      dots,
      activeNum: String(active + 1).padStart(2, '0'),
      prevT: () => this.setState((s) => ({ activeT: (s.activeT - 1 + n) % n })),
      nextT: () => this.setState((s) => ({ activeT: (s.activeT + 1) % n })),"""
return_block_new = """    return {
      setRoot: (el) => { this.rootEl = el; },
      timeline,
      modalities,
      faqs,"""
content = content.replace(return_block_old, return_block_new)

# Remove _syncT from script
content = content.replace('    this._syncT();\n', '')
content = re.sub(r'  _syncT\(\) \{.*?\n  \}\n\n', '', content, flags=re.DOTALL)


# Fix the href links in the navbar
# Because we replaced the chronicles section with "reviews"
nav_old = """<a data-nav="chronicles" href="#chronicles" """
nav_new = """<a data-nav="reviews" href="#reviews" """
content = content.replace(nav_old, nav_new)

spy_old = """const ids = ['clinic', 'curations', 'chronicles', 'atelier'];"""
spy_new = """const ids = ['clinic', 'curations', 'reviews', 'atelier'];"""
content = content.replace(spy_old, spy_new)

with open('index.html', 'w') as f:
    f.write(content)
