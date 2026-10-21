"""Generates index.html, services/*.html and sitemap.xml. Run: python3 build.py

All business facts live here once. Only add copy that is verified (current site / Google profile).
"""
import html, json, pathlib

BASE = "https://revupag.github.io/sandpoint-tree-services/"
NAME = "Sand Point Tree Services LLC"
PHONE, TEL = "(321) 746-8933", "+13217468933"
EMAIL = "sandpointe5tar@gmail.com"
GMAPS = "https://www.google.com/maps/place/data=!4m2!3m1!1s0x2f2010b05a15b7ad:0xd5bb09c6d27dcad5"
FB = "https://www.facebook.com/profile.php?id=61575041909936"
WA = "https://wa.me/13217468933?text=" + "Hi%20Sand%20Point!%20I%27d%20like%20a%20free%20tree%20service%20estimate."
ROOT = pathlib.Path(__file__).parent

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1L6.6 10.8z"/></svg>',
    "wa": '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><path d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6a10.6 10.6 0 0 1-5.4-1.5l-.4-.2-3.9 1 1-3.8-.2-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7.1a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.5l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.7 3.7 0 0 0-1.1 2.7 6.4 6.4 0 0 0 1.4 3.4 14.6 14.6 0 0 0 5.6 4.9c2.1.9 2.9 1 3.9.8a3.3 3.3 0 0 0 2.2-1.5 2.7 2.7 0 0 0 .2-1.5c-.1-.2-.3-.3-.6-.4z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/></svg>',
    "broom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M14 3 9 14M5 21l3-8 6 2-1 7M7 17l2 1M10 16l1 3"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3 7 7 .6-5.4 4.6 1.7 7.3L12 17.8 5.7 21.5l1.7-7.3L2 9.6 9 9z"/></svg>',
    "left": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M15 18 9 12l6-6"/></svg>',
    "right": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m9 18 6-6-6-6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
}

# Verbatim Google reviews (all 13, all 5 stars), captured 2026-10-21.
REVIEWS = {
    "ruth": ("Ruth Ann Donahue", "I called Vern to get a quote and he was out within 2 days to quote and did the tree work that very week! He and his worker did an excellent job taking down a dead tree, trimming down my live oak and also trimming up my 3 palms. He did amazing work and cleaned the property up before he left. Great service, great pricing and I would highly recommend this local company for your tree project."),
    "kjohnson": ("Kathie Johnson", "Vern and his team started by trimming several of our very large oak trees, and then we had them take down a massive oak tree that was rotting. They worked hard, price was very good, and they cleaned everything up after finishing. Would recommend Sand Point Tree Services and have recommended them to many neighbors and clients!"),
    "deme": ("Deme V", "Vern did an excellent job from start to finish. He was professional, showed up when he said he would, and worked efficiently while keeping the area clean and safe. The quality of the work exceeded my expectations, and his pricing was fair for the service provided. I would definitely recommend his tree service to anyone looking for reliable and professional work."),
    "jennifer": ("Jennifer Simpson", "I’ve used Sand Point Tree Services many times personally as well as using them to take care of problem trees on rental properties.. They always do a great job! Very respectful , and conscientious about cleanup and leaving things better than they found it. Highly recommend."),
    "barb": ("Barb Andes", "They are very professional, quick, and courteous. They did a wonderful job cutting down our big Tree . They cleaned up everything and took care of all the tree mess. My Husband and I were very pleased on how they treated our yard . We highly recommend this Tree Company to anyone."),
    "tina": ("Tina Harvill", "Highly recommend Vern and Sand Point Tree Services if you are looking for a job done well at a realistically affordable price. There when scheduled from the first meeting until the last. Beautiful results!! Definitely would use this service again!!"),
    "kanderson": ("Kathie Anderson", "We have used this tree service several times. Vern does great work & I highly recommend him. Such a hard worker and so pleasant to talk to. Listens to what you ask him to do and he will make sure you are happy with what he has done."),
    "melissa": ("Melissa Tyo-Grooten", "Paul and his co-worker were communicative, knowledgeable and attentive to work they were doing on the palms in my yard. They were very professional and left my yard looking great and my palms cut to perfection!"),
    "dianne": ("Dianne Bean", "Vern showed up on time. Showed me his liability policy which I think is important. Was careful to listen to what I wanted. Cleaned up and took everything with him. Very polite and friendly. Hired him twice"),
    "rhonda": ("Rhonda Cox", "Vern was awesome! Came out when he said he would, and was on-time. We all know that’s not very common. I would highly recommend him and his services!"),
    "betsy": ("Betsy West", "Great communication. Cleanup was spotless. Sand point tree services puts pride into their work. Thanks"),
    "roger": ("Roger Prieto", "Excellent service fast and very clean recommend 100%"),
    "ray": ("rayfarag", "Had a great experience. I highly recommend!"),
}

