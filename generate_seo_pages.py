import os
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Base Configurations
BASE_DIR = "/Users/sohamghadge/Desktop/Projects/work/Good Genes Clinic"
DOMAIN = "https://good-genes-clinic.com"

TREATMENTS = {
    "botox": {
        "name": "Botox & Dysport",
        "anchor": "botox",
        "category": "Lifting & Contouring",
        "description": "Micro-dosing treatments for smoothing fine lines, crow's feet, forehead lines, and wrinkles using premium neuromodulators.",
        "cost": "₹12,000 - ₹35,000 per session depending on units",
        "procedure": "Micro-injections directly into targeted muscles to relax expressions and restore smoothness.",
        "benefits": ["Smooths active lines", "Softens forehead wrinkles", "Quick 15-minute session", "No clinical downtime"],
        "avoid": "Pregnant or lactating mothers, patients with neuromuscular disorders, or local skin infections."
    },
    "fillers": {
        "name": "Dermal Fillers & Facial Contouring",
        "anchor": "fillers",
        "category": "Lifting & Contouring",
        "description": "Hyaluronic acid dermal fillers to restore lost volume, define jawlines, contour lips, and fill under-eye hollows.",
        "cost": "₹22,000 - ₹55,000 per syringe",
        "procedure": "Targeted placement of premium fillers to suspend tissues, define contours, and add structural support.",
        "benefits": ["Instant volume restoration", "Natural jawline definition", "Plumped lips", "Under-eye rejuvenation"],
        "avoid": "Active skin infections, history of severe allergies or anaphylaxis, or bleeding disorders."
    },
    "skin-lifting": {
        "name": "Skin Lifting & Tightening",
        "anchor": "skin-lifting",
        "category": "Lifting & Contouring",
        "description": "Non-surgical skin tightening protocols using state-of-the-art energy devices to rebuild collagen structures.",
        "cost": "₹40,000 - ₹95,000",
        "procedure": "Clinical energy delivery to heat deep dermal layers, stimulating contraction and collagen growth.",
        "benefits": ["Firm skin tone", "Tightened jowls", "Stimulates collagen", "Long-lasting tissue firming"],
        "avoid": "Active acne flare-ups, metal implants in the treatment area, or cardiac pacemakers."
    },
    "hifu": {
        "name": "HIFU (High-Intensity Focused Ultrasound)",
        "anchor": "hifu",
        "category": "Lifting & Contouring",
        "description": "Non-invasive SMAS layer tissue tightening and lifting using ultrasound energy for jawline and neck refinement.",
        "cost": "₹35,000 - ₹80,000",
        "procedure": "Ultrasound energy focuses deep below the skin to induce thermal coagulation, triggering deep tissue lift.",
        "benefits": ["Deep SMAS layer lifting", "Refines jawline", "Reduces double chin", "Single session protocol"],
        "avoid": "Open wounds, metallic implants, severe cystic acne in the treatment zone."
    },
    "facelift": {
        "name": "Facelift without Surgery",
        "anchor": "facelift",
        "category": "Lifting & Contouring",
        "description": "Liquid and energy facelift protocols combining fillers, thread contouring, and energy tightening for complete facial rejuvenation.",
        "cost": "₹75,000 - ₹1,80,000",
        "procedure": "Multimodal combination therapy tailored to suspend volume, smooth wrinkles, and tighten loose skin.",
        "benefits": ["Complete facial lifting", "Restores youthful contours", "No surgical scars", "Minimal clinical recovery"],
        "avoid": "Patients expecting surgical-grade laxity removal, active infections, or immune conditions."
    },
    "salmon-dna": {
        "name": "Salmon DNA / PDRN Therapy",
        "anchor": "salmon-dna",
        "category": "Regenerative Aesthetics",
        "description": "Polynucleotide cellular recovery treatments for skin hydration, collagen synthesis, and scar healing.",
        "cost": "₹18,000 - ₹30,000 per session",
        "procedure": "Intradermal micro-droplet injection of PDRN to trigger cellular repair and enhance hydration.",
        "benefits": ["Intense deep hydration", "Repairs acne scars", "Enhances elasticity", "Calms skin redness"],
        "avoid": "Known fish allergies, active skin infections, or bleeding disorders."
    },
    "microneedling": {
        "name": "Microneedling & MNRF",
        "anchor": "microneedling",
        "category": "Regenerative Aesthetics",
        "description": "Microneedling Radio Frequency (MNRF) to rebuild collagen, refine skin texture, and smooth acne scars.",
        "cost": "₹12,000 - ₹25,000 per session",
        "procedure": "Fine insulated needles penetrate the skin and deliver radiofrequency energy, heating the dermis.",
        "benefits": ["Reduces acne scars", "Refines large pores", "Smooths skin texture", "Tightens mild laxity"],
        "avoid": "History of keloids, active eczema or psoriasis, or active inflammatory acne."
    },
    "pico-laser": {
        "name": "Pico Laser Pigmentation Treatment",
        "anchor": "pico-laser",
        "category": "Regenerative Aesthetics",
        "description": "Ultra-fast picosecond laser treatments to shatter pigment particles, clearing melasma, freckles, and tattoos.",
        "cost": "₹15,000 - ₹28,000 per session",
        "procedure": "Picosecond laser pulses deliver photo-acoustic energy to break up melanin without burning surrounding skin.",
        "benefits": ["Clears deep melasma", "Fades dark spots", "Improves skin tone", "No laser heat damage"],
        "avoid": "Recent sun tan, active eczema, or photosensitizing medications."
    },
    "chemical-peels": {
        "name": "Chemical Peels & Exfoliation",
        "anchor": "chemical-peels",
        "category": "Regenerative Aesthetics",
        "description": "Medical-grade chemical peels using salicylic, glycolic, or TCA mixtures to clear acne and restore even skin tone.",
        "cost": "₹4,000 - ₹9,500 per session",
        "procedure": "Application of clinical exfoliating acids to peel away damaged outer skin layers, revealing fresh skin.",
        "benefits": ["Fades dark marks", "Clears active acne", "Brightens dull skin", "Refines skin texture"],
        "avoid": "Sunburnt skin, open cuts, or recent use of oral isotretinoin."
    },
    "medical-facials": {
        "name": "Medical Facials & Hydration",
        "anchor": "medical-facials",
        "category": "Regenerative Aesthetics",
        "description": "Customized clinical facials integrating serums, hydradermabrasion, and oxygen infusions for skin barrier health.",
        "cost": "₹6,000 - ₹12,000 per session",
        "procedure": "Multi-step deep cleaning, exfoliation, extraction, and targeted hydration matching your skin profile.",
        "benefits": ["Deeply cleanses pores", "Restores skin barrier", "Instant radiant glow", "Supports active treatments"],
        "avoid": "Severe active skin infections, eczema flare-ups, or open wounds."
    },
    "acne-scars": {
        "name": "Acne & Acne Scar Treatment",
        "anchor": "acne-scars",
        "category": "Targeted Corrective Procedures",
        "description": "Comprehensive scar reconstruction using subcision, chemical peels, MNRF, and Pico lasers for smooth skin.",
        "cost": "₹15,000 - ₹45,000 per session",
        "procedure": "Combination protocols designed to release deep scars, peel pigmentation, and stimulate structural collagen.",
        "benefits": ["Smooths boxcar/icepick scars", "Fades post-acne marks", "Prevents active breakouts", "Restores even skin texture"],
        "avoid": "Active inflammatory skin infections, bleeding disorders, or pregnancy."
    },
    "dark-circles": {
        "name": "Under-Eye Dark Circles Treatment",
        "anchor": "dark-circles",
        "category": "Targeted Corrective Procedures",
        "description": "Advanced tear-trough fillers, vascular lasers, and custom peels to treat hollows, shadows, and pigmentation.",
        "cost": "₹20,000 - ₹45,000",
        "procedure": "Dermal fillers to restore under-eye volume, combined with lasers to target superficial vascular networks.",
        "benefits": ["Fills hollow eyes", "Reduces dark shadows", "Refreshes tired look", "Tightens under-eye skin"],
        "avoid": "Severe under-eye bags (herniated fat), chronic sinus issues, or active allergies."
    },
    "cautery": {
        "name": "Cautery for Skintags & Milia",
        "anchor": "cautery",
        "category": "Targeted Corrective Procedures",
        "description": "Safe electrocautery or radiofrequency ablation to cleanly remove milia, skintags, warts, and spots.",
        "cost": "₹3,000 - ₹10,000 depending on count",
        "procedure": "Precise heat application to vaporize skin lesions cleanly, followed by skin healing support.",
        "benefits": ["Instant tag removal", "Smooths skin surface", "Minimal scarring risk", "Quick single-visit clinic treatment"],
        "avoid": "Cardiac pacemakers (for electrocautery), active localized infections, or keloidal skin history."
    }
}

