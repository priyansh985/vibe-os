# Adaptive mode selection

Assess four independent dimensions before significant changes: **impact/risk**, **scope**, **uncertainty**, and **reversibility**. These are engineering judgments, not a statistical risk model.

| Dimension | Low / small / easy | Medium | High / large / hard |
|---|---|---|---|
| Risk | non-sensitive local change | moderate regression concerns | auth/security/financial/privacy impact, production availability |
| Scope | localized one-concern change | multiple connected modules | architectural or cross-service change |
| Uncertainty | clear behavior and known patterns | some unknowns | core requirements/constraints unresolved |
| Reversibility | quick rollback | manageable rollback | migration, data loss, external irreversible change |

- **DEEP** if any dimension is in the right-most category. Sensitive production changes and hard-to-reverse actions need explicit controls and approvals.
- **QUICK** only if all four dimensions are in the left-most category.
- **STANDARD** otherwise, including tasks with missing risk information until clarified.

QUICK: avoid formal planning artifacts except where project policy requires them. STANDARD: write measurable acceptance criteria and a short plan. DEEP: compare options, document safety and rollback, seek approval for irreversible or high-impact operations.

Re-assess when new facts emerge. CLI `assess` implements the deterministic conservative rule above using explicit flags; it does not infer risk from natural-language task descriptions.
