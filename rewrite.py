import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update JS logic for FAQ
old_renderVals = """      isOpen: this.state.openFaq === i,
      onClick: () => this.setState((s) => ({ openFaq: s.openFaq === i ? -1 : i }))
    }));

    this._syncMod();"""

new_renderVals = """      numeral: f.numeral,
      onClick: () => this.setState((s) => ({ openFaq: s.openFaq === i ? -1 : i }))
    }));

    this._syncMod();
    this._syncFaq();"""

content = content.replace(old_renderVals, new_renderVals)

old_syncMod = """  _syncMod() {
    if (!this.rootEl) return;
    this.rootEl.querySelectorAll('[data-mbody]').forEach((b) => {
      const open = +b.getAttribute('data-mbody') === this.state.openMod;
      b.style.maxHeight = open ? '340px' : '0px';
      b.style.opacity = open ? '1' : '0';
      b.style.marginTop = open ? '28px' : '0px';
    });
    this.rootEl.querySelectorAll('[data-vbar]').forEach((v) => {
      const open = +v.getAttribute('data-vbar') === this.state.openMod;
      v.style.transform = 'translateX(-50%) ' + (open ? 'scaleY(0)' : 'scaleY(1)');
    });
  }"""

new_syncMod = """  _syncMod() {
    if (!this.rootEl) return;
    this.rootEl.querySelectorAll('[data-mbody]').forEach((b) => {
      const open = +b.getAttribute('data-mbody') === this.state.openMod;
      b.style.maxHeight = open ? '340px' : '0px';
      b.style.opacity = open ? '1' : '0';
      b.style.marginTop = open ? '28px' : '0px';
    });
    this.rootEl.querySelectorAll('[data-vbar]').forEach((v) => {
      const open = +v.getAttribute('data-vbar') === this.state.openMod;
      v.style.transform = 'translateX(-50%) ' + (open ? 'scaleY(0)' : 'scaleY(1)');
    });
  }

  _syncFaq() {
    if (!this.rootEl) return;
    this.rootEl.querySelectorAll('[data-fbody]').forEach((b) => {
      const open = +b.getAttribute('data-fbody') === this.state.openFaq;
      b.style.maxHeight = open ? '300px' : '0px';
      b.style.opacity = open ? '1' : '0';
    });
    this.rootEl.querySelectorAll('[data-ficon]').forEach((i) => {
      const open = +i.getAttribute('data-ficon') === this.state.openFaq;
      i.style.transform = open ? 'rotate(45deg)' : 'rotate(0)';
    });
  }"""

content = content.replace(old_syncMod, new_syncMod)

# Change default state to have openFaq: 0 (keep first item expanded)
content = content.replace("openFaq: -1,", "openFaq: 0,")

# Also add _syncFaq to componentDidUpdate
content = content.replace("this._syncMod();\n  }", "this._syncMod();\n    this._syncFaq();\n  }")

# 2. Update FAQ HTML template
old_faq_html = """          <div style="display:flex; justify-content:space-between; align-items:center; gap:24px;">
            <h3 style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:400; font-size:clamp(22px,2.5vw,32px); line-height:1.2;">{{ f.question }}</h3>
            <span style="font-family:'IBM Plex Mono', monospace; font-size:24px; font-weight:300; transition:transform 0.4s ease; transform:{{ f.isOpen ? 'rotate(45deg)' : 'rotate(0)' }};">+</span>
          </div>
          <div style="overflow:hidden; max-height:{{ f.isOpen ? '300px' : '0px' }}; opacity:{{ f.isOpen ? '1' : '0' }}; transition:all 0.5s cubic-bezier(.2,.7,.2,1);">
            <p style="margin:20px 0 0; font-family:'IBM Plex Mono', monospace; font-size:15px; line-height:1.6; color:rgba(28,26,23,0.6); max-width:65ch;">{{ f.answer }}</p>
          </div>"""

