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
# PDF 1 – Artificial Intelligence: Foundations and Applications (50+ pages)
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
    (
        "Chapter 8 – Transfer Learning and Fine-Tuning",
        """
Transfer learning is the practice of using knowl edge and representations learned on one task
to improve performance on another task. This approach dramatically reduces the amount of labelled
data and training time required, especially when the target task has limited data.

The intuition behind transfer learning is that low-level features (edges, textures, simple shapes)
learned on large datasets are broadly useful across different vision tasks. A CNN pretrained on
ImageNet learns hierarchical feature representations: lower layers capture simple patterns, while
higher layers learn increasingly complex features relevant to object categories.

Fine-tuning is the most common transfer learning approach. Steps include: (1) load a pretrained
model trained on a large source dataset; (2) remove the task-specific head (classification layer);
(3) add a new head for the target task; (4) train only the new head on the target dataset, or
optionally fine-tune later layers as well. Learning rates are typically much lower than for
training from scratch, preserving learned features while adapting to the new task.

Domain adaptation addresses the shift between source and target domains. Adversarial domain
adaptation uses a domain discriminator to learn domain-invariant features. Self-training and
pseudo-labelling leverage unlabelled target data: the model makes predictions on unlabelled
examples and retrains on high-confidence predictions. Mixup and CutMix augmentation techniques
interpolate between examples, improving robustness to distribution shift.

Few-shot learning aims to learn from a handful of examples. Meta-learning algorithms such as
MAML (Model-Agnostic Meta-Learning) optimise the learning process itself, enabling rapid
adaptation. Prototypical networks and matching networks learn similarity metrics; a new class
is classified based on proximity to prototype embeddings of support examples.

Zero-shot learning learns without any labeled examples of the target class. This requires semantic
information (class descriptions, attributes, or learned embeddings) and assumes the model can
generalise to unseen classes. Vision-language models like CLIP exemplify zero-shot capabilities,
predicting class labels from text descriptions without task-specific fine-tuning.
""",
    ),
    (
        "Chapter 9 – Model Optimization and Efficient Inference",
        """
As AI models grow larger, deployment becomes increasingly challenging. Model optimization
techniques reduce memory footprint, latency, and energy consumption.

Quantization reduces the precision of model weights and activations from floating-point (32-bit)
to lower precision (8-bit or 4-bit integers). Challenges include maintaining accuracy while
reducing dynamic range. Post-training quantization applied after training often causes accuracy
loss; quantization-aware training incorporates quantization during training. Mixed-precision
training uses lower precision for some operations and higher precision for others.

Pruning removes redundant weights or neurons. Magnitude-based pruning removes weights below a
threshold. Structured pruning removes entire neurons or filters, enabling hardware acceleration.
Knowledge distillation trains a smaller student model to mimic a larger teacher model's predictions.
The student learns to approximate the teacher's knowledge, often achieving 95%+ of teacher
performance with far fewer parameters.

Hardware acceleration uses specialised chips (GPUs, TPUs, ASICs) and optimised software stacks
(cuDNN, TensorRT, ONNX Runtime). Operator fusion combines multiple operations into a single
kernel. Memory layout optimisation (NHWC vs NCHW) and cache-friendly algorithms improve throughput.

Model parallelism splits models across multiple devices when they exceed a single device's memory.
Tensor parallelism partitions matrices across devices; pipeline parallelism splits layers across
devices. Distributed training synchronises gradient updates across many GPUs or TPUs.

Embedded and edge AI deploys models on mobile phones, IoT devices, and embedded systems. Challenges
include limited memory (MB to GB), no GPU, and real-time latency constraints. TensorFlow Lite,
ONNX, and Neural Engine frameworks enable on-device inference. Federated learning trains models
collaboratively while keeping data locally, addressing privacy concerns.
""",
    ),
    (
        "Chapter 10 – Data Engineering and Feature Engineering",
        """
High-quality data is foundational to model success. Data engineering prepares raw data for training;
feature engineering manually crafts or learns representations that improve model performance.

Data collection at scale requires infrastructure for storage, versioning, and quality control.
Data lakes consolidate raw data from diverse sources. Data warehousing organises structured data
for analytics. Data pipelines automate ingestion, validation, and preprocessing. Tools like Apache
Spark, Airflow, and Dataflow enable large-scale data processing.

Data cleaning addresses missing values, outliers, and inconsistencies. Imputation strategies
include mean/median fill, forward-fill for time series, or learned imputation. Outlier detection
uses statistical methods (z-score, IQR) or isolation forests. Deduplication removes redundant
records. Data validation ensures schema compliance and constraint satisfaction.

Feature engineering manually creates discriminative features. Domain knowledge is leveraged:
in NLP, features include word counts, n-grams, and linguistic properties. In time series,
features include lags, rolling statistics, and seasonal components. Automated feature engineering
discovers relevant features via genetic programming or neural networks.

Imbalanced datasets, common in fraud detection or disease diagnosis, lead to biased classifiers.
Techniques include stratified sampling, oversampling minorities (random or SMOTE), undersampling
majorities, and cost-weighted loss functions. Evaluation metrics must account for imbalance:
precision, recall, F1 score, and AUC-ROC are preferable to accuracy.

Feature scaling normalises or standardises features to similar ranges, improving optimisation
convergence. Standardisation (z-score) and min-max scaling are common. Categorical features are
encoded as one-hot vectors, ordinal numbers, or learned embeddings. Feature selection reduces
dimensionality via statistical tests (chi-square, correlation), model-based importance (permutation
importance, SHAP), or regularisation (L1 penalty).
""",
    ),
    (
        "Chapter 11 – Distributed Training and Scaling",
        """
Training large models requires distributed systems. Two main paradigms are data parallelism and
model parallelism.

Data parallelism replicates the model across multiple devices, each processing a different batch.
Gradients are synchronised afterward via AllReduce. Synchronous training waits for all devices
before updating; asynchronous training allows stragglers but risks gradient staleness and
convergence issues. Ring AllReduce and tree-based reduction are efficient communication topologies.

Model parallelism splits models across devices. Vertical parallelism assigns different layers to
different devices. Horizontal (tensor) parallelism splits matrices (e.g., split transformer
attention heads or language model embeddings across devices). Pipeline parallelism overlaps
backward passes of earlier layers with forward passes of later layers, improving utilisation.

Communication overhead is a bottleneck. Gradient compression reduces message size via quantisation
or sparsification (only communicating large gradients). Local SGD allows devices to diverge for
k steps before syncing, reducing communication frequency. Parameter servers decouple compute and
storage, enabling asynchronous updates.

Distributed optimization algorithms adapt to asynchronous settings. Delayed gradient descent
accounts for stale gradients. Federated averaging (FedAvg) updates a central model from local
models trained independently. Byzantine-robust aggregation handles faulty or adversarial devices.

Frameworks including PyTorch Distributed, TensorFlow Distributed, and Horovod abstract parallelism,
allowing users to write single-device code that automatically scales. JAX enables functional
transformations like vmap (vectorisation) and pmap (parallel mapping).

Scaling laws quantify how performance improves with model size, data size, and compute. Chinchilla
scaling suggests optimal allocation: compute should be distributed roughly equally between model
parameters and training tokens. Larger models with more data consistently outperform smaller models
with less data, assuming sufficient compute budget.
""",
    ),
    (
        "Chapter 12 – Testing, Validation, and Robustness",
        """
AI systems must be rigorously tested before deployment. Beyond traditional accuracy metrics,
robustness to distribution shift and adversarial perturbations is critical.

Benchmark datasets enable standardised evaluation. Common vision benchmarks include ImageNet,
CIFAR-10, and Pascal VOC. NLP benchmarks include GLUE, SuperGLUE, and SQuAD. Time series benchmarks
include UCR Archive. Leaderboards incentivise progress but raise concerns about overfitting to
benchmarks; strong performance on benchmarks does not guarantee real-world robustness.

Evaluation metrics must align with goals. For classification, accuracy is insufficient if classes
are imbalanced; precision, recall, and F1 score are more informative. For ranking, NDCG and MAP
measure ranking quality. For segmentation, Jaccard index and Dice coefficient assess overlap.
For generative models, BLEU, ROUGE, and METEOR assess quality; FID and Inception score assess
realism.

Adversarial examples are inputs crafted to fool classifiers. Rotations, translations, and
brightness shifts test invariance. Adversarial perturbations—small, imperceptible noise—can flip
predictions. FGSM (Fast Gradient Sign Method) and PGD (Projected Gradient Descent) are standard
attack methods. Certified defences (randomised smoothing, IBP) provide provable robustness bounds,
though at accuracy cost.

Distribution shift occurs when test data differs from training. Covariate shift changes input
distribution. Label shift changes class frequencies. Concept drift is when the mapping from input
to output fundamentally changes (e.g., spam definitions evolving). Strategies include importance
weighting, domain adversarial training, and continual learning.

Interpretability and explainability help practitioners understand model decisions. Linear models
and decision trees are inherently interpretable. Complex models need post-hoc explanations: LIME
approximates local models around an instance; SHAP computes shapley values attributing each
feature's contribution; attention saliency maps highlight important input regions.

Model auditing and bias detection identify discrimination. Red-teaming involves finding
adversarial inputs and edge cases. Fairness audits check for disparities across demographic groups.
Fairness-accuracy tradeoffs require balancing performance with equitable treatment.
""",
    ),
    (
        "Chapter 13 – Large Language Models and In-Context Learning",
        """
Large language models (LLMs) have emerged as dominant AI systems, demonstrating remarkable
capabilities across language understanding and generation tasks.

LLMs are Transformer-based models pretrained on vast text corpora using next-token prediction.
Scaling up model size (parameters), data size (tokens), and compute enables emergent capabilities—
abilities absent in smaller models. GPT-3 (175B parameters) showed in-context learning: adapting
to new tasks from a handful of examples without gradient updates, purely from prompt context.

In-context learning is a form of implicit meta-learning. The prompt provides context (examples,
instructions, or demonstrations) that the model uses to infer the task. Few-shot prompting provides
examples; zero-shot prompting provides instructions. Chain-of-thought prompting breaks complex tasks
into intermediate steps, improving reasoning. Instruction fine-tuning (RLHF—Reinforcement Learning
from Human Feedback) aligns models with human preferences, reducing harmful outputs and improving
helpfulness.

Prompt engineering optimises the natural language instructions sent to LLMs. Temperature and top-p
sampling control output randomness. Top-k sampling limits the vocabulary to the k most likely
tokens. Repetition penalties discourage repeated phrases. Prompt templates structure inputs for
downstream tasks (classification, summarisation, translation).

Grounding and retrieval-augmented generation (RAG) address hallucination. Dense retrieval (e.g.,
DPR—Dense Passage Retrieval) fetches relevant documents from a knowledge base via learned
embeddings. Sparse retrieval (BM25) uses term frequency. Reranking ensures retrieved passages
are relevant. The LLM then generates answers grounded in retrieved context.

LLM limitations include hallucination (confident false claims), brittleness to prompt variations,
biases inherited from training data, and computational expense. Mitigations include RLHF fine-tuning,
constitutional AI (CAI) providing explicit principles, continuous monitoring, and safety
testing. Ongoing research aims for more truthful, aligned, and efficient LLMs.
""",
    ),
    (
        "Chapter 14 – Multimodal Learning and Vision-Language Models",
        """
Modern AI increasingly processes multiple modalities—images, text, audio, and video—jointly.
Multimodal learning leverages cross-modal signals for richer understanding.

Vision-language pretraining learns joint representations of images and text. CLIP (Contrastive
Language-Image Pretraining) trains encoders for both modalities, learning to align images with
their descriptions via contrastive loss. ViLBERT fuses visual and textual information via
transformer layers. ALBEF (Align Before Fusion) aligns modalities before fusion, improving
robustness.

Vision-language models enable zero-shot classification and retrieval. Given a test image and
candidate labels, CLIP computes similarities between the image embedding and text embeddings of
each label, enabling classification without fine-tuning. Cross-modal retrieval retrieves images
matching text queries or vice versa.

Image captioning generates textual descriptions of images. Encoder-decoder architectures use a
CNN (or ViT) encoder to extract image features and a Transformer decoder to generate captions
autoregressively, conditioned on image features. Training requires paired image-caption datasets;
evaluation uses BLEU, CIDEr, and METEOR metrics.

Visual question answering (VQA) answers natural language questions about images. Models encode
both image and question, combine representations, and decode answers. VQA requires reasoning
over visual content and language understanding. Attention mechanisms highlight which image
regions are relevant to each question word.

Multimodal generation produces images from text (DALL-E, Stable Diffusion), video from text,
audio from text (text-to-speech), and cross-modal synthesis. Diffusion models for text-to-image
generation iteratively refine noise into images, conditioned on text embeddings.

Multimodal fusion strategies include early fusion (combine raw modalities), late fusion (combine
learned representations), and hybrid approaches. Co-training uses one modality to regularise
another. Knowledge distillation transfers knowledge from one modality to another.
""",
    ),
    (
        "Chapter 15 – AI for Scientific Discovery",
        """
AI increasingly accelerates scientific research, from materials discovery to drug development
to fundamental physics.

Protein structure prediction: AlphaFold 2 (DeepMind, 2020) predicted the 3D structures of nearly
all known proteins using a deep learning architecture combining evolutionary and co-evolutionary
information. This solved the protein folding problem—a longstanding challenge—and has enabled
drug design and understanding of disease mechanisms. AlphaFold3 extended prediction to complexes
and non-protein molecules.

Drug discovery involves identifying compounds that bind to disease-related proteins. Molecular
generation uses graph neural networks (GNNs) and autoregressive models to generate novel molecules.
Molecular property prediction uses GNNs to predict drug-like properties (solubility, toxicity,
binding affinity). Virtual screening ranks molecules by predicted binding; promising candidates
undergo experimental validation.

Materials science benefits from ML-accelerated discovery. Crystal structure prediction, band gap
prediction, and stability assessment guide synthesis. Inverse design searches for materials with
target properties. Data-driven models trained on computed or experimental databases enable rapid
property predictions, reducing the need for expensive experiments.

High-energy physics uses deep learning for particle detector data analysis. CNNs and RNNs process
detector events to identify rare interactions. Generative models simulate detector response,
reducing computational expense compared to traditional Monte Carlo simulations.

Computational biology applies NLP and sequence models to genomics. Transformer-based models
(e.g., DNABERT, ESM) learn representations from protein and DNA sequences, enabling variant-effect
prediction, protein-protein interaction prediction, and functional annotation. These models are
particularly useful for large-scale genomic studies.

Scientific machine learning combines domain knowledge with learning. Physics-informed neural
networks (PINNs) encode differential equations as loss terms, ensuring learned models satisfy
physical laws. Neural operators (DeepONet, FNO) learn infinite-dimensional mappings (e.g.,
solving PDEs) more expensively than neural networks but much faster than classical solvers.
""",
    ),
    (
        "Chapter 16 – AI Safety and Alignment",
        """
As AI systems become more powerful and influential, ensuring they operate safely and align with
human values is critical.

The alignment problem asks: how can we ensure advanced AI systems reliably pursue intended goals?
A system might optimise the specified objective perfectly but in unintended ways (reward hacking).
A robot instructed to "make people smile" might paralyse faces. These aren't bugs but failures to
capture true human preferences.

Value learning aims to infer human preferences from observa tions (behaviour, rankings, explanations).
Inverse reinforcement learning (IRL) infers a reward function from expert demonstrations. Learning
from human feedback (LFHF) and RLHF use human-provided rankings to train preference models, which
then guide policy optimisation.

Robustness to distribution shift is crucial. A system trained on a particular distribution may
fail catastrophically on slightly different inputs. Worst-case robustness searches for adversarial
examples the model fails on. Distributional robustness optimises the worst-case loss over plausible
distributions. Certified defences provide provable guarantees.

Interpretability helps engineers understand and debug systems. Mechanistic interpretability aims
to understand learned circuits. Feature importance and saliency methods highlight what inputs
matter. Attention visualisation reveals which tokens a model attends to. Post-hoc explanations
approximate complex model decisions.

Containment and specification limits damage from misbehaving systems. Sandboxing restricts system
access to critical resources. Approval requirements involve humans in high-stakes decisions.
Reversibility enables turning off systems. Verifiable outcomes (where correctness can be checked)
are preferable to approval-based outcomes.

Long-term AI safety research addresses existential risks from advanced AI. Cooperation and
deception research explores how to ensure systems cooperate with humans rather than deceive them.
Goal misgeneralisation studies how learned objectives generalise beyond training distribution.
Power-seeking research explains why advanced systems might acquire power-seeking subgoals.
""",
    ),
    (
        "Chapter 17 – Reinforcement Learning and Control",
        """
Reinforcement learning (RL) enables agents to learn through trial and error, adapting to new
environments without explicit programming.

Markov Decision Processes (MDPs) formalise RL. An agent observes state s, takes action a, receives
reward r, and transitions to next state s'. The objective is to maximise cumulative reward. MDPs
assume the Markov property: the future depends only on the current state, not history.

Q-learning learns the value of state-action pairs offline. The Q-function Q(s, a) estimates
expected cumulative reward from state s after taking action a. Q-values are updated using the
Bellman equation: Q(s, a) ← Q(s, a) + α(r + γ max_a' Q(s', a') - Q(s, a)). Convergence is
guaranteed for tabular problems with sufficient exploration.

Deep Q-Networks (DQN) use neural networks to approximate Q-values, enabling learning in
high-dimensional state spaces. Experience replay stores past transitions and samples minibatches
for training, breaking temporal correlations and improving stability. Target networks decouple
the Q-network used for updates from the network generating targets, reducing divergence.

Policy gradient methods directly optimise the policy. REINFORCE samples trajectories and updates
the policy in the direction of high-value returns. Actor-critic methods combine a policy network
(actor) and value network (critic), using the critic's prediction to reduce variance. PPO (Proximal
Policy Optimisation) clips probability ratios to stabilise training. A3C (Asynchronous Advantage
Actor-Critic) enables distributed training.

Model-based RL learns a model of environment dynamics (e.g., a neural network predicting next states).
Planning algorithms use the learned model to search for good action sequences. Imagination-based
methods plan in a learned latent space. Dyna algorithms interleave learning and planning.

RL applications include game playing (AlphaGo, AlphaStar), robotics (manipulation, navigation),
autonomous systems, recommendation systems, and energy management. Challenges include sample
efficiency (learning from limited interactions), exploration-exploitation tradeoff, and credit
assignment in long-horizon tasks.
""",
    ),
    (
        "Chapter 18 – Robotics and Autonomous Systems",
        """
Robotics combines mechanical engineering, control theory, and AI. Modern robots use machine learning
to perceive environments, plan actions, and adapt to unfamiliar scenarios.

Perception in robotics involves sensor fusion combining camera, lidar, radar, and IMU data. Computer
vision processes images for object detection, semantic segmentation, and depth estimation. Lidar
provides precise 3D point clouds. Traditional approaches use handcrafted features; modern systems
use CNNs and 3D convolutions for end-to-end learning.

Manipulation tasks require grasping and placing objects. Grasp planning predicts good contact points
on objects. Reinforcement learning trains policies for manipulation, though sample efficiency remains
a challenge. Sim-to-real transfer trains in simulation (faster, unlimited data) then deploys on real
robots. Domain randomisation (varying simulation parameters) improves transfer.

Autonomous vehicles integrate perception, planning, and control. Object detection identifies
pedestrians, vehicles, and obstacles. Trajectory prediction forecasts the motion of dynamic agents.
Path planning finds collision-free routes; SLAM (Simultaneous Localisation and Mapping) builds
maps while localising. End-to-end learning trains neural networks to map sensor observations
directly to steering commands, though interpretability and safety verification remain challenges.

Mobile robot navigation involves localisation and path planning. Monte Carlo localisation tracks
the robot's position given sensor observations. A* and RRT* plan optimal paths avoiding obstacles.
Simultaneous localisation and mapping (SLAM) is crucial for exploration in unknown environments.

Robot learning from demonstration (imitation learning) learns from human examples. Behavioural cloning
directly maps observations to actions. Inverse reinforcement learning infers the underlying reward
function. Meta-learning enables rapid adaptation to new tasks from a few demonstrations.

Safety is paramount in robotics. Formal verification proves correctness for critical systems. Robust
control handles model uncertainty. Real-time constraints ensure timely decision-making. Collaborative
robots (cobots) work safely around humans via compliance and force-limiting.
""",
    ),
    (
        "Chapter 19 – Graph Neural Networks",
        """
Many real-world data exhibit structure beyond sequences or grids: social networks, molecules, 
knowledge bases, and citation networks. Graph neural networks (GNNs) process tabular data where 
relationships between entities are as important as attributes.

Graphs consist of nodes (entities) and edges (relationships). Node features might include attributes;
edge features capture relationship properties. GNNs produce node embeddings that incorporate
neighbourhood information via message passing: each node's embedding is refined by aggregating
messages from neighbours.

Graph convolutional networks (GCNs) are a foundational GNN architecture. The update rule is:
h_v^{(k+1)} = W^{(k)} h_v^{(k)} + ∑_{u ∈ N(v)} h_u^{(k)}, where h_v is the node embedding,
W^{(k)} is a learnable weight matrix, and N(v) is the neighbourhood. Stacking layers enables
far-reaching information propagation: a k-layer GNN incorporates information from k-hop neighbours.

Graph attention networks (GATs) use multi-head attention to weight neighbour contributions. More
important neighbours receive higher attention weights. This is more flexible than uniform aggregation.

GraphSAGE introduces sampling and aggregating: rather than aggregating over all neighbours (which
is expensive for large graphs), it samples a fixed number of neighbours. This enables minibatch
training and scalability to billion-node graphs.

GNN applications include: node classification (labelling nodes e.g., document categorisation),
link prediction (predicting missing edges e.g., friend recommendations), and graph classification
(labelling entire graphs e.g., molecular property prediction). Molecular GNNs have accelerated drug
discovery: atoms are nodes, bonds are edges; properties are predicted end-to-end.

Challenges include handling directed/heterogeneous graphs, scaling to billions of nodes, and
integrating structural and temporal information. Recent advances include heterogeneous GNNs for
multi-type entities, temporal GNNs for evolving graphs, and graph pooling for whole-graph
representations.
""",
    ),
    (
        "Chapter 20 – Time Series Forecasting and Anomaly Detection",
        """
Time series data is ubiquitous: stock prices, weather, energy consumption, sensor readings. Predicting
future values and detecting anomalies enable proactive decision-making.

Temporal structure in time series demands special care. Autoregressive (AR) models predict future
values as functions of past values. ARIMA (Autoregressive Integrated Moving Average) is a classical
method. Exponential smoothing and Holt-Winters handle trends and seasonality.

Neural networks capture complex temporal dependencies. RNNs and LSTMs process sequences, overcoming
gradient vanishing. Gated Recurrent Units (GRUs) simplify LSTMs with fewer parameters. Attention
mechanisms—especially in Transformer architectures—enable efficient long-range dependencies without
RNN recurrence.

Transformer-based models like Temporal Fusion Transformers (TFT) and Transformers with learnable
embeddings model temporal patterns. Dilated convolutions (Temporal Convolutional Networks) process
long sequences efficiently. N-BEATS is a pure attention-free architecture achieving state-of-the-art
results.

Seasonality and trends require decomposition. Classical methods like seasonal decomposition separate
trend and seasonal components. Neural approaches learn these implicitly. Multiple-step ahead forecasting
(predicting multiple future timesteps) requires care: recursive prediction (feeding predictions back)
accumulates error; direct methods train separate heads for each horizon.

Anomaly detection identifies unusual patterns. Rule-based thresholds flag values exceeding statistical
bounds. Isolation forests are efficient unsupervised learners. Autoencoders reconstruct normal
patterns; anomalies show larger reconstruction error. GRU-based methods learn temporal patterns;
anomalies deviate from learned dynamics.

Online learning handles streaming data where new data continuously arrives. Online anomaly detection
updates models incrementally. Concept drift (when patterns change) requires adaptive models.

Applications include: financial forecasting (stock prices, volatility), energy (demand prediction,
grid stability), infrastructure (equipment failure prediction), and security (intrusion detection).
""",
    ),
    (
        "Chapter 21 – Recommendation Systems",
        """
E-commerce, streaming, and social media platforms rely on recommendation systems to personalise
user experience, increase engagement, and drive revenue.

Collaborative filtering predicts user preferences from "wisdom of the crowd." User-based CF finds
similar users and recommends items they liked. Item-based CF finds similar items to ones the user
has liked. Matrix factorisation decomposes the user-item interaction matrix into low-rank user and
item embeddings: r_ui ≈ u_u^T v_i. Singular Value Decomposition (SVD) and non-negative matrix
factorisation are classical approaches.

Content-based filtering recommends items similar to those the user previously liked, based on
item features (genre, director, keywords). Hybrid systems combine collaborative and content-based
approaches.

Neural collaborative filtering uses deep neural networks to learn embeddings. Wide & Deep networks
combine memorisation (learning specific user-item pairs) with generalisation (learning patterns).
Matrix factorisation can be viewed as a shallow neural network. Deeper architectures learn
non-linear interactions between user and item embeddings.

Sequential recommendation models temporal dynamics. RNNs and Transformers process user interaction
sequences, predicting the next item. Attention mechanisms highlight which past items are important
for the next prediction.

Context-aware systems incorporate contextual information: time of day, location, device type.
Knowledge-aware systems leverage knowledge graphs, incorporating side information about items and
relationships.

Implicit feedback (clicks, purchases, dwell time) is more abundant than explicit ratings but noisier.
Ranking loss (BPR—Bayesian Personalized Ranking) assumes clicked items are preferred to unclicked
ones. Point-wise loss (predicting rating value) differs from pairwise loss (relative ranking).

Cold-start problems arise for new users and items with minimal history. Solutions include feature-based
initialisation, meta-learning, and hybrid filtering. Diversity and novelty encourage exploring beyond
items similar to past preferences. Exploration-exploitation tradeoffs balance popularity (safe) with
discovery (engaging).

Major platforms use ensembles: candidate generation retrieves promising items, ranking refines scores,
then diverse results are presented to balance relevance and discovery.
""",
    ),
    (
        "Chapter 22 – Causal Inference and Causal Learning",
        """
Machine learning typically learns correlations: patterns in data. Causal inference asks what happens
when we intervene: if we change X, how does Y respond? This is crucial for policy decisions, drug
trials, and marketing campaigns. Correlation is not causation.

Causal models encode assumptions as directed acyclic graphs (DAGs). Nodes are variables, edges represent
causal relationships. Confounder variables influence both treatment and outcome, creating spurious
correlation. A confounder must be adjusted for to estimate true causal effects.

Randomised controlled trials (RCTs) are the gold standard: randomly assigning subjects to treatment
and control isolates causal effects. But RCTs are expensive, slow, and unethical in some cases.
Observational studies use existing data but must account for confounding.

Causal identification asks whether causal effects can be determined from observed data. The
back-door criterion (blocking all non-causal paths) identifies the causal effect of treatment on
outcome. The front-door criterion handles cases with unobserved confounders.

Propensity score matching estimates treatment effects in observational data. The propensity score—
the probability of treatment given covariates—is estimated. Matching treated and untreated units
with similar propensity scores balances covariate distributions, approximating RCT balance.

Causal forests grow random forests where each tree estimates heterogeneous treatment effects: the
same treatment may benefit some subgroups more than others. Trees split on covariates to isolate
homogeneous subgroups with consistent treatment effects. This enables personalised interventions.

Instrumental variables address unmeasured confounding. An instrument is uncorrelated with confounders,
affects treatment, and affects outcome only through treatment. IV regression estimates local average
treatment effects (LATE) on compliers.

Causal discovery learns the causal graph from data, assuming no unmeasured confounding. Constraint-based
methods (PC, FCI) exploit conditional independence relationships. Score-based methods search for
high-scoring graphs. These assume acyclicity and no selection bias—strong assumptions often violated
in practice.

Applications include: personalisedmedicine (treatment effect heterogeneity), economics (impact evaluation),
and policy (effectiveness of interventions).
""",
    ),
    (
        "Chapter 23 – Meta-Learning (Learning to Learn)",
        """
Meta-learning or "learning to learn" aims to enable models to quickly adapt to new tasks. Classical
ML requires substantial task-specific data; meta-learning achieves good performance from few examples.

Few-shot learning is applied meta-learning: perform well on a new task from a handful of labelled
examples. This contrasts with classical deep learning's appetite for thousands of labelled examples.
Meta-learning algorithms train on a distribution of tasks, learning an inductive bias that transfers.

Model-Agnostic Meta-Learning (MAML) trains for fast adaptation. The meta-objective is to minimise
loss on a new task after one (or few) gradient steps. MAML performs inner-loop gradient updates on
each task, then outer-loop updates on the meta-objective. After meta-training, new tasks require
minimal gradient steps.

Prototypical networks learn a metric space where examples of the same class are close and different
classes are far. During meta-learning, support examples (labelled examples of each class) are projected
to prototypes (class centroids). Query examples are classified by proximity to prototypes. No gradient
updates on test tasks—only distance computation.

Matching networks and relation networks learn similarity metrics. Matching networks combine attention
and memory for few-shot classification. Relation networks learn pairwise similarity between examples.

Task distributions crucially affect meta-learning. Diverse task distributions enable learning broadly
applicable inductive biases. Task labels (e.g., "this is a novel class classification task") provide
useful information. Domain-specific task distributions may learn biases inapplicable across domains.

Meta-learning extends beyond classification. Meta-reinforcement learning learns policies adaptable
to new RL tasks quickly. Neural architecture search (NAS) meta-learns good architectures for new
datasets.

Optimisation-based meta-learning (MAML, FOMAML) learns a good initialisation. Metric-based meta-learning
(prototypical networks, matching networks) learns similarity metrics. Memory-augmented approaches use
external memory for few-shot learning.

Challenges include computational cost (many gradient steps during training), task distribution design,
and mismatch between meta-training and deployment tasks. Despite progress on benchmarks, real-world
few-shot learning remains challenging.
""",
    ),
    (
        "Chapter 24 – Continual Learning and Catastrophic Forgetting",
        """
Most ML systems learn from fixed datasets. Real-world scenarios involve streams of data where new tasks
continually arrive. Learning new tasks risks forgetting old ones—catastrophic forgetting.

Catastrophic forgetting occurs when training on new data substantially degrades performance on previous
tasks. When neural networks are trained on task B after task A, weights are updated to optimise task B,
moving away from the task A optimum. This is a fundamental challenge in continual learning.

Rehearsal (experience replay) mitigates forgetting by replaying samples from previous tasks during learning.
Elastic weight consolidation (EWC) identifies task-important weights (using Fisher information) and
constrains their changes during new-task training. Progressive neural networks add new columns for new
tasks, preventing overwriting of learned features.

Plasticity-stability tradeoff is central: plasticity enables learning new information; stability preserves
old knowledge. Rehearsal and consolidation approach this differently. Rehearsal maintains plasticity but
requires memory. Consolidation protects stability but may reduce plasticity for truly new concepts.

Dynamic architectures grow networks for new tasks. Progressive neural networks, PackNet, and adapter
modules add capacity for new tasks without modifying existing weights. This addresses stability but
increases model size.

Task boundaries and offline learning enable stronger solutions. With explicit task boundaries, features
can be frozen (stability) or replayed (rehearsal). Offline continual learning—where future tasks are
known but not yet arrived—enables replay and consolidation strategies.

Domain incremental learning sees a continuum of data from related domains. Class incremental learning
introduces new classes over time. Domain incremental is typically easier (features transfer across
domains) than class incremental (new classes may introduce new feature spaces).

Continual learning metrics assess forgetting, backward transfer (new learning improving old tasks), and
forward transfer (old learning aiding new tasks). Current benchmarks (Split-CIFAR, Split-ImageNet) are
relatively simple; realistic continual learning remains open.

Open questions: How can systems learn unlimited tasks? How do we detect when to consolidate versus
plastify? Can we achieve human-like continual learning, where extensive knowledge coexists without
catastrophic forgetting?

Applications: robotics (new skills without forgetting old ones), autonomous systems (adapting to new
environments), and lifelong learning.
""",
    ),
    (
        "Chapter 25 – Knowledge Graphs and Semantic Web",
        """
Knowledge graphs (KGs) represent entities and relationships in structured form. DBpedia, Wikidata, and
Freebase contain billions of facts: (subject, predicate, object) triples. Knowledge graphs enable
reasoning, entity resolution, and improved search and recommendations.

Link prediction fills missing relationships. Graph embeddings map entities and relations to vector space;
similarity indicates existence of relationships. TransE embeds entities and relations such that
h + r ≈ t (head + relation ≈ tail). Variants (TransH, TransR, DistMult) handle complex relationships.

Knowledge graph completion identifies missing triples. RotatE models relations as rotations in complex
space. ConvKB uses convolutional networks. Graph neural networks aggregate neighbourhood information,
learning rich representations.

Entity linking maps mention strings to entities in KGs. "New York" links to the entity representing
the city. Disambiguation handles ambiguous mentions. BERT-based methods achieve high accuracy. Coreference
resolution groups mentions referring to the same entity.

Named entity recognition (NER) identifies entity mentions in text. Classical approaches use sequence
labelling (BIO tags). LSTM-CRF combines RNNs and conditional random fields. Transformer-based models
(BERT-NER, SpanBERT) achieve state-of-the-art.

Relation extraction identifies relationships mentioned in text. Pattern-based approaches use handcrafted
rules. Supervised distant supervision leverages KGs to automatically label training data. Unsupervised
relation extraction discovers novel relations. Self-attention in Transformers highlights important input
spans and relations.

Knowledge graph reasoning deduces implicit facts from explicit ones. Rule-based reasoning applies rules
(if A→B and B→C then A→C). Embedding-based reasoning leverages learned KG embeddings. Neural-symbolic
approaches combine logical rules with neural learning.

Semantic web standards (RDF, OWL) enable interoperable KGs. Linked open data connects KGs across
organisations. SPARQL query language retrieves facts and reasons over KGs.

Applications: search (Google's Knowledge Graph), Q&A systems (retrieving facts for answers), recommendation
(discovering related entities), and scientific discovery (identifying research relationships).
""",
    ),
    (
        "Chapter 26 – Neural Architecture Search (NAS)",
        """
Designing neural network architectures is an art combining intuition and experimentation. Neural architecture
search (NAS) automates this, treating architecture design as an optimisation problem.

Topology search finds the connectivity between layers. Should two layers skip-connect? Which operations
(convolution, pooling) are present? Search spaces encode candidate architectures. Exponential search
spaces make brute-force enumeration infeasible.

Architecture properties matter: width (number of channels), depth (number of layers), skip connections
(residual links), and operations. The optimal architecture depends on dataset, hardware, and constraints
(latency, memory). ImageNet-optimised architectures may underperform on medical imaging.

Reinforcement learning approaches use an RNN controller to encode architectures. The controller is
trained with policy gradient using validation accuracy as reward. This enables joint learning of the
architecture and weights. Computational cost is high (1000s of GPU days) but can be amortised across
many tasks.

Evolutionary algorithms (genetic algorithms, evolutionary strategies) evolve populations of architectures.
Crossover and mutation generate offspring. Better-performing architectures are selected. Parallel
evaluation accelerates search. These are embarrassingly parallelisable.

Differentiable NAS (DARTS) relaxes discrete architecture search to continuous, enabling gradient-based
optimisation. Categorical choices become learnable mixed probability distributions. This reduces search
time from days to hours. DARTS variants (progressive shrinking, warmup) improve stability.

Efficient NAS addresses computational burden. Weight sharing (training a supernet containing all candidates)
enables quick validation accuracy estimation. Early stopping stops unpromising architectures. Zero-cost
proxies estimate architecture quality without training.

Hardware-aware NAS optimises for latency, energy, or memory constraints. Latency predictors estimate
deployment cost. Multi-objective NAS balances accuracy and efficiency. Pareto frontiers show
accuracy-efficiency tradeoffs.

Transfer NAS leverages architecture priors. Warm-starting NAS with known-good initialisation accelerates
search. Architecture analysis identifies what makes good architectures (patterns, modules) transferable
across datasets.

Applications: automating model design across domains, adapting architectures to hardware constraints,
and discovering novel operations (e.g., Swish activation, discovered via NAS).
""",
    ),
    (
        "Chapter 27 – Generative Adversarial Networks (GANs)",
        """
GANs pit two networks against each other: a generator produces fake samples; a discriminator
distinguishes real from fake. Training is a two-player game where both networks improve iteratively.

The generator learns to map random noise z to realistic data samples. The discriminator learns to classify
real vs generated samples. Nash equilibrium is reached when the discriminator cannot distinguish real from
fake (50% accuracy), and the generator produces realistic samples.

Training dynamics are tricky. Vanishing gradients: if the discriminator is too good, the generator's
gradient becomes very small, slowing learning. Mode collapse: the generator produces a limited variety of
samples instead of full data diversity. Non-convergence: training oscillates without reaching equilibrium.

DCGAN introduced convolutional architectures winning stability and quality. Batch normalisation in both
networks, strided convolutions instead of pooling, and leaky ReLU activations improved training.

WGAN (Wasserstein GAN) uses Wasserstein distance (optimal transport) instead of JS divergence. This provides
meaningful gradients even far from equilibrium. Gradient penalty enforces the Lipschitz constraint. Training
becomes more stable and mode collapse less severe.

Progressive GANs grow networks during training: start with low resolution, gradually add layers for higher
resolution. This stabilises training and produces high-quality high-resolution images.

Conditional GANs (CGAN) add class labels, enabling class-conditional generation. Diffusion models and score-based
models, though not strictly GANs, are now dominant for image generation due to superior stability and quality.

StyleGAN introduces learnable style mixing, enabling fine-grained control over generation. Style is injected
at multiple layers, allowing separate control of high and low-level details. Disentangled representations
enable intuitive editing.

GAN applications: image generation (faces, landscapes, objects), style transfer, image-to-image translation
(pix2pix, CycleGAN), domain adaptation, and data augmentation. GANs excel at generating realistic images
but struggle with other modalities (some success with audio, limited success with text).

Challenges: training instability, mode collapse, convergence assessment, and evaluation metrics. Inception
Score and Fréchet Inception Distance (FID) assess sample quality and diversity.
""",
    ),
    (
        "Chapter 28 – Variational Autoencoders (VAEs)",
        """
Variational autoencoders combine autoencoders (unsupervised representation learning) with probabilistic
modeling. The encoder compresses data to latent codes; the decoder reconstructs data from codes. The
latent space is a probability distribution enabling generation of new samples.

Autoencoders learn low-dimensional representations of data. An encoder maps inputs to latent codes z;
a decoder reconstructs inputs from codes. Training minimises reconstruction loss. The bottleneck (small
latent dimension) forces the encoder to capture essential information. Autoencoders discover structure
without labels.

VAEs add probabilistic structure. The encoder outputs parameters of a posterior distribution q(z|x),
not point estimates. Sampling latent codes introduces stochasticity. The decoder models the reconstruction
distribution p(x|z). The objective combines reconstruction loss (decoder quality) and KL divergence
(encoder closeness to prior).

The evidence lower bound (ELBO) decomposes into reconstruction and KL terms. Minimising KL pushes the
posterior toward the prior N(0, I), encouraging smooth latent space. The reparameterisation trick enables
backpropagation through sampling: z = μ + σ ⊙ ε, where ε ~ N(0, I).

A smooth latent space enables generation: sampling from the prior z ~ N(0, I) and decoding produces
realistic samples. Interpolation between codes produces smooth transitions. VAEs thus enable both
compression and generation.

β-VAE increases the KL weight β > 1. Stronger KL regularisation encourages disentanglement: latent
factors become interpretable, each capturing a distinct data property (colour, size, rotation).

Hierarchical VAEs use multiple stacked latent layers. Ladder variational autoencoders have skip connections
improving posterior accuracy. Sequential VAEs model temporal structure in videos.

Drawbacks: reconstructions are often blurry (probabilistic reconstruction with finite capacity). VAE
likelihoods are oft difficult to estimate. Despite this, VAEs remain valuable for interpretable,
disentangled representation learning.

Applications: representation learning, data compression, anomaly detection, and controlled generation
(by manipulating latent codes). VAEs excel where interpretability matters; diffusion models surpass VAEs
in generation quality.
""",
    ),
    (
        "Chapter 29 – Diffusion Models for Generative Modeling",
        """
Diffusion models add noise to images step-by-step, then learn to reverse this process. Beginning from
pure noise, the model gradually denoises to produce realistic images. Diffusion models now dominate
generative modeling, outperforming GANs and VAEs in quality and stability.

Forward process (diffusion): Images are gradually corrupted by adding small amounts of Gaussian noise
over T steps. x_t = √(ᾱ_t) x_0 + √(1 - ᾱ_t) ε, where ᾱ_t is a schedule of noise levels, ε ~ N(0, I).
After many steps, x_T is nearly pure noise.

Reverse process (denoising): The model learns to reverse diffusion, predicting the added noise at each
step. Training minimises the difference between predicted and actual noise: ||ε - ε_θ(x_t, t)||².
This is simpler than image reconstruction and enables better gradient flow.

Inference: Start with x_T ~ N(0, I), iteratively denoise for T steps, producing x_0. This is slow
compared to GANs and VAEs (100s-1000s of steps) but more stable.

DDPM (Denoising Diffusion Probabilistic Models) introduced the framework. Variance schedules control
noise progression. Predetermined schedules (linear, square root) or learnable schedules optimise training.

Stable Diffusion and DALL-E 2 dominate text-to-image generation. They condition on text embeddings
(CLIP), enabling text-to-image synthesis. Classifier-free guidance enables high-quality generation
without training separate classifiers.

Score-based models learn gradients of log probability rather than adding noise directly. Score matching
trains the model to match data score. Stochastic differential equations (SDEs) generalise diffusion and
score matching. These offer cleaner mathematics and connect to existing theory.

Sampling speed is addressed via fast samplers (DDIM, DPM-Solver) and distillation. Distillation
compresses 1000 steps into 10-20 steps with minimal quality loss. Latent diffusion (diffusing in
learned latent space rather than pixel space) accelerates training and sampling.

Advantages: Stable training (no adversarial dynamics), high-quality generation, flexible conditioning
(class, text, images), and strong theoretical foundation.

Disadvantages: Slow sampling, high training cost, and sequential sampling incompatible with parallelisation.

Applications: image generation, image editing, video generation, audio generation, and 3D shape synthesis.
""",
    ),
    (
        "Chapter 30 – Multi-task Learning",
        """
Multi-task learning trains a single model on multiple related tasks simultaneously. Shared representations
improve generalisation, especially when individual tasks have limited data. Task diversity provides a
regularisation effect: features useful for one task may hurt another, preventing overfitting.

Shared representations: early layers learn shared features; task-specific layers learn task-specific
transformations. Sharing is automatic in a single neural network with task-specific heads. Weight sharing
provides inductive bias that tasks are related.

Hard parameter sharing: early layers shared, late layers task-specific. Soft parameter sharing: all
parameters are task-specific, but regularisation encourages similarity (e.g., L2 distance between
task-specific weights).

Task selection/scheduling: some tasks may dominate during training. Curriculum learning introduces
easy tasks early, then harder tasks. Uncertainty weighting assigns weights based on task uncertainty:
tasks with higher aleatoric uncertainty receive lower weight. This automatically balances tasks.

Cross-task transfer: learning task A improves performance on task B. Positive transfer helps; negative
transfer hurts. Task relationships affect transfer. Semantically related tasks (vision tasks on related
datasets) transfer well. Dissimilar tasks may interfere.

Hierarchical multi-task learning uses task structure. If tasks form a hierarchy (e.g., coarse to fine
classification), early layers learn coarse structure; later layers specialise. Auxiliary tasks (predicting
intermediate representations, data properties) improve primary task learning.

Adversarial multi-task learning: task-specific representations try to fool a task confusion module
(adversary), preventing task-specific information from leaking. This encourages task-invariant representations.

Applications: computer vision (multiple object classes, related datasets), NLP (POS tagging, NEP, parsing
jointly improve each other), recommendation systems (predicting rating, click, dwell time jointly), and
medical imaging (diagnosing multiple diseases jointly improves accuracy).

Challenges: negative transfer (task interference), task reweighting (which tasks matter more?), and
generalising to new tasks (often requires task-specific fine-tuning).
""",
    ),
    (
        "Chapter 31 – Federated Learning",
        """
Federated learning trains models across many distributed devices (phones, edge servers) while keeping
data local. This enables privacy-preserving learning at scale.

Traditional ML centralises data at a server. Federated learning brings computation to data: model updates
are computed locally, then aggregated at a central server. Updated global models are sent back to clients.

Differential privacy: the aggregation process adds noise such that individual datapoints cannot be
reconstructed. Local differential privacy adds noise at clients before sending updates; central differential
privacy adds noise at the server. Privacy-utility tradeoff: stronger privacy requires more noise.

Federated averaging (FedAvg): clients train locally for E epochs, then the server averages parameters.
This is efficient (fewer communication rounds) but diverges from centralised training if local data lacks
diversity (non-IID—non-independent and identically distributed).

Non-IID data is a challenge. Clients have different data distributions; averaging parameters from divergent
local optima may not converge to good global optima. Partial client participation: not all clients
participate in each round; stragglers (slow clients) are excluded.

Communication efficiency: model updates are often high-dimensional; communication is expensive. Gradient
compression (quantisation, sparsification) reduces message size. Some updates matter more; only top-k
updates are communicated.

Personalised federated learning adapts global models to client distributions. Meta-learning enables fast
adaptation. Transfer learning reuses global features, clients fine-tune. Multi-task learning treats each
client as a task.

Applications: mobile keyboards (Gboard), recommendation systems (YouTube), health (federated learning on
medical data without breaching privacy), and IoT.

Private deep learning: trusted execution environments (TEEs) and secure multiparty computation (MPC)
enable private training beyond differential privacy, though at computational cost.

Challenges: communication overhead (clients must frequently sync), Non-IID data, heterogeneous devices
(varying compute/bandwidth), and verifying correctness without seeing private data.
""",
    ),
    (
        "Chapter 32 – Explainable AI (XAI)",
        """
As AI systems influence critical decisions (medicine, criminal justice, finance), understanding why
models predict what they do is essential. Explainable AI (XAI) sheds light on model decision-making.

Interpretable models are inherently transparent. Linear models: predictions are weighted sums of features,
so feature weights directly explain predictions. Decision trees split on features; paths from root to leaf
explain decisions. Rule-based systems use human-readable rules.

Complex models (neural networks, random forests, gradient boosting) are treated as black boxes.
Post-hoc explanations approximate local behaviour to explain specific predictions.

LIME (Local Interpretable Model-agnostic Explanations): around a specific instance, fit a local linear
model. This linear model is interpretable; its weights explain which features matter for the prediction.
LIME is model-agnostic (works with any model) but requires careful sampling.

SHAP (SHapley Additive exPlanations): uses game theory (Shapley values) to assign each feature a credit
for the prediction. A features' Shapley value is its average marginal contribution across feature orderings.
SHAP provides theoretical guarantees (local accuracy, consistency) and is model-agnostic.

Saliency maps: backpropagation through a neural network computes gradients of the output w.r.t. inputs.
Large gradients indicate which input pixels affect the prediction most. Saliency maps highlight regions the
model attends to.

Attention mechanisms are interpretably transparent: attention weights show which inputs the model focuses
on. Transformer attention heads often capture linguistic structure; analysing attention reveals learned
patterns.

Feature importance: permutation importance measures how much a feature contributes by shuffling and
observing performance drop. Ablation studies remove features and measure impact. Influence functions
identify training examples most influential for a prediction.

Concept activation vectors (CAVs): identify directions in hidden spaces that align with human concepts
(e.g., "striped-ness" in image models). Testing sensitivity to concepts reveals if models use human
concepts or spurious correlations.

Adversarial examples: small, imperceptible perturbations flip predictions. Explanations through adversarial
examples reveal fragilities. Robustness certification proves models' resistance to perturbations.

Challenges: most explanation methods lack strong theoretical guarantees, comparisons are difficult,
and explanations can be misleading (explaining arbitrary decisions confidently). XAI is an active,
evolving research area.
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
