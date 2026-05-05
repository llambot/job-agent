"""
Laurie Lambot — Candidate Profile
This file is the single source of truth Claude uses to rank jobs and write cover letters.
Update any section here and it propagates everywhere automatically.
"""

PROFILE = {

    "name": "Laurie Lambot",
    "credentials": "PhD, EMT",
    "email": "laurie@lambot.co",
    "website": "lambot.co",
    "phone": "(847) 246-2086",
    "address": "4 Tall Pine Ln, Boulder, CO 80302",
    "linkedin": "https://www.linkedin.com/in/laurie-lambot-phd/",

    # -------------------------------------------------------------------------
    # IDENTITY & VOICE
    # -------------------------------------------------------------------------
    "identity_summary": """
Laurie is a Belgian-born neuroscientist with a PhD from ULB (Université Libre de Bruxelles)
and 15 years of research experience across academia, industry, and clinical settings.
She is direct, scientifically precise, warm but not soft, and writes with European understatedness.
She is not a braggart — she lets the work speak. Her tone is confident and grounded.
She is also a certified EMT (IV endorsement, NREMT), volunteer medic-firefighter with
Boulder Mountain Fire Protection District, AHA BLS instructor, and pursuing paramedic certification.
She is originally from Belgium, native French speaker, and plans to relocate to Quebec.
She values pride in her work, intellectual challenge, and making a real difference.
She needs a real salary ($90k+). She prefers remote but is open to in-person.
Canadian companies are a strong bonus — especially Quebec-based.
""",

    "writing_rules": [
        "Never use em dashes ( — ) in any written communication",
        "Always include lambot.co in contact info or body when relevant",
        "Use 'volunteer medic-firefighter' where natural — never forced",
        "Sign off: Warm regards, Laurie Lambot, PhD",
        "For science/neuro jobs: lead with PhD, use EMT/fire as the memorable twist",
        "For EMS/fire jobs: lead with field credentials, PhD as the trump card",
        "Reference specific website content (lambot.co/project/...) when relevant",
        "French sign-off for Canadian/French companies: 'Chaleureusement' or 'Avec plaisir'",
        "Never use bullet points in the body of cover letters — prose only",
        "Bullet list only for the 'I offer:' section if appropriate for the role",
        "Sound human, European, thoughtful. Not American-corporate.",
    ],

    # -------------------------------------------------------------------------
    # SCIENTIFIC IDENTITY — for neuro/science/biotech jobs
    # -------------------------------------------------------------------------
    "phd": {
        "institution": "Université Libre de Bruxelles (ULB) & Collège de France",
        "year": 2015,
        "topic": "Neuroplasticity in the basal ganglia — memory, Parkinson's disease, cocaine addiction",
        "defense": "Public PhD defense, August 19, 2015, Brussels, Belgium",
    },

    "education": [
        {
            "degree": "MSc in Biomedical Science",
            "institution": "Université Catholique de Louvain (UCL)",
            "year": 2009,
            "notes": "Specialization in advanced fundamental research, minor in neuroscience"
        },
        {
            "degree": "BSc in Biomedical Sciences",
            "institution": "Université Catholique de Louvain (UCL)",
            "year": 2007,
            "notes": "School of Medicine — biology, chemistry, human physiology"
        },
    ],

    "research_experience": [
        {
            "role": "Senior Neuroscience Engineer",
            "org": "Modendo Inc.",
            "location": "Boulder, CO",
            "years": "2023 - Present",
            "highlights": [
                "Developed ultra-thin wavefront-shaping endomicroscopes for deep brain imaging",
                "Designed ISO-compliant biocompatible cranial implants (CAD/3D printing)",
                "Presented at SfN 2024, NINDS 2024, BRAIN Initiative 2023",
                "Pitched at Ascent Deep Tech Accelerator Investor Showcase (June 2024)",
                "NSF Award 2212906, NIH Award 5R43NS127710, OEDIT Advance Industries Grant",
                "Website details: lambot.co/project/chapter5/"
            ]
        },
        {
            "role": "Senior Postdoctoral Researcher",
            "org": "University of Chicago",
            "location": "Chicago, IL",
            "years": "2018 - 2023",
            "highlights": [
                "Designed imaging tools for sensorimotor cortex plasticity",
                "Built custom multimodal recording platforms from scratch (2-photon + cameras + encoders)",
                "Recorded activity from 400+ neurons simultaneously",
                "Implemented DeepLabCut ML pipelines for behavioral analysis",
                "Built generalized linear models predicting neural activity from physiological signals",
                "Website details: lambot.co/project/chapter2/",
                "Testimonial from Jason N. MacLean PhD (Director of Undergraduate Studies, UChicago): 'The breadth of her work is highly unusual and demonstrates a tremendous intellect.'"
            ]
        },
        {
            "role": "Postdoctoral Researcher",
            "org": "Northwestern University, Feinberg School of Medicine",
            "location": "Chicago, IL",
            "years": "2016 - 2018",
            "highlights": [
                "Investigated synaptic circuits and astrocyte-neuron interactions",
                "Developed open-source viral vectors (rAAV2-retro) shared globally",
                "Built WaveSurfer data acquisition software (presented SfN 2017)",
                "Optogenetic cortical motor mapping of corticospinal neurons",
                "Collaborated with Janelia Research Campus (HHMI)",
            ]
        },
        {
            "role": "Research Scientist",
            "org": "Janssen Pharmaceuticals",
            "location": "Belgium",
            "years": "2015 - 2016",
            "highlights": [
                "Developed human neuronal models from iPSCs to study Alzheimer's disease",
                "Contributed to xenotransplantation techniques for chimeric AD mouse model",
                "Work published in Neuron (2017) — featured in Nature Reviews Neurology, Science Daily, La Libre",
                "Presented to Janssen R&D leadership and European neuroscience leaders",
            ]
        },
        {
            "role": "PhD Fellow in Neuroscience",
            "org": "Université Libre de Bruxelles (ULB)",
            "location": "Brussels, Belgium",
            "years": "2010 - 2015",
            "highlights": [
                "Studied NMDA receptors in striatopallidal neurons",
                "Generated conditional knock-out mouse model (GluN1 deletion in iMSNs)",
                "Published in Journal of Neuroscience (2016)",
                "Mentored students, international conference presentations",
                "Funded by FRIA PhD Fellowship, Fondation Médicale Reine Elisabeth, Van Buuren Grant"
            ]
        },
    ],

    "publications": [
        {
            "journal": "Science Signaling",
            "year": 2019,
            "title": "CRAC channels regulate astrocyte Ca2+ signaling and gliotransmitter release to modulate hippocampal GABAergic transmission",
            "authors": "Toth AB, Hori K, Novakovic MM, Bernstein NG, Lambot L, Prakriya M.",
            "url": "https://www.science.org/doi/10.1126/scisignal.aaw5450"
        },
        {
            "journal": "Nature Neuroscience",
            "year": 2019,
            "title": "Long-range inhibitory intersection of a retrosplenial thalamocortical circuit by apical tuft-targeting CA1 neurons",
            "authors": "Yamawaki N, Li X, Lambot L, Ren LY, Radulovic J, Shepherd GMG.",
            "url": "https://www.nature.com/articles/s41593-019-0355-x"
        },
        {
            "journal": "Neuron",
            "year": 2017,
            "title": "Hallmarks of Alzheimer's Disease in Stem-Cell-Derived Human Neurons Transplanted into Mouse Brain",
            "authors": "Espuny-Camacho I, [...] Lambot L, [...] Vanderhaeghen P, De Strooper B.",
            "url": "https://www.cell.com/neuron/fulltext/S0896-6273(17)30058-2",
            "media": ["Science Translational Medicine Editor's Choice", "Nature Reviews Neurology", "Science Daily", "La Libre (Belgian press)"]
        },
        {
            "journal": "Journal of Neuroscience",
            "year": 2016,
            "title": "Striatopallidal Neuron NMDA Receptors Control Synaptic Connectivity, Locomotor, and Goal-Directed Behaviors",
            "authors": "Lambot L, Chaves Rodriguez E, Houtteman D, Li Y, Schiffmann SN, Gall D, de Kerchove d'Exaerde A.",
            "url": "https://www.jneurosci.org/content/36/18/4976.long",
            "media": ["Focus on Belgium", "ULB News — The Key Role of the NMDA Glutamate Receptor"]
        },
        {
            "journal": "Médecine/Sciences (Paris)",
            "year": 2016,
            "title": "Towards optical in vivo electrophysiology",
            "authors": "Lambot L, Gall D.",
            "url": "https://www.medecinesciences.org/en/articles/medsci/full_html/2016/08/medsci2016328-9p768/medsci2016328-9p768.html"
        },
        {
            "journal": "Disease Models & Mechanisms",
            "year": 2013,
            "title": "Neurons and cardiomyocytes derived from induced pluripotent stem cells as a model for mitochondrial defects in Friedreich's ataxia",
            "url": "https://journals.biologists.com/dmm/article/6/3/608/3411/"
        },
        {
            "journal": "Frontiers in Molecular Neuroscience",
            "year": 2012,
            "title": "Control of neuronal excitability by calcium binding proteins: a new mathematical model for striatal fast-spiking interneurons",
            "url": "https://www.frontiersin.org/journals/molecular-neuroscience/articles/10.3389/fnmol.2012.00078/full"
        },
    ],

    "editorial_roles": [
        "Review Editor, Cellular Neurophysiology, Frontiers (since 2023)",
        "Review Editor, Motivation and Reward, Frontiers in Behavioral Neuroscience (since 2023)",
        "Review Editor, Neurophotonics, SPIE (since 2025)",
    ],

    "key_testimonials": [
        {
            "from": "Jason N. MacLean, PhD (Professor, UChicago)",
            "quote": "The breadth of her work is highly unusual and demonstrates a tremendous intellect."
        },
        {
            "from": "Tim Morrissey, PhD (Investor, Drive Capital)",
            "quote": "Laurie is not just a scientist; she's a leader who understands how to translate innovative research into commercially viable products."
        },
        {
            "from": "Arianna Maffei, PhD (Specialty Chief Editor, Frontiers)",
            "quote": "Her inclusion was a unanimous decision, reflecting her outstanding scientific reputation."
        },
        {
            "from": "Pierre Vanderhaeghen, MD PhD (VIB Centre)",
            "quote": "Her innovative approach offers a unique opportunity to revolutionize Alzheimer's research."
        },
    ],

    "technical_skills": [
        "Python, MATLAB, C++",
        "Machine learning: DeepLabCut, GLMs, deep learning architectures",
        "2-photon microscopy, optical intrinsic imaging, wavefront shaping",
        "CAD design (Fusion360), 3D printing, biocompatible implant design",
        "Electrophysiology (patch-clamp, in vivo recording)",
        "Viral vector development (rAAV2-retro)",
        "Adobe Suite, WordPress",
        "Experimental programming (LabView, Arduino)",
        "Data visualization, statistical modeling",
    ],

    "website_projects": [
        {"title": "Chapter 1: Synaptic Plasticity", "url": "lambot.co/project/chapter1/"},
        {"title": "Chapter 2: Non-Synaptic Plasticity (multimodal recording platform)", "url": "lambot.co/project/chapter2/"},
        {"title": "Chapter 3: Friedreich's Ataxia", "url": "lambot.co/project/chapter3/"},
        {"title": "Chapter 4: Alzheimer's Disease", "url": "lambot.co/project/chapter4/"},
        {"title": "Chapter 5: Driving Innovation (Modendo, deep brain imaging)", "url": "lambot.co/project/chapter5/"},
        {"title": "Digital Fabrication for Multimodal Recording", "url": "lambot.co/project/multimodal-recording/"},
        {"title": "Head Attachment Tool (HAT) — cranial implant system", "url": "lambot.co/project/hat/"},
        {"title": "Marmoset contention jacket design", "url": "lambot.co/project/marmoset/"},
        {"title": "Motor cortex mapping with laser precision", "url": "lambot.co/project/motor/"},
        {"title": "Pupil dynamics and whisking with DeepLabCut", "url": "lambot.co/project/pupil3/"},
    ],

    # -------------------------------------------------------------------------
    # CLINICAL & FIRE IDENTITY — for EMS/fire/hybrid jobs
    # -------------------------------------------------------------------------
    "clinical_and_fire": {
        "emt": "Colorado-certified EMT, IV endorsement, NREMT",
        "als_experience": "UCHealth Loveland Emergency Department (started Jan 2026)",
        "bls_instructor": "AHA BLS Instructor",
        "fire": "Volunteer medic-firefighter, Boulder Mountain Fire Protection District (BMFPD) + Lefthand Fire",
        "wildland": "NWCG taskbooks: MEDL(t), ICT5, FFT1; deployments on Gifford and Garnet fires",
        "ff_certifications": "FF1 + FF2 (Colorado DFPC, IFSAC)",
        "paramedic": "Pursuing paramedic certification (PERCOMOnline, starting imminently)",
        "awards": "Rookie of the Year 2024, BMFPD",
        "other": "S-359 (MEDL prerequisite) completed; 2026 RMA Priority Trainee Program accepted",
    },

    # -------------------------------------------------------------------------
    # JOB SEARCH PREFERENCES
    # -------------------------------------------------------------------------
    "job_preferences": {
        "focus": "Science jobs that use the PhD — neuroscience, biotech, neurotech, digital health, medical research, clinical science",
        "salary_min_usd": 90000,
        "location": "Remote preferred, Colorado in-person ok",
        "canada_bonus": True,
        "canada_note": "Quebec especially valued — native French speaker, planning relocation",
        "avoid": ["Pure admin roles", "Jobs below $90k", "Roles with no intellectual challenge"],
        "pride_filter": True,
    },
}

# Quick string for use in Claude prompts
PROFILE_SUMMARY = f"""
Candidate: Laurie Lambot, PhD
Website: lambot.co
Email: laurie@lambot.co
Location: Boulder, CO (remote preferred)

PhD: Neuroscience, ULB Brussels (2015)
Research: 15 years — Northwestern, U Chicago, Janssen Pharma, Modendo Inc.
Publications: Nature Neuroscience, Neuron, J Neuroscience, Science Signaling, and more
Clinical: EMT (IV endorsement, NREMT), AHA BLS Instructor, UCHealth Loveland ED
Fire: Volunteer medic-firefighter, BMFPD + Lefthand Fire; wildland deployments
Paramedic: Pursuing certification imminently
Languages: English (bilingual), French (native)
Canada: Strong preference for Canadian employers, especially Quebec

Writing rules:
- No em dashes ever
- Always include lambot.co
- Volunteer medic-firefighter (not forced)
- Warm regards, Laurie Lambot, PhD
- Lead with PhD for science jobs; EMT/fire is the memorable twist
"""
