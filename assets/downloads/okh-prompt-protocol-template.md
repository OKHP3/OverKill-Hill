# OKH Prompt Protocol Template
### OverKill Hill P³™ — overkillhill.com/prompt-forge/

A governed prompt is not a paragraph. It is a structured operating brief.
Copy this template. Fill every field. Leave nothing as "you'll know it when you see it."

---

**Template version:** v1.0  
**Source:** overkillhill.com/prompt-forge/#anatomy  
**License:** Free to use, adapt, and share. Credit appreciated, not required.

---

## THE TEN ANATOMY ELEMENTS

---

### 1. ROLE

> Who or what is this model being asked to become for this task?

```
Role:
[Describe the persona, expertise, perspective, or operating mode the model
should adopt. Be specific. "Act as an expert" is not a role. "Act as a senior
infrastructure engineer who has migrated three enterprise SaaS platforms to
Kubernetes and has strong opinions about blast radius" is a role.]
```

---

### 2. CONTEXT

> What domain, prior state, constraints, and vocabulary must the model know?

```
Context:
[Provide the operating environment: the project, the problem history, the
vocabulary in use, the constraints that already exist, and any prior decisions
that are locked. The model cannot reason well without this foundation.]
```

---

### 3. OBJECTIVE

> What is the actual job — not the surface question, the real outcome?

```
Objective:
[State the real deliverable. Not what you're going to ask, but what you need
to exist after the prompt runs. "Help me think through X" is not an objective.
"Produce a three-option architecture decision record with tradeoffs scored
against our four criteria" is an objective.]
```

---

### 4. INPUTS

> What documents, files, data, or tool access is the model drawing from?

```
Inputs:
[List everything the model should reference, read, or have access to:
- Attached documents
- Pasted content
- Tool outputs (web search, code interpreter, etc.)
- Prior conversation context
- External sources it should or should not consult]
```

---

### 5. CONSTRAINTS

> What must not happen? What is out of scope? What must not be invented?

```
Constraints:
[Explicit out-of-bounds. This is where you prevent hallucination, scope creep,
and unwanted behavior. Examples:
- Do not invent statistics or citations
- Do not recommend tools not already in our stack
- Do not reframe the objective
- Do not include legal or medical advice
- Stay within the context provided; do not assume prior knowledge]
```

---

### 6. METHOD

> How should the model reason? Step-by-step? Adversarial critique? Synthesis?

```
Method:
[Define the reasoning approach:
- Step-by-step decomposition
- Devil's advocate / adversarial critique
- Comparative analysis across N options
- Synthesis from multiple sources
- Structured outline first, then expand
- Socratic questioning before answering
If no method is specified, the model picks one. Specify one.]
```

---

### 7. OUTPUT FORMAT

> What does the result look like? Fields, tables, headings, file names, artifacts?

```
Output Format:
[Describe the exact shape of the output:
- Markdown headers, tables, code blocks
- Specific field names and data types
- File naming convention if producing artifacts
- Length targets (e.g., "no more than 600 words", "one page maximum")
- What to omit (no preamble, no summary header, no "as an AI" disclaimers)]
```

---

### 8. VALIDATION

> How do we verify this solved the actual problem? What are the acceptance criteria?

```
Validation:
[State the acceptance criteria before execution, not after:
- What does a correct answer look like?
- What would make you reject the output and ask again?
- If the model is unsure about a field, should it flag it or fill it?
- What edge case must the output handle?]
```

---

### 9. FAILURE HANDLING

> What should the model do if information is missing, unsafe, or out of scope?

```
Failure Handling:
[Define graceful degradation:
- If context is insufficient: ask one clarifying question or state the gap explicitly
- If the request is out of scope: say so, do not invent a workaround
- If the output would require unavailable information: return what is known
  and flag what is missing
- Do not fabricate. Surface uncertainty explicitly.]
```

---

### 10. HANDOFF

> Where does the output go? Notion? Replit? GitHub? Another agent?

```
Handoff:
[Define what happens after this prompt runs:
- Is the output a human deliverable or agent input?
- Will another model use this output as its context?
- Does it feed into a Replit execution spec?
- Is it being written to Notion, GitHub, or a document?
Knowing the handoff forces the output format to match the destination.]
```

---

## FILLED EXAMPLE (abbreviated)

```
Role:
A technical writer who has documented five B2B SaaS products and understands
the difference between feature documentation and user guidance.

Context:
We are documenting a Replit-hosted internal tool for a 12-person ops team.
The tool has no public documentation. Current "docs" are a Slack message from
March 2023. The audience is non-technical operations staff.

Objective:
Produce a three-section quick-start guide: What it does (one paragraph),
How to access it (numbered steps), and How to get help (one paragraph).
The guide should be usable without me in the room.

Inputs:
- Tool name and URL: [provided inline]
- Existing Slack message: [pasted below]
- Screenshot of the main UI: [attached]

Constraints:
Do not use technical jargon. Do not reference Replit or code. Do not assume
the reader has ever used the tool before.

Method:
Outline first. Wait for approval before expanding.

Output Format:
Markdown. H2 headers for each of the three sections. No introduction paragraph.
No footer or credits.

Validation:
A non-technical ops employee should be able to follow the guide with no
additional explanation from me.

Failure Handling:
If the screenshot is insufficient to describe a step, note the gap with
[NEEDS SCREENSHOT: description] rather than guessing.

Handoff:
Output goes into Notion. Format for pasting directly into a Notion page.
```

---

## USAGE NOTES

**Start with Objective.** If you can't clearly state what you need to exist
after the prompt runs, you're not ready to write the prompt.

**Constraints are not optional.** Every constraint you omit is a decision
you're handing to the model. The model will make that decision. You may not
like what it decides.

**Handoff forces precision.** If the output is feeding another AI agent,
write for that agent's input requirements, not for human readability.

**Iterate with the skeleton, not around it.** If a prompt isn't working, find
which of the ten elements is missing or underspecified. Don't rewrite from
scratch — diagnose and fix.

---

## ABOUT PROMPT FORGE

The Prompt Forge is OverKill Hill P³™'s protocol-driven promptcraft workshop.
Prompts become governed AI systems, audit contracts, and Replit-ready specs.

**Site:** overkillhill.com/prompt-forge/  
**Methodology archive:** github.com/OKHP3/first-diagram-is-a-liar  
**Contact:** overkillhill.com/contact/

---

*OverKill Hill P³™ — Protocol. Process. Practice.*