# Benefit and FAQ text comes from sandpointtreeservices.com service pages (insurance/certification claims left out).
SERVICES = [
    dict(
        slug="tree-removal", short="Tree Removal", nav="Tree Removal & Storm Damage",
        title="Tree Removal Titusville FL | Hazardous & Storm-Damaged Trees",
        desc="Safe tree removal in Titusville, FL for dead, rotting, hazardous and storm-damaged trees, with full cleanup and stump grinding. Sand Point Tree Services – call (321) 746-8933.",
        h1=("Tree Removal", "in Titusville, FL"),
        tagline="Safe removal of hazardous, dead or storm-damaged trees, and a clean yard when we leave.",
        hero="tree-removal.jpg", hero_alt="Large tree trunk sections and stump left after a tree removal in a Titusville yard",
        side="removal-in-progress.jpg", side_alt="Dead tree being cut back in stages beside a home",
        intro=[
            "When a tree is dead, rotting, leaning over your home or damaged in a storm, it needs to come down the right way. Sand Point Tree Services removes unwanted and dangerous trees for homeowners and property owners in Titusville and across Brevard County.",
            "Our crew takes trees down in controlled sections, protects the rest of your property while we work, and hauls away the logs, branches and debris. Need the stump gone too? We can grind it below ground level so the area is ready for grass, plants or construction.",
        ],
        signs=["Dead or mostly bare trees", "Trunks that are rotting, cracked or hollow", "Trees leaning toward your house, fence or driveway",
               "Storm-damaged trees with split trunks or hanging limbs", "Trees crowding your roof, power lines or foundation"],
        benefits=[("Fast storm damage response", "We quickly assess and remove hazardous trees to protect your property after storms."),
                  ("Safe & professional removal", "Our experienced arborists prioritize safety while efficiently removing unwanted or dangerous trees."),
                  ("Thorough cleanup & site restoration", "We ensure your landscape is left clean and safe with comprehensive debris removal."),
                  ("Long-term tree care", "Beyond removal, we offer pruning and health assessments to keep your remaining trees thriving.")],
        photos=[("storm-cleanup.jpg", "Damaged tree being taken down next to a home with cut branches below"),
                ("climb-ladder.jpg", "Climber working at the top of a tall dead tree before removal"),
                ("tree-thinning.jpg", "Tree cut back next to a fence before full removal")],
        reviews=["kjohnson", "barb", "ruth", "dianne"],
        faqs=[("How quickly can you respond to storm damage in Titusville?", "We prioritize emergency calls and aim to respond promptly to assess and address storm-related hazards."),
              ("What should I do if a hazardous tree threatens my property?", "Contact us immediately for a thorough assessment. We can recommend safe removal or mitigation measures."),
              ("Do you handle stump grinding after tree removal?", "Absolutely. We provide stump grinding and site cleanup to restore your landscape's appearance."),
              ("Can you assist with trees damaged in storms in the Port St. John area?", "Yes, we serve Port St. John FL and nearby areas with storm damage response and hazardous tree removal.")],
    ),
    dict(
        slug="tree-trimming", short="Tree Trimming", nav="Tree Trimming & Pruning",
        title="Tree Trimming Titusville FL | Pruning, Palms & Canopy Care",
        desc="Professional tree trimming and pruning in Titusville, FL: canopy thinning, shaping, deadwood removal and palm trimming. Sand Point Tree Services – call (321) 746-8933.",
        h1=("Tree Trimming", "& Pruning in Titusville"),
        tagline="Pruning, shaping and canopy thinning for healthier, safer, better-looking trees, palms included.",
        hero="tree-pruning.jpg", hero_alt="Freshly trimmed oak tree with a balanced canopy in front of a Titusville home",
        side="climber.jpg", side_alt="Climber in a safety harness trimming high in a tree",
        intro=[
            "Regular trimming keeps your trees healthy, strong and good-looking, and it keeps heavy limbs away from your roof, driveway and power lines. Sand Point Tree Services trims and prunes oaks, shade trees and palms for homes and properties in Titusville and throughout Brevard County.",
            "We remove dead and weak branches, thin crowded canopies, raise low limbs and shape trees so they fit your landscape. Every job ends the same way: the branches and debris are cleaned up and hauled off.",
        ],
        signs=["Branches hanging over your roof, pool or driveway", "Dead, broken or weak limbs", "A dense canopy that blocks light and wind",
               "Palms with dead fronds or seed pods", "Low limbs blocking walkways, the street or your view"],
        benefits=[("Promotes tree health", "Proper pruning encourages healthy growth and prevents disease, ensuring your trees thrive for years to come."),
                  ("Enhances safety", "Removing dead or weak branches reduces the risk of storm damage or falling limbs that could harm people or property."),
                  ("Improves aesthetics", "Shaping and thinning the canopy enhances your landscape's beauty and curb appeal."),
                  ("Prevents structural issues", "Regular canopy care helps identify and address potential structural problems early.")],
        photos=[("oak-trim.jpg", "Large shade tree after trimming over a residential street"),
                ("palm-trim.jpg", "Tall palm tree trimmed beside a home"),
                ("tree-shaping.jpg", "Tree shaped and mulched in the middle of a front lawn")],
        reviews=["melissa", "ruth", "kjohnson", "kanderson"],
        faqs=[("How often should I have my trees pruned?", "The frequency depends on the tree species and growth rate. Generally, annual or bi-annual pruning helps maintain optimal health."),
              ("Will pruning harm my trees?", "When done correctly by experienced arborists, pruning promotes healthy growth and does not harm your trees."),
              ("Can you help with storm-damaged trees?", "Yes, we respond promptly to storm damage to assess and safely prune or remove affected trees."),
              ("Do you serve areas outside Titusville?", "Absolutely. We provide tree pruning and canopy care services throughout Rockledge, Cocoa, Port St. John, Palm Bay, Mims and surrounding areas.")],
    ),
    dict(
        slug="stump-grinding", short="Stump Grinding", nav="Stump Grinding & Cleanup",
        title="Stump Grinding Titusville FL | Stump Removal & Site Cleanup",
        desc="Stump grinding in Titusville, FL: stumps ground below ground level, wood chips and debris cleaned up. Sand Point Tree Services – call (321) 746-8933 for a free estimate.",
        h1=("Stump Grinding", "in Titusville, FL"),
        tagline="Old stumps ground below ground level, with the chips and debris cleaned up.",
        hero="stump-grinding.jpg", hero_alt="Ground-down stump area covered in fresh wood mulch in a front lawn",
        side="hero.jpg", side_alt="Crew member cutting a large trunk down close to the ground with a chainsaw",
        intro=[
            "A leftover stump is a tripping hazard, an eyesore and an obstacle for mowing, planting or building. Sand Point Tree Services grinds stumps in Titusville and across Brevard County so you can finally use that part of your yard again.",
            "We use specialized equipment to grind the stump below ground level, take care to protect the plants and lawn around it, and remove the debris and wood chips so your property is left clean.",
        ],
        signs=["Stumps left behind after an old tree removal", "Stumps in the way of mowing or new landscaping",
               "Areas you want to replant or build on", "Stumps that are sprouting new shoots"],
        benefits=[("Safe & efficient removal", "We use modern equipment to quickly and safely grind stumps and clear debris from your property."),
                  ("Thorough site cleanup", "Our team ensures your yard is clean and ready for future landscaping or construction projects."),
                  ("Minimal landscape impact", "We take care to protect your surrounding plants and landscape during the cleanup process."),
                  ("Done on schedule", "Smaller jobs can often be completed within a few hours, and we show up when we say we will.")],
        photos=[("stump-ground.jpg", "Front yard with a ground stump and fresh mulch after tree removal"),
                ("yard-cleanup.jpg", "Clean patio and yard after tree work"),
                ("tree-removal.jpg", "Stump and log sections after a tree was taken down")],
        reviews=["betsy", "dianne", "jennifer", "roger"],
        faqs=[("How does stump grinding work?", "Stump grinding involves using specialized equipment to grind the remaining stump below ground level, eliminating tripping hazards and preparing the area for replanting or construction."),
              ("Is site cleanup included in stump grinding?", "Yes, our service includes thorough removal of debris and wood chips resulting from stump grinding to leave your property clean."),
              ("How long does a typical stump grinding job take?", "The duration depends on the size and number of stumps. Smaller jobs can be completed within a few hours, while larger projects may take longer."),
              ("Is there any damage to surrounding plants during stump removal?", "Our team takes care to minimize impact on surrounding landscape while efficiently removing stumps."),
              ("Do you serve areas like Cocoa and Port St. John?", "Absolutely. We provide stump grinding and site cleanup services throughout Titusville and Brevard County, including Cocoa and Port St. John.")],
    ),
    dict(
        slug="land-clearing", short="Land Clearing", nav="Land Clearing",
        title="Land Clearing Titusville FL | Tree, Brush & Lot Clearing",
        desc="Land clearing in Titusville and Brevard County: trees, brush and debris removed to prepare land for construction or landscaping. Sand Point Tree Services – (321) 746-8933.",
        h1=("Land Clearing", "in Titusville & Brevard"),
        tagline="Trees, brush and debris cleared to get your property ready for its next phase.",
        hero="land-clearing.jpg", hero_alt="Cleared dirt access path along a pasture fence line after brush and tree clearing",
        side="pasture-clearing.jpg", side_alt="Overgrown fence line being cleared next to a cattle pasture",
        intro=[
            "Planning to build, add a driveway, open up a fence line or reclaim an overgrown part of your property? Sand Point Tree Services clears trees, brush and debris for residential and rural properties in Titusville and throughout Brevard County.",
            "We clear the land thoroughly, keep safety first throughout the job, and finish with a full cleanup so the site is ready for construction, landscaping or whatever comes next.",
        ],
        signs=["Lots that need to be cleared before construction", "Overgrown fence lines and access paths",
               "Brush and small trees taking over pasture or yard", "Areas cleared for a driveway, shed or pool"],
        benefits=[("Comprehensive site preparation", "We clear the land thoroughly to prepare your property for development or landscaping."),
                  ("Safety-first approach", "Our team prioritizes safety to protect your property and ensure a smooth clearing process."),
                  ("Minimal disruption & cleanup", "We leave your site clean and ready for its next phase with minimal impact on surrounding areas."),
                  ("Experienced crew", "Trust our skilled arborists to handle land clearing efficiently and responsibly.")],
        photos=[("pasture-clearing.jpg", "Fence line along a pasture during clearing"),
                ("tree-thinning.jpg", "Trees cut back along a property fence"),
                ("storm-cleanup.jpg", "Tree and brush being cleared beside a building")],
        reviews=["deme", "tina", "jennifer", "ray"],
        faqs=[("What does land clearing involve?", "Land clearing includes removing trees, brush, and debris to prepare the land for construction or landscaping."),
              ("How long does land clearing typically take?", "The duration depends on the size and complexity of the site but generally ranges from a few days to a week."),
              ("Is land clearing safe for the environment?", "Yes, our team follows best practices to minimize environmental impact while ensuring safety and efficiency."),
              ("Can you assist with site cleanup after land clearing?", "Absolutely. We provide thorough cleanup to leave your property ready for its next use."),
              ("Where do you offer land clearing?", "We serve Titusville, Rockledge, Palm Bay, Port St. John, Mims, Cocoa and surrounding regions.")],
    ),
    dict(
        slug="storm-cleanup", short="Storm Cleanup", nav="Hurricane & Storm Cleanup",
        title="Hurricane & Storm Cleanup Titusville FL | Emergency Tree Service",
        desc="Hurricane and storm cleanup in Titusville and Brevard County: fallen trees, hazardous limbs and debris removed fast. Sand Point Tree Services – call (321) 746-8933.",
        h1=("Storm Cleanup", "Hurricane Response"),
        tagline="Rapid storm cleanup and debris removal to restore safety and peace of mind.",
        hero="storm-cleanup.jpg", hero_alt="Storm-damaged tree being removed next to a home with branches on the ground",
        side="climb-ladder.jpg", side_alt="Climber taking down a damaged tree from the top",
        intro=[
            "After a hurricane or severe storm, fallen trees and hanging limbs can block driveways, damage roofs and put your family at risk. Sand Point Tree Services responds quickly across Titusville and Brevard County to remove hazardous trees and clear storm debris.",
            "We prioritize emergency calls, work safety-first around damaged and unstable trees, and clean up thoroughly so your property is safe again as soon as possible.",
        ],
        signs=["Trees or large limbs down on your house, car or fence", "Split trunks or limbs hanging in the canopy",
               "Trees leaning after high winds or soaked ground", "Yard and driveway covered in storm debris"],
        benefits=[("Swift emergency response", "Our team responds quickly to hurricane aftermaths to clear debris and remove hazardous trees promptly."),
                  ("Safety-first practices", "We prioritize safety-first practices to ensure your property is safe and free of storm-related hazards."),
                  ("Thorough cleanup", "We haul away fallen trees, limbs and debris so your yard is clear and usable again."),
                  ("Local storm support", "Serving Titusville, Rockledge, Palm Bay and surrounding areas with reliable storm recovery services.")],
        photos=[("removal-in-progress.jpg", "Dead tree being taken down in sections beside a home"),
                ("climber.jpg", "Climber in harness working in a tall tree"),
                ("tree-removal.jpg", "Cut trunk sections after a tree was taken down")],
        reviews=["rhonda", "deme", "barb", "kanderson"],
        faqs=[("What types of storm damage do you handle?", "We manage debris removal and hazardous tree removal caused by hurricanes and severe storms."),
              ("How quickly can you respond after a storm?", "Our team prioritizes rapid response to ensure your property is addressed as soon as possible after a storm."),
              ("Do you serve areas outside Titusville?", "Absolutely. We provide hurricane response services throughout Brevard County including Rockledge, Palm Bay, Mims, Cocoa, and Port St. John.")],
    ),
]

