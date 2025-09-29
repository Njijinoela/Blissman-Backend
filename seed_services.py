from config import db, create_app
from Models.service import Service

app = create_app()
app.app_context().push()

# Clear existing
Service.query.delete()

services = [
    {
        "title": "Website Design",
        "description": "We create visually stunning, responsive, and user-friendly websites tailored to your brand...",
        "image_url": "/services/webdesign.jpg",
        "icon": "Palette",
        "portfolio": [],
        "faqs": [
            {"question": "How long does it take to design a website?", "answer": "Most websites take between 2–6 weeks depending on complexity and features."},
            {"question": "Will my website be mobile-friendly?", "answer": "Yes, all our websites are fully responsive and optimized for all screen sizes."},
            {"question": "Can you redesign an existing website?", "answer": "Absolutely, we can modernize and improve your current website."},
            {"question": "Do you provide SEO optimization?", "answer": "Yes, we include basic SEO and can offer advanced SEO as an add-on service."},
            {"question": "Will I be able to update the website myself?", "answer": "Yes, we build with user-friendly CMS platforms so you can manage your site content."}
        ]
    },
    {
        "title": "IT Support",
        "description": "Our IT support team provides reliable troubleshooting, system maintenance, and proactive monitoring...",
        "image_url": "/services/itsuppport.webp",
        "icon": "ShieldCheck",
        "portfolio": ["repairs", "maintenance", "networking"],
        "faqs": [
            {"question": "Do you provide remote IT support?", "answer": "Yes, we can resolve many issues remotely without needing an on-site visit."},
            {"question": "What systems do you support?", "answer": "We support Windows, macOS, Linux, and major enterprise applications."},
            {"question": "Is your IT support available 24/7?", "answer": "Yes, we offer round-the-clock support plans depending on your package."},
            {"question": "Can you help with network setup?", "answer": "Absolutely, we set up and secure wired and wireless networks for businesses and homes."},
            {"question": "Do you offer ongoing maintenance contracts?", "answer": "Yes, we provide flexible monthly or annual support agreements."}
        ]
    },
    {
        "title": "IT Consulting",
        "description": "We offer strategic IT consulting to help businesses align technology with growth...",
        "image_url": "/services/itconsult.jpeg",
        "icon": "Network",
        "portfolio": ["software", "security"],
        "faqs": [
            {"question": "What is IT consulting?", "answer": "It’s professional guidance to align your IT strategy with your business goals."},
            {"question": "Can you help with cloud migration?", "answer": "Yes, we assist businesses in moving safely and efficiently to the cloud."},
            {"question": "Do you provide cybersecurity consulting?", "answer": "Yes, we analyze your current setup and provide strategies to strengthen your security."},
            {"question": "Will you recommend software for my business?", "answer": "Yes, we suggest cost-effective and scalable software solutions tailored to your needs."},
            {"question": "Do you work with small businesses?", "answer": "Absolutely! We help businesses of all sizes make the most of their technology."}
        ]
    },
    {
        "title": "Company Profile Design",
        "description": "A well-crafted company profile sets you apart. We design professional and compelling profiles...",
        "image_url": "/services/profiledesign.jpeg",
        "icon": "FileText",
        "portfolio": [],
        "faqs": [
            {"question": "What is included in a company profile design?", "answer": "We include company overview, services, mission, vision, branding, and visuals."},
            {"question": "Can you design both digital and print profiles?", "answer": "Yes, we create designs optimized for both print and digital use."},
            {"question": "Do you write the content or just design?", "answer": "We offer both — we can create original content or work with text you provide."},
            {"question": "How long does it take to complete?", "answer": "Most company profiles take 1–2 weeks depending on complexity."},
            {"question": "Can you update my existing profile?", "answer": "Yes, we can refresh and modernize your current company profile."}
        ]
    },
    {
        "title": "Computer Services",
        "description": "From software installation and system upgrades to virus removal and performance optimization...",
        "image_url": "/services/compservice.jpeg",
        "icon": "Laptop",
        "portfolio": ["products"],
        "faqs": [
            {"question": "Do you install all types of software?", "answer": "Yes, we install licensed operating systems, applications, and drivers."},
            {"question": "Can you remove viruses and malware?", "answer": "Yes, we specialize in removing threats and securing your computer."},
            {"question": "Do you provide data recovery services?", "answer": "Yes, we can often recover lost files depending on the issue."},
            {"question": "Will you speed up my slow computer?", "answer": "Yes, we optimize system performance through upgrades and cleanup."},
            {"question": "Do you provide on-site computer services?", "answer": "Yes, we offer both in-shop and on-site computer support."}
        ]
    },
    {
        "title": "Computer Repair Services",
        "description": "We specialize in diagnosing and repairing computer issues — whether it’s faulty hardware, broken screens...",
        "image_url": "/services/crs.jpeg",
        "icon": "Wrench",
        "portfolio": ["repairs"],
        "faqs": [
            {"question": "What types of hardware do you repair?", "answer": "We repair motherboards, RAM, hard drives, screens, keyboards, and more."},
            {"question": "Do you replace laptop screens?", "answer": "Yes, we can replace cracked or malfunctioning screens."},
            {"question": "How long do repairs usually take?", "answer": "Simple fixes may take a few hours, while complex repairs may take 2–5 days."},
            {"question": "Do you use genuine replacement parts?", "answer": "Yes, we use high-quality parts to ensure durability and performance."},
            {"question": "Do you offer a warranty on repairs?", "answer": "Yes, we provide a warranty on most hardware and repair services."}
        ]
    },
    {
        "title": "Domains & Hosting",
        "description": "Secure your online presence with our domain registration and reliable hosting services...",
        "image_url": "/services/domain.jpeg",
        "icon": "Globe",
        "portfolio": ["printing"],
        "faqs": [
            {"question": "Can you register any domain extension?", "answer": "Yes, we register .com, .org, .co.ke, and many more extensions."},
            {"question": "Do you provide email hosting?", "answer": "Yes, we set up professional email accounts linked to your domain."},
            {"question": "Is your hosting reliable?", "answer": "Yes, our hosting has 99.9% uptime and is backed by strong security."},
            {"question": "Can I transfer my domain to you?", "answer": "Yes, we handle domain transfers with minimal downtime."},
            {"question": "Do you provide SSL certificates?", "answer": "Yes, we provide SSL to keep your website secure and trusted."}
        ]
    }
]

for s in services:
    service = Service(
        title=s["title"],
        description=s["description"],
        image_url=s["image_url"],
        icon=s["icon"],
        portfolio=s["portfolio"],
        faqs=s["faqs"]
    )
    db.session.add(service)

db.session.commit()
print("✅ Services seeded successfully!")
