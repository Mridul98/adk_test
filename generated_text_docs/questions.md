mahmudnabi-optimizely: #file:input 

GitHub Copilot: Gathering the SQL documentation files to craft advanced BI questions from their content. Expecting to extract key metrics, dimensions, and grain for insightful queries.

Searched for files matching `**/data/generated_sql_docs/*.md`, 18 matches

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/int_customer_metrics.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/int_product_performance.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/int_region_sales.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/rpt_customer_segments.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/rpt_product_trends.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/rpt_sales_summary.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/stg_customers.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/stg_order.md)

Read [](file:///Users/mahmud.nabi/adk_test/data/generated_sql_docs/stg_products.md)

Here are 5 tough, insight-focused BI questions grounded in the documented models and suitable for answering with SQL:

1. Which customer segments (Platinum/Gold/Silver/Bronze) are driving disproportionate revenue growth month over month, and within each region, how does their average time since last order (recency) correlate with changes in total_spent and avg_order_value?  
2. For each region × product category, does month_over_month_growth_pct in sales accelerate or decelerate as active_days increases, and which region-category pairs show sustained growth (≥X% for ≥3 consecutive months) despite fewer active_days (below the median)?  
3. Among products with declining total_revenue but increasing avg_selling_price, which categories are losing order volume (total_orders) while retaining or upgrading high-value buyers (unique_customers staying flat or rising in those regions)?  
4. What share of total monthly sales comes from newly “upgraded” customers (e.g., those crossing from Silver→Gold or Gold→Platinum based on total_spent thresholds within the last N days), and how does their avg_order_value compare to long‑tenured customers in the same segment and region?  
5. Which products exhibit a “boom-bust” pattern: ≥50% growth_pct in one month followed by a ≥30% decline the next, and how does that volatility differ by category in regions where overall regional_sales total_sales remains stable (±5%) over the same period?

Let me know if you’d like accompanying SQL patterns or to tailor these to a specific warehouse dialect.

mahmudnabi-optimizely: #file:input you have to look into the provided folder only

GitHub Copilot: Created 4 todos

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/subscription_snapshot.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/opportunity_analytics_snapshot.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/marketing_qualified_leads.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/pipe_generation_bookings_product_w_targets.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/product_snapshot.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/gainsightcs_scorecard_snapshot.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/exp_activation_flags_snapshot.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/exp_customer_adoption_brave.txt)

Read [](file:///Users/mahmud.nabi/adk_test/generated_text_docs/input/user_role_snapshot.txt)

Starting (2/4) *Derive BI domains*

Starting (3/4) *Generate 5 tough BI questions*

Completed (3/4) *Generate 5 tough BI questions*

Below are 5 tough, insight‑driven BI questions strictly based on (and only answerable with) the datasets in the provided folder:

1. Experimentation Impact on Revenue Trajectory  
Using `exp_customer_adoption_brave` (monthly counts of experiments started/concluded, significant increases, feature flags enabled, rolling averages) and ARR metrics, which customer cohort (grouped by months_since_first_exp_product_identified_in_tat bucket: 0–6, 7–12, 13–24, >24) shows the highest median ARR growth rate in the 6 months after crossing a threshold of ≥3 experiments_started AND ≥2 experiments_sig_increase in a single month?

2. Early Experiment Velocity vs Later Pipeline & Bookings Attainment  
Link weekly experimentation intensity from `exp_activation_flags_snapshot` (last_30_days experiments_started counts) to quarterly proportional target metrics in `pipe_generation_bookings_product_w_targets`: Do accounts with sustained ≥10 experiments in any rolling 30‑day window two quarters prior achieve a statistically higher average bookings target attainment ratio (actual bookings / target_bookings_proportional) in the current quarter, controlling for segment and region?

3. Product Configuration Complexity vs Subscription Renewal Uplift  
From `subscription_snapshot` and `product_snapshot`, compare renewal uplift rate (`SBQQ_RENEWAL_UPLIFT_RATE_C`) across subscriptions whose associated products have high CPQ configuration entropy (e.g., count of non‑null advanced CPQ config fields per product: pricing_method, subscription_term, discount_schedule, upgrade_ratio, overage flags). Does higher configuration complexity correlate with higher median ARR_C renewal uplift, after filtering out subscriptions marked as churn (`CHURN_REASON_C IS NOT NULL`)?

4. Lead Journey Efficiency and Role Hierarchy Influence  
Using `marketing_qualified_leads`, `opportunity_analytics_snapshot` (stage dates), and `user_role_snapshot` (role hierarchy), which user_role_name groups (aggregated at parent role tree depth) exhibit the shortest median lead time from `date_status_qualified` to `date_entered_stage_closed_won` for leads that converted, and how does that median time vary by opportunity_source_category and segment? Identify outlier role tiers whose cycle time is >1.5× the overall median.

5. Customer Health Signal Alignment with Experiment Adoption  
Combining monthly experiment adoption metrics (`exp_customer_adoption_brave`: experiments_started, flags_enabled, user_logins_unique, exp_usage) with scorecard risk indicators in `gainsightcs_scorecard_snapshot` (e.g., CHURN_RISK_GC, ENGAGEMENT_GC, CUSTOMER_EXPERIENCE_GC), which leading experimentation signal (lagged by 1–2 months) has the strongest correlation (e.g., highest absolute Spearman rho) with subsequent improvement in CURRENT_SCORE_GC quartile for at‑risk customers (CHURN_RISK_GC in bottom quartile), and does this differ between customers with ARR above vs below the median?

If you’d like, I can next draft SQL starter templates for any of these. Just say which number(s) you want to pursue.