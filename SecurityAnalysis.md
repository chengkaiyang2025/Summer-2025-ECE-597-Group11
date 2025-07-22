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

The goal of this application is to provide a fast, lightweight tool for identifying potential spam emails using machine learning. Unlike traditional filtering tools, our system does not rely on user login, does not store data, and operates in a stateless manner.

Key benefits of this system include:

1. Stateless design, which reduces privacy liability by avoiding storage of any user data.
2. Lightweight architecture, making it easy to integrate into firewalls or email pipelines.
3. No data retention, minimizing compliance concerns around handling personal or sensitive content.
4. Practical utility, as it helps raise awareness about spam and phishing risks through generated explanations.

These features make the application suitable for broader deployment as a browser extension, firewall plugin, or email-scanning API, especially in environments where simplicity, speed, and privacy are prioritized.

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

![Figure.2](Explaination_provided.png)

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

## Integration and Future Expansion

With fine-tuning the results, this application could be integrated into a firewall to alert users of potential spam emails and help raise awareness within organizations to prevent fraud or sensitive information leaks. Transforming our website-based spam detection tool into an API for firewalls or email systems introduces several technical and operational concerns.

Privacy and data handling will not be our responsibility, but rather that of the firewall or the integrating organization. If encryption is needed, it is up to the client system to ensure that email content is securely transmitted. Our system remains stateless and does not store or log any data; it simply returns a coarse confidence score for each analyzed email. However, as mentioned earlier, the API is still vulnerable to man-in-the-middle (MITM) attacks if transmission is not secured. Therefore, proper controls—such as enforcing HTTPS and requiring authentication—should be in place.

In firewall or email system integrations, the API will be expected to provide fast and reliable responses. This becomes a technical concern, especially under high-volume traffic or real-time filtering. Ensuring high accuracy, low latency, and scalability will be important challenges moving forward.

## Conclusion
- **Summary of Risks**

Despite its lightweight and privacy-preserving architecture, the UVIC Spam Detector faces several key security risks that could compromise its effectiveness and integrity if left unaddressed. These risks span both the web application layer and the underlying machine learning models, and highlight the challenges of building transparent yet secure systems.
1. Model Exploitation and Evasion Attacks
The system's transparency — in terms of detailed model feedback that includes the classifier type, confidence scores, and influential tokens — could unintentionally assist the adversary in generating adversarial inputs. Attackers may systematically probe the model to:
- Identify heavily weighted spam features to exploit.
- Inject benign "ham" tokens to reduce spam features (data poisoning).
- Obscure high-value terms to avoid detection.
- Approximating the decision boundary through model extraction attacks.
These strategies involve a process of iterative spam evasion where attackers modify the messages to get around detection with fewer attempts, ultimately spoiling the reliability of the classifier.
2. Lack of Rate Limiting and Abuse Prevention
The nature of the application allows public, unauthenticated access without rate limiting, meaning that it is susceptible to attacks based on brute-force or automated submissions. Specifically, adversaries can submit a range of queries testing spam variations, or exploit the public access to conduct model inversion attacks revealing valuable knowledge of the model. The nature of its unrestricted access constitutes the following potential vulnerabilities:
- Rapid probe and evasion attempts. 
- Automated scraping of confidence metrics for reverse engineering.
- Potential Denial-of-Service (DoS) due to effectively unregulated query traffic.
3. Man-in-the-Middle (MitM) and Transport Security Risks:
Users copy raw email content and paste it into the web form. Investigators should consider this: no encryption and/or no SSL encryption (https) means that email content could be intercepted. Sensitive or personally identifiable information (PII) in emails could be a concern as the content is not being stored in the system, but will be exposed when sent and threatening privacy and creating unethical violations in email communication.
4. Model Staleness and Drift:
Although the system is designed to operate with a stateless process, lacking a retraining mechanism or any feedback loop of the user can result in continual model decline. As spam methods will change, the static models will not be as effective, resulting in more false negatives, and ultimately diminish trust in the tool.
By addressing these risks—by implementing some safeguards such as throttling, obfuscating any confidential model feedback, utilizing secure transmission methods, and periodically update the model—the UVIC Spam Detector could maintain a stronger posture and still offer the original features of speed and usability, as well as privacy considerations.
 
 
- **Next Steps**  
To enhance the security, reliability, and scalability of the UVIC Spam Detector while preserving its core advantages (stateless design, privacy, and speed), we propose the following next steps:
1. Implement Security Enhancements
- Implement Rate Limiting and CAPTCHA: Limit the number of API requests or form submissions allowed from a particular IP address to combat automated abuse. Implement CAPTCHA to assist in the mitigation of bot-level probing.
- Use HTTPS by default: Ensure all communications happen over secure HTTPS protocols to protect the content of emails in transit and combat man-in-the-middle (MitM) attacks.
- Limit Exposure of Feedback: Limit or randomize the exposure of model explanations to limit model probing/extraction (i.e., only allow higher-level explanations; token level feedback can be limited).
2. Harden the ML Model Against Evasion
- Adversarial Training: Present adversarial examples in training the model, to help ensure the model is more robust to constructed inputs.
- Confidence Smoothing: Introduce some noise, or use other techniques such as differential privacy, to lessen the fidelity of confidence scores without dramatically reducing user utility.
- Token Obfuscation Detection: Add preprocessing checks to identify token obfuscation techniques (inserting extra characters, Unicode look-alikes, etc.).
3. Improve Model Management
- Model Documentation and Tracking: Document and track model versions and output history for auditing and rollback to previous models in the eventuality of drift or exploitation.
- Model Updating: While the model will be static for now, investigate lightweight, privacy-preserving updating mechanisms (e.g., differential learning, federated updates utilizing synthetic or anonymized spam datasets).
- Drift Monitoring: Integrate tools to assess shifts in data input distribution over time, or monitoring model performance.
4. Conduct Formal Risk Assessment
- Threat Modeling: Employ STRIDE or something comparable to identify and categorize risks systematically throughout the system (spoofing, tampering, etc., information disclosure).
- Red Team Assessment: Simulate attacks using ethical hacking techniques to discover additional vulnerabilities that have not been recognized.
- Security Review and Penetration Testing: Use third-party reviewers or ethical hackers to provide independent security reviews for the application and its endpoints.
5. Expand Deployment Use Cases
- Browser Extension Creation: Create a Chrome/Firefox extension that uses the spam detector to conduct real-time scanning of webmail.
- Firewall / Email Gateway Plugin: Package the tool as a plugin for deployment in corporate email pipelines to provide a lightweight, real-time spam filtering ability.
- API Productization: Develop and secure an API layer that includes keys, rate limits, and usage logs that third-party developers can use to integrate the service into their platform.
-6. Research Extensions
- Comparative study: Test the UVIC Spam Detector against other easily implementable ML spam detectors in adversarial settings.
- Dataset expansion and diversity: Build a rich dataset representative of new phishing methods, cross-language datasets, and new ways of obfuscation to enhance generalization of models.

