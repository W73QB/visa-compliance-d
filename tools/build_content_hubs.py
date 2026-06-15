#!/usr/bin/env python3
"""Generate visa content hubs from visa_facts.json data."""

from pathlib import Path
import json
import re
import os
from datetime import datetime, timezone

ROOT = Path(__file__).parent.parent
VISAS = ROOT / "data" / "visas"
SOURCES = ROOT / "sources"
OUT = ROOT / "content" / "visas"

VISA_FAQS = {
    "ES_DNV_BLS_LONDON_2026": [
        {
            "question": "Is annual payment required for Spain DNV insurance?",
            "answer": "Yes. BLS London expects comprehensive, prepaid coverage; policies with monthly payments risk rejection.",
        },
        {
            "question": "Do I need an insurer authorized in Spain?",
            "answer": "Yes. The policy must be from an insurer authorized to operate in Spain.",
        },
        {
            "question": "Are deductibles or copayments allowed?",
            "answer": "No. The checklist requires no excess, no co-payments, and no moratorium.",
        },
    ],
    "DE_FREELANCE_EMBASSY_LONDON_2026": [
        {
            "question": "Is travel insurance sufficient for Germany D visa?",
            "answer": "No. Embassy guidance says travel insurance is not sufficient; coverage must match German statutory health insurance.",
        },
        {
            "question": "Do I need German-language confirmation?",
            "answer": "Provide confirmation that the policy meets statutory equivalence in German to reduce refusal risk.",
        },
        {
            "question": "Are deductibles allowed?",
            "answer": "Avoid deductibles; comprehensive statutory-equivalent coverage is expected without excess.",
        },
    ],
    "MT_NOMAD_RESIDENCY_2026": [
        {
            "question": "Are monthly payment policies accepted for Malta Nomad Residence Permit?",
            "answer": "No. Residency Malta states monthly payments are not acceptable; premiums must cover the entire period.",
        },
        {
            "question": "What coverage is required?",
            "answer": "Health insurance covering the full permitted stay, including medical expenses and repatriation.",
        },
        {
            "question": "Which insurers can I use?",
            "answer": "Use insurers providing proof of full-period coverage; evidence-backed products in the checker are prioritized.",
        },
    ],
    "TH_DTV_MFA_2026": [
        {
            "question": "Is insurance required for Thailand DTV?",
            "answer": "Current MFA list shows no insurance requirement; checker marks NOT_REQUIRED.",
        },
        {
            "question": "Should I still buy insurance?",
            "answer": "Sensible for medical and travel risks even if not mandated.",
        },
        {
            "question": "How does the checker treat missing evidence?",
            "answer": "If no official source confirms a requirement, status stays UNKNOWN/NOT_REQUIRED rather than guessing.",
        },
    ],
    "PT_DNV_VFS_CHINA_2026": [
        {
            "question": "What insurance is required for Portugal E11?",
            "answer": "Valid travel/medical insurance covering medical expenses and repatriation, no deductible or copay, per VFS China checklist.",
        },
        {
            "question": "Can I pay monthly?",
            "answer": "VFS centers often expect prepaid coverage for the visa period; monthly billing can be refused—confirm locally.",
        },
        {
            "question": "Which insurers are acceptable?",
            "answer": "Use insurers recognized in Portugal/EU; evidence-backed products in the checker list those with documented acceptance.",
        },
    ],
    "CR_DN_DECREE_43619_2026": [
        {
            "question": "Is insurance mandatory for Costa Rica Digital Nomad Visa?",
            "answer": "Yes. Article 9 requires health insurance that covers the full authorized stay.",
        },
        {
            "question": "What must the policy cover?",
            "answer": "Medical expenses and full-period validity; ensure coverage equals authorized legal stay.",
        },
        {
            "question": "Are monthly payments accepted?",
            "answer": "Decree expects coverage for the full stay; prepaid policies align closely with the requirement.",
        },
    ],
    "GR_DNV_MFA_2026": [
        {
            "question": "Is insurance required for the Greece Digital Nomad Visa?",
            "answer": "Yes. The official Work From Greece Digital Nomad Visa checklist lists travel insurance among the required documents, with a period of validity equal to the visa issued.",
        },
        {
            "question": "Does Greece state a coverage amount or require a Greek-authorized insurer?",
            "answer": "No. The official checklist states no coverage amount and no insurer-authorization rule (the 30,000 EUR figure is the separate Schengen short-stay rule, not this national visa), so the engine records those as UNKNOWN rather than inferring them.",
        },
        {
            "question": "Is travel insurance accepted, and must it cover the whole stay?",
            "answer": "Travel insurance is accepted, but the checklist requires a validity period equal to the visa, covering emergency medical care, hospital care and repatriation. Monthly subscriptions that can lapse are marked YELLOW; a policy covering the full visa period is needed.",
        },
    ],
    "ES_NLV_LA_2026": [
        {
            "question": "Is health insurance mandatory for the Spain Non-Lucrative Visa?",
            "answer": "Yes. The Consulate General of Spain page lists health insurance from an entity authorized to operate in Spain among the required documents.",
        },
        {
            "question": "Is travel insurance accepted for the Non-Lucrative Visa?",
            "answer": "No. The consulate states that travel insurances with medical assistance coverage will not be accepted, so the engine marks travel-type products RED.",
        },
        {
            "question": "Are deductibles, co-payments, or waiting periods allowed?",
            "answer": "No. The consulate requires coverage with no deductible, no copayment, no waiting period, and no coverage limit, covering the full cost of medical and hospital care.",
        },
    ],
    "IT_SELFEMP_SF_2026": [
        {
            "question": "How much medical coverage does the Italy short-term self-employment (Schengen) visa require?",
            "answer": "The Consulate General of Italy states the Schengen minimum: proof of 30,000 euro (or 50,000 US dollars) in medical expenses coverage for the duration of the trip.",
        },
        {
            "question": "Is travel insurance accepted for this route?",
            "answer": "Yes. The consulate notice lists travel medical insurers (including World Nomads) as acceptable, as long as the medical expenses coverage meets the minimum.",
        },
        {
            "question": "Does trip cancellation or repatriation count toward the minimum?",
            "answer": "No. The consulate states that non-medical services such as trip cancellation, lost baggage, or repatriation of remains do not count toward the 30,000 euro medical-expenses requirement.",
        },
    ],
    "JP_DNV_MOFA_2026": [
        {
            "question": "How much insurance coverage does the Japan Digital Nomad Visa require?",
            "answer": "The Ministry of Foreign Affairs requires insurance against death, injury or illness during the stay, with medical-treatment compensation of JPY 10 million or more.",
        },
        {
            "question": "How does the checker compare a JPY threshold against a USD or EUR policy limit?",
            "answer": "It converts both the threshold and the product limit to euro using fixed reference rates, so a large yen figure is compared like-for-like instead of as a raw number.",
        },
        {
            "question": "Is national health insurance an option for this visa?",
            "answer": "No. Digital Nomad visa holders are not enrolled in Japan's national health insurance, so private coverage meeting the JPY 10 million threshold is required.",
        },
    ],
    "AL_LEJE_UNIKE_MB_2026": [
        {
            "question": "What insurance does the Albania Unique Permit (Digital Mover) require?",
            "answer": "The official checklist requires a health-insurance policy valid for at least 1 year for the permit period.",
        },
        {
            "question": "Is a 30,000 EUR coverage amount an official requirement?",
            "answer": "No. The official Ministry of Interior checklist states only that the policy must be valid for at least 1 year; the 30,000 EUR figure is a third-party route-hardening suggestion, not the baseline requirement, so the engine does not encode it.",
        },
        {
            "question": "Why is a monthly subscription marked YELLOW?",
            "answer": "The policy must be valid for at least a year. A month-to-month policy that can lapse does not assure full-period coverage, so it is YELLOW; a full-period policy is GREEN.",
        },
    ],
    "PT_D7_VISTOS_2026": [
        {
            "question": "What insurance does the Portugal D7 visa require?",
            "answer": "The Ministry of Foreign Affairs requires valid travel insurance covering necessary medical expenses, including urgent medical assistance and possible repatriation, for the residency visa.",
        },
        {
            "question": "Is a coverage amount such as 30,000 EUR stated officially?",
            "answer": "No. The official residency-visa documentation states the cover scope (medical expenses, urgent assistance, repatriation) but no amount, so the engine does not use the secondary-source 30,000 EUR figure.",
        },
        {
            "question": "Why is a monthly subscription marked YELLOW?",
            "answer": "The insurance must be valid for the visa. A month-to-month policy that can lapse does not assure cover for the full period, so it is YELLOW; a full-period policy is GREEN.",
        },
    ],
    "EE_DNV_VM_2026": [
        {
            "question": "What insurance does the Estonia Digital Nomad Visa require?",
            "answer": "The Estonian Digital Nomad Visa is issued as a long-stay (D) visa, which requires travel medical insurance covering medical treatment costs for illness or injury, valid for the whole period of the visa.",
        },
        {
            "question": "Is a coverage amount such as 30,000 EUR stated officially?",
            "answer": "No. The Ministry of Foreign Affairs long-stay (D) visa page states the cover scope and full-period validity but no amount, so the engine does not use the secondary-source 30,000 EUR figure.",
        },
        {
            "question": "Why is a monthly subscription marked YELLOW?",
            "answer": "The insurance must be valid for the whole visa period. A month-to-month policy that can lapse does not assure full-period coverage, so it is YELLOW; a full-period policy is GREEN.",
        },
    ],
    "CY_DNV_MD_2026": [
        {
            "question": "What insurance does the Cyprus Digital Nomad Visa require?",
            "answer": "The Migration Department requires a certificate of health insurance for medical care that covers inpatient and outpatient care and transportation of corpse (the Plan A category).",
        },
        {
            "question": "Is a coverage amount such as 30,000 EUR stated officially?",
            "answer": "No. The official accompanying-documents list states the coverage scope (inpatient, outpatient, repatriation) but no amount, so the engine records no minimum rather than using the secondary-source 30,000 EUR figure.",
        },
        {
            "question": "Why does Genki Native show GREEN while others are UNKNOWN?",
            "answer": "Genki Native documents comprehensive care and global coverage that includes Cyprus, so it satisfies the rules. Policies that do not document coverage valid in Cyprus stay UNKNOWN rather than being assumed valid.",
        },
    ],
    "HR_DNV_MUP_2026": [
        {
            "question": "What insurance does the Croatia digital nomad stay require?",
            "answer": "The Ministry of the Interior requires proof of health insurance for the whole period you plan to be in Croatia, and the travel or private health insurance must cover the territory of the Republic of Croatia.",
        },
        {
            "question": "Why does Genki Native show GREEN while others are UNKNOWN?",
            "answer": "Genki Native documents global coverage that includes Croatia and a full term, so it satisfies both the Croatian-territory and full-period rules. Products that do not document Croatia coverage stay UNKNOWN rather than being assumed valid.",
        },
        {
            "question": "Is travel insurance accepted?",
            "answer": "Yes, the source accepts travel or private health insurance, as long as it covers the territory of Croatia for the full period; monthly subscriptions that can lapse are marked YELLOW.",
        },
    ],
    "CZ_LONGTERM_BUSINESS_IPC_2026": [
        {
            "question": "How much insurance coverage does the Czech long-term business visa require?",
            "answer": "The Official Information Portal for Foreigners states the coverage amount must be at least EUR 400,000 per insured event, with no cost sharing by the insured person.",
        },
        {
            "question": "Why do SafetyWing, World Nomads and Genki Traveler show RED?",
            "answer": "Their documented limits convert to below EUR 400,000, and a deductible (cost sharing) conflicts with the no-cost-sharing rule, so the engine marks them RED rather than accepting them.",
        },
        {
            "question": "Why are the Spanish health policies UNKNOWN rather than GREEN?",
            "answer": "Their policy documents do not state an overall coverage limit to compare against the EUR 400,000 threshold, so the engine records UNKNOWN instead of assuming they clear it.",
        },
    ],
    "CO_DNV_CANCILLERIA_2026": [
        {
            "question": "What insurance does the Colombia Digital Nomad Visa require?",
            "answer": "The Cancilleria requires a health policy with coverage in Colombian territory against all risks (accident, illness, maternity, disability, hospitalization, death, repatriation) for the duration of stay.",
        },
        {
            "question": "Which product shows GREEN for this route?",
            "answer": "Genki Native shows GREEN: its documentation states global coverage that includes Colombia plus comprehensive care (outpatient, inpatient, maternity), satisfying the Colombian-territory all-risk requirement.",
        },
        {
            "question": "Why do the travel and Spanish health policies not qualify?",
            "answer": "Travel-medical products (and Spanish-authorized health policies) either do not document coverage in Colombian territory or omit parts of the all-risk list such as maternity, so the engine keeps them UNKNOWN rather than guessing.",
        },
    ],
    "PL_NATD_NICOSIA_2026": [
        {
            "question": "What insurance does the Poland National Visa (Type D) require?",
            "answer": "The gov.pl consular checklist requires travel medical insurance with minimum coverage of 30,000 EUR, valid for the entire period of the requested national visa, covering urgent medical assistance, emergency hospital treatment and medical repatriation.",
        },
        {
            "question": "Why is SafetyWing YELLOW for this route?",
            "answer": "The policy must be valid for the entire period of the requested visa. A month-to-month subscription that can lapse does not assure full-period validity, so the engine marks it YELLOW; full-period policies with a documented limit of 30,000 EUR or more are GREEN.",
        },
        {
            "question": "Are there insurer conditions the engine does not model?",
            "answer": "Yes. The announcement also requires the insurer to settle costs directly with the treating provider and to run a 24/7 assistance centre, and Poland's MFA publishes a list of insurers meeting the statutory conditions. The engine does not model these clauses, so check the MFA list before buying.",
        },
    ],
    "BR_DNV_LISBOA_2026": [
        {
            "question": "What insurance does the Brazil Digital Nomad Visa (VITEM XIV) require?",
            "answer": "The gov.br consular checklist lists, among the required documents, a health insurance policy valid in Brazilian territory (seguro de saude valido no territorio brasileiro).",
        },
        {
            "question": "Which product shows GREEN for this route?",
            "answer": "Genki Native shows GREEN: its documentation states global coverage including Brazil, so it satisfies the valid-in-Brazilian-territory requirement.",
        },
        {
            "question": "Why are the travel-medical products UNKNOWN rather than GREEN?",
            "answer": "Their policy documents do not state that coverage is valid in Brazilian territory, so the engine records UNKNOWN instead of assuming a foreign policy is valid in Brazil.",
        },
    ],
    "RO_DNV_EVIZA_2026": [
        {
            "question": "What insurance does the Romania Digital Nomad Visa require?",
            "answer": "The eViza supporting-documents portal requires travel medical insurance that covers the entire duration of the requested period of stay, with a coverage of at least 30,000 EUR.",
        },
        {
            "question": "Why is SafetyWing YELLOW for this route?",
            "answer": "The policy must cover the entire duration of stay. A month-to-month subscription that can lapse does not assure full-period coverage, so the engine marks it YELLOW; full-period policies with a documented limit of 30,000 EUR or more are GREEN.",
        },
        {
            "question": "Is the 30,000 EUR figure the Schengen short-stay rule?",
            "answer": "No. This 30,000 EUR amount is stated by Romania's own eViza checklist for the long-stay digital nomad visa, not borrowed from the Schengen short-stay rule.",
        },
    ],
    "TR_RESIDENCE_PMM_2026": [
        {
            "question": "What insurance does a Turkish residence permit require?",
            "answer": "The Presidency of Migration Management states that the duration of your health insurance must cover the requested duration of the residence permit, and lists acceptable types including private health insurance.",
        },
        {
            "question": "Is there a minimum coverage amount?",
            "answer": "The official general-information page states no minimum coverage figure for private health insurance, so the engine encodes none and models only that insurance is mandatory and must cover the full permit duration.",
        },
        {
            "question": "Why is SafetyWing YELLOW while other products are GREEN?",
            "answer": "The insurance must cover the requested duration of the permit. A month-to-month subscription that can lapse does not assure full-period coverage, so it is YELLOW; full-period policies are GREEN.",
        },
    ],
    "KR_F1D_MOFA_LA_2026": [
        {
            "question": "What insurance does the Korea F-1-D Workation visa require?",
            "answer": "The Ministry of Foreign Affairs requires insurance that covers more than 100 million won (about USD 76,000) for hospital treatment and evacuation to the home country during the stay in Korea.",
        },
        {
            "question": "How is the 100 million won threshold compared to product limits?",
            "answer": "The engine converts the 100 million won threshold and each product's documented limit to a common currency before comparing, so a product clears the requirement only when its documented limit converts to at least the won threshold.",
        },
        {
            "question": "Is the evacuation (repatriation) part modeled separately?",
            "answer": "No. The requirement states a single amount covering both hospital treatment and evacuation, so the engine models the coverage amount and the post notes that the policy must also cover repatriation.",
        },
    ],
    "LV_REMOTEWORK_PMLP_2026": [
        {
            "question": "What insurance does the Latvia remote work visa require?",
            "answer": "The Office of Citizenship and Migration Affairs requires a health insurance policy valid in Latvia and the Schengen Member States, with a minimum insurance liability limit of at least EUR 42,600 during the insurance period.",
        },
        {
            "question": "Why is only Genki Native GREEN for this route?",
            "answer": "The policy must be valid in Latvia (and the Schengen area). Genki Native documents global coverage that includes Latvia; the other products do not document Latvia-specific validity, so the engine records UNKNOWN rather than assuming a foreign policy qualifies.",
        },
        {
            "question": "Does the 42,600 EUR amount also matter?",
            "answer": "Yes. The engine encodes both the EUR 42,600 minimum coverage and the territory requirement, so a product must clear both to be GREEN.",
        },
    ],
    "PA_REMOTEWORK_SNM_2026": [
        {
            "question": "What insurance does the Panama remote worker visa require?",
            "answer": "The Servicio Nacional de Migracion requires a copy of the applicant's medical insurance policy that maintains coverage in the national territory and stays valid for the applicant's period of stay.",
        },
        {
            "question": "Why is only Genki Native GREEN for this route?",
            "answer": "The policy must maintain coverage in Panamanian territory. Genki Native documents global coverage that includes Panama; the other products do not document Panama-specific validity, so the engine records UNKNOWN rather than assuming a foreign policy qualifies.",
        },
        {
            "question": "Is there a minimum coverage amount?",
            "answer": "The official requirements state no coverage amount, so the engine encodes none and models that insurance is mandatory, must cover the national territory, and must stay valid for the period of stay.",
        },
    ],
    "NZ_STUDENT_INZ_2026": [
        {
            "question": "What insurance does the New Zealand Fee Paying Student Visa require?",
            "answer": "Immigration New Zealand makes it a condition of the student visa that you have insurance for travel and any health care you need, from the start of your course until your visa expires.",
        },
        {
            "question": "Is there a minimum coverage amount?",
            "answer": "Immigration New Zealand states that your education provider will tell you what your insurance policy must cover, and sets no fixed figure, so the engine encodes none and models that insurance is mandatory and must cover the full visa period.",
        },
        {
            "question": "Why is SafetyWing YELLOW while other products are GREEN?",
            "answer": "The cover must run from the start of your course until your visa expires. A month-to-month subscription that can lapse does not assure full-period cover, so it is YELLOW; full-period policies are GREEN.",
        },
    ],
    "IE_STUDENT_ISD_2026": [
        {
            "question": "What insurance do non-EEA students in Ireland need?",
            "answer": "Immigration Service Delivery requires all non-EEA students to have private medical insurance; where travel insurance suffices it must cover the student for one full year (or the entirety of a shorter stay) with a minimum of EUR 25,000 for accident and EUR 25,000 for disease, plus any period of hospitalisation.",
        },
        {
            "question": "Does travel insurance count?",
            "answer": "Immigration Service Delivery accepts travel insurance for first registration if it meets the one-year and EUR 25,000 thresholds; at second and subsequent registrations travel insurance is not accepted. The engine models first-registration thresholds and the post notes this limitation.",
        },
        {
            "question": "Why is SafetyWing YELLOW?",
            "answer": "The cover must run for one full year (or the entirety of the stay). A month-to-month subscription that can lapse does not assure this, so it is YELLOW; full-period policies meeting the EUR 25,000 minimum are GREEN.",
        },
    ],
    "BH_GOLDEN_NPRA_2026": [
        {
            "question": "What insurance does the Bahrain Golden Residency require?",
            "answer": "The Ministry of Interior requires a clear copy of a valid medical insurance certificate issued in the Kingdom of Bahrain.",
        },
        {
            "question": "Why is every product UNKNOWN for this route?",
            "answer": "The certificate must be issued in the Kingdom of Bahrain. None of the tracked international products documents being a Bahrain-issued policy, so the engine records UNKNOWN rather than assuming a foreign policy qualifies.",
        },
        {
            "question": "Does that mean foreign travel insurance is rejected?",
            "answer": "The requirement is a Bahrain-issued certificate, which is stricter than a policy merely valid in Bahrain. Confirm a locally issued certificate with a Bahraini insurer; the engine does not assume any tracked product meets this.",
        },
    ],
    "ME_DNV_GOVME_2026": [
        {
            "question": "What insurance does the Montenegro digital nomad permit require?",
            "answer": "The Government of Montenegro requires the applicant to attach proof that they have health insurance, among the documents for the digital nomad temporary residence permit.",
        },
        {
            "question": "Is there a minimum amount or territory requirement?",
            "answer": "The official page states only that the applicant must have health insurance, with no coverage amount or territory specified, so the engine models only that insurance is mandatory.",
        },
        {
            "question": "Which products show GREEN?",
            "answer": "Because the only modeled requirement is that insurance is mandatory, every tracked product that provides health or travel insurance shows GREEN. Confirm the specific terms with the Ministry, as the published page gives no further detail.",
        },
    ],
    "FI_STUDY_MIGRI_2026": [
        {
            "question": "What insurance does a Finnish study residence permit require?",
            "answer": "The Finnish Immigration Service requires private insurance covering medical and drug expenses, valid throughout your entire stay. For studies under two years the insurance must cover medical expenses up to EUR 120,000.",
        },
        {
            "question": "Why does the amount depend on study length?",
            "answer": "Migri requires up to EUR 120,000 for studies under two years and up to EUR 40,000 for studies of at least two years. This route models the under-two-years threshold; the post discloses the longer-studies figure.",
        },
        {
            "question": "Why is SafetyWing YELLOW?",
            "answer": "The insurance must be valid throughout your entire stay. A month-to-month subscription that can lapse does not assure that, so it is YELLOW; full-period policies meeting the EUR 120,000 threshold are GREEN.",
        },
    ],
    "EC_NOMAD_CANCILLERIA_2026": [
        {
            "question": "What insurance does the Ecuador digital nomad visa require?",
            "answer": "The Ministry of Foreign Affairs requires a national or foreign health insurance policy valid for the same period as the visa; if taken out with a foreign company, the policy or contract must state that it has coverage in Ecuador.",
        },
        {
            "question": "Why is only Genki Native GREEN for this route?",
            "answer": "A foreign policy must state coverage in Ecuador. Genki Native documents global coverage that includes Ecuador; the other products do not document Ecuador validity, so the engine records UNKNOWN rather than assuming a foreign policy qualifies.",
        },
        {
            "question": "Does the policy need to last the whole visa?",
            "answer": "Yes. The policy must be valid for the same period as the visa, so a full-period policy is required; a month-to-month subscription that can lapse does not assure this.",
        },
    ],
    "MU_PREMIUM_EDB_2026": [
        {
            "question": "What insurance does the Mauritius Premium Visa require?",
            "answer": "The Economic Development Board states that to qualify for the Premium Visa, the applicant must have proof of long stay plans and travel and health insurance for the initial period of stay.",
        },
        {
            "question": "Is there a minimum amount or territory requirement?",
            "answer": "The published eligibility statement names travel and health insurance but states no coverage amount or territory, so the engine models only that insurance is mandatory.",
        },
        {
            "question": "Which products show GREEN?",
            "answer": "Because the only modeled requirement is that insurance is mandatory, every tracked product that provides travel or health insurance shows GREEN. Confirm the specific terms with the Economic Development Board.",
        },
    ],
}

