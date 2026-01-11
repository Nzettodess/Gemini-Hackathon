---
name: fact-checker
description: AI tool that analyzes language and context to identify potential misinformation and fact-check claims made by public figures
---

# Public Figure Fact Checker

Identify potential misinformation and fact-check claims made by public figures with structured true/false output and correction recommendations.

## When to use

Trigger when users request:
- "Fact-check this document"
- "Verify these specifications"
- "Check if this information is still accurate"
- "Update outdated data in this claim"
- "Validate the claims in this section"

## Workflow

Copy this checklist to track progress:

```
Public Figure Fact-Check Progress:
- [ ] Step 1: Extract verifiable claims
- [ ] Step 2: Search Google Fact Check Tools (MANDATORY)
- [ ] Step 3: Search additional authoritative sources
- [ ] Step 4: Generate structured fact-check report
```

### Step 1: Extract verifiable claims

Identify specific factual statements made by the public figure:

**Target claim types:**
- Statistical data and numbers
- Historical events and dates
- Scientific or medical statements
- Financial figures and company data
- Policy positions and voting records
- Biographical information

**Extract format:**
```
CLAIM: [Exact quote from public figure]
CONTEXT: [When/where it was said]
TYPE: [Statistical/Historical/Scientific/etc.]
```

### Step 2: Search Google Fact Check Tools (MANDATORY)

**REQUIRED: Always start with Google Fact Check Tools before other sources**

1. **Google Fact Check Explorer**: Search for the exact claim or similar statements
2. **Review existing fact-checks**: Check if the claim has been previously verified
3. **Analyze ClaimReview data**: Look for structured fact-check results
4. **Cross-reference sources**: Note which fact-checkers have covered this topic

**If Google Fact Check Tools shows existing fact-checks:**
- Review the verdict and methodology
- Check if the context matches current claim
- Verify the credibility of the fact-checking organization
- Use as primary reference point for your analysis

**If no existing fact-checks found:**
- Proceed to Step 3 for original verification
- Note in report that this is a new claim requiring fresh fact-checking

### Step 3: Search additional authoritative sources

For each claim, search official and credible sources:

**Government data:**
- Official statistics (census.gov, bls.gov, cdc.gov)
- Government databases and reports
- Congressional voting records
- Court documents and legal filings

**Academic and research:**
- Peer-reviewed studies
- University research institutions
- Scientific journals and publications
- Medical organizations (WHO, CDC, FDA)

**Financial and business:**
- SEC filings and annual reports
- Financial news from established outlets
- Company press releases
- Stock market data

**Historical verification:**
- Historical archives and records
- Newspaper archives
- Documentary evidence
- Timeline verification from multiple sources

### Step 4: Generate structured fact-check report

Output format for each claim:

```markdown
## FACT-CHECK RESULT

### CLAIM #[N]
**Statement:** "[Exact quote]"
**Source:** [Public figure name] on [date/platform]
**Category:** [Statistical/Historical/Scientific/Financial/Policy]

**VERDICT:** ✅ TRUE / ❌ FALSE / ⚠️ MISLEADING / ❓ UNVERIFIABLE

**VERIFICATION:**
- **Google Fact Check Result:** [Run: python scripts/google_fact_checker.py "claim text"]
- **Primary Source:** [Authoritative source URL]
- **Supporting Sources:** [Additional verification sources]
- **Date Checked:** [Current date]

**ANALYSIS:**
[Brief explanation of why the claim is true/false/misleading]

**CORRECTION (if applicable):**
**Accurate Statement:** "[Corrected version of the claim]"
**Key Difference:** [What was wrong/misleading about original]
```

## Source Evaluation Guidelines

### Authoritative Sources (High Priority)
1. **Google Fact Check Tools** - MANDATORY first step for all claims
2. **Government agencies** - Official statistics, records, databases
3. **Academic institutions** - Peer-reviewed research, university studies
4. **Medical organizations** - WHO, CDC, FDA, medical journals
5. **Financial regulators** - SEC filings, central bank data
6. **News organizations** - Established outlets with fact-checking standards
7. **Other fact-checking platforms** - Snopes, PolitiFact, FactCheck.org (as secondary verification)

