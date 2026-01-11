I built Clinical Note AI as a hybrid extraction engine because clinical notes range from structured "72yo COPD SpO2 88%" to messy narratives like "gardening then elbow pain after ladder fall." I went LLM-first (Mistral via OpenRouter) for universal understanding - it handles any clinical context without predefined patterns. Then overlaid rule-based precision for medications (25+ common drugs) and vitals (BP/HR/RR/SpO2) because regex never hallucinates drugs and runs in <1ms vs LLM's 500ms.

Trade-offs were deliberate: Single API key dependency (OpenRouter) keeps it simple but creates a failure point - I added graceful fallbacks so rule-based extraction works standalone. Confidence scoring (0.0-1.0) reflects data completeness transparently: COPD cases hit 0.95, partial notes get 0.67 realistically. Multi-file structure (app/, deployment/, frontend/)

![Uploading Untitled diagram-2026-01-11-195944.png…]()

