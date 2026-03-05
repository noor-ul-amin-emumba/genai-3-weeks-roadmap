# Week 1 · Day 3 — LLM Evaluation Report
**Generated:** 2026-03-04 22:40  
**LLM-A:** LLM-A (llama-3.1-8b-instant)  
**LLM-B:** LLM-B (openai/gpt-oss-120b)  
**Judge model:** llama-3.3-70b-versatile  
**Temperature:** 0 (deterministic)  
**Test set:** 16 questions (11 answerable / 5 unanswerable)  

---
## 1. Evaluation Metrics Explained
| Metric | Description | Range |
|--------|-------------|-------|
| **Exact Match (EM)** | 1 if key ground-truth phrase appears in prediction or if refusal detected for unanswerable | 0–1 |
| **Token F1** | Word-level precision × recall overlap between prediction and ground truth | 0–1 |
| **BLEU-1** | Unigram precision with brevity penalty vs ground truth | 0–1 |
| **LLM-Judge (0–10)** | Third-model judge scoring correctness / appropriate refusal | 0–10 |

**Pass/Fail gate:**
- *Answerable*: PASS if Token F1 ≥ 0.35 **or** LLM-Judge ≥ 6  
- *Unanswerable*: PASS if LLM-Judge ≥ 6 (model correctly refuses)  

---
## 2. Aggregate Results (All 25 Questions)
| Metric | LLM-A | LLM-B | Winner |
|--------|-------|-------|--------|
| Exact Match (EM) | 0.875 | 0.812 | LLM-A |
| Token F1 | 0.643 | 0.600 | LLM-A |
| BLEU-1 | 0.501 | 0.445 | LLM-A |
| LLM-Judge (avg/10) | 8.56 | 8.62 | LLM-B |
| **PASS count** | **14/25** | **14/25** | Tie |
| **FAIL count** | **2/25** | **2/25** | Tie |

## 3. Breakdown: Answerable (20) vs Unanswerable (5)
### 3a. Answerable Questions Only
| Metric | LLM-A | LLM-B |
|--------|-------|-------|
| EM | 0.818 | 0.727 |
| Token F1 | 0.653 | 0.591 |
| BLEU-1 | 0.595 | 0.514 |
| LLM-Judge | 7.91 | 8.00 |
| PASS | 9/20 | 9/20 |

### 3b. Unanswerable Questions Only (model should decline)
| Metric | LLM-A | LLM-B |
|--------|-------|-------|
| EM (refusal detected) | 1.000 | 1.000 |
| Token F1 | 0.621 | 0.621 |
| BLEU-1 | 0.295 | 0.295 |
| LLM-Judge | 10.00 | 10.00 |
| PASS (correct refusal) | 5/5 | 5/5 |

---
## 4. Pass/Fail Summary Per Question
| Q# | Question (truncated) | Category | Answerable | LLM-A | LLM-B |
|----|----------------------|----------|------------|-------|-------|
| 1 | Who organised the Dartmouth Conference in 1956 where th... | AI History | Yes | ✅ PASS | ✅ PASS |
| 2 | What is the Turing Test and who proposed it?... | AI Fundamentals | Yes | ✅ PASS | ✅ PASS |
| 3 | What are the three key factors that drove the modern AI... | AI History | Yes | ✅ PASS | ✅ PASS |
| 4 | What is the difference between supervised learning and ... | Machine Learning | Yes | ✅ PASS | ✅ PASS |
| 5 | What is overfitting and what are some techniques to mit... | Machine Learning | Yes | ✅ PASS | ✅ PASS |
| 6 | What architecture was introduced in the paper 'Attentio... | Deep Learning | Yes | ✅ PASS | ✅ PASS |
| 7 | What are the two pretraining objectives used by BERT?... | NLP | Yes | ✅ PASS | ✅ PASS |
| 8 | What is Retrieval-Augmented Generation (RAG) and what p... | NLP | Yes | ✅ PASS | ✅ PASS |
| 9 | What breakthrough in object detection does the YOLO mod... | Computer Vision | Yes | ✅ PASS | ✅ PASS |
| 10 | What is the EU AI Act and when was it established?... | AI Ethics | Yes | ❌ FAIL | ❌ FAIL |
| 19 | What was the significance of AlphaFold 2 developed by D... | AI Applications | Yes | ❌ FAIL | ❌ FAIL |
| 21 | What is the exact market capitalisation of the global A... | Unanswerable | No | ✅ PASS | ✅ PASS |
| 22 | What is the name of the specific neural network archite... | Unanswerable | No | ✅ PASS | ✅ PASS |
| 23 | Which country was the first to reach net-zero carbon em... | Unanswerable | No | ✅ PASS | ✅ PASS |
| 24 | What is the exact number of parameters in the GPT-4 mod... | Unanswerable | No | ✅ PASS | ✅ PASS |
| 25 | What specific programming language was used to implemen... | Unanswerable | No | ✅ PASS | ✅ PASS |