### Use with Caution
- Corporate press releases (may contain bias)
- Think tank reports (check funding sources)
- Social media posts (even from experts)
- Single-source claims

### Red Flags
- No authoritative source available
- Google Fact Check Tools returns contradictory results
- Sources contradict each other significantly
- Only partisan sources support the claim
- Information is very recent with limited verification

**CRITICAL RULE: Never complete a fact-check without consulting Google Fact Check Tools first**

## Utility Scripts

To automate Google Fact Checker API requests, use the simplified script:

### Simple Google Fact Check Query
```bash
python scripts/google_fact_checker.py "Senator X said unemployment dropped 40% during his term"
```

**Returns raw string format:**
- Multiple lines for top 5 results: `#N: InformationContent`
- `NO_RESULTS` - if no existing fact-checks  
- `ERROR: message` - if API error occurred

**Example outputs:**
```
#1: Donald Trump was born in the United States | Birth certificate confirms he was born in New York City | Original claim: Trump was born in USA
#2: Official records verify Trump's birthplace as New York | Original claim: Donald Trump birthplace question
#3: Birth certificate authentic and valid | Multiple sources confirm NYC birth
NO_RESULTS
ERROR: API key not found
```

## Examples

### Example 1: Political Statistical Claim

**User request:** "Fact-check: 'Senator X said unemployment dropped 40% during his term'"

**Output:**
```markdown
## FACT-CHECK RESULT

### CLAIM #1
**Statement:** "Unemployment dropped 40% during my term in office"
**Source:** Senator X on Twitter, January 8, 2026
**Category:** Statistical

**VERDICT:** ⚠️ MISLEADING

**VERIFICATION:**
- **Google Fact Check Result:** #1: Unemployment claim misleading - shows 2.1 percentage point decrease, not 40% absolute drop | Original claim: Unemployment dropped 40% during term
#2: Economic statistics misrepresented in political statement | Original claim: Similar unemployment claim
- **Primary Source:** Bureau of Labor Statistics unemployment data
- **Supporting Sources:** Federal Reserve economic data, state employment records
- **Date Checked:** January 11, 2026

**ANALYSIS:**
Unemployment did decrease during the senator's term, but only by 2.1 percentage points (from 5.3% to 3.2%), which represents a 40% relative decrease but not an absolute 40% drop.

**CORRECTION:**
**Accurate Statement:** "Unemployment decreased by 2.1 percentage points (a 40% relative reduction) during my term"
**Key Difference:** Original statement implies much larger absolute decrease than actually occurred
```

### Example 2: CEO Business Claim

**User request:** "Verify: 'Our company's revenue grew 500% last year'"

**Output:**
```markdown
## FACT-CHECK RESULT

### CLAIM #1
**Statement:** "Our company's revenue grew 500% last year"
**Source:** CEO Jane Doe at investor conference, January 2026
**Category:** Financial

**VERDICT:** ✅ TRUE

**VERIFICATION:**
- **Google Fact Check Result:** NO_RESULTS
- **Primary Source:** Company's SEC 10-K filing
- **Supporting Sources:** Annual report, audited financial statements
- **Date Checked:** January 11, 2026

**ANALYSIS:**
SEC filings confirm revenue increased from $2M in 2024 to $12M in 2025, representing exactly a 500% increase.

**CORRECTION:** None needed - claim is accurate.
```

## Quality checklist

Before completing fact-check:

- [ ] All factual claims extracted with exact quotes
- [ ] Google Fact Check Tools consulted FIRST (MANDATORY)
- [ ] Each claim verified against authoritative sources
- [ ] Verdict clearly stated (TRUE/FALSE/MISLEADING/UNVERIFIABLE)
- [ ] Sources are credible and current
- [ ] Analysis explains the reasoning
- [ ] Corrections provided for false/misleading claims
- [ ] Temporal context included where relevant

## Limitations

**This skill cannot:**
- Verify future predictions or speculation
- Determine subjective truth in opinion-based statements
- Access private or confidential information
- Resolve disputes where authoritative sources disagree
- **Complete fact-checks without using Google Fact Check Tools**

**For such cases:**
- Mark as ❓ UNVERIFIABLE
- Note the limitation in analysis
- Suggest seeking additional expert consultation
- **Always include Google Fact Check Tools results even if no matches found**
