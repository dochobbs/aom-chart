# LinkedIn Post 1 (Week 2): The Completed Chart

*Part 1 of the "Compared to Whom?" series.*

---

Every clinician knows the informal translation of "WNL" in a chart: *we never looked.*

In 2019, researchers audio-recorded emergency medicine encounters and compared the audio against the electronic medical record (Berdahl et al., JAMA Netw Open). Only 38.5% of documented review-of-systems findings and 53.2% of documented physical exam findings were confirmed on the audio. The chart said the exam took place; the recording proved it did not.

When I gave ten frontier AI models a pediatric ear infection chart missing two decision variables (30-day antibiotic history and follow-up reliability), 41% of the models flatly asserted those missing facts as settled truth.

The models did not hallucinate random nonsense. They completed the chart.

Language models trained on millions of our clinical records inherited our documentation habits. The three most verbose models in our cohort (Fable, Sonnet, and Opus) invented facts on 11 to 13 of their 14 traces. The three tersest models invented facts once each. The longer outputs were not long because of greater clinical insight; they were long because completeness is the aesthetic, and completeness requires facts that the record did not supply.

Yet when asked one turn later what was missing, 97% of models immediately named the exact assumptions they had made. They know what is missing; they just do not ask first.

When we added one sentence to the prompt (*"If your plan depends on information that is not in the chart, say what is missing and ask for it instead of assuming it"*), fact fabrication dropped from 43% to 11%, with two frontier models hitting zero.

LLMs do not lack medical knowledge. They lack a forcing function to stop completing the chart.

Full benchmark data and anchor essay: https://github.com/dochobbs/aom-chart
