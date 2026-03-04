# Context Window Experiment Results

**Model:** `openai/gpt-oss-120b`  
**Document:** `long_document.txt`  
**Document size:** 25,348 chars | ~6,337 estimated tokens  
**Context window limit (model):** 8,192 tokens  
**Chunks (Strategy B):** 11

---

## Strategy Descriptions

| Strategy | Description |
|---|---|
| **A – Naive Stuffing** | Entire document + question sent in one API call. Simple but risks context pressure and 'lost-in-the-middle' degradation. |
| **B – Summarize-then-Answer** | Document chunked by chapter → each chunk summarised (map) → summaries combined → question answered on combined summary (reduce). |

---

## Question 1

> What percentage reduction in precipitation forecast errors did AI-enhanced climate models achieve compared to traditional NWP models, and which study reported this?

### Strategy A – Naive Stuffing

**Status:** `ok`  
**Prompt tokens (actual):** 5484  
**Estimated prompt tokens:** ~6427  
**Completion tokens:** 150  

**Answer:**

AI‑enhanced climate models cut 10‑year precipitation forecast errors by **34 %** compared with traditional NWP models. This result is reported in **Zhang et al., 2023, *Nature Climate Change***.

**Failure / Warning Notes:**

- WARNING: Estimated prompt tokens (6427) is high — context limit pressure likely.

### Strategy B – Summarize-then-Answer

**Status:** `ok`  
**Total API tokens (map + reduce):** 10600  
**Map chunks:** 11  
**Approx reduce-prompt tokens:** ~1595  

**Answer:**

AI‑enhanced climate models reduced 10‑year precipitation forecast errors by **34 %** compared with traditional numerical weather prediction (NWP) models. This result is reported in **Zhang et al., 2023, *Nature Climate Change*** (see the **EXECUTIVE SUMMARY**).

---

## Question 2

> What was the median annual energy production gain achieved by ML-optimised wind farm layouts according to the meta-analysis cited in the report, and how many commercial projects were included?

### Strategy A – Naive Stuffing

**Status:** `ok`  
**Prompt tokens (actual):** 5492  
**Estimated prompt tokens:** ~6434  
**Completion tokens:** 199  

**Answer:**

The meta‑analysis reported a **median annual energy‑production gain of 14.2 %**, based on **47 commercial wind‑farm projects**.

**Failure / Warning Notes:**

- WARNING: Estimated prompt tokens (6434) is high — context limit pressure likely.

### Strategy B – Summarize-then-Answer

**Status:** `ok`  
**Total API tokens (map + reduce):** 10533  
**Map chunks:** 11  
**Approx reduce-prompt tokens:** ~1418  

**Answer:**

The report does not give a single median value for the energy‑production increase. It reports a **range of 11 %–18 % higher annual energy production** for machine‑learning‑optimised wind‑farm layouts (see the **Executive Summary**). The underlying meta‑analysis combined **47 European commercial wind‑farm projects** (also noted in the **Executive Summary** and reiterated in **Chapter 3**). Since a specific median figure is not stated in the summaries, it cannot be provided.

---

## Question 3

> What are the four specific policy recommendations made in the Conclusion of the report?

### Strategy A – Naive Stuffing

**Status:** `ok`  
**Prompt tokens (actual):** 5472  
**Estimated prompt tokens:** ~6408  
**Completion tokens:** 400  

**Answer:**

The report’s Conclusion lists four concrete policy recommendations:

1. **Mandatory lifecycle carbon accounting** for all large‑scale climate‑AI deployments.  
2. **Open‑access repositories for climate‑AI training data**, with a priority on expanding coverage for the Global South.  
3. **Interpretability requirements** for

**Failure / Warning Notes:**

- WARNING: Estimated prompt tokens (6408) is high — context limit pressure likely.

### Strategy B – Summarize-then-Answer

**Status:** `ok`  
**Total API tokens (map + reduce):** 10761  
**Map chunks:** 11  
**Approx reduce-prompt tokens:** ~1538  

**Answer:**

The Conclusion lists a set of concrete policy actions. Based on the summary, the first two are:

