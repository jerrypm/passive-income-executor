## 8 — Data Analysis, Research & Finance
### 100 Expert Prompts Inside

> EDA · SQL queries · Pandas · hypothesis testing · A/B test design · cohort analysis · LTV/CAC · DCF models · 3-statement models · personal finance · portfolio strategy

---


### 1. Rigorous EDA Playbook
**Prompt**: Act as a senior data scientist with a PhD in statistics who has led analytics at a Fortune 100 company. Perform a full exploratory data analysis on [DATASET] focused on [TARGET_VARIABLE]. Profile distributions, missingness, cardinality, outliers (IQR + z-score), multicollinearity (VIF), and class imbalance. Flag leakage risks and suggest feature engineering. Output a structured markdown EDA report with summary tables, ranked data quality issues, and a prioritized cleaning checklist with Pandas snippets.

### 2. Missing Data Strategy
**Prompt**: Act as a staff-level data scientist specializing in statistical inference. For [DATASET] with [MISSING_COLUMNS], diagnose whether data is MCAR, MAR, or MNAR using Little's test and visual patterns. Recommend an imputation strategy (mean/median, KNN, MICE, or model-based) with trade-offs. Justify choice against downstream model [MODEL_TYPE]. Output a decision matrix table, Python implementation using scikit-learn and fancyimpute, and a validation plan comparing pre/post distributions.

### 3. Outlier Detection Framework
**Prompt**: Act as a principal data scientist at a fraud analytics team. Design a multi-method outlier detection pipeline for [DATASET] covering univariate (z-score, IQR, MAD), multivariate (Mahalanobis, Isolation Forest, LOF), and time-series (STL residuals) techniques. Explain when each fails. Output Python code, a comparison of flagged records, false-positive risk analysis, and a business-rule layer to prevent auto-removal of legitimate extremes.

### 4. Data Quality Scorecard
**Prompt**: Act as a data governance lead building a quality scorecard for [DATASET]. Define metrics across completeness, uniqueness, validity, consistency, timeliness, and accuracy dimensions with weighted scoring. Implement automated checks using Great Expectations or Soda. Output the scorecard schema as YAML, SQL validation queries, a sample HTML report, and a remediation playbook tied to each failing dimension.

### 5. Feature Engineering Deep Dive
**Prompt**: Act as a Kaggle Grandmaster mentoring a team on feature engineering for [DATASET] predicting [TARGET]. Propose 20+ features across aggregation, interaction, target encoding, lag/window, frequency, and domain-specific transforms. Explain leakage risks and cross-validation strategy (group/time-based). Output a feature catalog table with name, definition, Pandas code, expected signal, and a ranked hypothesis for feature importance.

### 6. EDA on Time Series
**Prompt**: Act as a forecasting expert who built demand models at Amazon. Conduct EDA on time series [DATASET] for [METRIC] at [GRANULARITY]. Decompose using STL, test stationarity (ADF, KPSS), assess seasonality (FFT, ACF/PACF), detect changepoints (PELT), and identify holidays/anomalies. Output a Jupyter-ready Python analysis with plots, a markdown report on series characteristics, and recommended forecasting model family (ARIMA, Prophet, LightGBM, DeepAR).

### 7. Categorical Encoding Audit
**Prompt**: Act as an ML engineer auditing feature encoding choices for [DATASET]. For each categorical column, recommend encoding (one-hot, ordinal, target, frequency, hashing, James-Stein) based on cardinality, rarity, and relationship to [TARGET]. Quantify risk of target leakage and high-cardinality explosion. Output a decision table, scikit-learn column transformer code, and cross-validation scheme to measure lift per encoding choice.

### 8. Data Profiling Automation
**Prompt**: Act as a senior analytics engineer building a reusable data profiling script. For any CSV/Parquet [DATASET], output column-level stats (dtype, nulls, unique, skew, kurtosis, top categories), correlation matrix, mutual information with [TARGET], and sample records. Use ydata-profiling and polars for speed. Output the full Python script, CLI interface, and an executive summary template rendered via Jinja2.

### 9. EDA Narrative Report
**Prompt**: Act as a data storytelling coach. Convert raw EDA findings on [DATASET] into a 1-page executive narrative for a C-suite audience. Frame findings as three takeaways, three risks, and three recommendations. Back every claim with a statistic and uncertainty bound. Output the narrative in markdown with a Pyramid Principle structure, one headline chart recommendation, and a glossary for non-technical readers.

### 10. Data Cleaning Runbook
**Prompt**: Act as a data reliability engineer. Produce a reproducible data cleaning runbook for [DATASET] that handles duplicates, type coercion, whitespace, encoding, unit normalization, and referential integrity. Emphasize idempotency and logging. Output a Python module using pandas and pydantic with unit tests, an input/output schema contract, and a before/after row-count reconciliation report.

### 11. SQL Query Optimization
**Prompt**: Act as a principal database engineer with 15 years of PostgreSQL and BigQuery experience. Optimize the following query [SQL_QUERY] running against [TABLE] with [ROWCOUNT] rows. Analyze the execution plan, identify full scans, missing indexes, spill-to-disk, and suboptimal joins. Rewrite using CTEs, window functions, and partition pruning. Output the optimized SQL, EXPLAIN ANALYZE comparison, index DDL, and expected cost reduction in percentage.

