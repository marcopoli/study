"""Reproducible analysis of the UniVox user study (N = 33).

Input : results.csv (userstudy/results/results.csv in the project repository)
Usage : python user_study_analysis.py path/to/results.csv
All statistics reported in the manuscript are printed by this script.
"""
import sys
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

SEED, B = 42, 20000
rng = np.random.default_rng(SEED)
df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "results.csv")
n = len(df)
Q = ["qual_completeness", "qual_clarity", "qual_utility", "qual_sources", "qual_trust"]
SUS_ITEMS = [f"sus_q{i}" for i in range(1, 11)]


def sus_score(d):
    rec = d[SUS_ITEMS].copy()
    for i in range(1, 11):
        c = f"sus_q{i}"
        rec[c] = rec[c] - 1 if i % 2 else 5 - rec[c]
    return rec.sum(axis=1) * 2.5, rec


def t_ci(x):
    x = np.asarray(x, float)
    h = stats.t.ppf(0.975, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x))
    return x.mean(), x.std(ddof=1), x.mean() - h, x.mean() + h


def cronbach(items):
    items = np.asarray(items, float)
    k = items.shape[1]
    return k / (k - 1) * (1 - items.var(axis=0, ddof=1).sum() / items.sum(axis=1).var(ddof=1))


def holm(p):
    p = np.asarray(p)
    order, adj, run = np.argsort(p), np.empty(len(p)), 0.0
    for rank, idx in enumerate(order):
        run = max(run, min(1.0, (len(p) - rank) * p[idx]))
        adj[idx] = run
    return adj


def boot_spearman(a, b):
    a, b, out = np.asarray(a), np.asarray(b), []
    for _ in range(B):
        i = rng.integers(0, len(a), len(a))
        r = stats.spearmanr(a[i], b[i]).statistic
        if not np.isnan(r):
            out.append(r)
    return np.percentile(out, [2.5, 97.5])


def nps(x):
    x = np.asarray(x)
    return 100 * ((x >= 9).mean() - (x <= 6).mean())


df["SUS"], rec = sus_score(df)

print(f"N = {n}")
age = df.age.dropna()
print(f"Age: n={len(age)}, M={age.mean():.1f}, SD={age.std(ddof=1):.1f}, range={age.min():.0f}-{age.max():.0f}")
print("Gender:", df.gender.value_counts().to_dict(), "| Enrolment:", df.enrollment.value_counts().to_dict())
print("Collection days:", sorted(df.timestamp.str[:10].unique()))

# Data quality: straight-lining across all 15 closed items
sl = df[SUS_ITEMS + Q].nunique(axis=1) == 1
print(f"Straight-lining respondents: {int(sl.sum())}")

# RQ1 usability
m, sd, lo, hi = t_ci(df.SUS)
print(f"\nSUS: M={m:.1f}, SD={sd:.1f}, 95% CI [{lo:.1f}, {hi:.1f}], Mdn={df.SUS.median():.1f}, "
      f"range {df.SUS.min():.1f}-{df.SUS.max():.1f}, alpha={cronbach(rec):.2f}")
t, p = stats.ttest_1samp(df.SUS, 68)
print(f"vs 68: t({n-1})={t:.2f}, p={p:.1e}, d={(m-68)/sd:.2f}; share>=68={(df.SUS>=68).mean():.2f}; "
      f"share>=84.1 (A+)={(df.SUS>=84.1).mean():.2f}")
m2, sd2, lo2, hi2 = t_ci(df.SUS[~sl])
print(f"SUS without straight-liner: M={m2:.1f}, SD={sd2:.1f}, 95% CI [{lo2:.1f}, {hi2:.1f}]")

# RQ2 perceived quality and trust
print("\nAnswer-quality items (1-5):")
for c in Q:
    mm, s, l, h = t_ci(df[c])
    print(f"  {c}: M={mm:.2f}, SD={s:.2f}, 95% CI [{l:.2f}, {h:.2f}], Mdn={df[c].median():.0f}, "
          f"top-2-box={(df[c]>=4).mean()*100:.0f}%")