COUNTIES = [("Brevard County", ["Titusville", "Mims", "Port St. John", "Cocoa", "Rockledge", "Palm Bay"]),
            ("Volusia County", ["New Smyrna Beach", "Edgewater", "Deltona", "DeLand", "Daytona Beach"]),
            ("Seminole County", ["Sanford", "Oviedo", "Winter Springs", "Lake Mary"]),
            ("Orange County", ["Orlando", "Winter Park", "Apopka", "Christmas"])]

e = html.escape


def business_schema(p):
    return {
        "@context": "https://schema.org", "@type": ["LocalBusiness", "TreeService"], "@id": BASE + "#business",
        "name": NAME, "url": BASE, "image": BASE + "img/hero.jpg", "logo": BASE + "img/logo.jpg",
        "telephone": "+1-321-746-8933", "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Titusville", "addressRegion": "FL", "postalCode": "32754", "addressCountry": "US"},
        "areaServed": [{"@type": "AdministrativeArea", "name": c + ", FL"} for c, _ in COUNTIES],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                       "opens": "09:00", "closes": "18:00"}],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "13"},
        "sameAs": [GMAPS, FB],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Tree services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["nav"], "url": BASE + "services/" + s["slug"] + ".html"}} for s in SERVICES]},
    }


def head(p, title, desc, canonical, image, schemas, intro=False):
    ld = "\n".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schemas)
    intro_js = ("<script>try{var q=location.search.indexOf('intro')>-1;if(q||(!matchMedia('(prefers-reduced-motion: reduce)').matches&&!sessionStorage.getItem('introSeen')))"
                "document.documentElement.classList.add('intro')}catch(e){}</script>") if intro else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}img/{image}">
