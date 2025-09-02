# Edit Plan Example (Dry-Run Template)

This is the exact process Cursor and contributors should follow before making any changes to ToneGPT.

## 📋 **Edit Plan Template**

**Goal:** <What needs to change - be specific>

**Authoritative excerpts (3–5)**
1) `docs/ground-truth.md#<heading>` — "<1-line quote from ground truth>"
2) `docs/fm9-mapping-tldr.md#<heading>` — "<1-line quote from mapping rules>"
3) `docs/ground-truth.md#<heading>` — "<1-line quote from safety/constraints>"
4) `docs/ground-truth.md#<heading>` — "<1-line quote from acceptance criteria>"
5) `docs/ground-truth.md#<heading>` — "<1-line quote from future-proofing>"

**Acceptance criteria**
- [ ] FM9 single-mode; no dual_mode in core
- [ ] Params only from config/reference (no inventions)
- [ ] Typed + docstrings include **Constraints**
- [ ] Tests updated/added and passing
- [ ] No network calls in core
- [ ] Feature flags respected (`FEATURE_MULTI_DEVICE` if relevant)

**Deliverables**
- Minimal diff + tests
- Bullets mapping edits → excerpts above

---

## 🎯 **Example: Adding New Mesa Boogie Mark V Amp**

**Goal:** Add Mesa Boogie Mark V amp model with proper FM9 parameter mapping

**Authoritative excerpts (3–5)**
1) `docs/ground-truth.md#Invariants` — "All block/cab defaults & ranges come from: 1) data/fm9_config.json 2) data/fm9_comprehensive_reference.json"
2) `docs/fm9-mapping-tldr.md#Parameter Rules` — "NEVER invent parameters - if missing, raise ValueError with exact file+key"
3) `docs/ground-truth.md#Acceptance Criteria` — "Any param change cites the doc + heading that authorizes it"
4) `docs/ground-truth.md#Safety Constraints` — "Data sources are read-only. Parameter validation against official specs"
5) `docs/ground-truth.md#Future-proofing` — "Multi-device MAY be added later behind `FEATURE_MULTI_DEVICE` (adapters only)"

**Acceptance criteria**
- [x] FM9 single-mode; no dual_mode in core
- [x] Params only from config/reference (no inventions)
- [x] Typed + docstrings include **Constraints**
- [x] Tests updated/added and passing
- [x] No network calls in core
- [x] Feature flags respected (`FEATURE_MULTI_DEVICE` if relevant)

**Deliverables**
- Add Mark V to data/fm9_config.json AMP section
- Update gear mapping in clean_ai_tone_generator.py
- Add test case for Mark V selection
- Update documentation

---

## ✅ **Summary**
What changed and why (FM9 single-mode context).

## Authoritative Excerpts (3–5)
1. file#heading — <quote>
2. file#heading — <quote>
3. file#heading — <quote>

## Acceptance Criteria
- [ ] FM9 single-mode; no dual_mode in core
- [ ] Params only from config/reference (no inventions)
- [ ] Typed + docstrings include **Constraints**
- [ ] Tests updated/added and passing
- [ ] No network calls in core
- [ ] Feature flags respected (`FEATURE_MULTI_DEVICE` if relevant)

## Validation
- [ ] `pytest` green
- [ ] Manual sanity check notes (1–2 bullets)

## Mapping (Edits → Excerpts)
- Edit A → Excerpt #1 …
- Edit B → Excerpt #2 …

---

## 🚀 **Usage Instructions**

1. **Copy this template** for any new changes
2. **Fill in the Goal** - be specific about what needs to change
3. **Find 3-5 relevant excerpts** from the docs
4. **Check acceptance criteria** before coding
5. **Map each edit** to the excerpts after completion
6. **Validate** with tests and manual checks

This ensures all changes follow the FM9 single-mode architecture and maintain system integrity.