### 12. Window Function Masterclass
**Prompt**: Act as a senior analytics engineer at a unicorn startup. Write advanced SQL using window functions to compute running total, 7-day moving average, rank within partition, first/last value, and percent of parent for [METRIC] on [TABLE] grouped by [SEGMENT]. Handle ties and sparse dates via generate_series. Output a single annotated query, expected output schema, and 3 gotchas around frame clauses that juniors miss.

### 13. Slowly Changing Dimensions
**Prompt**: Act as a dimensional modeling expert trained in Kimball methodology. Design a Type 2 SCD for [DIMENSION_TABLE] tracking [ATTRIBUTES] over time. Define surrogate keys, effective_from/to, is_current flag, and hash diff detection. Output the DDL, a MERGE statement for upserts, a validation query for overlapping intervals, and a downstream fact-join example preserving historical truth.

### 14. Funnel Analysis SQL
**Prompt**: Act as a product analytics lead at a SaaS company. Write SQL to compute a conversion funnel for [PRODUCT_FLOW] with steps [STEP_LIST] over [TIME_WINDOW], segmented by [SEGMENT]. Handle step ordering, time-to-convert, and drop-off rates. Output the query using window functions, a summary table schema, and a secondary query computing statistical significance of drop-off differences between segments using two-proportion z-test.

### 15. Cohort Retention Query
**Prompt**: Act as a growth analytics specialist. Write a SQL query that builds a weekly cohort retention matrix for [USER_TABLE] with signup_date and activity_date columns over [N_WEEKS]. Include cohort size, retained users, and retention percent. Output the query (BigQuery and Postgres variants), the pivoted heatmap shape, and a Python snippet using seaborn to visualize the triangle.

### 16. SQL Anti-Patterns Audit
**Prompt**: Act as a database performance consultant. Review [SQL_QUERY] for anti-patterns: SELECT *, implicit casts, functions on indexed columns, correlated subqueries, OR in join predicates, NOT IN with nullable columns, and missing statistics. Output a ranked findings table, the refactored query, and a preventive linting rule set for SQLFluff that blocks these in CI.

### 17. Dbt Model Design
**Prompt**: Act as an analytics engineering lead implementing dbt at a Series C startup. Design a staging-to-mart model for [DOMAIN] following Kimball conventions. Define sources, staging (stg_), intermediate (int_), and marts (fct_/dim_) layers. Output the dbt project folder structure, sample SQL model with Jinja macros, schema.yml with tests (unique, not_null, relationships, accepted_values), and a dbt docs block explaining grain.

### 18. Incremental Materialization
**Prompt**: Act as a data platform engineer optimizing [FACT_TABLE] with billions of rows. Design an incremental dbt model using merge strategy, partition pruning on [DATE_COLUMN], and late-arriving data handling with a lookback window. Output the dbt SQL with incremental config, unit test fixtures, a backfill procedure, and metrics on expected cost savings vs full refresh per run.

### 19. SQL to Pandas Translation
**Prompt**: Act as a data engineer fluent in both SQL and Python. Translate [SQL_QUERY] into idiomatic Pandas using groupby, agg, merge, pivot, and assign. Preserve exact semantics including NULL handling. Output a side-by-side comparison table (SQL clause to Pandas method), the executable Python code using type hints, and a note on when Pandas is faster vs Polars or DuckDB for the same task.

### 20. Data Warehouse Schema Review
**Prompt**: Act as a senior data architect. Review the schema for [WAREHOUSE] including fact and dimension tables. Assess grain consistency, conformed dimensions, junk dimensions for flags, degenerate dimensions, and snowflaking risks. Output a schema health scorecard, an ER diagram description, 5 prioritized refactors with DDL, and a BI-tool impact assessment for each change.

### 21. Pandas Performance Tuning
**Prompt**: Act as a Pandas core contributor. Optimize [PANDAS_SCRIPT] processing a [SIZE]-row DataFrame. Diagnose bottlenecks using memory_usage, dtype downcasting, chunking, vectorization over apply, categorical dtypes, and eval/query. Compare against Polars and DuckDB alternatives. Output a profiled before/after with timings, the refactored script, and a decision tree for when to migrate off Pandas.

### 22. Plotly Dashboard Spec
**Prompt**: Act as a senior data visualization engineer who built dashboards at Airbnb. Design a Plotly Dash dashboard for [BUSINESS_QUESTION] using [DATASET]. Specify KPIs, filters, cross-filtering, drill-downs, and color encoding following Cole Knaflic principles. Output a layout wireframe in markdown, the Dash app.py skeleton, chart recommendations per KPI, and accessibility notes (colorblind-safe palettes, ARIA).

### 23. Matplotlib Publication Chart
**Prompt**: Act as a scientific visualization expert publishing in Nature. Produce a publication-quality matplotlib figure for [DATA] showing [RELATIONSHIP]. Follow conventions: 300 DPI, serif fonts, minimal chart junk, error bars with 95% CI, significance annotations. Output the Python code using matplotlib and seaborn, a caption draft, alt text, and a checklist validating against journal figure guidelines.

### 24. Pandas Groupby Recipes
**Prompt**: Act as a senior analyst writing a Pandas cookbook. Demonstrate 10 groupby patterns on [DATASET]: multi-agg, named agg, transform for z-score, filter, rolling within group, top-N per group, apply with custom function, pivot_table, crosstab with margins, and groupby on categorical. Output annotated code blocks, performance notes, and the equivalent SQL for each pattern.

