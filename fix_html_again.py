import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Update Featured In with text-based authentic logos
featured_old = re.compile(r'<div style="max-width:1440px; margin:0 auto; padding:0 clamp\(24px,6vw,120px\); display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap; opacity:0.8;">.*?</div>', re.DOTALL)

featured_new = """<div style="max-width:1440px; margin:0 auto; padding:0 clamp(24px,6vw,120px); display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap;">
      <span style="font-family:'Didot', 'Bodoni MT', 'Times New Roman', serif; font-size:42px; font-weight:normal; letter-spacing:1px; color:#000;">VOGUE</span>
      <span style="font-family:'Helvetica Neue', Arial, sans-serif; font-size:34px; font-weight:900; letter-spacing:-2px; color:#e0006a; text-transform:uppercase; transform:scaleY(1.1);">COSMOPOLITAN</span>
      <span style="font-family:'Arial Black', 'Helvetica Neue', sans-serif; font-size:34px; font-weight:900; letter-spacing:-1px; color:#000;">Mumbai<span style="color:#e21f26;">Mirror</span></span>
      <span style="font-family:'Georgia', serif; font-size:36px; font-weight:bold; letter-spacing:-1.5px; color:#000;">hindustan<span style="color:#0094d4;">times</span></span>
    </div>"""

content = featured_old.sub(featured_new, content)

# 2. Update Reviews with authentic Google and Practo cards
reviews_old = re.compile(r'<div data-reveal style="display:grid; grid-template-columns:repeat\(auto-fit, minmax\(320px, 1fr\)\); gap:24px;">.*?</div>\n  </section>', re.DOTALL)

reviews_new = """<div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px;">
      
      <!-- Google Review -->
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

      <!-- Practo Review -->
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
  </section>"""

content = reviews_old.sub(reviews_new, content)

with open('index.html', 'w') as f:
    f.write(content)
