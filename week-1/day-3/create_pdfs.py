"""
Week 1 · Day 3 — PDF Generator
================================
Creates two large synthetic PDFs used as knowledge sources for LLM evaluation:

  - ai_foundations.pdf      (~5 000+ words on Artificial Intelligence)
  - climate_change.pdf      (~5 000+ words on Climate Change)

Run this script once before running evaluate_llms.py.

Requirements:
  pip install reportlab
"""

from pathlib import Path
from textwrap import wrap

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)

OUTPUT_DIR = Path(__file__).parent

# ---------------------------------------------------------------------------
# PDF 1 – Artificial Intelligence: Foundations and Applications
# ---------------------------------------------------------------------------

AI_SECTIONS = [
    (
        "Chapter 1 – Introduction to Artificial Intelligence",
        """
Artificial intelligence (AI) refers to the simulation of human intelligence processes by machines,
especially computer systems. These processes include learning, reasoning, problem-solving, perception,
and language understanding. The field of AI was formally founded at the Dartmouth Conference in 1956,
organised by John McCarthy, Marvin Minsky, Nathaniel Rochester, and Claude Shannon. The conference
proposed that "every aspect of learning and every feature of intelligence can in principle be so
precisely described that a machine can be made to simulate it."

Early AI research in the 1950s and 1960s explored symbolic reasoning, theorem proving, and game
playing. Arthur Samuel developed one of the first self-learning programs — a checkers-playing program
that improved through experience. Alan Turing proposed the famous Turing Test in 1950 as a measure
of machine intelligence: a machine passes the test if a human evaluator cannot reliably distinguish
its responses from those of a human.

AI development has gone through several boom-and-bust cycles, often called "AI winters," where
funding and interest dropped sharply after overly optimistic predictions failed to materialise. The
first AI winter (1974–1980) followed criticism of the Perceptron model and the failure of machine
translation systems. The second AI winter (1987–1993) saw collapse of the Lisp machine market.

Modern AI has experienced a renaissance since 2010 driven by three key factors: the availability
of massive datasets, dramatic improvements in computing hardware (especially GPUs), and breakthroughs
in deep learning algorithms. Deep learning enabled machines to surpass human-level performance on
tasks such as image classification (ImageNet, 2012) and the board game Go (AlphaGo, 2016).

AI is typically divided into narrow AI — systems designed for a specific task — and artificial
general intelligence (AGI) — hypothetical systems capable of performing any intellectual task that
a human can. All existing AI systems as of 2024 are narrow AI. AGI remains an open research
challenge with no consensus on when or whether it will be achieved.
""",
    ),
    (
        "Chapter 2 – Machine Learning Fundamentals",
        """
Machine learning (ML) is a sub-field of AI that enables computer systems to learn and improve from
experience without being explicitly programmed. Instead of hand-crafted rules, ML models learn
patterns from data.

Supervised learning is the most widely used paradigm. The model is trained on a labelled dataset,
where every input example is paired with the correct output. The objective is to learn a mapping
function f(x) → y that generalises from the training distribution to unseen data. Common supervised
learning algorithms include linear regression, logistic regression, decision trees, random forests,
support vector machines (SVM), and gradient-boosted trees (e.g., XGBoost, LightGBM).

Unsupervised learning finds hidden patterns or intrinsic structures in unlabelled data. Key
techniques include k-means clustering, hierarchical clustering, principal component analysis (PCA),
t-SNE (t-distributed stochastic neighbor embedding) for dimensionality reduction, and autoencoders.
Unsupervised methods are used for anomaly detection, customer segmentation, and feature learning.

Semi-supervised learning combines a small labelled dataset with a large unlabelled dataset.
Self-supervised learning, a variant that has become prominent in NLP and vision, generates
supervisory signals from the data itself — for example, predicting masked tokens in BERT.

Reinforcement learning (RL) trains an agent to make sequential decisions by maximising cumulative
reward. The agent interacts with an environment, receives feedback in the form of rewards or
penalties, and updates its policy. Key RL algorithms include Q-learning, Deep Q-Networks (DQN),
Proximal Policy Optimisation (PPO), and Soft Actor-Critic (SAC). RL has achieved remarkable
results in game playing (Atari, Go, Dota 2), robotics, and recommendation systems.

Overfitting occurs when a model memorises training data and fails to generalise. Regularisation
techniques such as L1/L2 penalties, dropout, batch normalisation, early stopping, and data
augmentation mitigate overfitting. The bias-variance tradeoff is a central concept: high-bias
models underfit; high-variance models overfit.

A model's performance is evaluated using a held-out test set. Common evaluation metrics include
accuracy, precision, recall, F1 score, area under the ROC curve (AUC-ROC), mean absolute error
(MAE), and root mean squared error (RMSE). Cross-validation, especially k-fold cross-validation,
provides more reliable performance estimates than a single train-test split.
""",
    ),
    (
        "Chapter 3 – Deep Learning and Neural Networks",
        """
Deep learning is a subset of machine learning that uses artificial neural networks with many
layers (hence "deep") to learn hierarchical representations from raw data. The artificial neuron,
inspired by biological neurons, computes a weighted sum of its inputs, adds a bias, and passes the
result through a non-linear activation function such as ReLU (rectified linear unit), sigmoid,
or tanh.

Feedforward neural networks (also called multilayer perceptrons, MLPs) consist of an input layer,
one or more hidden layers, and an output layer. Parameters are learned by minimising a loss
function (e.g., cross-entropy for classification, mean squared error for regression) using
stochastic gradient descent (SGD) and backpropagation. The Adam optimiser, which adapts learning
rates per parameter, is currently the most popular choice.

Convolutional neural networks (CNNs) are designed for grid-structured data such as images. They
apply learned filters (kernels) across spatial locations, sharing weights to capture local features.
Pooling layers reduce spatial dimensions. Landmark CNN architectures include AlexNet (2012),
VGGNet, ResNet (introduced residual/skip connections to train very deep networks), DenseNet, and
EfficientNet. CNNs power applications in image classification, object detection (YOLO, Faster R-CNN),
and medical imaging.

Recurrent neural networks (RNNs) model sequential data by maintaining a hidden state passed across
time steps. Long short-term memory networks (LSTMs) and gated recurrent units (GRUs) address the
vanishing gradient problem of vanilla RNNs by using gating mechanisms to selectively remember or
forget information.

The Transformer architecture (introduced in "Attention Is All You Need," Vaswani et al., 2017)
replaced recurrence with self-attention mechanisms. Transformers model long-range dependencies
efficiently in parallel. They underpin all large language models (LLMs), including GPT, BERT,
T5, PaLM, and LLaMA. The self-attention mechanism computes pairwise interactions between all
tokens in a sequence, producing context-aware representations.

Generative adversarial networks (GANs), introduced by Ian Goodfellow in 2014, consist of a
generator and a discriminator trained adversarially. The generator produces synthetic data;
the discriminator distinguishes real from fake. GANs are used in image synthesis, style transfer,
and data augmentation. Diffusion models such as DALL-E 2 and Stable Diffusion have since
surpassed GANs for image generation quality.
""",
    ),
    (
        "Chapter 4 – Natural Language Processing",
        """
Natural language processing (NLP) is the branch of AI concerned with enabling machines to
understand, interpret, and generate human language. NLP tasks include tokenisation, part-of-speech
tagging, named entity recognition (NER), sentiment analysis, machine translation, question
answering, text summarisation, and dialogue systems.

Word embeddings represent words as dense vectors in a continuous high-dimensional space, capturing
semantic relationships. Word2Vec (2013) learns embeddings by predicting surrounding words (skip-gram)
or predicting a word from its context (CBOW). GloVe learns embeddings from global word co-occurrence
statistics. Both methods produce static embeddings that do not vary with context.

Contextual embeddings, introduced by ELMo (2018), LLMs trained on massive corpora, produce
different vector representations for the same word depending on its context. BERT (Bidirectional
Encoder Representations from Transformers, 2018) uses masked language modelling (MLM) and next-
sentence prediction (NSP) as pretraining objectives, producing deeply contextual representations
that can be fine-tuned on downstream tasks with minimal additional data.

The GPT (Generative Pre-trained Transformer) family, developed by OpenAI, uses autoregressive
language modelling: the model predicts the next token given preceding tokens. GPT-3 (175 billion
parameters, 2020) demonstrated remarkable few-shot learning — the ability to solve new tasks from
a handful of examples without weight updates. GPT-4 (2023) extended capabilities further with
multimodal understanding. The LLaMA model family by Meta provides open-weight alternatives.

Retrieval-augmented generation (RAG) combines a retrieval component (which fetches relevant
documents from a knowledge base) with a generative LLM (which synthesises an answer grounded in
those documents). RAG reduces hallucinations and allows the model to access up-to-date information
without retraining.

Key NLP evaluation benchmarks include GLUE/SuperGLUE (general language understanding), SQuAD
(extractive question answering), WMT (machine translation), CNN/DailyMail (summarisation), and
MMLU (massive multitask language understanding across 57 academic subjects).
""",
    ),
    (
        "Chapter 5 – Computer Vision",
        """
Computer vision enables machines to interpret and understand visual information from images and
videos. Core tasks include image classification, object detection, semantic segmentation, instance
segmentation, optical character recognition (OCR), image generation, and video understanding.

Image classification assigns a single label to an entire image. Deep CNNs dramatically improved
accuracy on the ImageNet Large-Scale Visual Recognition Challenge (ILSVRC); top-5 error dropped
from 26% (non-deep methods) to 15% (AlexNet, 2012) and below 4% (ResNet, 2015), surpassing human
performance (~5% measured at the time).

Object detection localises and classifies multiple objects. Two-stage detectors (e.g., Faster R-CNN)
first propose candidate regions, then classify them. Single-stage detectors (e.g., YOLO — You
Only Look Once, SSD) process the whole image in one forward pass; they trade accuracy for speed
and are preferred for real-time applications.

Semantic segmentation assigns a class label to every pixel. Models such as Fully Convolutional
Networks (FCN), U-Net (popular in medical imaging), and DeepLab achieve state-of-the-art results
using dilated convolutions and atrous spatial pyramid pooling.

Vision Transformers (ViT), introduced in 2020, apply the Transformer architecture directly to
sequences of image patches. When trained on sufficient data, ViT matches or surpasses CNNs on
classification benchmarks. Hybrid models combine CNNs' local feature extraction with Transformers'
global attention.

Multimodal models such as CLIP (Contrastive Language–Image Pretraining, OpenAI, 2021) learn
joint embeddings of text and images from web-scale paired data. CLIP enables zero-shot image
classification without task-specific fine-tuning. DALL-E 2 builds on CLIP embeddings to generate
images from text descriptions using diffusion models.
""",
    ),
    (
        "Chapter 6 – AI Ethics and Responsible AI",
        """
As AI systems become more pervasive, concerns about their ethical implications have intensified.
Key ethical challenges include bias and fairness, transparency and explainability, privacy,
accountability, safety, and the long-term societal impact of advanced AI.

Algorithmic bias arises when AI systems produce systematically unfair outcomes, often reflecting
biases present in training data or arising from flawed model design. Notable examples include
facial recognition systems with significantly higher error rates for darker-skinned women
(reported by Joy Buolamwini and Timnit Gebru, 2018) and hiring algorithms that discriminated
against women. Fairness metrics include demographic parity, equalised odds, and individual
fairness.

Explainable AI (XAI) aims to make AI decisions interpretable. Techniques include LIME (Local
Interpretable Model-agnostic Explanations), SHAP (SHapley Additive exPlanations), attention
visualisation, and saliency maps. Regulatory frameworks such as GDPR's "right to explanation"
create legal incentives for interpretable systems.

Privacy concerns include the use of personal data for training (sometimes without consent) and
the ability of models to memorise and leak sensitive training examples. Differential privacy adds
calibrated noise during training to protect individual data points. Federated learning trains
models locally on user devices, sharing only gradients rather than raw data.

AI safety research addresses the challenge of building systems that reliably pursue intended goals
without harmful side effects. Key areas include reward hacking, distributional shift, robustness
to adversarial examples, and the alignment problem — ensuring that superintelligent systems act
in accordance with human values.

Governance frameworks have proliferated: the EU AI Act (2024) establishes risk-based categories
for AI systems; the US Executive Order on AI (2023) requires safety evaluations for powerful AI
models; UNESCO adopted a Recommendation on the Ethics of AI in 2021. Industry initiatives include
Responsible AI principles published by major technology companies.
""",
    ),
    (
        "Chapter 7 – AI Applications Across Industries",
        """
AI is transforming virtually every sector of the economy.

Healthcare: AI assists radiologists in detecting cancer from imaging data, often matching
specialist accuracy. IBM Watson was an early high-profile medical AI project, though it faced
challenges translating research to clinical use. AlphaFold 2 by DeepMind (2020) predicted the
3D structures of nearly all known proteins, a breakthrough for drug discovery. Clinical NLP
tools extract structured data from unstructured clinical notes.

Finance: Fraud detection systems use anomaly detection and graph neural networks to identify
suspicious transactions in real time. Algorithmic trading employs reinforcement learning and
time-series models. Credit scoring models increasingly incorporate alternative data beyond
traditional credit history. Robo-advisors provide automated portfolio management.

Autonomous vehicles: Self-driving cars integrate computer vision, lidar point cloud processing,
sensor fusion, path planning, and RL-based decision making. Companies including Waymo, Cruise,
Tesla, and Mobileye have deployed or tested autonomous vehicles at varying levels of automation
(SAE levels 0–5). Full autonomy (level 5) across all conditions remains an open problem.

Education: Intelligent tutoring systems adapt to individual learners, identifying misconceptions
and adjusting difficulty. AI-powered essay graders and automated feedback tools support educators.
Generative AI tools such as ChatGPT are reshaping how students access information and draft work,
raising concerns about academic integrity.

Agriculture: Precision agriculture uses satellite and drone imagery analysed by computer vision
models to detect crop diseases, optimise irrigation, and guide harvesting. AI-driven weather
prediction and soil analysis improve yield forecasts.

Manufacturing: Predictive maintenance models analyse sensor data from machinery to predict
failures before they occur, reducing downtime. Quality control vision systems detect defects
on production lines at speeds and accuracy unachievable by human inspectors.
""",
    ),
]


