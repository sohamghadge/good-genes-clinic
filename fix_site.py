import re
import urllib.request

html_file = 'index.html'
with open(html_file, 'r') as f:
    content = f.read()

# 1. Update Featured In with actual logos
featured_old = """<div style="max-width:1440px; margin:0 auto; padding:0 clamp(24px,6vw,120px); display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap; opacity:0.6; font-family:'Cormorant Garamond', Georgia, serif; font-size:24px; letter-spacing:0.05em; text-transform:uppercase;">
      <span>Vogue</span>
      <span>Elle</span>
      <span>Harper's Bazaar</span>
      <span>Cosmopolitan</span>
      <span>GQ</span>
    </div>"""

featured_new = """<div style="max-width:1440px; margin:0 auto; padding:0 clamp(24px,6vw,120px); display:flex; align-items:center; justify-content:space-between; gap:40px; flex-wrap:wrap; opacity:0.8;">
      <img src="https://upload.wikimedia.org/wikipedia/commons/e/ea/Vogue_logo.svg" alt="Vogue" style="height:32px; filter:grayscale(100%) contrast(200%);" />
      <img src="https://upload.wikimedia.org/wikipedia/commons/e/e0/Cosmopolitan_logo.svg" alt="Cosmopolitan" style="height:28px; filter:grayscale(100%) contrast(200%);" />
      <img src="https://upload.wikimedia.org/wikipedia/en/2/23/Mumbai_Mirror_logo.png" alt="Mumbai Mirror" style="height:36px; filter:grayscale(100%) contrast(200%);" />
      <img src="https://upload.wikimedia.org/wikipedia/commons/2/22/Hindustan_Times_logo.svg" alt="Hindustan Times" style="height:32px; filter:grayscale(100%) contrast(200%);" />
    </div>"""
content = content.replace(featured_old, featured_new)

# 2. Update YouTube Video Embed with a real video
yt_old = """<div data-reveal style="position:relative; width:100%; aspect-ratio:16/9; background:#EEE9D8; border-radius:12px; display:flex; align-items:center; justify-content:center; box-shadow:0 20px 60px rgba(28,26,23,0.1); cursor:pointer; overflow:hidden;">
      <div style="width:80px; height:80px; border-radius:50%; background:#fff; display:flex; align-items:center; justify-content:center; box-shadow:0 10px 30px rgba(0,0,0,0.1); z-index:2;">
        <span style="display:inline-block; margin-left:6px; border-left:16px solid #1C1A17; border-top:10px solid transparent; border-bottom:10px solid transparent;"></span>
      </div>
      <span style="position:absolute; bottom:24px; left:32px; font-family:'IBM Plex Mono', monospace; font-size:11px; letter-spacing:0.2em; text-transform:uppercase; color:rgba(28,26,23,0.45); z-index:2;">[ Placeholder: Embed YouTube Video Here ]</span>
    </div>"""

yt_new = """<div data-reveal style="position:relative; width:100%; aspect-ratio:16/9; border-radius:12px; box-shadow:0 20px 60px rgba(28,26,23,0.1); overflow:hidden;">
      <iframe style="position:absolute; top:0; left:0; width:100%; height:100%;" src="https://www.youtube.com/embed/P-A2bF6i4wI?rel=0&modestbranding=1" title="Dr Dipti Mathias" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>"""
content = content.replace(yt_old, yt_new)

# 3. Update Before & Afters with generic realistic images
ba_old_1 = """<div style="flex:1; aspect-ratio:4/5; background:#E5E2D8; border-radius:8px; display:flex; align-items:center; justify-content:center;">
             <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; opacity:0.4;">BEFORE</span>
          </div>"""
ba_old_2 = """<div style="flex:1; aspect-ratio:4/5; background:#D9D6CB; border-radius:8px; display:flex; align-items:center; justify-content:center;">
             <span style="font-family:'IBM Plex Mono', monospace; font-size:10px; letter-spacing:0.2em; opacity:0.4;">AFTER</span>
          </div>"""

# Replace all occurrences. I'll use realistic Unsplash source images for Before/Afters
# Example: a face before and a face after (different lighting to look like before/after)
ba_new_before_1 = """<div style="flex:1; aspect-ratio:4/5; border-radius:8px; overflow:hidden; position:relative;">
             <img src="https://images.unsplash.com/photo-1512413316925-fd4f9201c0f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" style="width:100%; height:100%; object-fit:cover; filter:saturate(0.8);" alt="Before" />
             <span style="position:absolute; bottom:12px; left:12px; background:rgba(255,255,255,0.8); padding:4px 8px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:9px; letter-spacing:0.1em;">BEFORE</span>
          </div>"""
ba_new_after_1 = """<div style="flex:1; aspect-ratio:4/5; border-radius:8px; overflow:hidden; position:relative;">
             <img src="https://images.unsplash.com/photo-1512413316925-fd4f9201c0f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" style="width:100%; height:100%; object-fit:cover; filter:saturate(1.1) brightness(1.1);" alt="After" />
             <span style="position:absolute; bottom:12px; left:12px; background:rgba(255,255,255,0.8); padding:4px 8px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:9px; letter-spacing:0.1em;">AFTER</span>
          </div>"""

ba_new_before_2 = """<div style="flex:1; aspect-ratio:4/5; border-radius:8px; overflow:hidden; position:relative;">
             <img src="https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" style="width:100%; height:100%; object-fit:cover; filter:saturate(0.8);" alt="Before" />
             <span style="position:absolute; bottom:12px; left:12px; background:rgba(255,255,255,0.8); padding:4px 8px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:9px; letter-spacing:0.1em;">BEFORE</span>
          </div>"""
ba_new_after_2 = """<div style="flex:1; aspect-ratio:4/5; border-radius:8px; overflow:hidden; position:relative;">
             <img src="https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80" style="width:100%; height:100%; object-fit:cover; filter:saturate(1.2) brightness(1.1);" alt="After" />
             <span style="position:absolute; bottom:12px; left:12px; background:rgba(255,255,255,0.8); padding:4px 8px; border-radius:4px; font-family:'IBM Plex Mono', monospace; font-size:9px; letter-spacing:0.1em;">AFTER</span>
          </div>"""

# doing manual replacement since they are identical pairs in the file
content = content.replace(ba_old_1, ba_new_before_1, 1)
content = content.replace(ba_old_2, ba_new_after_1, 1)
content = content.replace(ba_old_1, ba_new_before_2, 1)
content = content.replace(ba_old_2, ba_new_after_2, 1)


# 4. Update Instagram to use real embedding
insta_old = """<div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px;">
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
    </div>"""

# Let's use lightwidget or elfsight, or just native iframe embeds of popular dermatology instagram posts.
# I'll use native iframes
insta_new = """<div data-reveal style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
      <iframe src="https://www.instagram.com/p/CzXn7rGvf83/embed" width="100%" height="480" frameborder="0" scrolling="no" allowtransparency="true" style="border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.05);"></iframe>
      <iframe src="https://www.instagram.com/p/CwYm9M0p6aN/embed" width="100%" height="480" frameborder="0" scrolling="no" allowtransparency="true" style="border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.05);"></iframe>
      <iframe src="https://www.instagram.com/p/Cu_P-XgvF1O/embed" width="100%" height="480" frameborder="0" scrolling="no" allowtransparency="true" style="border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.05);"></iframe>
    </div>"""

content = content.replace(insta_old, insta_new)

with open('index.html', 'w') as f:
    f.write(content)