<meta name="theme-color" content="#14281c">
<link rel="icon" href="{p}img/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}style.css">
<link rel="preload" as="image" href="{p}img/{image}">
{intro_js}
{ld}
</head>"""


def header(p, page):
    subs = "".join(f'<li><a href="{p}services/{s["slug"]}.html">{e(s["nav"])}</a></li>' for s in SERVICES)
    dsubs = "".join(f'<a href="{p}services/{s["slug"]}.html">{e(s["nav"])}</a>' for s in SERVICES)
    home = "" if not page else p + "index.html"
    return f"""
<body{' class="page"' if page else ''}>
<header>
  <nav class="wrap nav" aria-label="Main">
    <a class="logo" href="{p}index.html"><img src="{p}img/logo.jpg" alt="Sand Point Tree Services logo" width="94" height="40"></a>
    <div class="menu">
      <ul>
        <li class="has-sub"><a href="{home}#services">Services ▾</a><ul class="sub">{subs}</ul></li>
        <li><a href="{home}#why">Why Us</a></li>
        <li><a href="{home}#reviews">Reviews</a></li>
        <li><a href="{home}#area">Service Area</a></li>
        <li><a href="{home}#faq">FAQ</a></li>
      </ul>
      <a class="btn btn-orange call-btn" href="tel:{TEL}">{ICON['phone']} {PHONE}</a>
      <button class="burger" data-drawer aria-label="Open menu">{ICON['menu']}</button>
    </div>
  </nav>
</header>
<div class="drawer" id="drawer">
  <button class="close" data-drawer aria-label="Close menu">×</button>
  <a href="{p}index.html">Home</a>
  <a href="{home}#services">Services</a>
  <div class="small">{dsubs}</div>
  <a href="{home}#why">Why Us</a>
  <a href="{home}#reviews">Reviews</a>
  <a href="{home}#area">Service Area</a>
  <a href="{home}#faq">FAQ</a>
  <a href="{home}#estimate" style="color:var(--orange)">Free Estimate</a>
  <p style="margin-top:24px"><a class="btn btn-orange" style="font-size:1.1rem;display:inline-flex" href="tel:{TEL}">{ICON['phone']} {PHONE}</a></p>
</div>"""


def footer(p, page):
    home = "" if not page else p + "index.html"
    svc = "".join(f'<li><a href="{p}services/{s["slug"]}.html">{e(s["nav"])}</a></li>' for s in SERVICES)
    return f"""