LOCATIONS = {
    "khar": "Khar West",
    "bandra": "Bandra West",
    "santacruz": "Santacruz West",
    "juhu": "Juhu"
}

ASPECTS = {
    "guide": {
        "suffix": "Treatment Guide",
        "description": "Comprehensive patient guide covering the procedure, expected results, and clinical considerations."
    },
    "cost": {
        "suffix": "Cost & Pricing in Mumbai",
        "description": "Detailed guide on pricing factors, packages, and cost estimates in Khar West, Mumbai."
    },
    "side-effects": {
        "suffix": "Side Effects & Safety Profile",
        "description": "Clinical safety details, potential mild side effects, recovery timeline, and candidate guidelines."
    },
    "before-after": {
        "suffix": "Before & After Results Timeline",
        "description": "Timeline of visible changes, maintenance sessions, and what results to expect post-procedure."
    },
    "faqs": {
        "suffix": "Frequently Asked Questions",
        "description": "Detailed answers to common questions about candidates, pain, downtime, and long-term safety."
    }
}

def load_template():
    with open(os.path.join(BASE_DIR, "seo_template.html"), "r") as f:
        return f.read()

def generate_faqs(treatment_name, treatment_info):
    name = treatment_name
    return [
        {
            "q": f"How long does the {name} procedure take?",
            "a": f"A standard session of {name} at our Khar West clinic typically takes about 30 to 45 minutes of active treatment, though we suggest planning for an hour to complete consultation and preparation."
        },
        {
            "q": f"Is {name} painful?",
            "a": f"Most patients describe the sensation as a mild pinch or warmth. For needle-based or energy treatments, we apply a premium topical numbing cream for 30-45 minutes beforehand to ensure absolute comfort."
        },
        {
            "q": f"What is the cost of {name} in Mumbai?",
            "a": f"The cost for {name} typically ranges from {treatment_info['cost']}. The exact pricing depends on the surface area, severity of the condition, and number of sessions required."
        },
        {
            "q": f"Are there any side effects of {name}?",
            "a": f"Mild redness, slight swelling, or temporary tenderness are normal and resolve within a few hours to a couple of days. We provide comprehensive post-care guidelines to support healing."
        },
        {
            "q": f"Who is the ideal candidate for this treatment?",
            "a": f"This procedure is ideal for patients looking to address specific cosmetic or clinical skin issues. However, {treatment_info['avoid']} should be avoided."
        }
    ]