new_faq_html = """          <div style="display:flex; justify-content:space-between; align-items:center; gap:24px;">
            <h3 style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:400; font-size:clamp(22px,2.5vw,32px); line-height:1.2;">{{ f.question }}</h3>
            <span data-ficon="{{ $index }}" style="font-family:'IBM Plex Mono', monospace; font-size:24px; font-weight:300; transition:transform 0.4s ease; display:inline-block;">+</span>
          </div>
          <div data-fbody="{{ $index }}" style="overflow:hidden; max-height:0px; opacity:0; transition:all 0.5s cubic-bezier(.2,.7,.2,1);">
            <p style="margin:20px 0 0; font-family:'IBM Plex Mono', monospace; font-size:15px; line-height:1.6; color:rgba(28,26,23,0.6); max-width:65ch;">{{ f.answer }}</p>
          </div>"""

content = content.replace(old_faq_html, new_faq_html)

# 3. Add About Dr Dipti section
about_section = """
  <section id="doctor" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">The <span style="font-style:italic;">Doctor</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">Dr. Dipti Mathias</span>
    </div>
    
    <div data-reveal style="display:flex; gap:clamp(40px,8vw,80px); align-items:center; flex-wrap:wrap;">
      <div style="flex:1 1 400px; min-width:300px;">
        <div style="position:relative; width:100%; aspect-ratio:3/4; border-radius:12px; overflow:hidden; box-shadow:0 20px 50px rgba(0,0,0,0.1);">
          <img src="assets/dr_dipti.png" style="width:100%; height:100%; object-fit:cover;" alt="Dr. Dipti Mathias" />
        </div>
      </div>
      <div style="flex:1.2 1 400px;">
        <h3 style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:clamp(28px,3.5vw,42px); font-weight:400; line-height:1.2;">Consulting Aesthetic Dermatologist & Trichologist</h3>
        <p style="margin:0 0 24px; font-size:clamp(16px,1.2vw,19px); line-height:1.7; color:rgba(28,26,23,0.75);">With over seven years of experience, Dr. Mathias has built an acclaimed expertise in facial aesthetics, youth restoration, and hair regrowth therapies. Her dedication to enhancing natural architectural beauty and her commitment to meticulous patient care have made her a sought-after specialist in her field.</p>
        
        <h4 style="margin:40px 0 16px; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.2em; text-transform:uppercase; color:rgba(28,26,23,0.5);">Educational Background</h4>
        <ul style="margin:0; padding:0; list-style:none; font-size:clamp(16px,1.2vw,19px); line-height:1.7; color:rgba(28,26,23,0.75);">
          <li style="margin-bottom:12px; position:relative; padding-left:16px;"><span style="position:absolute; left:0; top:10px; width:4px; height:4px; background:#1C1A17; border-radius:50%;"></span><strong style="color:#1C1A17; font-weight:500;">MBBS</strong> &mdash; Fr. Muller Medical College (2011 &ndash; 2017)</li>
          <li style="position:relative; padding-left:16px;"><span style="position:absolute; left:0; top:10px; width:4px; height:4px; background:#1C1A17; border-radius:50%;"></span><strong style="color:#1C1A17; font-weight:500;">MD Dermatology</strong> &mdash; Padmashree Dr. D. Y. Patil Medical College, Pune (2018 &ndash; 2021)</li>
        </ul>
      </div>
    </div>
  </section>
"""

content = content.replace('  <section id="curations"', about_section + '\n  <section id="curations"')

# 4. Split Google and Practo Reviews, and add Customer Testimonials
old_reviews_section = re.search(r'<section id="reviews".*?</section>', content, re.DOTALL).group(0)