<footer>
  <div class="wrap">
    <p class="foot-big">Have a tree that needs attention?<br><a href="tel:{TEL}">Call {PHONE}</a></p>
    <div class="foot-grid">
      <div>
        <span class="logo" style="display:inline-block;margin-bottom:14px"><img src="{p}img/logo.jpg" alt="Sand Point Tree Services logo" loading="lazy" style="height:48px"></span>
        <p>{NAME}<br>Tree trimming, tree removal and stump grinding in Titusville, FL and Central Florida.</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="tel:{TEL}">{PHONE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>Titusville, FL 32754</li>
        <li>Open daily 9 AM – 6 PM</li>
        <li><a href="{home}#estimate">Free estimate</a></li></ul></div>
      <div><h4>Service Areas</h4><ul>{''.join(f'<li>{c}</li>' for c, _ in COUNTIES)}</ul>
        <h4 style="margin-top:20px">Follow</h4><ul><li><a href="{GMAPS}" target="_blank" rel="noopener">Google Reviews</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
    </div>
    <p class="copy">© <span id="yr">2026</span> {NAME}. All rights reserved.</p>
  </div>
</footer>
<a class="wa" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">
  <span class="wa-tip">Need a tree quote?<small>Chat with us on WhatsApp</small></span>
  <span class="wa-btn">{ICON['wa']}</span>
</a>
<div class="callbar">
  <a class="btn btn-orange" href="tel:{TEL}">{ICON['phone']} Call Now</a>
  <a class="btn btn-green" href="{home}#estimate">Free Estimate</a>
</div>
<script src="{p}main.js" defer></script>
</body>
</html>
"""


def review_cards(keys):
    out = []
    for k in keys:
        n, t = REVIEWS[k]
        out.append(f'<figure class="review"><span class="stars" aria-label="5 out of 5 stars">★★★★★</span>'
                   f'<blockquote>{e(t)}</blockquote><figcaption><i aria-hidden="true">{e(n[0].upper())}</i>'
                   f'<span>{e(n)}<small>Google review</small></span></figcaption></figure>')
    return "\n".join(out)


def carousel(keys, title="What Customers Say"):
    return f"""
<section id="reviews">
  <div class="wrap">
    <div class="rev-head reveal">
      <div><span class="eyebrow">Google reviews</span><h2>{title}</h2></div>
      <a class="score" href="{GMAPS}" target="_blank" rel="noopener" style="text-decoration:none">
        <b>5.0</b><div><span class="stars" aria-label="5 out of 5 stars">★★★★★</span><small>Based on 13 Google reviews</small></div>
      </a>
    </div>
    <div class="carousel reveal" aria-roledescription="carousel" aria-label="Customer reviews">
      <div class="track">
{review_cards(keys)}
      </div>
      <div class="progress"><span></span></div>
      <div class="car-ctrl">
        <div class="dots"></div>
        <div class="arrows">
          <button class="arrow prev" aria-label="Previous review">{ICON['left']}</button>
          <button class="arrow next" aria-label="Next review">{ICON['right']}</button>
        </div>
      </div>
    </div>
    <p style="text-align:center;margin-top:28px"><a class="btn btn-outline" href="{GMAPS}" target="_blank" rel="noopener">Read our reviews on Google →</a></p>
  </div>
</section>"""


def faq_block(faqs, title="Frequently Asked Questions"):
    items = "\n".join(f'<details class="reveal"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)
    return f"""
<section id="faq" style="background:#fff">
  <div class="wrap faq">
    <span class="eyebrow">FAQ</span>
    <h2 class="reveal">{title}</h2>
{items}
  </div>
</section>"""


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def estimate_block(p, selected=""):
    opts = ["Tree removal", "Tree trimming / pruning", "Palm trimming", "Stump grinding", "Land clearing", "Storm / hurricane cleanup", "Other / not sure"]
    o = "".join(f'<option{" selected" if x == selected else ""}>{x}</option>' for x in opts)
    return f"""
<section class="estimate" id="estimate">
  <div class="wrap estimate-grid">
    <div class="reveal">
      <span class="eyebrow">Free estimate</span>
      <h2>Get Your Free Estimate</h2>
      <p class="lead">Send us a few details about the job and we'll get back to you. For storm damage or anything urgent, call or WhatsApp us.</p>
      <ul class="contact-list">
        <li><span class="ico">{ICON['phone']}</span><div><small>Call or text</small><a href="tel:{TEL}">{PHONE}</a></div></li>
        <li><span class="ico" style="background:var(--wa)">{ICON['wa']}</span><div><small>WhatsApp</small><a href="{WA}" target="_blank" rel="noopener">Message us</a></div></li>
        <li><span class="ico">{ICON['mail']}</span><div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="ico">{ICON['clock']}</span><div><small>Hours</small><strong>Open every day, 9 AM – 6 PM</strong></div></li>
      </ul>
    </div>
    <form id="estimate-form" class="reveal d1" action="mailto:{EMAIL}" method="post" enctype="text/plain">
      <div class="two">
        <label>Name<input name="name" autocomplete="name" required></label>
        <label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
      </div>
      <label>Address / City<input name="address" autocomplete="street-address" placeholder="e.g. 123 Main St, Titusville" required></label>
      <label>Type of work<select name="work" required><option value="">Select a service…</option>{o}</select></label>
      <label>Message<textarea name="message" placeholder="Tell us about the trees: size, location, access, and anything else we should know."></textarea></label>
      <button class="btn btn-orange" type="submit">Send My Estimate Request</button>
      <p class="form-note">Submitting opens your email app with your details filled in. Just press send.</p>
    </form>
  </div>
</section>"""


CHAINSAW = """<svg class="saw" viewBox="0 0 440 160" aria-hidden="true">
<defs>
<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f5f6"/><stop offset=".45" stop-color="#a3aaae"/><stop offset=".55" stop-color="#7f878c"/><stop offset="1" stop-color="#d9dde0"/></linearGradient>
<linearGradient id="red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d4532f"/><stop offset=".6" stop-color="#a8361d"/><stop offset="1" stop-color="#7a2412"/></linearGradient>
<radialGradient id="cream" cx=".35" cy=".35"><stop offset="0" stop-color="#fbf3dc"/><stop offset="1" stop-color="#d9c79c"/></radialGradient>
</defs>
<g class="smoke"><circle cx="34" cy="122" r="9"/><circle cx="34" cy="122" r="9"/><circle cx="34" cy="122" r="9"/></g>
<g class="saw-body">
<path d="M176 66H410a14 14 0 0 1 0 28H176z" fill="url(#chrome)" stroke="#4a4f52" stroke-width="2"/>
<path class="chain teeth" d="M176 62H410a18 18 0 0 1 0 36H176" fill="none" stroke="#3a3d3f" stroke-width="12" stroke-dasharray="3 12"/>
<path class="chain" d="M176 62H410a18 18 0 0 1 0 36H176" fill="none" stroke="#1c1d1e" stroke-width="6" stroke-dasharray="5 5"/>
<g fill="#5d6468"><circle cx="205" cy="80" r="4"/><circle cx="232" cy="80" r="4"/><circle cx="410" cy="80" r="5"/></g>
<rect x="196" y="74" width="190" height="2" rx="1" fill="#fff" opacity=".5"/>
<path d="M40 128H8a6 6 0 0 1-6-6V98a6 6 0 0 1 6-6h34" fill="none" stroke="url(#chrome)" stroke-width="11" stroke-linecap="round"/>
<path d="M40 128H8a6 6 0 0 1-6-6V98a6 6 0 0 1 6-6h34" fill="none" stroke="#4a4f52" stroke-width="1.5" opacity=".6"/>
<rect x="38" y="36" width="146" height="98" rx="20" fill="url(#red)" stroke="#5c1a0c" stroke-width="2.5"/>
<path d="M50 44h120" stroke="#e8805f" stroke-width="3" stroke-linecap="round" opacity=".7"/>
<rect x="96" y="14" width="62" height="26" rx="6" fill="#3b3f42"/>
<path d="M104 16v22M112 16v22M120 16v22M128 16v22M136 16v22M144 16v22M152 16v22" stroke="#8b9296" stroke-width="3"/>
<circle cx="78" cy="84" r="27" fill="url(#cream)" stroke="#5c1a0c" stroke-width="2.5"/>
<circle cx="78" cy="84" r="9" fill="#a8361d" stroke="#5c1a0c" stroke-width="2"/>
<path d="M78 60v12M78 96v12M54 84h12M90 84h12M61 67l8 8M87 93l8 8M95 67l-8 8M69 93l-8 8" stroke="#a89668" stroke-width="2.5"/>
<path d="M58 66C40 52 30 50 20 50" fill="none" stroke="#2a2a2a" stroke-width="2" stroke-dasharray="1 2"/>
<rect x="6" y="44" width="10" height="14" rx="3" fill="#2a2a2a" transform="rotate(-10 11 51)"/>
<rect x="112" y="64" width="62" height="30" rx="4" fill="#f3e6c4" stroke="#5c1a0c" stroke-width="2"/>
<text x="143" y="78" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-weight="700" font-size="11" fill="#7a2412" letter-spacing=".5">SAND</text>
<text x="143" y="90" text-anchor="middle" font-family="Georgia,'Times New Roman',serif" font-weight="700" font-size="11" fill="#7a2412" letter-spacing=".5">POINT</text>
<g fill="#d9dde0" stroke="#5c1a0c" stroke-width="1"><circle cx="116" cy="68" r="2"/><circle cx="170" cy="68" r="2"/><circle cx="116" cy="90" r="2"/><circle cx="170" cy="90" r="2"/></g>
<circle cx="60" cy="120" r="7" fill="url(#chrome)" stroke="#4a4f52" stroke-width="1.5"/>
<path d="M70 38C70 -2 186 -2 186 40" fill="none" stroke="url(#chrome)" stroke-width="11" stroke-linecap="round"/>
<path d="M70 38C70 -2 186 -2 186 40" fill="none" stroke="#4a4f52" stroke-width="1.5" opacity=".5"/>
<rect x="172" y="48" width="16" height="66" rx="4" fill="#2f3335"/>
<g fill="#5c1a0c" opacity=".18"><circle cx="160" cy="118" r="5"/><circle cx="58" cy="50" r="3"/><circle cx="100" cy="122" r="4"/><circle cx="176" cy="46" r="2"/></g>
</g></svg>"""


def intro_block():
    brand = '<div class="intro-brand"><span class="logo"><img src="img/logo.jpg" alt=""></span><p>Tree Service · Titusville, FL</p></div>'
    return f"""
<div id="intro" aria-hidden="true">
  <div class="half top"><div class="half-in">{brand}</div></div>
  <div class="half bot"><div class="half-in">{brand}</div></div>
  <div class="cut"></div>
  {CHAINSAW}
</div>"""


def build_home():
    p = ""
    svc_cards = "\n".join(f"""      <a class="svc reveal d{i % 3}" href="services/{s['slug']}.html">
        <img src="img/{s['hero']}" alt="{e(s['hero_alt'])}" loading="lazy">
        <div class="body"><h3>{e(s['nav'])}</h3><p>{e(s['tagline'])}</p><span class="more">Learn more <i>→</i></span></div>
      </a>""" for i, s in enumerate(SERVICES))
    ticker_words = "".join(f"<span>{w}</span>" for w in ["Tree Removal", "Tree Trimming", "Palm Trimming", "Stump Grinding", "Land Clearing", "Storm Cleanup", "Titusville, FL"]) * 2
    gallery = "".join(f'<img src="img/{f}" alt="{e(a)}" loading="lazy">' for f, a in [
        ("climber.jpg", "Climber working high in a tree"), ("removal-in-progress.jpg", "Dead tree being cut back next to a home"),
        ("canopy-reduction.jpg", "Tree with reduced canopy after trimming"), ("stump-ground.jpg", "Ground stump with fresh mulch"),
        ("palm-trim.jpg", "Tall palm after trimming"), ("climb-ladder.jpg", "Climber at the top of a dead tree"),
        ("tree-shaping.jpg", "Shaped tree with mulch ring"), ("oak-trim.jpg", "Large trimmed shade tree")])
    counties = "\n".join(f'<div class="county reveal d{i}"><h3>{c}</h3><ul>{"".join(f"<li>{x}</li>" for x in cities)}</ul></div>' for i, (c, cities) in enumerate(COUNTIES))
    home_faqs = [
        ("Do you offer emergency tree removal services?", "Yes, we provide emergency tree removal and storm damage response to protect your property promptly."),
        ("How quickly can you respond after a storm?", "We prioritize emergency calls and aim to respond as soon as possible to assess and address storm-related hazards."),
        ("What should I do if a hazardous tree threatens my property?", "Contact us immediately for a thorough assessment. We can recommend safe removal or mitigation measures."),
        ("How often should I have my trees pruned?", "It depends on the tree species and growth rate. Generally, annual or bi-annual pruning helps maintain optimal health."),
        ("Will pruning harm my trees?", "When done correctly by experienced arborists, pruning promotes healthy growth and does not harm your trees."),
        ("How does stump grinding work?", "We use specialized equipment to grind the remaining stump below ground level, eliminating tripping hazards and preparing the area for replanting or construction."),
        ("Is cleanup included?", "Yes. Stump grinding includes removal of the debris and wood chips, and after tree removal or land clearing we clean up so your property is ready for its next use."),
        ("What does land clearing involve, and how long does it take?", "Land clearing includes removing trees, brush and debris to prepare the land for construction or landscaping. It depends on the size and complexity of the site, but generally ranges from a few days to a week."),
        ("What areas do you serve?", "We're based in Titusville and serve Brevard County, including Mims, Port St. John, Cocoa, Rockledge and Palm Bay, as well as Volusia, Seminole and Orange counties."),
    ]
    why = [("shield", "Safety-first approach", "Careful, controlled work that protects your home, your landscape and our crew."),
           ("clock", "On time, as scheduled", "Our customers keep telling us the same thing: we show up when we say we will."),
           ("broom", "Thorough cleanup", "We haul away the branches, logs and debris. No mess left behind."),
           ("check", "Reliable and honest", "Honest assessments, clear pricing and guidance tailored to your trees and budget.")]
    why_html = "\n".join(f'<li class="reveal d{i}"><span class="ico">{ICON[ic]}</span><div><strong>{t}</strong><span>{d}</span></div></li>' for i, (ic, t, d) in enumerate(why))

    body = f"""{intro_block()}
<main>
<section class="hero">
  <img class="hero-bg" src="img/hero.jpg" alt="Sand Point Tree Services crew member cutting a large tree trunk with a chainsaw in a Titusville front yard" fetchpriority="high">
  <div class="wrap">
    <a class="rating-pill fade-up" href="{GMAPS}" target="_blank" rel="noopener"><span class="stars" aria-hidden="true">★★★★★</span> 5.0 on Google · 13 reviews</a>
    <h1><span class="line"><span>Tree Service</span></span><span class="line"><span>in <span class="outline">Titusville</span>, FL</span></span></h1>
    <p class="fade-up">Tree trimming, tree removal, stump grinding and storm cleanup for homes and properties across Brevard, Volusia, Seminole and Orange counties.</p>
    <div class="cta-row fade-up">
      <a class="btn btn-orange" href="tel:{TEL}">{ICON['phone']} Call Now</a>
      <a class="btn btn-ghost" href="#estimate">Get a Free Estimate</a>
    </div>
  </div>
  <span class="scroll-hint">Scroll</span>
</section>
<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker_words}</div></div>