1. **Mandatory lifecycle carbon accounting for large‑scale climate‑AI deployments**【Conclusion】  
2. **Open‑access climate‑AI training‑data repositories, with priority given to coverage in the Global South**【Conclusion】

The summary truncates the remainder of the list (it begins “Interpret

---

## Question 4

> What are the three main limitations of AI in climate applications as described in Chapter 6? Provide at least one specific example for each.

### Strategy A – Naive Stuffing

**Status:** `ok`  
**Prompt tokens (actual):** 5484  
**Estimated prompt tokens:** ~6421  
**Completion tokens:** 400  

**Answer:**

**Chapter 6 identifies three principal limitations of AI for climate work**

| Limitation (Chapter 6) | What the report says | Concrete example from the text |
|------------------------|----------------

**Failure / Warning Notes:**

- WARNING: Estimated prompt tokens (6421) is high — context limit pressure likely.

### Strategy B – Summarize-then-Answer

**Status:** `ok`  
**Total API tokens (map + reduce):** 10777  
**Map chunks:** 11  
**Approx reduce-prompt tokens:** ~1525  

**Answer:**



**Failure / Warning Notes:**

- Short answer — detail may have been lost during summarisation.

---

## Question 5

> What is the projected GDP impact of a 2°C warming scenario on India according to this report?

### Strategy A – Naive Stuffing

**Status:** `ok`  
**Prompt tokens (actual):** 5477  
**Estimated prompt tokens:** ~6409  
**Completion tokens:** 152  

**Answer:**

The report does not provide any information on the projected GDP impact of a 2 °C warming scenario for India.

**Failure / Warning Notes:**

- WARNING: Estimated prompt tokens (6409) is high — context limit pressure likely.

### Strategy B – Summarize-then-Answer

**Status:** `ok`  
**Total API tokens (map + reduce):** 10516  
**Map chunks:** 11  
**Approx reduce-prompt tokens:** ~1530  

**Answer:**

The provided document summaries do not contain any information about the projected GDP impact of a 2 °C warming scenario on India.

---

## Appendix – Combined Chapter Summaries (Strategy B Map Output)

### Preamble
- **Report Overview**: “Artificial Intelligence in Climate Change Mitigation and Adaptation – A Comprehensive Technical and Policy Review” (Report No. ENV‑2024‑117) presents a systematic analysis of AI‑driven solutions for both reducing greenhouse‑gas emissions and enhancing

### EXECUTIVE SUMMARY
- AI‑enhanced climate models cut 10‑year precipitation forecast errors by **34%** versus traditional NWP (Zhang et al., 2023, *Nature Climate Change*).  
- Machine‑learning optimization of wind‑farm layouts yields **11–18%** higher annual energy production, shown in a meta‑analysis of **47** European commercial projects (Osei & Lindqvist, 2024).  
- Satellite‑based AI carbon‑flux models now identify deforestation within **72 hours** at **10 m** resolution, enabling near‑real‑time REDD+ verification (Nair et al., 2023, *Remote Sensing of Environment*).  
- Climate‑risk AI tools used

### CHAPTER 1: INTRODUCTION
- The IPCC Sixth Assessment Report (2021) confirms human‑driven warming, with 2023 global surface temperatures 1.45 °C above the 1850‑1900 pre‑industrial baseline (WMO Global Climate Report, 2024); limiting warming to 1.5 °C demands a ~43 % cut in GHG emissions by 2030 and net‑zero by 2050 (IPCC AR6, Ch. 4).  
- AI is highlighted as a “force multiplier” for climate action because its pattern‑recognition capabilities can handle the petabytes of satellite, sensor, and model‑output data produced annually by climate science.  
- This report reviews peer‑reviewed and grey‑literature from Jan 2019–Aug 202

### CHAPTER 2: AI IN CLIMATE MODELLING AND PREDICTION
- **Traditional NWP limitations:** Operational systems like ECMWF’s IFS discretize the atmosphere into grid cells and need ~1,200 CPU‑core hours for a global 10‑day forecast, yet still rely on costly parameterisations to capture sub‑grid processes such as convective precipitation.  

- **Data‑driven forecasting breakthroughs:** *Pangu‑Weather* (Huawei, Bi et

### CHAPTER 3: AI IN RENEWABLE ENERGY
- **Solar power forecasting:** Deep‑learning models (e.g., LSTM + attention) cut day‑ahead GHI RMSE by **22.4 % vs. NWP** across 12 German sites (Nie et al., 2022). SolarEdge’s proprietary ML reduced curtailment by **8.3 %** in 2023, adding ≈**430 GWh** of generation fleet‑wide.  

- **Wind farm wake modeling & layout:** Physics‑informed neural networks achieve **97 % accuracy** vs. high‑fidelity CFD while running in milliseconds, addressing €1.2 bn/yr

### CHAPTER 4: AI IN CARBON MONITORING, REPORTING AND VERIFICATION (MRV)
- **Deforestation monitoring:** The Global Forest Watch AI system (Hansen et al., 2013 → 2023) processes Sentinel‑2/Landsat data with multi‑temporal CNNs, achieving a mean detection latency of **68 h** (target < 72 h) and a **false‑positive rate of 4.1 %** (down from 11.3 % in 2019). Alerts are delivered at **10 m** (Sentinel‑2) and **30 m** (Landsat) resolution.  

- **Cloud‑cover mitigation:** Nair et al. (2023, *Remote Sensing of Environment*) showed that SAR‑optical multi‑modal fusion

### CHAPTER 5: AI IN CLIMATE FINANCE AND RISK
- **AI‑driven physical risk tools** now deliver near‑real‑time, high‑resolution hazard forecasts: neural‑network hydraulic emulators generate 1‑in‑100‑year coastal flood maps at building level in <10 s (vs. ~6 h for full hydrodynamic models; Wing et al., 2022, *Nature Communications*), a system JPMorgan Chase rolled out in 2023 to cover $620 bn of real‑estate‑secured loans. Ensemble ML models for wildfire spread reach 85 % accuracy on 6‑hour forecasts and are used by Pacific Gas & Electric for pre‑emptive de‑energisation. Gradient‑boosting heat‑wave mortality models achieve cross‑validated R² = 0.87 (Chen

### CHAPTER 6: CHALLENGES AND LIMITATIONS
- **Data gaps hinder model fidelity**: High‑resolution climate observations are sparse in Sub‑Saharan Africa and Southeast Asia, and emissions inventories systematically under‑report agriculture, waste, and informal industry, limiting supervised‑learning labels in data‑poor regions.  
- **AI training itself emits CO₂**: A 100‑billion‑parameter climate foundation model can emit ≈ 590 tCO₂e per training run (Patterson et al., 2022, *Communications of the ACM*); continuous planetary‑scale remote‑sensing inference also incurs substantial energy use, and lifecycle analyses for AI climate tools remain underdeveloped.  
- **Interpretability remains a barrier**: Post‑hoc methods such as SHAP and LIME are used for climate risk models,

### CHAPTER 7: FUTURE DIRECTIONS
- **Foundation models for climate science:**  
  - *ClimaX* (Nguyen et al., 2023, ICML) – a transformer pre‑trained on five CMIP6 ensembles + ERA5; fine‑tuning yields top‑1 scores on six ClimateBench tasks, showing strong transfer to new variables/regions.  
  - *Earth‑2* (NVIDIA, 2024) – combines foundation‑model training with a digital‑twin pipeline to deliver metre‑scale urban climate projections.

- **Active learning & human‑in‑the‑loop:**  
  - By querying only the most informative unlabeled samples, active‑learning pipelines cut labeling effort by **60–70 %** while keeping performance on deforestation detection comparable (Rolf et

### CONCLUSION
- AI can meaningfully accelerate climate mitigation and adaptation across the entire value chain—enhancing climate projections, renewable‑energy optimization, carbon monitoring, and climate‑risk finance—showing consistent gains over traditional methods in controlled studies.  

- Major obstacles remain, including data gaps, high computational costs, limited interpretability, equity issues, and vulnerability to distribution shift; these require coordinated investment in research infrastructure, governance, and capacity building, especially in climate‑vulnerable nations.  

- The authors propose five actionable recommendations: (1) mandatory lifecycle carbon accounting for large‑scale climate‑AI projects; (2) open‑access climate AI training datasets with a focus on

### REFERENCES (SELECTED)