# ---------------------------------------------------------------------------
# PDF 2 – Climate Change: Science, Impacts, and Global Response
# ---------------------------------------------------------------------------

CLIMATE_SECTIONS = [
    (
        "Chapter 1 – The Science of Climate Change",
        """
Climate change refers to long-term shifts in global temperatures and weather patterns. While
climate has always varied naturally, scientific evidence shows that human activities — primarily
the burning of fossil fuels — have become the dominant driver of rapid climate change since the
mid-20th century.

The greenhouse effect is the process by which certain gases in Earth's atmosphere trap heat.
Solar radiation passes through the atmosphere and warms the Earth's surface; the warmed surface
emits infrared radiation. Greenhouse gases (GHGs) such as carbon dioxide (CO₂), methane (CH₄),
nitrous oxide (N₂O), and water vapour absorb and re-emit this infrared radiation, warming the
lower atmosphere. Without the natural greenhouse effect, Earth's average surface temperature
would be approximately –18°C rather than the observed +15°C.

The Intergovernmental Panel on Climate Change (IPCC), established in 1988 by the UN Environment
Programme (UNEP) and the World Meteorological Organization (WMO), synthesises the scientific
consensus. Its Sixth Assessment Report (AR6, 2021–2022) concluded with "unequivocal" certainty
that human influence has warmed the atmosphere, ocean, and land. Global surface temperature
increased by approximately 1.1°C above the 1850–1900 baseline by 2011–2020.

CO₂ concentrations in the atmosphere have risen from pre-industrial levels of about 280 parts
per million (ppm) to over 420 ppm in 2023 — the highest in at least 800 000 years, as
evidenced by ice-core records from Antarctica. Methane concentrations have more than doubled
since the pre-industrial era. Major anthropogenic sources of methane include livestock digestion,
rice cultivation, landfills, and leaks from natural gas pipelines.

Climate feedbacks amplify or dampen the initial warming. The ice-albedo feedback is a positive
(amplifying) feedback: melting sea ice exposes darker ocean, which absorbs more solar radiation,
causing further warming. Water vapour feedback is the strongest positive feedback: a warmer
atmosphere holds more water vapour, which itself is a potent greenhouse gas. Cloud feedbacks
remain the largest source of uncertainty in climate projections.
""",
    ),
    (
        "Chapter 2 – Observed Impacts of Climate Change",
        """
The physical and biological impacts of climate change are already being documented across the
globe. Rising temperatures, changing precipitation patterns, and more frequent extreme weather
events are altering natural and human systems.

Temperature: The past decade (2011–2020) was the warmest on record, and each of the last four
decades has been successively warmer than any decade prior since 1850. The Arctic is warming at
more than twice the global average rate — a phenomenon known as Arctic amplification —
due to sea-ice loss and other feedbacks.

Sea level rise: Global mean sea level has risen by approximately 20 cm since 1900. The rate of
rise has accelerated, averaging 3.7 mm per year in 2006–2018 compared to 1.3 mm per year in
1901–1971. Melting of the Greenland and Antarctic ice sheets is the dominant contributor.
Under high-emission scenarios, sea levels could rise by 1 metre or more by 2100, threatening
low-lying coastal cities and island nations.

Extreme weather: Climate change increases the frequency and intensity of heatwaves, heavy
precipitation events, and droughts. Attribution science — a rapidly growing field — has shown
that human-caused warming made the 2019–2020 Australian "Black Summer" bushfires about twice
as likely, and the 2003 European heatwave approximately five times more likely.

Biodiversity: Ecosystems are being reshaped as species shift their ranges, alter migration
timing, and face mismatches with food sources. Coral reefs, which house roughly 25% of all
marine species, are threatened by ocean warming and acidification. The Great Barrier Reef
experienced mass bleaching events in 2016, 2017, 2020, 2022, and 2024.

Agriculture and food security: Changes in temperature and precipitation affect crop yields.
Studies project that wheat, rice, and maize yields could decline by 2–6% per decade under
moderate warming. Developing nations in tropical regions are disproportionately affected because
their crops are already near heat tolerance thresholds.

Human health: Heat-related mortality is increasing, particularly among the elderly. Vector-borne
diseases such as malaria and dengue fever are expanding their geographic range. Extreme weather
events cause direct casualties and displace millions of people — the Internal Displacement
Monitoring Centre recorded over 26 million new climate displacement events in 2022 alone.
""",
    ),
    (
        "Chapter 3 – The Paris Agreement and International Cooperation",
        """
The Paris Agreement, adopted in December 2015 under the United Nations Framework Convention
on Climate Change (UNFCCC), is a landmark international treaty on climate change. It was
adopted by 196 parties and entered into force on 4 November 2016.

The central aim of the Paris Agreement is to strengthen the global response to climate change
by keeping a global temperature rise this century well below 2°C above pre-industrial levels
and pursuing efforts to limit the temperature increase even further to 1.5°C. Countries submit
Nationally Determined Contributions (NDCs) — national climate action plans — every five years,
with an expectation that successive NDCs will be more ambitious (the "ratchet mechanism").

A key distinction from its predecessor, the Kyoto Protocol (1997), is that the Paris Agreement
is universal: all countries — including major emitters such as China, the US, India, and the EU —
commit to action, rather than only developed nations bearing binding targets. However, NDCs
are not legally binding; only the obligation to submit and update them is enforceable.

The climate finance goal was a major area of negotiation. Developed countries committed to
mobilise at least $100 billion per year by 2020 to support developing nations. This goal was
not met on time; revised estimates suggest it was reached in 2022. A new collective quantified
goal (NCQG) is being negotiated for the post-2025 period.

The Loss and Damage mechanism, formalised at COP27 in Sharm el-Sheikh in 2022, addresses
harm from climate change that cannot be avoided through mitigation or adaptation — a breakthrough
demand of vulnerable nations. A dedicated fund was formally established at COP28 in Dubai in 2023.

The IPCC's Special Report on Global Warming of 1.5°C (SR1.5, 2018) found that limiting warming
to 1.5°C would require reducing global net CO₂ emissions by about 45% from 2010 levels by 2030,
and reaching net zero around 2050. Current NDCs are collectively insufficient to meet even the
2°C target; independent analyses project a trajectory of 2.5–3°C under current policies.
""",
    ),
    (
        "Chapter 4 – Mitigation: Reducing Greenhouse Gas Emissions",
        """
Mitigation refers to efforts to reduce or prevent greenhouse gas emissions. Pathways consistent
with limiting warming to 1.5°C require rapid, far-reaching transitions in energy, land use,
industry, and transport.

Energy: Electricity generation is responsible for approximately 25% of global GHG emissions.
Decarbonising the power sector requires deploying renewable energy (solar, wind, hydropower,
geothermal) at scale while phasing out coal and, eventually, natural gas. The levelised cost
of electricity (LCOE) from utility-scale solar photovoltaics (PV) fell by 89% between 2010 and
2021, making solar the cheapest source of new electricity in most of the world. Wind power costs
fell by 68% over the same period.

Nuclear power produces minimal lifecycle GHG emissions and provides dispatchable baseload power.
However, high capital costs, long construction timelines, and public acceptance concerns have
limited expansion in many countries. Advanced reactor designs including small modular reactors
(SMRs) are under development.

Transport: About 16% of global emissions come from transport. Electrification of passenger
vehicles is accelerating: electric vehicle (EV) sales passed 10% of new car sales globally in
2022. Battery costs per kWh have fallen by ~97% since 1991. Aviation and shipping, responsible
for about 5% of global emissions combined, are harder to electrify; sustainable aviation fuels
(SAF) and green hydrogen are candidate solutions.

Industry: Heavy industries — steel, cement, chemicals — are responsible for approximately 22%
of emissions. Many industrial processes produce CO₂ as a chemical by-product, not just from
energy combustion, making decarbonisation technically challenging. Green hydrogen (produced by
electrolysis using renewable electricity) is a promising decarbonisation route for steelmaking.

Carbon capture, utilisation, and storage (CCUS): Technologies that capture CO₂ from industrial
point sources or directly from the air (direct air capture, DAC) and store it geologically or
convert it into useful products. Current deployment is limited; scale-up is needed for many
1.5°C scenarios.

Land use: Reducing deforestation, restoring forests, and transitioning to sustainable agriculture
can sequester substantial carbon. Forests absorb approximately 2.6 billion tonnes of CO₂ per
year. The REDD+ mechanism under the UNFCCC incentivises developing countries to reduce
deforestation.
""",
    ),
    (
        "Chapter 5 – Adaptation: Adjusting to Climate Impacts",
        """
Adaptation involves adjusting natural or human systems in response to actual or anticipated
climate change. Even under the best mitigation scenarios, some degree of warming is already
"locked in" due to the long residence time of CO₂ in the atmosphere, making adaptation necessary.

Coastal adaptation: Strategies include building seawalls, restoring mangroves and salt marshes
as natural buffers, elevating buildings, and managed retreat — planned relocation of communities
from flood-prone areas. The Netherlands has extensive experience with water management, including
its Delta Programme which plans for sea-level rise out to 2100.

Water resources: Changing precipitation patterns are increasing water scarcity in some regions
and flooding in others. Adaptation measures include improving water use efficiency, constructing
desalination plants, expanding rainwater harvesting, and restoring watershed forests.

Agriculture: Farmers are adapting by shifting planting dates, using drought-resistant crop
varieties, implementing precision irrigation, and diversifying crops and income sources. Climate-
smart agriculture integrates mitigation and adaptation co-benefits.

Urban resilience: Green roofs, urban tree canopies, and permeable surfaces reduce the urban
heat island effect and improve stormwater management. Early warning systems for extreme weather
events significantly reduce casualties.

Health systems: Strengthening public health infrastructure, improving disease surveillance,
and developing heat-health action plans protect populations from climate-related health risks.

Adaptation gap: A major challenge is that adaptation finance and action fall far short of needs.
The Global Adaptation Commission (the "Global Commission on Adaptation") estimated in 2019 that
$1.8 trillion invested in five adaptation areas between 2020–2030 could yield $7.1 trillion in
total net benefits.
""",
    ),
    (
        "Chapter 6 – Renewable Energy and the Energy Transition",
        """
The transition from fossil fuels to renewable energy sources is the cornerstone of climate
mitigation. Renewable energy includes solar, wind, hydropower, geothermal, and biomass.

Solar photovoltaics (PV) have experienced the most dramatic cost decline of any energy technology.
Global installed solar PV capacity reached 1.2 terawatts (TW) in 2022. China is the world's
largest solar market and manufacturer. Rooftop solar is enabling distributed energy generation,
and floating solar installations are emerging on reservoirs and other water bodies.

Wind power comes in onshore and offshore varieties. Offshore wind benefits from higher and more
consistent wind speeds. The world's largest offshore wind turbines in 2023 have a capacity of
over 14 MW per unit. The UK, Denmark, and China are leaders in offshore wind deployment. Wind
power supplied about 7% of global electricity in 2022.

Hydropower is the largest source of renewable electricity globally, providing about 16% of world
electricity generation. Major hydropower projects include the Three Gorges Dam in China (22.5 GW)
and the Itaipu Dam on the Brazil-Paraguay border. While hydropower is low-carbon, large dams
have significant environmental and social impacts, including displacement of communities and
disruption of river ecosystems.

Energy storage: The intermittency of solar and wind power requires storage solutions. Lithium-
ion batteries dominate grid-scale storage, and capacity is growing rapidly. Pumped hydro storage
remains the dominant long-duration storage technology. Green hydrogen, flow batteries, and
compressed air energy storage are being developed for longer-duration applications.

The International Energy Agency (IEA) in its Net Zero by 2050 scenario projects that by 2030,
global clean energy investment must reach $4 trillion per year, solar and wind must supply
about 40% of electricity, and no new fossil fuel development beyond already-approved projects
should occur.
""",
    ),
    (
        "Chapter 7 – Climate Justice and Vulnerable Communities",
        """
Climate justice emphasises that the communities least responsible for causing climate change
are often the most vulnerable to its impacts. This intersects issues of global geopolitics,
equity, and human rights.

Responsibility gap: Historically, developed nations are responsible for the majority of
accumulated CO₂ emissions. The United States and EU together account for roughly 45% of
cumulative CO₂ emissions since 1850. However, high-population emerging economies such as China,
India, and Brazil have rapidly increasing current emissions. China surpassed the US as the
world's largest annual CO₂ emitter in 2006.

Vulnerability: Small Island Developing States (SIDS) like Tuvalu, the Maldives, Kiribati, and
the Marshall Islands face existential threats from sea-level rise. The Maldives has explored
purchasing land in other countries for potential population relocation. Sub-Saharan Africa and
South Asia face the most severe agriculture and health impacts relative to GDP.

Climate migration: The World Bank estimates that internal climate migration could reach 216 million
people by 2050 without aggressive mitigation and adaptation. Hotspot regions include sub-Saharan
Africa, South Asia, and Latin America.

Indigenous peoples: Indigenous communities are disproportionately affected by climate change,
as many depend directly on climate-sensitive resources such as glacial meltwater, forest products,
and marine ecosystems. Indigenous knowledge systems offer valuable insights for adaptation,
and Indigenous-led conservation covers approximately 22% of the world's land surface.

Youth climate activism: Youth-led movements, epitomised by Greta Thunberg's Fridays for Future
campaign (launched in 2018), have amplified pressure on governments and corporations. Over 4
million people participated in the September 2019 global climate strike, making it one of the
largest climate demonstrations in history.

Loss and Damage finance: Establishing the dedicated Loss and Damage fund at COP28 (Dubai, 2023)
was a hard-won breakthrough. Initial pledges totalled approximately $700 million — widely
regarded as far short of actual needs estimated at hundreds of billions per year by 2030.
""",
    ),
]