<section style="padding-bottom:0">
  <div class="wrap stats">
    <div class="stat reveal"><b><span data-count="5.0">5.0</span>★</b><span>Google rating</span></div>
    <div class="stat reveal d1"><b data-count="13">13</b><span>Five-star Google reviews</span></div>
    <div class="stat reveal d2"><b data-count="4">4</b><span>Counties served</span></div>
    <div class="stat reveal d3"><b data-count="7">7</b><span>Days a week, 9 AM – 6 PM</span></div>
  </div>
</section>

<section id="services">
  <div class="wrap">
    <span class="eyebrow">What we do</span>
    <h2 class="reveal">Our tree services</h2>
    <p class="lead reveal">From a single overgrown oak to a full lot, we handle the work and the cleanup.</p>
    <div class="svc-list">
{svc_cards}
      <div class="svc-cta reveal d2">
        <h3>Not sure what you need?</h3>
        <p>Tell us about your trees and we'll take a look and give you a free estimate.</p>
        <a class="btn" href="#estimate">Get a Free Estimate →</a>
      </div>
    </div>
  </div>
</section>

<section class="why" id="why">
  <div class="wrap why-grid">
    <div>
      <span class="eyebrow">Why choose us</span>
      <h2 class="reveal">Local crew. <span class="hl">Clean work.</span></h2>
      <p class="lead reveal">A Titusville-based tree service that shows up, listens and leaves your yard better than we found it.</p>
      <ul class="why-list">
{why_html}
      </ul>
    </div>
    <div class="why-photos reveal d1">
      <img src="img/crew.jpg" alt="Sand Point Tree Services crew in matching shirts on a client's lawn" loading="lazy">
      <img src="img/climber.jpg" alt="Climber in a safety harness working high in a tree" loading="lazy">
      <img src="img/climb-ladder.jpg" alt="Climber working at the top of a tall dead tree" loading="lazy">
      <a class="badge" href="{GMAPS}" target="_blank" rel="noopener" style="text-decoration:none"><b>5.0</b><div><span class="stars" aria-hidden="true">★★★★★</span><small>13 Google reviews</small></div></a>
    </div>
  </div>