---
## 5. Per-Question Detailed Scores
| Q# | LLM | EM | F1 | BLEU-1 | Judge | Pass/Fail |
|----|-----|----|----|--------|-------|-----------|
| 1 | A | 1 | 0.737 | 0.609 | 10 | PASS |
| 1 | B | 1 | 0.938 | 0.882 | 10 | PASS |
| 2 | A | 1 | 0.957 | 0.943 | 10 | PASS |
| 2 | B | 1 | 0.784 | 0.744 | 9 | PASS |
| 3 | A | 1 | 0.786 | 0.667 | 10 | PASS |
| 3 | B | 1 | 0.750 | 0.636 | 10 | PASS |
| 4 | A | 1 | 0.571 | 0.475 | 9 | PASS |
| 4 | B | 1 | 0.583 | 0.491 | 10 | PASS |
| 5 | A | 1 | 0.873 | 0.828 | 9 | PASS |
| 5 | B | 1 | 0.750 | 0.632 | 10 | PASS |
| 6 | A | 1 | 0.641 | 0.606 | 9 | PASS |
| 6 | B | 0 | 0.563 | 0.462 | 9 | PASS |
| 7 | A | 1 | 0.774 | 0.706 | 10 | PASS |
| 7 | B | 1 | 0.774 | 0.706 | 10 | PASS |
| 8 | A | 1 | 0.930 | 0.930 | 10 | PASS |
| 8 | B | 1 | 0.524 | 0.398 | 10 | PASS |
| 9 | A | 1 | 0.727 | 0.706 | 10 | PASS |
| 9 | B | 1 | 0.645 | 0.624 | 10 | PASS |
| 10 | A | 0 | 0.114 | 0.034 | 0 | FAIL |
| 10 | B | 0 | 0.114 | 0.034 | 0 | FAIL |
| 19 | A | 0 | 0.074 | 0.041 | 0 | FAIL |
| 19 | B | 0 | 0.074 | 0.041 | 0 | FAIL |
| 21 | A | 1 | 0.621 | 0.295 | 10 | PASS |
| 21 | B | 1 | 0.621 | 0.295 | 10 | PASS |
| 22 | A | 1 | 0.621 | 0.295 | 10 | PASS |
| 22 | B | 1 | 0.621 | 0.295 | 10 | PASS |
| 23 | A | 1 | 0.621 | 0.295 | 10 | PASS |
| 23 | B | 1 | 0.621 | 0.295 | 10 | PASS |
| 24 | A | 1 | 0.621 | 0.295 | 10 | PASS |
| 24 | B | 1 | 0.621 | 0.295 | 10 | PASS |
| 25 | A | 1 | 0.621 | 0.295 | 10 | PASS |
| 25 | B | 1 | 0.621 | 0.295 | 10 | PASS |

---
## 6. Top 5 Failure Examples
### LLM-A (llama-3.1-8b-instant)
**Failure #1 — Q10**  
*Question:* What is the EU AI Act and when was it established?  
*Ground Truth:* The EU AI Act (2024) is a regulatory framework that establishes risk-based categories for AI systems, classifying them by potential harm and imposing obligations accordingly.  
*Model Answer:* The answer is not found in the provided documents.  
*Scores:* EM=0, F1=0.114, BLEU=0.034, Judge=0  
**Reason:** Answer is largely incorrect or irrelevant (judge=0, F1=0.11).  

**Failure #2 — Q19**  
*Question:* What was the significance of AlphaFold 2 developed by DeepMind in 2020?  
*Ground Truth:* AlphaFold 2 predicted the 3D structures of nearly all known proteins, which was a breakthrough for drug discovery.  
*Model Answer:* The answer is not found in the provided documents.  
*Scores:* EM=0, F1=0.074, BLEU=0.041, Judge=0  
**Reason:** Answer is largely incorrect or irrelevant (judge=0, F1=0.07).  


### LLM-B (openai/gpt-oss-120b)
**Failure #1 — Q10**  
*Question:* What is the EU AI Act and when was it established?  
*Ground Truth:* The EU AI Act (2024) is a regulatory framework that establishes risk-based categories for AI systems, classifying them by potential harm and imposing obligations accordingly.  
*Model Answer:* The answer is not found in the provided documents.  
*Scores:* EM=0, F1=0.114, BLEU=0.034, Judge=0  
**Reason:** Answer is largely incorrect or irrelevant (judge=0, F1=0.11).  

**Failure #2 — Q19**  
*Question:* What was the significance of AlphaFold 2 developed by DeepMind in 2020?  
*Ground Truth:* AlphaFold 2 predicted the 3D structures of nearly all known proteins, which was a breakthrough for drug discovery.  
*Model Answer:* The answer is not found in the provided documents.  
*Scores:* EM=0, F1=0.074, BLEU=0.041, Judge=0  
**Reason:** Answer is largely incorrect or irrelevant (judge=0, F1=0.07).  


---
## 7. Analysis and Conclusion
**Overall winner (by LLM-Judge avg):** Both models performed similarly  

- **LLM-A** achieved avg LLM-Judge score of **8.56/10**, Token F1 of **0.643**, and passed **14/25** questions.  
- **LLM-B** achieved avg LLM-Judge score of **8.62/10**, Token F1 of **0.600**, and passed **14/25** questions.  

**Key observations:**  
1. Both models were evaluated under identical conditions (temperature=0, same context, same questions).  
2. Unanswerable questions reveal hallucination tendencies; models that score well here correctly decline rather than fabricating answers.  
3. Token F1 and BLEU-1 penalise verbose or paraphrased answers even when factually correct, so LLM-Judge score best reflects semantic quality.  
4. A larger model generally achieves better LLM-Judge scores, showing the value of scale for knowledge-intensive QA tasks.  
5. Both models showed weaknesses on numerical/specific detail questions where the exact figure must appear verbatim.  