### 25. Data Pipeline with Prefect
**Prompt**: Act as a data engineering tech lead. Build a Prefect 2 flow ingesting [SOURCE], transforming with Pandas, and loading to [DESTINATION]. Include retries, caching, concurrency limits, and Slack alerts on failure. Output the flow code, a deployment YAML with schedule, unit tests using pytest, and a monitoring dashboard spec covering SLA, latency, and freshness.

### 26. Polars Migration Guide
**Prompt**: Act as a data performance engineer evaluating Polars vs Pandas for [WORKLOAD]. Benchmark key operations (join, groupby, window) on [SIZE] data. Translate [PANDAS_SNIPPET] into Polars lazy API. Output a migration playbook, gotchas (null semantics, dtype mapping, method name changes), a benchmark table with timings, and ROI estimate for team-wide adoption.

### 27. Seaborn EDA Visuals
**Prompt**: Act as a statistics professor teaching visual EDA. Produce a seaborn gallery for [DATASET] covering distribution (histplot, kdeplot), relationship (pairplot, jointplot), categorical (boxplot, violinplot, stripplot), and matrix (heatmap, clustermap) plots. Output Python code, a one-paragraph reading guide per chart type, and a rubric scoring each plot on clarity, honesty, and information density.

### 28. Interactive Notebook Report
**Prompt**: Act as an analytics engineer delivering findings via Jupyter. Build a notebook analyzing [QUESTION] on [DATASET] using Quarto or Jupyter Book for reproducibility. Include parameterized cells with papermill, widgets for filtering, and exportable HTML. Output the notebook outline, key code cells, markdown narrative placeholders, and a rendering command plus CI workflow to republish on every data refresh.

### 29. Python Data Validation
**Prompt**: Act as a senior MLOps engineer. Implement schema validation for [DATASET] using Pandera or Great Expectations. Define column types, ranges, uniqueness, null rules, and cross-column constraints derived from [BUSINESS_RULES]. Output the schema class, a validation wrapper that fails fast in CI, test fixtures for valid and invalid cases, and integration with Prefect/Airflow task failure hooks.

### 30. Streamlit Analyst Tool
**Prompt**: Act as an analytics tools developer. Build a Streamlit app that lets non-technical stakeholders explore [DATASET] with filters, dynamic charts, and CSV export. Cache data with @st.cache_data, add session state for saved views, and secure with OAuth. Output the app.py code, requirements.txt, a Dockerfile, and a 30-second user walkthrough script for onboarding.

### 31. Hypothesis Test Selector
**Prompt**: Act as a biostatistician with 20 years of clinical trial experience. Given a research question about [COMPARISON] on [DATA_TYPE], recommend the appropriate statistical test among t-test, Welch's t, Mann-Whitney U, ANOVA, Kruskal-Wallis, chi-square, Fisher's exact, or paired alternatives. Justify based on normality, variance, independence, and sample size. Output a decision flowchart, Python (scipy.stats) code, and interpretation template with effect size and power.

### 32. P-Value Interpretation
**Prompt**: Act as a statistics educator correcting common p-value misinterpretations. For [STUDY_DESIGN] testing [HYPOTHESIS] with [SAMPLE_SIZE] observations, explain what the p-value does and does not mean. Discuss the ASA 2016 statement, base rate fallacy, and alternatives (confidence intervals, Bayes factors). Output a markdown explainer with 5 myths debunked, a worked numerical example, and guidance on reporting to a non-technical executive audience.

### 33. Confidence Interval Construction
**Prompt**: Act as a frequentist statistician. Construct a 95% confidence interval for [PARAMETER] from [DATASET] using both analytical (normal/t-approximation) and bootstrap (percentile, BCa) methods. Compare widths and assumptions. Output Python code using scipy and pingouin, a visualization of the bootstrap distribution, an interpretation paragraph, and guidance on when to prefer bootstrap over parametric.

### 34. Power Analysis Plan
**Prompt**: Act as an experimental design expert at a research lab. Compute required sample size for detecting [EFFECT_SIZE] in [METRIC] at alpha 0.05 and power 0.8 for a [TEST_TYPE]. Adjust for multiple comparisons using Bonferroni or Benjamini-Hochberg. Output the calculation using statsmodels power module, a sensitivity table varying effect size and power, and a written rationale for the chosen minimum detectable effect.