</section>
{carousel(list(REVIEWS))}
<div class="gallery" aria-label="Recent work photos"><div class="gallery-track">{gallery}{gallery}</div></div>

<section class="area" id="area" style="margin-top:84px">
  <div class="wrap">
    <span class="eyebrow">Service area</span>
    <h2 class="reveal">Serving Central Florida</h2>
    <p class="lead reveal">Based in Titusville, we serve homes and properties throughout Brevard County and the surrounding counties.</p>
    <div class="counties">
{counties}
    </div>
    <p style="margin-top:22px;color:var(--muted)">Don't see your town? Call <a href="tel:{TEL}"><strong>{PHONE}</strong></a> and ask.</p>
  </div>
</section>
{estimate_block(p)}
{faq_block(home_faqs)}
</main>"""
    page = (head(p, "Tree Service Titusville FL | Sand Point Tree Services LLC",
                 "Tree Service Titusville FL – Sand Point Tree Services LLC offers tree trimming, tree removal, stump grinding, land clearing and storm cleanup across Brevard, Volusia, Seminole and Orange counties. Call (321) 746-8933.",
                 BASE, "hero.jpg", [business_schema(p), faq_schema(home_faqs)], intro=True)
            + header(p, False) + body + footer(p, False))
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def build_service(s):
    p = "../"
    url = BASE + "services/" + s["slug"] + ".html"
    signs = "".join(f"<li>{e(x)}</li>" for x in s["signs"])
    benefits = "\n".join(f'<div class="benefit reveal d{i % 2}"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(s["benefits"]))
    photos = "".join(f'<img class="reveal d{i}" src="{p}img/{f}" alt="{e(a)}" loading="lazy">' for i, (f, a) in enumerate(s["photos"]))
    others = "".join(f'<a href="{o["slug"]}.html">{e(o["nav"])} <span>→</span></a>' for o in SERVICES if o is not s)
    work = {"tree-removal": "Tree removal", "tree-trimming": "Tree trimming / pruning", "stump-grinding": "Stump grinding",
            "land-clearing": "Land clearing", "storm-cleanup": "Storm / hurricane cleanup"}[s["slug"]]
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["nav"], "serviceType": s["nav"], "url": url,
                  "description": s["desc"], "provider": {"@id": BASE + "#business", "@type": ["LocalBusiness", "TreeService"], "name": NAME, "telephone": "+1-321-746-8933"},
                  "areaServed": [{"@type": "AdministrativeArea", "name": c + ", FL"} for c, _ in COUNTIES]}
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": s["nav"], "item": url}]}
    body = f"""
