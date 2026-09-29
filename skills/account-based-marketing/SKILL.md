---
name: account-based-marketing
description: "Account-Based Marketing (ABM) for B2B. Tiered account selection (1:1, 1:few, 1:many), ICP and account scoring, multi-channel orchestration (LinkedIn, email, ads, direct mail), buying committee mapping, personalized content production, sales/marketing alignment, and ABM measurement. Use when targeting a defined list of high-value accounts, building tiered account programs, mapping buying committees, orchestrating multi-touch campaigns on named accounts, or measuring ABM impact vs broad demand gen."
---

# Account-Based Marketing (ABM)

## When ABM beats demand gen
- High ACV (typically > €10k–20k/year)
- Long sales cycles, multiple decision-makers
- Finite, identifiable target market (e.g., "200 BTP companies in France with 50+ employees")
- Strong product–segment fit but generic demand gen is too noisy

## Three ABM tiers

| Tier | Accounts | Personalization | Investment / account |
|---|---|---|---|
| **1:1 Strategic** | 5–25 | Custom content per account, exec-level outreach | High |
| **1:few Cluster** | 25–100 | Personalized by industry/persona cluster | Medium |
| **1:many Programmatic** | 100–1000 | Light personalization (firmographic, intent data) | Low |

Most B2B SMEs start at 1:few then graduate to 1:1 for top accounts.

## Account selection framework

1. **ICP definition** — firmographic (industry, size, geo, tech stack), behavioral (intent signals, recent funding, hiring), pain triggers (regulation change, expansion, M&A).
2. **Tier scoring** — fit (0–10) × intent (0–10) × revenue potential (€). Tier A = top 10–25%, B = next 25%, C = rest.
3. **Buying committee mapping** — for each account, identify Champion, Economic Buyer, User, Blocker. Use LinkedIn Sales Navigator, ZoomInfo, Apollo, or Lusha.

## Orchestration playbook (1:few example, 30-day sequence)

| Day | Touch | Channel | Persona |
|---|---|---|---|
| 1 | LinkedIn connect + soft note | LinkedIn | Champion |
| 3 | Personalized intro email | Email | Champion |
| 7 | Industry case study sent | Email | Champion |
| 10 | Targeted ad campaign live | LinkedIn / Meta retargeting | All committee |
| 14 | Direct mail or value gift (optional, Tier A only) | Postal | Economic Buyer |
| 18 | LinkedIn voice note or video | LinkedIn | Champion |
| 25 | Bump email with clear CTA | Email | Champion |
| 30 | Break-up email + handoff to sales | Email | Champion |

## Account list sources
- LinkedIn Sales Navigator (Boolean filters by industry + size + geo)
- Apollo / Lusha / Cognism — contact enrichment
- 6sense / Bombora / Demandbase — intent data
- Public registries (Pappers, Infogreffe in France) — firmographic
- Industry associations / federations — vertical lists

## Personalization layers (cheap → expensive)
1. Firmographic ("Hi {firstname} at {company}, in {industry}…")
2. Trigger event ("Saw you just opened a new site in Lyon")
3. Persona pain ("HSE managers in BTP often struggle with…")
4. Account-specific insight ("Your last accident report on {publication} mentioned…")
5. Custom content (microsite or video specifically for that account — 1:1 only)

## Metrics

| Stage | Metric |
|---|---|
| Reach | Account coverage %, contacts per account engaged |
| Engagement | Account engagement score (web visits + email opens + ad clicks weighted) |
| Pipeline | Accounts → meetings, meetings → opportunities, opportunity value |
| Revenue | Win rate per tier, ACV per tier, sales cycle length, ABM-influenced revenue |

Compare ABM cohort vs non-ABM control: pipeline velocity, ACV, win rate.

## Common mistakes
- Treating ABM as "spam with the company name" — personalization must be substantive
- No sales/marketing alignment on account list — sales ignores leads
- Measuring ABM with MQL volume instead of pipeline/revenue per account
- Spreading 1:1 effort across too many accounts (dilution)
- No exit criteria — accounts that don't engage in 90 days should drop to 1:many

## ABM tooling stack (typical)

- **List + intent**: Sales Navigator, Apollo, 6sense, Bombora
- **Outreach**: Lemlist, Outreach, Salesloft, La Growth Machine
- **Ads**: LinkedIn Matched Audiences, Meta custom audiences, Demandbase
- **CRM**: HubSpot or Salesforce with account hierarchy + engagement scoring
- **Content**: Personalized landing pages (Mutiny, RightMessage, or custom Next.js)
