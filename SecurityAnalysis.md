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

### Website Vulnerables

#### Man‑in‑the‑Middle (MITM)

Because the web UI and its JSON API are served over plain HTTP (no TLS), an attacker who controls—or is on the path of—the user's network (e.g. a public Wi‑Fi, compromised router, or via ARP/DNS spoofing) can:

**Passive interception**

- Position themselves between the user and server using techniques like ARP poisoning, rogue access points, or DNS hijacking
- Deploy packet sniffing tools to capture all HTTP traffic
- Filter and extract every POST /api/classify request containing:
```json
{
  "model": "svm",
  "email": "Dear Alice, your invoice is attached…"
}
```

- Steal the entire email body in cleartext as it traverses the network
Log timestamps, source IPs, and user patterns for profiling
Build databases of intercepted emails for later exploitation

**Active tampering**

- Intercept the initial client request using proxy tools (e.g., Burp Suite, mitmproxy)
- Forward the legitimate request to the server while maintaining the connection
- Capture the server's JSON response:
```json
{
  "label": "ham",
  "confidence": 0.87
}
```

- Modify the response payload on the fly to manipulate classification results:
```json
{
  "label": "spam",
  "confidence": 0.99
}
```
- Calculate correct Content-Length headers to avoid detection
- Replay the forged response so the client's st.markdown() renders a false "SPAM (99%)" verdict
- Maintain persistent MITM position for continuous manipulation of all subsequent requests



#### Consequences of MITM on Website

**Confidentiality breach:** Any sensitive or private text pasted by the user (personal emails, business correspondence, financial documents) is captured in plaintext. Attackers can build comprehensive profiles of users' communication patterns and contacts. Intercepted data can be stored indefinitely, sold on dark web markets, or used for targeted attacks. Enables downstream phishing campaigns using legitimate email content as templates. Furthermore, it facilitates blackmail, extortion, or identity theft using compromised personal information


**Integrity compromise:** Classification results become completely untrustworthy and manipulable. 

Attackers can force legitimate mail to be marked "spam" causing:
- Important emails to be deleted or ignored
- Business communications to be missed
- Critical notifications to go unread

Dangerous/malicious mail can be marked "ham" causing:

- Phishing emails to appear trustworthy
- Malware-laden messages to bypass user suspicion
- Spam campaigns to reach inboxes successfully

#### Denial of Service (DoS/DDoS)

Even without login or rate limits, the public API can be overwhelmed: A single attacker can script repeated `/api/classify` calls, using up CPU/memory and making the service unresponsive to real users. Also coordinated bots can flood the endpoint from many IPs, causing prolonged downtime and requiring scaling or WAF protection.

As the website deployed on AWS, it is provided with some protection from AWS against DDoS attacks. However, there is still future work we can do to get better protection.


  

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

Our team identifies two major vunerbabilities threatening this applicaiton, MITM and Evasion, one targeting on traditonal website and the other on machine learning models. 
 
- **Next Steps**  
implementing fixes