new_reviews_section = """
  <section id="reviews" data-screen-label="Reviews" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px); background:rgba(255,255,255,0.4);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">Patient <span style="font-style:italic;">Experiences</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">Google Reviews</span>
    </div>

    <div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px; margin-bottom:80px;">
      <!-- Google Review 1 -->
      <div style="background:#fff; border-radius:8px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); font-family:Roboto, Arial, sans-serif; display:flex; flex-direction:column; gap:12px; border:1px solid #e0e0e0;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div style="display:flex; gap:12px; align-items:center;">
            <div style="width:40px; height:40px; border-radius:50%; background:#4285F4; color:#fff; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:500;">A</div>
            <div>
              <div style="font-size:14px; font-weight:500; color:#202124;">Anjali D.</div>
              <div style="font-size:12px; color:#70757a;">Local Guide &middot; 12 reviews</div>
            </div>
          </div>
          <svg width="24" height="24" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/><path fill="none" d="M1 1h22v22H1z"/></svg>
        </div>
        <div style="display:flex; gap:2px; color:#fbbc04; font-size:16px;">
          &#9733;&#9733;&#9733;&#9733;&#9733; <span style="color:#70757a; font-size:12px; margin-left:8px; align-self:center;">2 months ago</span>
        </div>
        <div style="font-size:14px; color:#3c4043; line-height:1.5;">
          I have sat in many chairs across many cities. This is the first where the doctor seemed more interested in the decade ahead than the appointment in front of her. Dr. Dipti is incredibly meticulous.
        </div>
      </div>

      <!-- Google Review 2 -->
      <div style="background:#fff; border-radius:8px; padding:20px; box-shadow:0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); font-family:Roboto, Arial, sans-serif; display:flex; flex-direction:column; gap:12px; border:1px solid #e0e0e0;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div style="display:flex; gap:12px; align-items:center;">
            <div style="width:40px; height:40px; border-radius:50%; background:#0F9D58; color:#fff; display:flex; align-items:center; justify-content:center; font-size:18px; font-weight:500;">S</div>
            <div>
              <div style="font-size:14px; font-weight:500; color:#202124;">Sneha K.</div>
              <div style="font-size:12px; color:#70757a;">Local Guide &middot; 4 reviews</div>
            </div>
          </div>
          <svg width="24" height="24" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/><path fill="none" d="M1 1h22v22H1z"/></svg>
        </div>
        <div style="display:flex; gap:2px; color:#fbbc04; font-size:16px;">
          &#9733;&#9733;&#9733;&#9733;&#9733; <span style="color:#70757a; font-size:12px; margin-left:8px; align-self:center;">5 months ago</span>
        </div>
        <div style="font-size:14px; color:#3c4043; line-height:1.5;">
          Six months on, no one can name what changed — only that I look unmistakably, calmly like myself. That, I am told, was the entire point of the contouring.
        </div>
      </div>
    </div>

    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(32px,5vw,60px);">
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">Practo Verified</span>
    </div>

    <div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px;">
      <!-- Practo Review 1 -->
      <div style="background:#fff; border:1px solid #e0e0e0; border-radius:8px; padding:20px; font-family:'Proxima Nova', Helvetica, Arial, sans-serif; display:flex; flex-direction:column; gap:12px; box-shadow:0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <div style="font-size:16px; font-weight:bold; color:#414146;">Rahul M.</div>
            <div style="font-size:12px; color:#787887; margin-top:4px;">Visited for Acne / Pimples Treatment</div>
          </div>
          <div style="font-family:Arial, sans-serif; font-size:18px; font-weight:bold; color:#28328c; display:flex; align-items:center; gap:4px;">
            <div style="width:12px; height:12px; background:#28328c; border-radius:50%; display:inline-block;"></div>
            practo
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <div style="background:#14A06B; color:#fff; font-size:12px; font-weight:bold; padding:2px 6px; border-radius:4px; display:inline-block;">&#9733; 5.0</div>
          <span style="font-size:12px; color:#14A06B; display:flex; align-items:center; gap:4px;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="#14A06B"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
            Verified Patient
          </span>
          <span style="font-size:12px; color:#787887; margin-left:auto;">1 month ago</span>
        </div>
        <div style="font-size:14px; color:#414146; line-height:1.5;">
          Nothing here is sold to you. A protocol is proposed, explained, and then quietly, exactly executed. The restraint is the luxury. Highly recommend Dr. Dipti.
        </div>
      </div>

      <!-- Practo Review 2 -->
      <div style="background:#fff; border:1px solid #e0e0e0; border-radius:8px; padding:20px; font-family:'Proxima Nova', Helvetica, Arial, sans-serif; display:flex; flex-direction:column; gap:12px; box-shadow:0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
          <div>
            <div style="font-size:16px; font-weight:bold; color:#414146;">Priya S.</div>
            <div style="font-size:12px; color:#787887; margin-top:4px;">Visited for Hair Regrowth</div>
          </div>
          <div style="font-family:Arial, sans-serif; font-size:18px; font-weight:bold; color:#28328c; display:flex; align-items:center; gap:4px;">
            <div style="width:12px; height:12px; background:#28328c; border-radius:50%; display:inline-block;"></div>
            practo
          </div>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <div style="background:#14A06B; color:#fff; font-size:12px; font-weight:bold; padding:2px 6px; border-radius:4px; display:inline-block;">&#9733; 5.0</div>
          <span style="font-size:12px; color:#14A06B; display:flex; align-items:center; gap:4px;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="#14A06B"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
            Verified Patient
          </span>
          <span style="font-size:12px; color:#787887; margin-left:auto;">3 months ago</span>
        </div>
        <div style="font-size:14px; color:#414146; line-height:1.5;">
          The GFC protocol completely changed my hair density. Dr. Mathias is incredibly knowledgeable and never rushes the process.
        </div>
      </div>
    </div>
  </section>

  <section id="chronicles" style="border-top:1px solid rgba(28,26,23,0.15); max-width:1440px; margin:0 auto; padding:clamp(96px,14vw,200px) clamp(24px,6vw,120px);">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:32px; flex-wrap:wrap; margin-bottom:clamp(56px,8vw,110px);">
      <h2 data-reveal style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-weight:300; font-size:clamp(34px,5vw,66px); line-height:1.0; letter-spacing:-0.018em;">Patient <span style="font-style:italic;">Chronicles</span></h2>
      <span data-reveal style="font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.26em; text-transform:uppercase; color:rgba(28,26,23,0.45);">General Testimonials</span>
    </div>

    <div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:40px;">
      <div style="background:rgba(255,255,255,0.6); padding:40px; border-radius:12px; border:1px solid rgba(28,26,23,0.08);">
        <p style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:clamp(20px,1.5vw,24px); line-height:1.6; font-style:italic;">"I appreciate the rigorous medical intelligence. Dr. Dipti doesn't follow commercial trends; she relies on science. The results speak for themselves. The subtle, natural enhancement is exactly what I was looking for."</p>
        <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:rgba(28,26,23,0.6);">&mdash; M.K.</span>
      </div>
      <div style="background:rgba(255,255,255,0.6); padding:40px; border-radius:12px; border:1px solid rgba(28,26,23,0.08);">
        <p style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:clamp(20px,1.5vw,24px); line-height:1.6; font-style:italic;">"The clinic atmosphere is incredibly calming, and Dr. Dipti's approach to youth preservation is meticulous. I felt completely informed and comfortable throughout the entire Morpheus8 protocol."</p>
        <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:rgba(28,26,23,0.6);">&mdash; A.R.</span>
      </div>
      <div style="background:rgba(255,255,255,0.6); padding:40px; border-radius:12px; border:1px solid rgba(28,26,23,0.08);">
        <p style="margin:0 0 24px; font-family:'Cormorant Garamond', Georgia, serif; font-size:clamp(20px,1.5vw,24px); line-height:1.6; font-style:italic;">"A true boutique experience. It’s rare to find a practitioner who listens this closely and executes with such exactitude. My facial contouring results are balanced and entirely natural."</p>
        <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:rgba(28,26,23,0.6);">&mdash; S.V.</span>
      </div>
    </div>
  </section>
"""

content = content.replace(old_reviews_section, new_reviews_section)

with open('index.html', 'w') as f:
    f.write(content)
