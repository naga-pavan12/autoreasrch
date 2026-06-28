# Task
You are analyzing competitor research inputs for a Product Manager doing problem discovery.

Your goal is to identify real user problems and weakly solved market pains from the provided input.

Do not produce feature comparisons only.
Focus on the underlying user or operational problem.

## Instructions
Read the input carefully and extract up to 5 distinct problems.

For each problem:
- state the problem clearly and specifically
- identify the likely affected user type
- include 1 to 3 exact evidence quotes from the source text
- label whether the problem appears to be a symptom, root cause, or unclear
- estimate severity as low, medium, or high
- estimate frequency as low, medium, or high
- explain why this may matter strategically for our company
- avoid unsupported claims
- do not invent evidence
- avoid generic statements like "users want better UX"

## Strategic Context
Use the company context files to judge whether the discovered problem aligns with:
- faster resolution
- lower manual work
- easier setup
- more trustworthy AI-assisted workflows
- mid-market support team needs

## Output Rules
Return valid JSON only.
Follow the provided schema exactly.

## Input
{{input_text}}