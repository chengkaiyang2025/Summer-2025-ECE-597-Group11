# Security Analysis and Suggestions on UVIC Spam Detector

## Abstract
- **Purpose & Scope**  

  UVic Spam Detector is a web-based tool that allows anyone to upload their email content and choose from several machine learning models to determin if it is in fact a spam email. 
  
  This analysis covers:

  1. **Application Security**  
   - Transport layer (lack of HTTPS)  
   - Input handling (file uploads, form fields, JSON endpoints)  
   - Session‑ and endpoint‑level controls (CSRF, auth, rate limiting)

  2. **ML‑Pipeline Security**  
   - Data‑poisoning and adversarial‑evasion threats against the models  
   - Model‑extraction risks via repeated inference queries

  We will discuss possible attack surface and vectors, then propose concrete mitigations.  (To be revaluated e.g. TLS enforcement, input sanitization, adversarial training, request throttling, dependency hardening)

## Introduction

### Background  
UVic Spam Detector is a lightweight, publicly accessible web-based application that allows anyone to submit raw email content to receive a “spam” or “not spam” verdict, using one of four models: Logistic Regression, Naive Bayes, Support Vector Machine (SVM), or Random Forest. The site exposes a simple upload form and JSON API for inference but lacks HTTPS, authentication, and access controls—making every endpoint vulnerable to public and automated abuse. Internally, uploaded emails are tokenized and vectorized before being classified by models such as Naive Bayes, Random Forest, or a small neural network.

### Objectives  
Based on the usage and design of this web application, we will focus on how confidentiality, integrity, and availability, the three pillars of cyber security. Each vulnerability will be discussed based on the nature of this tool to see if it poses a threat to the application. We will also discuss criticality (impact + likelihood) of these vulnerabilities and how they can be exploit in practice.

### Methodology
Our approach combines traditional web‑app testing and ML‑specific threat modeling.
This structured methodology ensures comprehensive coverage of both classic web vulnerabilities and emerging risks in machine‑learning‑driven applications.

## System Overview
### Architecture Diagram  
- Brief diagram or description of components (data inputs, processing pipeline, classification engine, user interface, storage).  
### Key Technologies & Dependencies  
- ML model(s), libraries, deployment platform (e.g. Flask + scikit‑learn, AWS Lambda, etc.).  
### Data Flow  
user input raw email content through website in text. the punctuations will be removed for better analysis on word distributions.  (- How email/text enters the system, is preprocessed, classified, and logged.

## Security Analysis
### Threat Model  
- **Actors**: malicious users, adversarial ML attackers, insider threats  
- **Assets**: model weights, email content, user metadata  
### Attack Surfaces  
- **Input channels**: poisoned training data, crafted emails  
- **API endpoints**: injection, authentication bypass  
- **Model inference**: query‑based model extraction or evasion  
### Vulnerabilities & Findings  
- **Data poisoning risks**: how unvetted input could skew model  
- **Model evasion**: adversarial
