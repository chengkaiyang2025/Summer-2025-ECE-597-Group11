# Security Analysis and Suggestions on UVIC Spam Detector

## Abstract
 UVic Spam Detector is a publicly accessible web application that lets users submit email text and select from multiple machine‑learning classifiers to determine if a message is spam or legitimate. This report analyzes both the web application surface and the underlying models, identifying vulnerabilities, rating their criticality, and recommending concrete mitigations.

## Introduction

### Background  
UVic Spam Detector is a lightweight, publicly accessible web-based application that allows anyone to submit raw email content to receive a “spam” or “not spam” verdict, using one of four models: Logistic Regression, Naive Bayes, Support Vector Machine (SVM), or Random Forest. The site exposes a simple upload form and JSON API for inference but lacks HTTPS, authentication, and access controls—making every endpoint vulnerable to public and automated abuse. Internally, uploaded emails are tokenized and vectorized before being classified by models such as Naive Bayes, Random Forest, or a small neural network.

### Objectives  
Based on the usage and design of this web application, we will focus on confidentiality, integrity, and availability, the three pillars of cyber security. Found vulnerabilities will be discussed based on the nature of this tool to see if it poses a threat to the application. We will also discuss criticality (impact + likelihood) of these vulnerabilities and how they can be exploit in practice.

### Methodology
Our approach combines traditional threat modeling techniques targeting the website with machine-learning-specific threat models. The report also addresses privacy concerns and potential future risks, especially if the system is extended as a browser extension or API for third-party use. This structured methodology ensures comprehensive coverage of both classic web vulnerabilities and emerging threats in machine learning–driven applications.

## System Overview
### Architecture Diagram  
(data inputs, processing pipeline, classification engine, user interface, storage).  

### Key Technologies & Dependencies  
Machine Learning Models including: Logistic Regression, Naive Bayes, SVM, and Random Forest; Develped on Jupter Notebook using Python, Depolyed using AWS.  

### Data Flow  
A user (no login required) pastes raw email text into the web form, after which the application normalizes it (e.g., strips punctuation and tokenizes words) and vectorizes the tokens with the pre‑built Bag‑of‑Words / TF‑IDF model for the selected classifier (Logistic Regression, Naive Bayes, SVM, or Random Forest). The chosen static model then produces a spam / ham (non‑spam) label and currently a confidence score plus indicative tokens for explanation, which is returned in the response. The email content provided by users is neither stored or used in retraining, but processed only in memory for the current classification and then discarded.

## Security Analysis

Website


  

### Machine Learning Model Information Disclosure & Feedback Risk

While the UI currently discloses the specific classifier family (e.g., Logistic Regression) and the top contributing words plus a numeric confidence score [Figure 2], the primary enabling factor for attack is the public endpoint access without rate limitation. Our effort to provide transparency, such as showing users why a message was labeled spam or ham (legitimate, non‑spam email), does improve trust and can educate users. However, the same explanations given (exact model name, precise confidence percentage, and ranked contributing tokens) provides attackers with rich feedback. By iteratively submitting modified emails and observing how individual token changes shift contribution rankings or changes the confidence score, an adversary can rapidly:

1. Learn which “spam” tokens have the highest positive weights.
2. Inject “ham” tokens or benign filler phrases to dilute those weights.
3. Obfuscate high‑impact spam tokens (e.g., spacing) and confirm success via rising confidence.
4. Approximate the model’s decision boundary (model extraction) with far fewer queries than if only a binary label were returned.

To conclude, unlimited queries reduce the time to achieve reliable evasion from potentially thousands of probes (label‑only) to tens or low hundreds (rich explanations), significantly increasing the likelihood of successful large‑scale spam evasion. It's important to find the balance between transparency and security in this case.

![alt text](Explaination_provided.png)

### Mitigations & Transparency Trade‑Off

We propose the following three mitigations that most effectively achieve a trade‑off between security and transparency.

**Rate Limiting & Monitoring**

For each IP address, implement request quotas (e.g., limit requests per 5 minutes to 30) and log anomalies such as unusually high volume from the same IP address. Consider temporarily blocking an IP if abnormal usage is repeatedly found in the logs. This directly cuts an attacker’s attempts and slows the process of crafting evasions while having minimal effect on normal users, whose request volume should remain below the limits.

**Output Minimization**

Instead of the current numeric confidence score, return only a coarse confidence bucket (e.g., High, Medium, Low). This removes fine‑grained signals attackers can analyze to fine‑tune their spam recipes, yet still provides legitimate users a reasonable sense of certainty and transparency.

**Feature Attribution Throttling**

Return only a small set of category or indicative terms (e.g., “urgent call‑to‑action,” “financial request,” “ambiguous origin”) to show why a message was classified as spam or non‑spam. These descriptors still give users useful explanation, although some detail is lost. At the same time, this greatly hinders attackers from reverse‑engineering exact feature weights across models for evasion. The full ranked token list currently shown can be moved to internal logs only.

These mitigation methods, tuned based on real‑world usage data, provide a good balance of security and transparency, helping ensure the web‑based application remains effective and resilient over the long term.

## Privacy Concerns

As the application does not require user authentication and primarily processes spam emails without storing them, we do not consider privacy a critical concern at this stage. However, we recommend displaying a clear warning to users, advising them not to paste any sensitive or personal information into the website. For now, we rely on user discretion to avoid sharing private data. This reduces potential harm in the event of a man-in-the-middle (MITM) attack or data interception.

## Future Work

With fine-tuning the results, this application could be integrated into a firewall to alert users of potential spam emails and help raise awareness within organizations to prevent fraud or sensitive information leaks. Transforming our website-based spam detection tool into an API for firewalls or email systems introduces several technical and operational concerns.

Privacy and data handling will not be our responsibility, but rather that of the firewall or the integrating organization. If encryption is needed, it is up to the client system to ensure that email content is securely transmitted. Our system remains stateless and does not store or log any data; it simply returns a coarse confidence score for each analyzed email. However, as mentioned earlier, the API is still vulnerable to man-in-the-middle (MITM) attacks if transmission is not secured. Therefore, proper controls—such as enforcing HTTPS and requiring authentication—should be in place.

In firewall or email system integrations, the API will also be expected to provide fast and reliable responses. This becomes a technical concern, especially under high-volume traffic or real-time filtering. Ensuring low latency, fault tolerance, and scalability will be important challenges moving forward.


## Conclusion
- **Summary of Risks & Benefits**

Our team identifies two major vunerbabilities threatening this applicaiton, MITM and Evasion, one targeting on traditonal website and the other on machine learning models. 
 
- **Next Steps**  
  Roadmap for implementing fixes, timelines, and responsible teams.  
- **Future Work**  