<main>
<section class="hero page-hero">
  <img class="hero-bg" src="{p}img/{s['hero']}" alt="{e(s['hero_alt'])}" fetchpriority="high">
  <div class="wrap">
    <nav class="crumbs fade-up" aria-label="Breadcrumb"><a href="{p}index.html">Home</a> / <a href="{p}index.html#services">Services</a> / {e(s['nav'])}</nav>
    <h1><span class="line"><span>{e(s['h1'][0])}</span></span><span class="line"><span class="outline">{e(s['h1'][1])}</span></span></h1>
    <p class="fade-up">{e(s['tagline'])}</p>
    <div class="cta-row fade-up">
      <a class="btn btn-orange" href="tel:{TEL}">{ICON['phone']} Call Now</a>
      <a class="btn btn-ghost" href="#estimate">Get a Free Estimate</a>
    </div>
  </div>
</section>
<div class="ticker" aria-hidden="true"><div class="ticker-track">{''.join(f'<span>{e(s["short"])}</span><span>Titusville, FL</span><span>5.0★ on Google</span>' for _ in range(4))}</div></div>

<section>
  <div class="wrap split">
    <div class="prose reveal">
      <span class="eyebrow">{e(s['short'])} in Titusville</span>
      <h2>{e(s['nav'])}</h2>
      {''.join(f'<p>{e(x)}</p>' for x in s['intro'])}
      <h3 style="margin-top:28px;color:var(--green-800)">When to call us</h3>
      <ul class="checks">{signs}</ul>
    </div>
    <img class="reveal d1" src="{p}img/{s['side']}" alt="{e(s['side_alt'])}" loading="lazy">
  </div>
</section>

<section style="background:var(--green-100)">
  <div class="wrap">
    <span class="eyebrow">Why Sand Point</span>
    <h2 class="reveal">What You Get</h2>
    <div class="benefits">
{benefits}
    </div>
    <div class="photo-row">{photos}</div>
  </div>
</section>

<section class="why">
  <div class="wrap">
    <span class="eyebrow">How it works</span>
    <h2 class="reveal">Simple From Start to Finish</h2>
    <div class="steps">
      <div class="step reveal"><h3>Call or message</h3><p>Call, text or WhatsApp {PHONE}, or send the estimate form.</p></div>
      <div class="step reveal d1"><h3>Free estimate</h3><p>We look at the job, listen to what you want and give you a clear price.</p></div>
      <div class="step reveal d2"><h3>The work</h3><p>Our crew shows up as scheduled and gets the job done safely.</p></div>
      <div class="step reveal d3"><h3>Cleanup</h3><p>We haul away the debris and leave your property clean.</p></div>
    </div>
  </div>
</section>
{carousel(s['reviews'], 'Customers Love Our Work')}
{estimate_block(p, work)}
{faq_block(s['faqs'], e(s['short']) + ' FAQ')}
<section style="padding-top:0;background:#fff">
  <div class="wrap">
    <span class="eyebrow">More services</span>
    <div class="others">{others}</div>
  </div>
</section>
</main>"""
    page = (head(p, s["title"], s["desc"], url, s["hero"], [service_ld, crumbs_ld, faq_schema(s["faqs"])])
            + header(p, True) + body + footer(p, True))
    (ROOT / "services").mkdir(exist_ok=True)
    (ROOT / "services" / (s["slug"] + ".html")).write_text(page, encoding="utf-8")


def build_sitemap():
    urls = [BASE] + [BASE + "services/" + s["slug"] + ".html" for s in SERVICES]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build_home()
    for s in SERVICES:
        build_service(s)
    build_sitemap()
    print("built", 1 + len(SERVICES), "pages")
