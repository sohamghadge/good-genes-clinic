import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Add animation to style
style_insertion = """  @keyframes waPop {
    0% { opacity: 0; transform: scale(0.9) translateY(10px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
  }
</style>"""
content = content.replace('</style>', style_insertion)

# 2. Remove the old WhatsApp link and replace with the floating widget
old_wa = """  <a href="#atelier" style="position:fixed; bottom:24px; right:24px; z-index:100; width:60px; height:60px; background-color:#25D366; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 14px rgba(0,0,0,0.15); transition:transform 0.3s ease;" style-hover="transform:scale(1.1);">
    <svg viewBox="0 0 24 24" width="32" height="32" fill="#fff"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  </a>"""

new_wa = """  <div style="position:fixed; bottom:24px; right:24px; z-index:100; display:flex; flex-direction:column; align-items:flex-end; gap:16px;">
    
    <sc-if value="{{ waOpen }}" hint-placeholder-val="{{ false }}">
      <div style="background:#fff; width:320px; border-radius:12px; box-shadow:0 10px 40px rgba(0,0,0,0.15); border:1px solid rgba(28,26,23,0.1); overflow:hidden; transform-origin:bottom right; animation:waPop 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);">
        <div style="background:#25D366; color:#fff; padding:16px 20px; font-family:'IBM Plex Mono', monospace; font-size:12px; letter-spacing:0.1em; text-transform:uppercase; display:flex; justify-content:space-between; align-items:center;">
          <span>Private Inquiry</span>
          <button onClick="{{ toggleWa }}" style="background:none; border:none; color:#fff; cursor:pointer; font-size:24px; line-height:1; padding:0; margin-top:-4px;">&times;</button>
        </div>
        <div style="padding:24px 20px;">
          <sc-if value="{{ notSubmitted }}" hint-placeholder-val="{{ true }}">
            <form onSubmit="{{ onSubmit }}">
              <div style="margin-bottom:20px;">
                <label style="display:block; font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:rgba(28,26,23,0.5); margin-bottom:8px;">Name</label>
                <input value="{{ name }}" onChange="{{ onName }}" placeholder="Your full name" required style="width:100%; box-sizing:border-box; background:transparent; border:none; border-bottom:1px solid rgba(28,26,23,0.2); padding:6px 0; font-family:'Cormorant Garamond', Georgia, serif; font-size:18px; color:#1C1A17; outline:none;" />
              </div>
              <div style="margin-bottom:28px;">
                <label style="display:block; font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.15em; text-transform:uppercase; color:rgba(28,26,23,0.5); margin-bottom:8px;">Concern</label>
                <input value="{{ concern }}" onChange="{{ onConcern }}" placeholder="e.g. cellular longevity" required style="width:100%; box-sizing:border-box; background:transparent; border:none; border-bottom:1px solid rgba(28,26,23,0.2); padding:6px 0; font-family:'Cormorant Garamond', Georgia, serif; font-size:18px; color:#1C1A17; outline:none;" />
              </div>
              <button type="submit" style="width:100%; background:#1C1A17; color:#fff; border:none; border-radius:4px; padding:12px; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.2em; text-transform:uppercase; cursor:pointer; transition:opacity 0.3s ease;" style-hover="opacity:0.8;">Start Chat &#8594;</button>
            </form>
          </sc-if>
          <sc-if value="{{ submitted }}" hint-placeholder-val="{{ false }}">
            <div style="text-align:center; padding:20px 0;">
              <p style="margin:0; font-family:'Cormorant Garamond', Georgia, serif; font-style:italic; font-size:22px; line-height:1.4; color:#25D366;">Redirecting...</p>
              <p style="margin:8px 0 0; font-family:'IBM Plex Mono', monospace; font-size:10px; color:rgba(28,26,23,0.5); text-transform:uppercase;">Opening WhatsApp</p>
            </div>
          </sc-if>
        </div>
      </div>
    </sc-if>

    <button onClick="{{ toggleWa }}" style="width:60px; height:60px; background-color:#25D366; border:none; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 14px rgba(0,0,0,0.15); cursor:pointer; transition:transform 0.3s ease; padding:0;" style-hover="transform:scale(1.1);">
      <svg viewBox="0 0 24 24" width="32" height="32" fill="#fff"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
    </button>
  </div>"""

content = content.replace(old_wa, new_wa)

# 3. Add state and handlers
old_state = "  state = { openMod: 0, openFaq: -1, name: '', concern: '', submitted: false };"
new_state = "  state = { openMod: 0, openFaq: -1, name: '', concern: '', submitted: false, waOpen: false };"
content = content.replace(old_state, new_state)

old_return = "      notSubmitted: !this.state.submitted,"
new_return = "      notSubmitted: !this.state.submitted,\n      waOpen: this.state.waOpen,\n      toggleWa: () => this.setState((s) => ({ waOpen: !s.waOpen })),"
content = content.replace(old_return, new_return)

with open('index.html', 'w') as f:
    f.write(content)