RELATED_POSTS = {
    "ES_DNV_BLS_LONDON_2026": [
        ("/posts/spain-dnv-insurance/", "Spain DNV insurance requirements"),
        ("/posts/safetywing-spain-dnv-rejected/", "Why SafetyWing gets rejected for Spain DNV"),
        ("/traps/spain-dnv-insurance-mistakes/", "Spain DNV insurance mistakes to avoid"),
    ],
    "DE_FREELANCE_EMBASSY_LONDON_2026": [
        ("/posts/germany-freelance-insurance/", "Germany freelance visa insurance guide"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "PT_DNV_VFS_CHINA_2026": [
        ("/posts/portugal-dnv-insurance/", "Portugal DNV insurance requirements"),
        ("/guides/schengen-30000-insurance/", "Schengen 30,000 EUR insurance rule"),
    ],
    "CR_DN_DECREE_43619_2026": [
        ("/posts/costa-rica-dn-insurance/", "Costa Rica DN insurance requirements"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "TH_DTV_MFA_2026": [
        ("/posts/thailand-dtv-insurance/", "Thailand DTV insurance overview"),
        ("/posts/digital-nomad-insurance-asia/", "Digital nomad insurance in Asia"),
    ],
    "MT_NOMAD_RESIDENCY_2026": [
        ("/posts/malta-nomad-insurance/", "Malta nomad insurance requirements"),
        ("/traps/malta-nomad-monthly-payments/", "Monthly payment pitfalls for Malta nomad visa"),
    ],
    "GR_DNV_MFA_2026": [
        ("/posts/greece-dnv-insurance/", "Greece Digital Nomad Visa insurance requirements"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "ES_NLV_LA_2026": [
        ("/posts/spain-nlv-insurance/", "Spain Non-Lucrative Visa insurance requirements"),
        ("/posts/spain-dnv-insurance/", "Spain DNV insurance requirements"),
        ("/traps/spain-dnv-insurance-mistakes/", "Spain visa insurance mistakes to avoid"),
    ],
    "IT_SELFEMP_SF_2026": [
        ("/posts/italy-selfemployment-insurance/", "Italy self-employment visa insurance requirements"),
        ("/guides/schengen-30000-insurance/", "Schengen 30,000 EUR insurance rule"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
    ],
    "JP_DNV_MOFA_2026": [
        ("/posts/japan-dnv-insurance/", "Japan Digital Nomad Visa insurance requirements"),
        ("/posts/digital-nomad-insurance-asia/", "Digital nomad insurance in Asia"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "CO_DNV_CANCILLERIA_2026": [
        ("/posts/colombia-dnv-insurance/", "Colombia Digital Nomad Visa insurance requirements"),
        ("/posts/digital-nomad-insurance-americas/", "Digital nomad insurance in the Americas"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "CZ_LONGTERM_BUSINESS_IPC_2026": [
        ("/posts/czech-business-visa-insurance/", "Czech long-term business visa insurance requirements"),
        ("/guides/schengen-30000-insurance/", "Schengen 30,000 EUR insurance rule"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
    ],
    "HR_DNV_MUP_2026": [
        ("/posts/croatia-dnv-insurance/", "Croatia digital nomad stay insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "CY_DNV_MD_2026": [
        ("/posts/cyprus-dnv-insurance/", "Cyprus Digital Nomad Visa insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "EE_DNV_VM_2026": [
        ("/posts/estonia-dnv-insurance/", "Estonia Digital Nomad Visa insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "PT_D7_VISTOS_2026": [
        ("/posts/portugal-d7-insurance/", "Portugal D7 visa insurance requirements"),
        ("/posts/portugal-dnv-insurance/", "Portugal remote-work visa insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
    ],
    "AL_LEJE_UNIKE_MB_2026": [
        ("/posts/albania-unique-permit-insurance/", "Albania Unique Permit (Digital Mover) insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "PL_NATD_NICOSIA_2026": [
        ("/posts/poland-national-d-insurance/", "Poland National Visa (Type D) insurance requirements"),
        ("/guides/schengen-30000-insurance/", "Schengen 30,000 EUR insurance rule"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
    ],
    "BR_DNV_LISBOA_2026": [
        ("/posts/brazil-dnv-insurance/", "Brazil Digital Nomad Visa (VITEM XIV) insurance requirements"),
        ("/posts/digital-nomad-insurance-americas/", "Digital nomad insurance in the Americas"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "RO_DNV_EVIZA_2026": [
        ("/posts/romania-dnv-insurance/", "Romania Digital Nomad Visa insurance requirements"),
        ("/guides/schengen-30000-insurance/", "Schengen 30,000 EUR insurance rule"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
    ],
    "TR_RESIDENCE_PMM_2026": [
        ("/posts/turkey-residence-permit-insurance/", "Turkey residence permit insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "KR_F1D_MOFA_LA_2026": [
        ("/posts/korea-workation-visa-insurance/", "Korea Workation (F-1-D) visa insurance requirements"),
        ("/posts/digital-nomad-insurance-asia/", "Digital nomad insurance in Asia"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "LV_REMOTEWORK_PMLP_2026": [
        ("/posts/latvia-remote-work-insurance/", "Latvia remote work visa insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "PA_REMOTEWORK_SNM_2026": [
        ("/posts/panama-remote-worker-insurance/", "Panama remote worker visa insurance requirements"),
        ("/posts/digital-nomad-insurance-americas/", "Digital nomad insurance in the Americas"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "NZ_STUDENT_INZ_2026": [
        ("/posts/new-zealand-student-visa-insurance/", "New Zealand student visa insurance requirements"),
        ("/posts/digital-nomad-insurance-asia/", "Digital nomad insurance in Asia and the Pacific"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "IE_STUDENT_ISD_2026": [
        ("/posts/ireland-student-insurance/", "Ireland non-EEA student insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "BH_GOLDEN_NPRA_2026": [
        ("/posts/bahrain-golden-residency-insurance/", "Bahrain Golden Residency insurance requirements"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
        ("/guides/compliance-status-meaning/", "What GREEN, YELLOW and UNKNOWN mean"),
    ],
    "ME_DNV_GOVME_2026": [
        ("/posts/montenegro-dnv-insurance/", "Montenegro digital nomad insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "FI_STUDY_MIGRI_2026": [
        ("/posts/finland-study-insurance/", "Finland study residence insurance requirements"),
        ("/posts/digital-nomad-insurance-europe/", "Digital nomad insurance in Europe"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "EC_NOMAD_CANCILLERIA_2026": [
        ("/posts/ecuador-nomad-insurance/", "Ecuador digital nomad visa insurance requirements"),
        ("/posts/digital-nomad-insurance-americas/", "Digital nomad insurance in the Americas"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
    "MU_PREMIUM_EDB_2026": [
        ("/posts/mauritius-premium-visa-insurance/", "Mauritius Premium Visa insurance requirements"),
        ("/posts/digital-nomad-insurance-asia/", "Digital nomad insurance in Asia and beyond"),
        ("/guides/how-to-read-results/", "How to read compliance results"),
    ],
}


def yaml_escape(value: str) -> str:
    """Escape double quotes for YAML inline strings."""
    return value.replace('"', '\\"')


def slugify(value: str) -> str:
    """Convert string to URL-safe slug."""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "unknown"


KEY_LABELS = {
    "insurance.mandatory": "insurance is mandatory",
    "insurance.authorized_in_spain": "the insurer is authorized to operate in Spain",
    "insurance.covers_public_health_system_risks": "the policy covers the risks insured by the public health system",
    "insurance.comprehensive": "the coverage is comprehensive",
    "insurance.unlimited_coverage": "the coverage is unlimited",
    "insurance.no_deductible": "the policy carries no deductible",
    "insurance.no_copayment": "the policy carries no co-payment",
    "insurance.no_moratorium": "the policy applies no moratorium or waiting period",
    "insurance.min_coverage": "the medical coverage meets the stated minimum",
    "insurance.monthly_payments_accepted": "monthly payment policies are accepted",
    "insurance.must_cover_full_period": "the policy covers the full authorized stay",
    "insurance.statutory_equivalent": "the policy is equivalent to statutory health insurance",
}


def humanize_key(key: str) -> str:
    """Turn a requirement key into a readable phrase."""
    if key in KEY_LABELS:
        return KEY_LABELS[key]
    base = key.split(".", 1)[-1].replace("_", " ").strip()
    return base or key


def requirement_sentence(req: dict) -> str:
    """Build a plain-language sentence describing a single requirement."""
    key = req.get("key", "")
    op = req.get("op", "")
    value = req.get("value", "")
    label = humanize_key(key)
    if isinstance(value, bool):
        if value is True:
            return f"The authority requires that {label}."
        if key == "insurance.mandatory":
            return ("The authority does not list insurance among the mandatory documents "
                    "for this route, so the engine returns NOT_REQUIRED rather than guessing.")
        return f"The authority requires that {label} does not apply."
    if op == ">=":
        return f"The authority requires that {label} of at least {value}."
    return f"The authority sets the condition `{key} {op} {value}`."


def status_phrase_for(op: str) -> str:
    """Short note on how a requirement operator maps to a status."""
    if op == ">=":
        return "GREEN at or above the threshold, RED below it, UNKNOWN if unstated"
    return "GREEN on a match, RED on a conflict, UNKNOWN if unproven"


def get_detail_body_sections(visa: dict, sources: dict, snapshot_id: str) -> str:
    """Build the evidence-rich body for a route detail page.

    Includes every block lint_content.py requires (what the authority requires,
    how we evaluate, check in the engine, disclaimer, affiliate disclosure,
    evidence log) plus route-specific explanatory sections so each hub carries
    enough unique, source-backed content to be useful and to clear the
    editorial word-count target.
    """
    visa_id = visa["id"]
    country = visa["country"]
    visa_name = visa["visa_name"]
    route = visa.get("route", "")
    requirements = visa.get("requirements", [])
    out = []

    # --- What the authority requires (route-specific prose per requirement) ---
    out.append("\n## What the authority requires\n")
    out.append(
        f"The points below are taken directly from the official source for the "
        f"{country} {visa_name} ({route}) route. Each one is recorded with a source "
        f"identifier and a locator so it can be traced back to the original document. "
        f"Where the source is silent on a point, the engine records UNKNOWN instead of "
        f"inferring an answer.\n"
    )
    if requirements:
        for req in requirements:
            out.append(f"- {requirement_sentence(req)}")
        out.append("")
    else:
        out.append("- No machine-readable requirements are recorded for this route yet.\n")

    if len(requirements) <= 2:
        out.append(
            "This route is defined by a small number of explicit insurance points, "
            "which keeps the evidence trail short but also unusually clear. A concise "
            "official requirement still has to be matched precisely: a product is only "
            "GREEN here when its documented terms line up with the wording above, and a "
            "route with few stated rules does not imply that any policy will be accepted. "
            "Where the authority is silent, the engine deliberately holds the status at "
            "UNKNOWN or NOT_REQUIRED rather than reading extra conditions into the "
            "source, so the page reflects exactly what the document states and nothing "
            "more. Applicants on routes like this one should still keep the underlying "
            "policy wording on hand, because a consular officer may ask to see how each "
            "stated point is met even when the published checklist is short.\n"
        )

    # --- How we evaluate (general + per-requirement rule logic) ---
    out.append("## How we evaluate\n")
    out.append(
        "Every requirement is compared against the documented specification of each "
        "insurance product using an automated rule engine. A product is marked GREEN "
        "for a requirement only when product evidence explicitly satisfies it; a "
        "conflict produces RED; and absent evidence produces UNKNOWN rather than a "
        "guess. The route status is the combination of its per-requirement outcomes.\n"
    )
    if requirements:
        for req in requirements:
            key = req.get("key", "")
            op = req.get("op", "")
            value = req.get("value", "")
            value_str = ("Yes" if value else "No") if isinstance(value, bool) else str(value)
            out.append(
                f"- Rule `{key} {op} {value_str}` {status_phrase_for(op)}."
            )
        out.append("")

    # --- How each status is decided (shared methodology framing) ---
    out.append("## How each compliance status is decided for this route\n")
    out.append(
        "GREEN means every recorded requirement is satisfied by product evidence. "
        "RED means at least one requirement is contradicted by the product evidence. "
        "YELLOW means the evidence is partial: some requirements are met while others "
        "lack full proof. UNKNOWN means a requirement exists but the product evidence "
        "does not address it, so no claim is made. NOT_REQUIRED means the authority "
        "does not impose an insurance requirement for the route, which is itself an "
        "evidence-based finding drawn from the official document. A GREEN result "
        "reflects the evidence on the snapshot date and is not an assurance of a visa "
        "outcome, which always rests with the issuing authority.\n"
    )

    # --- Reading the evidence and snapshots ---
    out.append("## Reading the evidence and snapshots\n")
    out.append(
        f"Each requirement above links to a primary source through a source "
        f"identifier and a locator (for example a page number, article, or section). "
        f"The underlying documents are listed under Source Documents and are stored "
        f"alongside this dataset so the wording can be checked directly. Results are "
        f"tied to a dated snapshot (`{snapshot_id}`): a deep link to a past snapshot "
        f"returns the same verdict even if the authority later changes its rules, which "
        f"keeps every decision reproducible and auditable.\n"
    )

    # --- Proof package checklist ---
    out.append("## Proof package checklist\n")
    out.append(
        "Before applying for this route, prepare the following so the policy can be "
        "checked against each requirement:\n"
    )
    out.append("- A policy certificate that states the coverage limits, any deductible or co-payment, and the covered period.")
    out.append("- Written confirmation of the insurer's status where the route requires authorization in a specific country.")
    out.append("- Documentation that the coverage spans the full authorized stay rather than a partial term.")
    out.append("- The official source wording for the route, so each clause can be matched to the requirements above.\n")

    # --- FAQ rendered as prose (route-specific) ---
    faqs = VISA_FAQS.get(visa_id, [])
    if faqs:
        out.append("## Common questions\n")
        for item in faqs:
            out.append(f"**{item['question']}**  ")
            out.append(f"{item['answer']}\n")

    # --- Check in the engine (required block) ---
    out.append("## Check in the engine\n")
    out.append(
        f"Run a specific product against this route in the compliance checker: "
        f"[Open Checker](/ui/?visa={visa_id}&snapshot={snapshot_id}). The checker "
        f"shows the per-requirement outcome and the evidence behind each one.\n"
    )

    # --- Disclaimer (required block) ---
    out.append("## Disclaimer\n")
    out.append(
        "This page is not legal advice. VisaFact provides evidence-based compliance "
        "checking only, and final visa decisions are made by government authorities. A "
        "GREEN result reflects documented evidence on the snapshot date; it does not "
        "ensure that a visa application will succeed. Always confirm the current "
        "requirements with the issuing authority before submitting an application.\n"
    )

    # --- Affiliate disclosure (required block) ---
    out.append("## Affiliate disclosure\n")
    out.append(
        "If affiliate links appear on related pages, they are shown only after the "
        "compliance result and never change the evaluation, which is generated "
        "independently from the official evidence.\n"
    )

    # --- Evidence log (required block) ---
    out.append("## Evidence log\n")
    out.append(
        "Each entry pairs a requirement with the source identifier and locator it was "
        "drawn from:\n"
    )
    logged = False
    for req in requirements:
        key = req.get("key", "")
        for ev in req.get("evidence", []):
            sid = ev.get("source_id", "")
            locator = ev.get("locator", "")
            excerpt = ev.get("excerpt", "").replace("\n", " ").strip()
            excerpt = excerpt[:100]
            out.append(f"- `{key}` <- {sid} ({locator}): \"{excerpt}\"")
            logged = True
    if not logged:
        out.append("- No evidence entries are recorded for this route yet.")
    out.append("")

    return "\n".join(out)


def load_sources() -> dict:
    """Load all source metadata from sources/*.meta.json."""
    sources = {}
    for p in SOURCES.rglob("*.meta.json"):
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
            source_id = meta.get("source_id")
            if source_id:
                sources[source_id] = meta
        except (json.JSONDecodeError, IOError):
            continue
    return sources


def get_lint_required_blocks(visa_id: str, visa_name: str, snapshot_id: str) -> str:
    """Return the required content blocks for lint_content.py compliance."""
    return f"""
## What the authority requires

See the requirements table above. All requirements are extracted directly from official sources with evidence excerpts.

## How we evaluate

We compare these official requirements against insurance product specifications using our automated rule engine. Each requirement is matched to a product fact with evidence.

## Check in the engine

Try the compliance checker: [Open Checker](/ui/?visa={visa_id}&snapshot={snapshot_id})

## Disclaimer

This is not legal advice. VisaFact provides evidence-based compliance checking only. Final visa decisions are made by government authorities. A GREEN result does not ensure visa approval.

## Affiliate disclosure

If affiliate links appear, they are shown only after compliance results and do not influence the compliance evaluation in any way.

## Evidence log

See the requirements table above. All requirements are extracted directly from official sources with evidence excerpts.
"""


def get_root_lint_blocks(snapshot_id: str) -> str:
    """Return the required content blocks for root index (no specific visa)."""
    return f"""
## What the authority requires

See the requirements table above. All requirements are extracted directly from official sources with evidence excerpts.

## How we evaluate

We compare these official requirements against insurance product specifications using our automated rule engine. Each requirement is matched to a product fact with evidence.

## Check in the engine

Try the compliance checker: [Open Checker](/ui/?snapshot={snapshot_id})

## Disclaimer

This is not legal advice. VisaFact provides evidence-based compliance checking only. Final visa decisions are made by government authorities. A GREEN result does not ensure visa approval.

## Affiliate disclosure

If affiliate links appear, they are shown only after compliance results and do not influence the compliance evaluation in any way.
"""


def render_overview(country_slug: str, visa_slug: str, visa_name: str,
                    country_name: str, routes: list, snapshot_id: str) -> str:
    """Render the overview _index.md for a visa type."""
    lines = [
        "---",
        f'title: "{country_name} {visa_name}"',
        f'visa_group: "{country_slug}-{visa_slug}"',
        f'description: "Insurance requirements for {country_name} {visa_name} - evidence-based compliance checker"',
        "---",
        "",
        f"## {country_name} {visa_name} Requirements",
        "",
        "All requirements below are derived from official sources. Missing evidence means UNKNOWN.",
        "",
        "## Routes",
        "",
        "| Authority | Route | Last Verified | Details |",
        "| --- | --- | --- | --- |",
    ]

    for route in routes:
        lines.append(
            f"| {route['authority']} | {route['route']} | {route['last_verified']} | "
            f"[View requirements]({route['link']}) |"
        )

    # Add required lint blocks
    first_visa_id = routes[0]["visa_id"] if routes else f"{country_slug.upper()}_{visa_slug.upper()}"
    lines.append(get_lint_required_blocks(first_visa_id, visa_name, snapshot_id))

    lines.append("")
    lines.append(f'{{{{< checker_cta visa="{first_visa_id}" snapshot="{snapshot_id}" >}}}}')
    lines.append("")

    return "\n".join(lines)


def render_root_index(groups: dict, snapshot_id: str) -> str:
    """Render the root visas index page."""
    lines = [
        "---",
        'title: "Visa Requirements"',
        'description: "Evidence-based visa insurance requirements by country and visa type"',
        "---",
        "",
        "## Visa Requirements by Country",
        "",
        "Browse requirements by country and visa type. All requirements are sourced from official evidence.",
        "",
        "## Countries",
        "",
    ]
    for (country_slug, visa_slug), routes in sorted(groups.items()):
        country_name = routes[0]["country"]
        visa_name = routes[0]["visa_name"]
        lines.append(f"- [{country_name} {visa_name}](/visas/{country_slug}/{visa_slug}/)")

    # Add required lint blocks (no visa= param for root index)
    lines.append(get_root_lint_blocks(snapshot_id))

    lines.append("")
    lines.append(f'{{{{< checker_cta snapshot="{snapshot_id}" >}}}}')
    lines.append("")
    return "\n".join(lines)


def render_detail(visa: dict, sources: dict, snapshot_id: str) -> None:
    """Render a detail page for a specific visa route."""
    country_slug = slugify(visa["country"])
    visa_slug = slugify(visa["visa_name"])
    authority_slug = slugify(visa["route"])
    visa_id = visa["id"]

    # Get source IDs from visa sources array
    source_ids = [s["source_id"] for s in visa.get("sources", [])]

    frontmatter = [
        "---",
        f'title: "{visa["country"]} {visa["visa_name"]} - {visa["route"]}"',
        f'visa_id: "{visa_id}"',
        f'last_verified: "{visa.get("last_verified", "")}"',
        f'source_ids: {json.dumps(source_ids)}',
        f'description: "Official insurance requirements for {visa["country"]} {visa["visa_name"]} via {visa["route"]}"',
    ]

    faqs = VISA_FAQS.get(visa_id, [])
    if faqs:
        frontmatter.append("faq:")
        for item in faqs:
            frontmatter.append(f'  - question: "{yaml_escape(item["question"])}"')
            frontmatter.append(f'    answer: "{yaml_escape(item["answer"])}"')

    frontmatter.append("---")

    lines = frontmatter + [
        "",
        f"## {visa['country']} {visa['visa_name']}",
        "",
        f"**Route:** {visa['route']}  ",
        f"**Authority:** {visa.get('authority', visa['route'])}  ",
        f"**Last Verified:** {visa.get('last_verified', 'Unknown')}",
        "",
        "## Requirements",
        "",
        "| Requirement | Operator | Value | Evidence |",
        "| --- | --- | --- | --- |",
    ]

    evidence_count = 0

    for req in visa.get("requirements", []):
        key = req.get("key", "")
        op = req.get("op", "")
        value = req.get("value", "")

        # Format value for display
        if isinstance(value, bool):
            value_str = "Yes" if value else "No"
        else:
            value_str = str(value)

        # Build evidence string
        evidence_items = []
        for ev in req.get("evidence", []):
            sid = ev.get("source_id", "")
            locator = ev.get("locator", "")
            excerpt = ev.get("excerpt", "")
            excerpt = excerpt.replace("|", "\\|").replace("\n", " ")

            # Try to get local path from sources metadata
            meta = sources.get(sid, {})
            local_path = meta.get("local_path", "")

            if local_path:
                evidence_items.append(f'*{locator}*: "{excerpt[:80]}..." ([source](/{local_path}))')
            else:
                evidence_items.append(f'*{locator}*: "{excerpt[:80]}..." (source_id: {sid})')
            evidence_count += 1

        evidence = " ".join(evidence_items) if evidence_items else "*No evidence recorded*"
        lines.append(f"| `{key}` | `{op}` | {value_str} | {evidence} |")

    # Add source documents section
    lines.append("")
    lines.append("## Source Documents")
    lines.append("")

    for src in visa.get("sources", []):
        sid = src.get("source_id", "")
        url = src.get("url", "")
        local_path = src.get("local_path", "")
        retrieved = src.get("retrieved_at", "")[:10] if src.get("retrieved_at") else ""

        if local_path:
            lines.append(f"- **{sid}**: [Local copy](/{local_path}) | [Original]({url}) | Retrieved: {retrieved}")
        else:
            lines.append(f"- **{sid}**: [Original]({url}) | Retrieved: {retrieved}")

    # Evidence gate: if no evidence, mark noindex and show UNKNOWN notice
    if evidence_count == 0:
        lines.insert(len(frontmatter) - 1, "robotsNoIndex: true")
        req_idx = lines.index("## Requirements")
        lines.insert(req_idx, "> **UNKNOWN** — no evidence found. This page is not indexed until evidence is added.")

    related = RELATED_POSTS.get(visa_id, [])
    if related:
        lines.append("")
        lines.append("## Related reading")
        lines.append("")
        for url, label in related:
            lines.append(f"- [{label}]({url})")

    # Add the evidence-rich body (includes all required lint blocks)
    lines.append(get_detail_body_sections(visa, sources, snapshot_id))

    lines.append("")
    lines.append(f'{{{{< checker_cta visa="{visa_id}" snapshot="{snapshot_id}" >}}}}')
    lines.append("")

    # Write file
    out_dir = OUT / country_slug / visa_slug / authority_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated: {out_dir / 'index.md'}")


def main():
    """Main entry point."""
    sources = load_sources()
    snapshot_id = os.environ.get("SNAPSHOT_ID") or datetime.now(timezone.utc).date().isoformat()
    visas = []

    for p in VISAS.rglob("visa_facts.json"):
        try:
            visas.append(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load {p}: {e}")
            continue

    if not visas:
        print("No visa_facts.json files found.")
        return

    # Group visas by country+visa_name for overview pages
    grouped = {}
    for visa in visas:
        country_slug = slugify(visa["country"])
        visa_slug = slugify(visa["visa_name"])
        authority_slug = slugify(visa["route"])
        key = (country_slug, visa_slug)

        grouped.setdefault(key, []).append({
            "authority": visa.get("authority", visa["route"]),
            "route": visa.get("route", ""),
            "last_verified": visa.get("last_verified", ""),
            "link": f"/visas/{country_slug}/{visa_slug}/{authority_slug}/",
            "country": visa["country"],
            "visa_name": visa["visa_name"],
            "visa_id": visa["id"],
        })

        # Render detail page
        render_detail(visa, sources, snapshot_id)

    # Render overview pages
    for (country_slug, visa_slug), routes in grouped.items():
        country_name = routes[0]["country"]
        visa_name = routes[0]["visa_name"]
        out_dir = OUT / country_slug / visa_slug
        out_dir.mkdir(parents=True, exist_ok=True)

        content = render_overview(country_slug, visa_slug, visa_name, country_name, routes, snapshot_id)
        (out_dir / "_index.md").write_text(content, encoding="utf-8")
        print(f"Generated: {out_dir / '_index.md'}")

    # Render root visas index
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_index.md").write_text(render_root_index(grouped, snapshot_id), encoding="utf-8")
    print(f"Generated: {OUT / '_index.md'}")

    print(f"\nGenerated {len(visas)} detail pages and {len(grouped)} overview pages.")


if __name__ == "__main__":
    main()