print(f"  alpha (5 items)={cronbach(df[Q]):.2f}")
fr = stats.friedmanchisquare(*[df[c] for c in Q])
print(f"  Friedman chi2(4)={fr.statistic:.2f}, p={fr.pvalue:.1e}, Kendall W={fr.statistic/(n*4):.2f}")
res = []
for c in Q[:-1]:
    d = df.qual_trust - df[c]
    nz = d[d != 0]
    r = stats.rankdata(np.abs(nz))
    rrb = (r[nz > 0].sum() - r[nz < 0].sum()) / r.sum()
    w = stats.wilcoxon(df.qual_trust, df[c])
    res.append((c, w.statistic, w.pvalue, rrb, d.mean()))
for (c, V, pv, rrb, md), pa in zip(res, holm([r[2] for r in res])):
    print(f"  trust vs {c}: V={V:.1f}, p_Holm={pa:.4f}, r_rb={rrb:.2f}, mean diff={md:.2f}")
print("  Friedman without straight-liner: p=%.1e" % stats.friedmanchisquare(*[df.loc[~sl, c] for c in Q]).pvalue)

# RQ3 recommendation
x = df.nps_score
P, D = (x >= 9).mean(), (x <= 6).mean()
se = 100 * np.sqrt((P + D - (P - D) ** 2) / n)
print(f"\nLTR: M={x.mean():.2f}, SD={x.std(ddof=1):.2f}, Mdn={x.median():.0f}; promoters={int((x>=9).sum())}, "
      f"passives={int(((x>=7)&(x<=8)).sum())}, detractors={int((x<=6).sum())}; "
      f"NPS={nps(x):.1f}, 95% CI [{nps(x)-1.96*se:.1f}, {nps(x)+1.96*se:.1f}]; "
      f"NPS without straight-liner={nps(x[~sl]):.1f}")

family = [("SUS", "nps_score")] + [(c, "nps_score") for c in Q] + [("SUS", "qual_trust"), ("qual_sources", "qual_trust")]
rows = []
for a, b in family:
    r = stats.spearmanr(df[a], df[b])
    r2 = stats.spearmanr(df.loc[~sl, a], df.loc[~sl, b]).statistic
    rows.append((a, b, r.statistic, r.pvalue, boot_spearman(df[a], df[b]), r2))
print("\nSpearman correlations (Holm across 8 tests; bootstrap 95% CI; rho without straight-liner):")
for (a, b, r, p_, ci, r2), pa in zip(rows, holm([r[3] for r in rows])):
    print(f"  {a} ~ {b}: rho={r:.2f} [{ci[0]:.2f}, {ci[1]:.2f}], p={p_:.4f}, p_Holm={pa:.4f}, rho_sens={r2:.2f}")


def std_ols(d):
    z = d[["nps_score", "SUS", "qual_trust"]].apply(lambda s: (s - s.mean()) / s.std(ddof=1))
    return sm.OLS(z.nps_score, sm.add_constant(z[["SUS", "qual_trust"]])).fit(cov_type="HC3")


for label, d in [("full sample", df), ("without straight-liner", df[~sl])]:
    f = std_ols(d)
    ci = f.conf_int()
    print(f"\nOLS LTR ~ SUS + trust ({label}, standardised, HC3): R2={f.rsquared:.2f}")
    for v in ["SUS", "qual_trust"]:
        print(f"  beta_{v}={f.params[v]:.2f} [{ci.loc[v,0]:.2f}, {ci.loc[v,1]:.2f}], p={f.pvalues[v]:.3f}")

print("\nFull Spearman matrix:")
print(df[["SUS", "nps_score"] + Q].corr(method="spearman").round(2).to_string())