# ---------------------------------------------------------------------------
# Helper: Build PDF
# ---------------------------------------------------------------------------

def build_pdf(output_path: Path, title: str, sections: list[tuple[str, str]]) -> None:
    """Create a PDF with the given title and sections."""
    doc = BaseDocTemplate(
        str(output_path),
        pagesize=LETTER,
        rightMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="normal",
    )

    page_template = PageTemplate(id="main", frames=[frame])
    doc.addPageTemplates([page_template])

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=22,
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading1"],
        fontSize=14,
        spaceBefore=14,
        spaceAfter=8,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )

    story = []
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.3 * inch))

    for section_title, section_body in sections:
        story.append(Paragraph(section_title, heading_style))
        # Split body into paragraphs on double newline
        for para in section_body.strip().split("\n\n"):
            clean = " ".join(para.split())
            if clean:
                story.append(Paragraph(clean, body_style))
        story.append(Spacer(1, 0.15 * inch))

    doc.build(story)
    print(
        f"  Created: {output_path} ({output_path.stat().st_size // 1024} KB)")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Creating PDFs for Week 1 · Day 3 ...")

    build_pdf(
        OUTPUT_DIR / "ai_foundations.pdf",
        "Artificial Intelligence: Foundations and Applications",
        AI_SECTIONS,
    )

    build_pdf(
        OUTPUT_DIR / "climate_change.pdf",
        "Climate Change: Science, Impacts, and Global Response",
        CLIMATE_SECTIONS,
    )

    print("Done. Both PDFs are ready in:", OUTPUT_DIR)