### 35. Linear Regression Diagnostics
**Prompt**: Act as an econometrician. Fit OLS on [DATASET] predicting [Y] from [X_LIST] and run full diagnostics: linearity (residual plots), normality (Shapiro, QQ), homoscedasticity (Breusch-Pagan, White), independence (Durbin-Watson), multicollinearity (VIF), and influence (Cook's distance, leverage). Output statsmodels code, an annotated diagnostic plot grid, a findings table, and remediation recommendations per violated assumption.

### 36. Logistic Regression Audit
**Prompt**: Act as a credit risk modeler at a retail bank. Fit a logistic regression predicting [BINARY_OUTCOME] on [FEATURES]. Assess with ROC-AUC, KS statistic, calibration (reliability plot, Brier score), and lift table. Check linearity of logit for continuous features. Output the scikit-learn code, a model card, variable importance via coefficients and SHAP, and regulatory documentation for model risk management.

### 37. Bayesian Inference Example
**Prompt**: Act as a Bayesian statistician trained at Columbia. For [PARAMETER] with prior [PRIOR] and data [DATA], compute the posterior using PyMC. Specify likelihood, run NUTS sampling, check convergence (R-hat, ESS), and produce posterior predictive checks. Output the PyMC model code, trace plots, a credible interval interpretation, and a comparison with the equivalent frequentist result highlighting philosophical differences.

### 38. Multiple Testing Correction
**Prompt**: Act as a statistician reviewing [STUDY] with [N_TESTS] hypotheses. Apply family-wise error control (Bonferroni, Holm) and false discovery rate control (Benjamini-Hochberg, Storey q-values). Explain the difference and recommend per context. Output Python code using statsmodels.multitest, a comparison table of adjusted p-values, and guidance on pre-registering the correction method to avoid p-hacking.

### 39. Correlation vs Causation
**Prompt**: Act as a causal inference researcher in the Judea Pearl tradition. For observed correlation between [X] and [Y] in [DATASET], list plausible confounders, mediators, and colliders. Draw a DAG using dagitty syntax, identify adjustment sets via backdoor criterion, and propose an estimation strategy (matching, IPTW, doubly robust). Output the DAG, Python DoWhy code, and a sensitivity analysis (E-value) for unmeasured confounding.

### 40. Non-Parametric Alternatives
**Prompt**: Act as a statistics consultant advising on small-sample analysis for [DATASET] with n=[N] and [DATA_TYPE]. Recommend non-parametric tests (Wilcoxon signed-rank, Mann-Whitney U, Spearman, permutation test, bootstrap) when normality fails. Output a decision table, Python implementations, expected statistical power vs parametric counterparts, and a reporting template for publication.

### 41. A/B Test Design Doc
**Prompt**: Act as a senior experimentation scientist at Meta. Write an A/B test design doc for [FEATURE] measuring [PRIMARY_METRIC] with [GUARDRAIL_METRICS]. Specify hypothesis, unit of randomization, sample size via power analysis, exposure duration, SRM check, and pre-registered analysis plan. Output the doc in markdown with sections Hypothesis, Metrics, Design, Analysis, Rollout Plan, and a sign-off checklist for stats, product, and engineering.

### 42. A/B Test Results Analysis
**Prompt**: Act as a lead data scientist analyzing [EXPERIMENT] with [N_USERS] and [VARIANTS]. Compute lift, confidence intervals, p-values with CUPED variance reduction, and segment heterogeneity. Perform SRM check and novelty effect detection. Output Python code using scipy and an A/B testing library, a results table with effect sizes, a recommendation (ship, iterate, kill), and a post-mortem section on learnings.

### 43. Multi-Armed Bandit Setup
**Prompt**: Act as a reinforcement learning engineer deploying bandits for [USE_CASE]. Compare epsilon-greedy, Thompson Sampling, and UCB1 for allocating traffic across [N_ARMS]. Simulate regret over [T_ROUNDS] and explain exploration-exploitation trade-off. Output a Python simulation, a recommendation for production algorithm, monitoring metrics (regret, pull counts), and a fallback plan for non-stationary reward distributions.

### 44. Quasi-Experiment Design
**Prompt**: Act as a causal inference expert applying difference-in-differences to [POLICY_CHANGE] affecting [TREATED_GROUP]. Identify a valid control, check parallel trends, specify the DiD regression with fixed effects, and test placebo timing. Output the statsmodels or linearmodels code, a parallel trends plot, robustness checks (leads/lags, event study), and caveats around SUTVA violations.

### 45. Switchback Test Design
**Prompt**: Act as a marketplace experimentation expert at Lyft. Design a switchback test for [TREATMENT] when network effects bias classical A/B tests. Define switchback units (time x region), duration, washout windows, and variance estimation via cluster bootstrap. Output the design doc, a simulation to estimate minimum detectable effect, analysis SQL/Python, and gotchas around carryover and seasonality.

### 46. Sample Ratio Mismatch Debug
**Prompt**: Act as an experimentation platform engineer investigating SRM on [EXPERIMENT]. Explain SRM causes (bucketing bugs, bot filtering, redirect drops, logging loss). Run chi-square test and diagnostic queries segmenting by device, geo, and entry point. Output SQL diagnostics, a root-cause decision tree, remediation playbook, and a pre-launch SRM check template to catch issues before day 1.

### 47. Novelty Effect Adjustment
**Prompt**: Act as a senior experimentation scientist at Netflix. For [EXPERIMENT] showing early lift that decays, model novelty vs sustained effect using a segmented regression on days since exposure. Recommend minimum run duration. Output Python code, a time-series plot, a decay curve fit, and a guidance note on when to extend, stop, or iterate based on decay half-life.

### 48. Holdout Group Strategy
**Prompt**: Act as a growth analytics lead designing a long-term holdout for [MARKETING_CHANNEL] with [BUDGET]. Allocate 5 percent of users to a perpetual holdout and measure incremental LTV over [TIME_WINDOW]. Address contamination, re-randomization cadence, and statistical power. Output the rollout plan, measurement SQL, expected incremental LTV calculation, and governance to protect holdout integrity across teams.

### 49. Meta-Analysis of Experiments
**Prompt**: Act as a principal data scientist consolidating learnings from [N_EXPERIMENTS] on [METRIC_FAMILY]. Perform a fixed and random effects meta-analysis, compute pooled effect size and heterogeneity (I^2). Identify moderators via subgroup analysis. Output Python code using PythonMeta or manual statsmodels, a forest plot, funnel plot for publication bias, and a summary memo with confidence-weighted recommendations.

### 50. Experimentation Program Audit
**Prompt**: Act as a VP of Data auditing an experimentation program running [N] tests per quarter. Evaluate velocity, win rate, ship rate, power distribution, guardrail coverage, and organizational adoption. Benchmark against Microsoft/Booking standards. Output a scorecard, 10 prioritized improvements (tooling, culture, governance), and a 90-day roadmap with owners and KPIs.

### 51. Three Statement Model
**Prompt**: Act as an investment banking associate at Goldman Sachs. Build a 5-year integrated three-statement model for [COMPANY] linking income statement, balance sheet, and cash flow statement. Use [HISTORICAL_FINANCIALS] as base. Drive revenue with [GROWTH_DRIVERS], margins from historicals. Output an Excel model structure with tabs, formula logic per line, circular reference handling for interest, and a stress-test toggle for bear/base/bull scenarios.

### 52. DCF Valuation Model
**Prompt**: Act as an equity research analyst covering [SECTOR]. Build a DCF for [COMPANY] with 10-year explicit forecast and terminal value via Gordon Growth and exit multiple. Compute WACC from CAPM with [BETA], [RF_RATE], [ERP]. Output the model in structured markdown, sensitivity tables (WACC vs g, EBITDA multiple vs exit), an implied share price, and a football field chart comparing with comparables and precedents.

### 53. LBO Model Build
**Prompt**: Act as a private equity associate at KKR. Build an LBO for [TARGET] at [ENTRY_MULTIPLE] EBITDA with [DEBT_LAYERS] (TLB, mezzanine, revolver). Model sources and uses, debt schedule, management rollover, and exit after 5 years. Output the model structure, IRR and MOIC calculations, a returns attribution (deleveraging, EBITDA growth, multiple expansion), and a covenant compliance check.

### 54. Comparable Company Analysis
**Prompt**: Act as an M&A banker building a comparables set for [TARGET]. Select [N] peers based on sector, size, growth, and geography. Compute EV/Revenue, EV/EBITDA, P/E, PEG, and forward multiples. Adjust for non-recurring items. Output the comps table, a statistical summary (min, 25th, median, 75th, max), an implied valuation range, and a defense memo on peer selection methodology.

### 55. Precedent Transactions
**Prompt**: Act as an M&A analyst at Morgan Stanley. Build a precedent transactions analysis for [DEAL_THESIS] pulling comparable deals from the last 5 years. For each deal, capture EV, EV/Revenue, EV/EBITDA, control premium, and strategic rationale. Output a transactions table, a commentary on multiple trends, an implied valuation, and a caveats section on comparability and synergies.

### 56. Merger Model Accretion
**Prompt**: Act as an M&A strategist modeling [ACQUIRER] buying [TARGET] for [DEAL_VALUE] mix of cash and stock. Project pro forma EPS with synergies, financing costs, and amortization of intangibles. Compute accretion/dilution in years 1-3 and breakeven synergies. Output the model outline, sensitivity to offer premium and synergy realization, and a board memo recommending deal structure.

### 57. Sensitivity and Scenario
**Prompt**: Act as an FP&A director running scenario analysis on [MODEL]. Define bear, base, bull, and downside scenarios varying [KEY_DRIVERS]. Build a two-variable sensitivity on [OUTPUT] for [INPUT_1] vs [INPUT_2]. Output an Excel-style sensitivity table, tornado chart prioritizing drivers, scenario probability weighting for expected value, and a narrative on key value levers.

### 58. Monte Carlo Valuation
**Prompt**: Act as a quantitative analyst at a hedge fund. Build a Monte Carlo simulation for [COMPANY] DCF varying revenue growth, margin, and WACC using triangular distributions calibrated to analyst consensus. Run 10,000 iterations in Python. Output the numpy/pandas code, the distribution of implied share prices, probability of undervaluation vs current price, and VaR-style tail risk metrics.

### 59. WACC Computation Deep Dive
**Prompt**: Act as a corporate finance professor. Compute WACC for [COMPANY] step by step: unlever comps betas, relever to target structure, derive cost of equity via CAPM, after-tax cost of debt from yield on debt, weights at market value. Output the calculation in a structured table, sources for each input, sensitivity to beta and risk premium, and pitfalls (book vs market, country risk, size premium).

### 60. Startup Valuation Methods
**Prompt**: Act as an early-stage VC partner valuing [STARTUP] at [STAGE] with [METRICS]. Apply scorecard, Berkus, VC method, and discounted revenue multiple approaches. Reconcile into a pre-money range. Output each method's calculation, strengths and weaknesses, the final range, and negotiation considerations (option pool, anti-dilution, liquidation preference) that affect effective valuation.

### 61. Rolling Forecast Build
**Prompt**: Act as an FP&A lead at a high-growth SaaS company. Build a 13-month rolling forecast for [METRIC] combining top-down targets and bottom-up sales pipeline. Update cadence is monthly. Output the process flow, template columns (actual, forecast, variance, commentary), driver tree linking bookings to revenue, and KPIs for forecast accuracy (MAPE, bias).

### 62. Variance Analysis Report
**Prompt**: Act as a controller writing the monthly variance analysis for [BUDGET] vs [ACTUAL]. Decompose variance into price, volume, and mix effects across [PRODUCT_LINES]. Quantify dollar impact and percent. Output a markdown report with executive summary, variance bridge table, waterfall chart description, root-cause commentary per material variance (>5 percent), and corrective actions with owners.

### 63. Zero Based Budgeting
**Prompt**: Act as a turnaround CFO implementing ZBB at [COMPANY]. Redesign the [DEPARTMENT] budget from scratch justifying every dollar against business drivers. Challenge baseline assumptions and rank activities. Output the ZBB framework, a decision package template, expected savings vs prior budget, and an implementation timeline with change management considerations.

### 64. Cash Flow Forecast 13 Week
**Prompt**: Act as a treasury manager at a Series C startup. Build a 13-week cash flow forecast with direct method capturing receipts, disbursements, debt service, and financing. Identify minimum cash covenant breaches. Output the weekly schedule, inflow/outflow categories, sensitivity to AR collection slippage and customer concentration, and a liquidity dashboard for board updates.

### 65. Revenue Forecasting Model
**Prompt**: Act as a head of FP&A forecasting revenue for [BUSINESS] by segment. Build a driver-based model: new logos x ACV, expansion via NRR, churn. Incorporate seasonality and sales cycle length. Output the model, a reconciliation with bottoms-up pipeline, forecast accuracy measurement plan, and a commentary on key risks (pipeline coverage, rep ramp, macro).

### 66. Expense Forecast Drivers
**Prompt**: Act as an FP&A analyst forecasting opex for [DEPARTMENT] with [HEADCOUNT] growing per hiring plan. Build a driver-based model covering salary and benefits (load factor), T&E per FTE, software per seat, and discretionary projects. Output the line-item model, a phasing assumption per driver, a what-if on hiring delays, and reconciliation with recruiting pipeline.

### 67. Unit Economics Model
**Prompt**: Act as a growth strategist at a marketplace. Build a unit economics model computing contribution margin per transaction, payback period, LTV, CAC, and LTV/CAC ratio. Segment by [COHORT_DIMENSION]. Output the model with definitions per metric, a sensitivity to take rate and churn, a benchmark vs industry (3:1 LTV/CAC, <12 month payback), and a profitability path to breakeven.

### 68. Forecast Accuracy Review
**Prompt**: Act as an analytics lead reviewing forecast accuracy for [METRIC] over [N_PERIODS]. Compute MAPE, WAPE, bias, and tracking signal. Diagnose systematic under/over-forecasting. Output a Python analysis, a funnel of errors by segment, a retrospective on drivers of error, and improvements to forecasting process (model, judgment overrides, cadence).

### 69. Budget vs Forecast Governance
**Prompt**: Act as a corporate controller designing budget governance for [COMPANY] with [N_COST_CENTERS]. Define budget lock, reforecast cadence, approval thresholds, and variance escalation. Output a governance policy document, a RACI matrix, a monthly close calendar, and templates for reforecast submission and variance explanation.

### 70. Headcount Planning Model
**Prompt**: Act as a workforce planning analyst building a headcount model for [COMPANY] over [YEARS]. Tie hires to revenue and ratio targets (e.g., S&M reps per $M ACV, engineer per PM). Incorporate attrition, time-to-hire, and ramp. Output a monthly headcount plan, cost impact, capacity output (pipeline, story points), and a sensitivity to attrition and productivity assumptions.

### 71. Portfolio Allocation Model
**Prompt**: Act as a CFA charterholder advising a [AGE] year-old investor with [RISK_TOLERANCE] and [INVESTMENT_HORIZON]. Recommend a strategic asset allocation across US equity, international equity, bonds, REITs, commodities, and cash. Justify with mean-variance optimization or risk-parity rationale. Output the target allocation percentages, rebalancing rules, expected return and volatility, and tax-efficient placement by account type (taxable, 401k, Roth).

### 72. FIRE Retirement Plan
**Prompt**: Act as a CFP specializing in early retirement. Build a FIRE plan for someone earning [INCOME] saving [SAVINGS_RATE] with [EXPENSES] target. Compute FI number at 25x, project years to FI using safe withdrawal rate sensitivity (3%, 3.5%, 4%). Output a year-by-year projection, sequence-of-returns risk analysis via Monte Carlo, healthcare bridge strategy pre-65, and a one-page action plan.

### 73. Tax Loss Harvesting Strategy
**Prompt**: Act as a tax-aware portfolio manager. Design a tax loss harvesting workflow for [TAXABLE_ACCOUNT] with positions [HOLDINGS]. Identify loss candidates, wash sale rules, substitute securities, and tax alpha estimation. Output the harvest decision table, a Python screener for 30-day wash sale risk, expected tax savings at marginal rate [BRACKET], and documentation for IRS reporting.

### 74. Roth Conversion Ladder
**Prompt**: Act as a retirement tax planner. Design a Roth conversion ladder for a client with [TRAD_IRA_BALANCE] and [EXPECTED_INCOME] during early retirement years. Optimize conversion amounts to fill lower brackets without triggering IRMAA or ACA cliffs. Output a multi-year conversion schedule, projected tax paid, future RMD reduction, and trade-offs vs leaving pre-tax and using rule 72(t).

### 75. Real Estate Cash Flow Analysis
**Prompt**: Act as a real estate investor with 20 years of rental portfolio experience. Analyze [PROPERTY] at [PRICE] with [RENT], [EXPENSES], [FINANCING]. Compute cap rate, cash-on-cash, DSCR, IRR over 10-year hold, and NPV. Output the pro forma, sensitivity to vacancy and rent growth, a hold-vs-sell decision framework, and risks (concentration, liquidity, interest rate).

### 76. Dividend Growth Screen
**Prompt**: Act as a quality-dividend portfolio manager. Screen US equities for dividend growth champions with 10+ years of increases, payout ratio under 60 percent, FCF growth, and reasonable valuation (P/E under sector median). Output the Python screener using yfinance, a ranked shortlist, a portfolio construction rule limiting single-name and sector weight, and backtested dividend yield on cost vs SP500.

### 77. Bond Ladder Construction
**Prompt**: Act as a fixed income strategist. Build a 10-year Treasury bond ladder for [CAPITAL] with equal annual rungs, reinvesting maturities. Compute duration, yield to maturity, and interest rate risk. Output the ladder schedule, expected cash flow, a comparison vs bond fund (BND), tax considerations for Treasuries vs municipals, and a rebalance plan if rates move 100 bps.

### 78. Risk Parity Portfolio
**Prompt**: Act as a quantitative portfolio manager replicating All Weather. Build a risk parity portfolio across equities, long bonds, intermediate bonds, commodities, and gold. Compute volatility contributions and use inverse-vol weighting. Output the target weights, a Python notebook using PyPortfolioOpt, historical backtest stats (CAGR, vol, max drawdown, Sharpe), and a rebalance policy (threshold vs calendar).

### 79. 401k Optimization Guide
**Prompt**: Act as a fiduciary financial advisor. Review [401K_PLAN] offerings and recommend optimal contribution strategy for someone earning [INCOME] with [MATCH]. Prioritize match, HSA, Roth vs traditional decision based on current and expected bracket, and backdoor Roth if eligible. Output a contribution waterfall, fund selection within plan (low-cost index), and annual review checklist.

### 80. Crypto Allocation Framework
**Prompt**: Act as a digital assets portfolio strategist. Design a crypto sleeve within a traditional portfolio for [RISK_PROFILE] capping at [PERCENT]. Allocate across BTC, ETH, and a basket of large-caps, with rebalancing and custody considerations (cold storage, multi-sig). Output the allocation rationale, rebalance rules, tax lot accounting plan, and a risk disclosure covering volatility, regulatory, and custody risks.

### 81. Survey Design Fundamentals
**Prompt**: Act as a market research director with 15 years at Kantar. Design a customer satisfaction survey for [PRODUCT] targeting [SEGMENT]. Craft question order, balanced scales, avoid leading language, and include attention checks. Output the full questionnaire with item types (Likert, NPS, open-ended), routing logic, estimated completion time, and a pre-test plan with cognitive interviews.

### 82. Sample Size for Surveys
**Prompt**: Act as a survey statistician. Compute required sample size for a survey on [POPULATION] estimating [PROPORTION] within [MARGIN_OF_ERROR] at 95 percent confidence. Adjust for finite population, design effect from stratification, and expected response rate. Output the calculation, stratification plan by [STRATA], and a rationale for over-sampling certain groups to enable subgroup analysis.

### 83. NPS Analysis Deep Dive
**Prompt**: Act as a CX analytics lead. Analyze NPS data from [SURVEY] with verbatims. Compute score by segment, trend over [TIME], statistical significance of differences, and topic modeling of open-ended responses using BERTopic. Output a SQL/Python analysis, a driver analysis tying NPS to behavioral metrics, a cohort view, and prioritized CX improvements with expected NPS impact.

### 84. Conjoint Analysis Setup
**Prompt**: Act as a pricing research expert. Design a choice-based conjoint for [PRODUCT] with attributes [ATTRIBUTE_LIST] and levels. Determine number of tasks, efficient design, and sample size. Output the design matrix, hierarchical Bayes estimation plan, expected part-worths, simulator to predict share at new price points, and a presentation template for the pricing committee.

### 85. Focus Group Moderator Guide
**Prompt**: Act as a qualitative research lead. Draft a 90-minute moderator guide for a focus group on [TOPIC] with [N_PARTICIPANTS]. Include warm-up, projective exercises, stimulus reactions, and closing. Ensure balanced participation and probe for why behind what. Output the timed agenda, question bank, stimulus material notes, and a coding framework for post-session analysis.

### 86. Market Sizing TAM SAM SOM
**Prompt**: Act as a strategy consultant at McKinsey. Size the market for [PRODUCT] in [GEOGRAPHY] using top-down and bottom-up approaches. Define TAM, SAM, SOM with clear assumptions. Output the calculations in a structured markdown with sources cited, a sanity check via triangulation, sensitivity to penetration rate, and a slide-ready summary for a board deck.

### 87. Competitive Intelligence Framework
**Prompt**: Act as a competitive intelligence analyst at a tech giant. Build a competitor profile for [COMPETITOR] covering products, pricing, positioning, financials, headcount, hiring trends, patents, and public statements. Output a structured profile in markdown, data sources (SEC, LinkedIn, job boards, app review, SimilarWeb), a threat assessment scorecard, and recommended countermoves.

### 88. Voice of Customer Synthesis
**Prompt**: Act as a VoC research lead analyzing [N] support tickets, reviews, and survey comments. Use topic modeling and sentiment analysis in Python (BERTopic, VADER) to extract themes. Triangulate with volume and severity. Output a prioritized pain point list, quote exemplars per theme, a Kano model classification (must-have, performer, delighter), and a roadmap input brief for PM.

### 89. Segmentation Analysis
**Prompt**: Act as a marketing scientist. Run behavioral segmentation on [CUSTOMER_DATA] using K-means or Gaussian mixture models. Select optimal k via elbow and silhouette. Profile each segment on demographics, behavior, and value. Output Python code, segment personas with names and descriptions, actionable targeting strategies, and a stability test across two time periods.

### 90. Pricing Research Report
**Prompt**: Act as a pricing strategist. Run a Van Westendorp price sensitivity meter for [PRODUCT] across [N_RESPONDENTS]. Derive the range of acceptable prices, optimal price point, and point of marginal cheapness/expensiveness. Output the analysis in Python, a visualization with all four curves, a recommendation with caveats, and a next-step plan using conjoint for triangulation.

### 91. Literature Review Protocol
**Prompt**: Act as a research librarian trained in PRISMA. Design a systematic literature review protocol on [RESEARCH_QUESTION]. Define inclusion/exclusion criteria, databases (PubMed, Scopus, Web of Science), search strings, screening process, and data extraction template. Output the protocol document, PRISMA flow diagram description, risk of bias tool (ROBIS or AMSTAR-2), and a timeline with milestones.

### 92. Citation Management Workflow
**Prompt**: Act as a PhD advisor onboarding a new student. Set up a Zotero-based citation workflow with browser connector, group library, tags, and BetterBibTeX for LaTeX integration. Output the setup steps, folder structure by project, naming conventions, note-taking template (summary, quotes, relevance), and backup strategy including sync and export to BibTeX.

### 93. Research Paper Outline
**Prompt**: Act as a journal editor at Nature. Draft a full outline for a research paper titled [TITLE] with sections Abstract, Introduction, Methods, Results, Discussion, Conclusion. For each section list key points, required figures/tables, and word count targets per journal guidelines. Output the annotated outline, a reviewer anticipation list, and a checklist against reporting standards (CONSORT, STROBE, PRISMA).

### 94. Methodology Selection
**Prompt**: Act as a research methods professor. For research question [QUESTION], recommend an appropriate methodology from quantitative (experiment, survey, secondary data), qualitative (ethnography, interviews, case study), or mixed methods. Justify based on epistemology, feasibility, and generalizability. Output a decision memo, a data collection plan, an analytical framework, and ethical considerations for IRB.

### 95. Meta-Analysis Forest Plot
**Prompt**: Act as a Cochrane reviewer. Perform a meta-analysis on [N_STUDIES] evaluating [INTERVENTION] on [OUTCOME]. Compute pooled effect size (Hedges g), 95 percent CI, heterogeneity (I^2, tau^2), and publication bias (funnel plot, Egger's test). Output Python or R (metafor) code, a forest plot description, sensitivity analyses (leave-one-out), and a GRADE rating of evidence quality.

### 96. Qualitative Coding Scheme
**Prompt**: Act as a qualitative researcher trained in grounded theory. Develop a coding scheme for [N] interview transcripts on [TOPIC]. Describe open, axial, and selective coding passes. Use Atlas.ti or NVivo conventions. Output the initial codebook, inter-rater reliability plan (Cohen's kappa), examples of coded excerpts, and a theoretical memo template to surface emergent concepts.

### 97. Reproducible Research Setup
**Prompt**: Act as an open science advocate. Set up a reproducible research project for [STUDY] using Git, DVC for data, Quarto or R Markdown, pinned environments (renv, conda-lock), and preregistration on OSF. Output the repo folder structure, a README template, commit conventions, a CI workflow running analysis end-to-end, and a data sharing plan compliant with FAIR principles.

### 98. Peer Review Response
**Prompt**: Act as a tenured professor coaching a postdoc on responding to peer review for [MANUSCRIPT] with [REVIEWER_COMMENTS]. Draft a point-by-point response that is respectful, substantive, and tracks every change. Output the response letter structure, language templates for agree/disagree/clarify, a change summary table, and a cover letter to the editor highlighting major revisions.

### 99. Research Proposal Grant
**Prompt**: Act as a grant writer with a 50 percent NIH R01 success rate. Draft a 5-page specific aims and significance section for [RESEARCH_TOPIC] targeting [FUNDING_AGENCY]. Articulate gap, central hypothesis, three aims, innovation, and impact. Output the draft, a scoring rubric against agency criteria, a pitfalls-and-alternative-approaches section, and reviewer psychology tips (skimmable formatting, signposting).

### 100. Data Ethics Review
**Prompt**: Act as a research ethics board chair. Review [STUDY] for ethical considerations including informed consent, privacy, data minimization, vulnerable populations, dual use, and algorithmic bias. Apply Belmont Principles and GDPR/HIPAA where relevant. Output an IRB-style review memo, a risk mitigation plan, consent form template, and a monitoring plan for ongoing ethical oversight during data collection and analysis.