def generate_pages():
    template = load_template()
    generated_urls = []
    
    # 1. Generate Treatment Aspect Pages (14 treatments * 5 aspects = 70 pages)
    for t_id, t_info in TREATMENTS.items():
        for a_id, a_info in ASPECTS.items():
            path_dir = os.path.join(BASE_DIR, "treatments", t_id)
            if a_id != "guide":
                path_dir = os.path.join(path_dir, a_id)
                
            os.makedirs(path_dir, exist_ok=True)
            
            page_title = f"{t_info['name']} {a_info['suffix']} | Good Genes Clinic"
            meta_desc = f"{a_info['description']} {t_info['description']} Available at Good Genes Clinic, Khar West, Mumbai."
            keywords = f"{t_info['name']}, {t_info['name']} cost, {t_info['name']} side effects, {t_info['name']} Mumbai"
            
            # Content compilation
            content_html = f"<h2 class='section-title'>Overview of {t_info['name']}</h2>"
            content_html += f"<p>{t_info['description']} Under the care of Dr. Dipti Mathias at Good Genes Clinic, each protocol is customized to deliver natural results.</p>"
            
            if a_id == "cost":
                content_html += f"<h2 class='section-title'>Cost and Pricing Details</h2>"
                content_html += f"<p>The estimated cost for this treatment is approximately <strong>{t_info['cost']}</strong>. Factors affecting the total price include:</p>"
                content_html += "<ul>"
                content_html += "<li>Number of units or product syringes used</li>"
                content_html += "<li>Severity of the skin condition</li>"
                content_html += "<li>Custom combined treatment protocols</li>"
                content_html += "</ul>"
            elif a_id == "side-effects":
                content_html += f"<h2 class='section-title'>Clinical Safety &amp; Post-Care</h2>"
                content_html += f"<p>{t_info['procedure']} Safety is our highest priority at Good Genes Clinic. Common mild reactions include brief redness or swelling.</p>"
                content_html += f"<p><strong>Contraindications:</strong> {t_info['avoid']}</p>"
            elif a_id == "before-after":
                content_html += f"<h2 class='section-title'>Expected Results Timeline</h2>"
                content_html += f"<p>Visible improvements typically develop within a few days to weeks depending on the exact modalities used. Maintenance sessions support long-term cellular health.</p>"
                content_html += "<ul>"
                for benefit in t_info['benefits']:
                    content_html += f"<li>{benefit}</li>"
                content_html += "</ul>"
            
            # Inject FAQs
            faqs = generate_faqs(t_info['name'], t_info)
            content_html += "<h2 class='section-title'>Frequently Asked Questions</h2>"
            for faq in faqs:
                content_html += f"<div class='faq-item'>"
                content_html += f"<h3 class='faq-question'>{faq['q']}</h3>"
                content_html += f"<p class='faq-answer'>{faq['a']}</p>"
                content_html += f"</div>"
                
            # Build Schema
            faq_schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": f["q"],
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": f["a"]
                        }
                    } for f in faqs
                ]
            }
            
            local_business_schema = {
                "@context": "https://schema.org",
                "@type": "MedicalBusiness",
                "name": "Good Genes Clinic",
                "description": f"Premium aesthetic dermatology and wellness treatments (including {t_info['name']}) by Dr. Dipti Mathias in Khar West, Mumbai.",
                "url": f"{DOMAIN}/treatments/{t_id}/" if a_id == "guide" else f"{DOMAIN}/treatments/{t_id}/{a_id}/",
                "logo": f"{DOMAIN}/assets/logo.png",
                "image": f"{DOMAIN}/assets/real-doctor.png",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "14th Floor, Amore Edge, 1402 Swami Vivekananda Road",
                    "addressLocality": "Khar West",
                    "addressRegion": "Mumbai",
                    "postalCode": "400052",
                    "addressCountry": "IN"
                },
                "telephone": "+919004185406",
                "medicalSpecialty": "Dermatology",
                "founder": {
                    "@type": "Physician",
                    "@id": f"{DOMAIN}/#doctor",
                    "name": "Dr. Dipti Mathias"
                }
            }
            
            schema_array = [local_business_schema, faq_schema]
            schema_str = f"<script type=\"application/ld+json\">\n{json.dumps(schema_array, indent=2)}\n</script>"
            
            # Replace template tokens
            page_html = template
            page_html = page_html.replace("{{ title }}", page_title)
            page_html = page_html.replace("{{ description }}", meta_desc)
            page_html = page_html.replace("{{ keywords }}", keywords)
            page_html = page_html.replace("{{ schema }}", schema_str)
            page_html = page_html.replace("{{ name }}", f"{t_info['name']} — {a_info['suffix']}")
            page_html = page_html.replace("{{ category_link }}", f'<a href="/index.html#curations">{t_info["category"]}</a>')
            page_html = page_html.replace("{{ introduction }}", t_info['description'])
            page_html = page_html.replace("{{ content }}", content_html)
            
            with open(os.path.join(path_dir, "index.html"), "w") as f:
                f.write(page_html)
                
            rel_url = f"/treatments/{t_id}" if a_id == "guide" else f"/treatments/{t_id}/{a_id}"
            generated_urls.append(rel_url)

    # 2. Generate Local Landing Pages (4 locations * 14 treatments = 56 pages)
    for loc_id, loc_name in LOCATIONS.items():
        # Main location page
        loc_dir = os.path.join(BASE_DIR, "locations", loc_id)
        os.makedirs(loc_dir, exist_ok=True)
        
        loc_title = f"Best Dermatologist in {loc_name}, Mumbai | Good Genes Clinic"
        loc_desc = f"Looking for the best dermatologist in {loc_name}, Mumbai? Visit Dr. Dipti Mathias at Good Genes Clinic for premium aesthetic dermatology, skin lifting, lasers, and wellness."
        loc_keywords = f"best dermatologist in {loc_name}, skin clinic {loc_name}, dermatologist near {loc_name}, skin specialist in {loc_name} Mumbai"
        
        loc_content = f"<h2 class='section-title'>Dermatology Services near {loc_name}</h2>"
        loc_content += f"<p>Patients from {loc_name} can easily access our boutique clinic located at Amore Edge, SV Road, Khar West. We specialize in customized skin lifting, anti-aging, and corrective aesthetics.</p>"
        loc_content += "<ul>"
        for t_id, t_info in TREATMENTS.items():
            loc_content += f"<li><a href='/treatments/{t_id}/index.html' style='color:#1C1A17; font-weight:500;'>{t_info['name']}</a> &mdash; {t_info['description']}</li>"
        loc_content += "</ul>"
        
        # Build Schema
        loc_schema = {
            "@context": "https://schema.org",
            "@type": "MedicalBusiness",
            "name": f"Good Genes Clinic - {loc_name}",
            "description": f"Premium aesthetic dermatology, wellness and aesthetics treatments for patients in {loc_name}, Mumbai.",
            "url": f"{DOMAIN}/locations/{loc_id}/",
            "logo": f"{DOMAIN}/assets/logo.png",
            "image": f"{DOMAIN}/assets/real-doctor.png",
            "address": {
                "@type": "PostalAddress",
                "addressLocality": loc_name,
                "addressRegion": "Mumbai",
                "addressCountry": "IN"
            },
            "telephone": "+919004185406",
            "medicalSpecialty": "Dermatology",
            "founder": {
                "@type": "Physician",
                "@id": f"{DOMAIN}/#doctor",
                "name": "Dr. Dipti Mathias"
            }
        }
        loc_schema_str = f"<script type=\"application/ld+json\">\n{json.dumps(loc_schema, indent=2)}\n</script>"
        
        page_html = template
        page_html = page_html.replace("{{ title }}", loc_title)
        page_html = page_html.replace("{{ description }}", loc_desc)
        page_html = page_html.replace("{{ keywords }}", loc_keywords)
        page_html = page_html.replace("{{ schema }}", loc_schema_str)
        page_html = page_html.replace("{{ name }}", f"Dermatology Services in {loc_name}")
        page_html = page_html.replace("{{ category_link }}", '<span>Locations</span>')
        page_html = page_html.replace("{{ introduction }}", f"Serving patients from {loc_name} with premium, science-backed skin care solutions.")
        page_html = page_html.replace("{{ content }}", loc_content)
        
        with open(os.path.join(loc_dir, "index.html"), "w") as f:
            f.write(page_html)
        generated_urls.append(f"/locations/{loc_id}")
        
        # Localized treatment pages
        for t_id, t_info in TREATMENTS.items():
            local_t_dir = os.path.join(loc_dir, t_id)
            os.makedirs(local_t_dir, exist_ok=True)
            
            local_t_title = f"Best {t_info['name']} Treatment in {loc_name}, Mumbai | Good Genes Clinic"
            local_t_desc = f"Seeking the best {t_info['name']} treatment in {loc_name}, Mumbai? Visit Dr. Dipti Mathias at Good Genes Clinic for advanced {t_info['name']} clinical protocols."
            local_t_keywords = f"best {t_info['name']} in {loc_name}, {t_info['name']} clinic {loc_name}, {t_info['name']} specialist {loc_name} Mumbai"
            
            local_t_content = f"<h2 class='section-title'>About the Procedure</h2>"
            local_t_content += f"<p>{t_info['procedure']} We welcome patients from {loc_name} seeking targeted {t_info['name']} treatments to support skin health.</p>"
            local_t_content += "<ul>"
            for benefit in t_info['benefits']:
                local_t_content += f"<li>{benefit}</li>"
            local_t_content += "</ul>"
            
            # Build Schema
            local_t_schema = {
                "@context": "https://schema.org",
                "@type": "MedicalBusiness",
                "name": f"Good Genes Clinic - {t_info['name']} in {loc_name}",
                "description": f"Premium aesthetic dermatology treatments (including {t_info['name']}) for patients in {loc_name}, Mumbai under dermatologist Dr. Dipti Mathias.",
                "url": f"{DOMAIN}/locations/{loc_id}/{t_id}/",
                "logo": f"{DOMAIN}/assets/logo.png",
                "image": f"{DOMAIN}/assets/real-doctor.png",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": loc_name,
                    "addressRegion": "Mumbai",
                    "addressCountry": "IN"
                },
                "telephone": "+919004185406",
                "medicalSpecialty": "Dermatology",
                "founder": {
                    "@type": "Physician",
                    "@id": f"{DOMAIN}/#doctor",
                    "name": "Dr. Dipti Mathias"
                }
            }
            local_t_schema_str = f"<script type=\"application/ld+json\">\n{json.dumps(local_t_schema, indent=2)}\n</script>"
            
            page_html = template
            page_html = page_html.replace("{{ title }}", local_t_title)
            page_html = page_html.replace("{{ description }}", local_t_desc)
            page_html = page_html.replace("{{ keywords }}", local_t_keywords)
            page_html = page_html.replace("{{ schema }}", local_t_schema_str)
            page_html = page_html.replace("{{ name }}", f"{t_info['name']} in {loc_name}")
            page_html = page_html.replace("{{ category_link }}", f'<a href="/locations/{loc_id}">{loc_name}</a>')
            page_html = page_html.replace("{{ introduction }}", t_info['description'])
            page_html = page_html.replace("{{ content }}", local_t_content)
            
            with open(os.path.join(local_t_dir, "index.html"), "w") as f:
                f.write(page_html)
            generated_urls.append(f"/locations/{loc_id}/{t_id}")
            
    print(f"Compiled {len(generated_urls)} total pages.")
    
    # 3. Generate Sitemap XML
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # Add home page
    usr = ET.SubElement(urlset, "url")
    loc = ET.SubElement(usr, "loc")
    loc.text = f"{DOMAIN}/"
    
    for url_path in generated_urls:
        usr = ET.SubElement(urlset, "url")
        loc = ET.SubElement(usr, "loc")
        loc.text = f"{DOMAIN}{url_path}/"
        
    xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
    with open(os.path.join(BASE_DIR, "sitemap.xml"), "w") as f:
        f.write(xml_str)
    print("Sitemap XML successfully created.")
    
    # 4. Generate Robots.txt
    robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n"
    with open(os.path.join(BASE_DIR, "robots.txt"), "w") as f:
        f.write(robots_content)
    print("Robots.txt successfully created.")
    
    return generated_urls

if __name__ == "__main__":
    generate_pages()