cm = df[df.comments.notna() & (df.comments.str.strip() != "")]
print(f"\nOpen comments: {len(cm)} of {n}")
print("Trust scores of commenters:", cm.qual_trust.tolist())

# Tool-use accuracy (Appendix B): exact Clopper-Pearson interval for 12/12
k, N = 12, 12
lo_cp = stats.beta.ppf(0.025, k, N - k + 1) if k > 0 else 0.0
print(f"\nTool-use accuracy {k}/{N}: 95% Clopper-Pearson CI [{lo_cp*100:.1f}%, 100%]")

# Exploratory mediation: source clarity -> trust -> likelihood to recommend
# (standardised OLS paths; percentile bootstrap CI of the indirect effect, 20,000 resamples)
def mediation(d, seed=SEED, reps=B):
    z = lambda v: (v - v.mean()) / v.std(ddof=1)
    X, M, Y = z(d.qual_sources).values, z(d.qual_trust).values, z(d.nps_score).values

    def paths(x, m, y):
        a = np.polyfit(x, m, 1)[0]
        coef = np.linalg.lstsq(np.column_stack([np.ones_like(x), x, m]), y, rcond=None)[0]
        c = np.polyfit(x, y, 1)[0]
        return a, coef[2], coef[1], c, a * coef[2]

    est = paths(X, M, Y)
    r = np.random.default_rng(seed)
    bs = []
    for _ in range(reps):
        i = r.integers(0, len(X), len(X))
        if np.std(X[i]) > 0 and np.std(M[i]) > 0:
            bs.append(paths(X[i], M[i], Y[i]))
    ci = np.percentile(np.array(bs), [2.5, 97.5], axis=0)
    return est, ci


for label, d in [("full sample", df), ("without straight-liner", df[~sl])]:
    (a, b, cp, c, ind), ci = mediation(d)
    print(f"\nMediation ({label}): a={a:.2f} [{ci[0,0]:.2f}, {ci[1,0]:.2f}], b={b:.2f} [{ci[0,1]:.2f}, {ci[1,1]:.2f}], "
          f"direct={cp:.2f} [{ci[0,2]:.2f}, {ci[1,2]:.2f}], total={c:.2f} [{ci[0,3]:.2f}, {ci[1,3]:.2f}], "
          f"indirect={ind:.2f} [{ci[0,4]:.2f}, {ci[1,4]:.2f}], proportion={ind / c:.2f}")


# Differences between dependent Spearman correlations (percentile bootstrap, 20,000 resamples)
def rho_difference(d, pair1, pair2, seed=SEED, reps=B):
    rs = lambda x, y: stats.spearmanr(x, y)[0]
    v = {c: d[c].values for c in set(pair1 + pair2)}
    est = rs(v[pair1[0]], v[pair1[1]]) - rs(v[pair2[0]], v[pair2[1]])
    r = np.random.default_rng(seed)
    bs = []
    for _ in range(reps):
        i = r.integers(0, len(d), len(d))
        diff = rs(v[pair1[0]][i], v[pair1[1]][i]) - rs(v[pair2[0]][i], v[pair2[1]][i])
        if not np.isnan(diff):
            bs.append(diff)
    return est, np.percentile(bs, [2.5, 97.5])


print("\nDifferences between dependent correlations (bootstrap 95% CI):")
for p1, p2 in [(("nps_score", "qual_trust"), ("nps_score", "SUS")),
               (("nps_score", "qual_trust"), ("nps_score", "qual_sources")),
               (("qual_trust", "qual_sources"), ("qual_trust", "SUS"))]:
    est, ci = rho_difference(df, p1, p2)
    print(f"  rho({p1[0]}, {p1[1]}) - rho({p2[0]}, {p2[1]}) = {est:.2f} [{ci[0]:.2f}, {ci[1]:.2f}]")
print("Share of maximum ratings:", {c: round((df[c] == 5).mean(), 2) for c in Q})
