(() => {
  const concepts = {
    restrained: { label: "Restrained", note: "Quiet editorial" },
    distinctive: { label: "Distinctive", note: "Two systems" },
    publication: { label: "Publication", note: "Long-form feature" },
    engine: { label: "Evidence Engine", note: "Scroll-driven evidence posters" },
    casefile: { label: "Case File", note: "Forensic clinical dossier" },
    cinematic: { label: "Cinematic", note: "Full-viewport narrative scenes" }
  };

  const requested = new URLSearchParams(location.search).get("concept");
  const concept = concepts[requested] ? requested : "restrained";
  const overdriveConcepts = new Set(["engine", "casefile", "cinematic"]);
  const isOverdrive = overdriveConcepts.has(concept);
  document.body.dataset.concept = concept;
  document.title = `Compared to whom? — ${concepts[concept].label} concept`;

  const main = document.querySelector("main");
  if (!main) return;
  main.id = "article";

  const make = (tag, className, html) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (html !== undefined) node.innerHTML = html;
    return node;
  };

  const progress = make("div", "progress-track", "<span></span>");
  progress.setAttribute("aria-hidden", "true");
  document.body.prepend(progress);

  const skip = make("a", "skip-link", "Skip to article");
  skip.href = "#article-body";
  document.body.prepend(skip);

  const oldNav = document.querySelector("body > nav");
  const bar = make("nav", "concept-bar");
  bar.setAttribute("aria-label", "Concept preview navigation");
  bar.innerHTML = `
    <a class="brand" href="index.html">Compared to whom?<span>design study</span></a>
    <div class="concept-switcher" aria-label="Choose a design concept">
      ${Object.entries(concepts).map(([key, value]) => `<a href="article.html?concept=${key}" ${key === concept ? 'aria-current="page"' : ""}>${value.label}</a>`).join("")}
    </div>
    <a class="packet-link" href="../../index.html">Open the local evidence packet ↗</a>`;
  oldNav.replaceWith(bar);

  const h1 = main.querySelector(":scope > h1");
  const firstH2 = main.querySelector(":scope > h2");
  if (!h1 || !firstH2) return;

  const intro = [];
  let cursor = h1.nextSibling;
  while (cursor && cursor !== firstH2) {
    const next = cursor.nextSibling;
    if (cursor.nodeType === Node.ELEMENT_NODE && cursor.matches("p")) intro.push(cursor);
    cursor = next;
  }

  const hero = make("header", "article-hero");
  const heroCopy = make("div", "hero-copy");
  heroCopy.append(
    make("p", "kicker", `A clinical-AI field essay · ${concepts[concept].note}`),
    h1,
    make("p", "dek", "A pediatrician tests what clinical AI invents, follows the same failures into forty years of human evidence, and finds the collaboration protocol neither side gets for free."),
    make("p", "article-meta", "Michael Hobbs, MD · August 2026 · 140 primary traces · synthetic case, no PHI · approximately 23 minutes")
  );
  const opening = make("div", "opening");
  intro.forEach((paragraph) => opening.append(paragraph));
  hero.append(heroCopy, opening);
  main.insertBefore(hero, firstH2);

  const quick = make("section", "quick-read");
  quick.setAttribute("aria-labelledby", "quick-read-title");
  quick.innerHTML = `
    <header><h2 id="quick-read-title">The 20-second read</h2><span>The argument before the evidence</span></header>
    <div class="quick-points">
      <p class="quick-point"><strong>41%</strong><span>of primary AI answers invented at least one chart fact.</span></p>
      <p class="quick-point"><strong>43 → 11%</strong><span>after one sentence required the model to ask instead of assume.</span></p>
      <p class="quick-point"><strong>92 / 76 / 74</strong><span>AI alone / physicians with AI / physicians alone in a cited diagnostic trial.</span></p>
    </div>`;
  main.insertBefore(quick, firstH2);

  if (isOverdrive) {
    const briefing = make("section", "scenario-briefing");
    briefing.setAttribute("aria-label", "Essay briefing notes");
    briefing.innerHTML = `
      <details><summary>What is this?</summary><p>A narrative comparison of clinical-AI errors, clinician errors, and the evidence on teams that combine both.</p></details>
      <details><summary>What was tested?</summary><p>One synthetic pediatric ear-infection chart, ten frontier models, 140 primary traces, identity contrasts, and a prompt intervention.</p></details>
      <details><summary>What remains untested?</summary><p>A clinical workflow that pairs ask-don’t-assume prompting with explicit training for the supervising clinician.</p></details>`;
    main.insertBefore(briefing, quick);
  }

  const readingShell = make("div", "reading-shell");
  const argumentMap = make("aside", "argument-map");
  argumentMap.setAttribute("aria-label", "Argument map");
  argumentMap.innerHTML = `
    <p>The argument</p>
    <ol>
      <li><a href="#an-easy-case-on-purpose"><span>01</span>The machine test</a></li>
      <li><a href="#the-part-we-dont-say-out-loud"><span>02</span>The human baseline</a></li>
      <li><a href="#the-cheap-fix-nobody-ships"><span>03</span>The cheap fix</a></li>
      <li><a href="#the-twist-adding-a-doctor-can-subtract"><span>04</span>The combination</a></li>
      <li><a href="#the-four-second-question"><span>05</span>The question</a></li>
    </ol>`;
  const articleBody = make("div", "article-body");
  articleBody.id = "article-body";
  readingShell.append(argumentMap, articleBody);
  main.insertBefore(readingShell, firstH2);

  while (firstH2.parentNode === main) articleBody.append(firstH2);
  while (readingShell.nextSibling) articleBody.append(readingShell.nextSibling);

  let chapter = null;
  let chapterNumber = 0;
  [...articleBody.childNodes].forEach((node) => {
    if (node.nodeType === Node.ELEMENT_NODE && node.matches("h2")) {
      chapterNumber += 1;
      chapter = make("section", "chapter");
      chapter.dataset.chapter = String(chapterNumber).padStart(2, "0");
      articleBody.insertBefore(chapter, node);
      const label = make("span", "chapter-index", `Chapter ${String(chapterNumber).padStart(2, "0")}`);
      node.prepend(label);
      chapter.append(node);
    } else if (chapter) {
      chapter.append(node);
    }
  });

  if (isOverdrive) {
    const stageLabels = [
      "Machine baseline", "Human baseline", "Error inheritance", "Prompt intervention",
      "Team failure", "Team success", "Proposed protocol", "Four-second question"
    ];
    argumentMap.innerHTML = `<p>Evidence journey</p><ol>${[...articleBody.querySelectorAll(".chapter > h2")].map((heading, index) => `<li><a href="#${heading.id}"><span>${String(index + 1).padStart(2, "0")}</span>${stageLabels[index]}</a></li>`).join("")}</ol>`;
  }

  const addCitation = (pattern, href, label) => {
    const paragraph = [...articleBody.querySelectorAll("p")].find((item) => item.textContent.includes(pattern));
    if (!paragraph) return;
    const link = make("a", "citation");
    link.href = href;
    link.setAttribute("aria-label", label);
    link.title = label;
    paragraph.append(" ", link);
  };

  addCitation("Forty-one percent", "../../site/results/smoke_20260815t160303z_tiebreak.html", "Open the adjudicated primary results");
  addCitation("Invented facts fell from", "../../site/results/smoke_20260815t214553z_notes.html", "Open the mitigation experiment");
  addCitation("Stanford researchers ran", "../../site/docs/combination_lit.html", "Open the human-AI combination evidence bank");
  addCitation("pre-registered meta-analysis", "../../site/docs/combination_lit.html", "Open the combination meta-analysis sources");
  addCitation("human versions carry numbers", "../../site/docs/human_parallels.html", "Open the verified human-error citation bank");

  const tables = [...articleBody.querySelectorAll("table")];
  const captions = [
    "Primary-answer findings after independent scoring and quote-level adjudication.",
    "Effect of the ask-don’t-assume instruction on the four highest-fabricating models."
  ];
  tables.forEach((table, index) => {
    const caption = make("caption", "", captions[index] || "Study results.");
    table.prepend(caption);
    table.querySelectorAll("th").forEach((cell) => cell.setAttribute("scope", "col"));
  });

  const mitigationText = [...articleBody.querySelectorAll("p")].find((p) => p.textContent.includes("Invented facts fell from 24 of 56 answers to 6"));
  if (mitigationText) {
    const figure = make("figure", "evidence-figure mitigation-figure");
    figure.innerHTML = `
      <div class="mitigation-flow" aria-label="Invention rate fell from 43 percent to 11 percent">
        <div class="rate before"><strong>43%</strong><span>bare prompt · 24 of 56</span></div>
        <div class="arrow" aria-hidden="true">→</div>
        <div class="rate after"><strong>11%</strong><span>ask, don’t assume · 6 of 56</span></div>
      </div>
      <figcaption>One sentence changed the model’s behavior. It did not repair stale knowledge or broken age math.</figcaption>`;
    mitigationText.after(figure);
  }

  const aiAlone = [...articleBody.querySelectorAll("p")].find((p) => p.textContent.trim() === "The AI alone scored 92 percent.");
  if (aiAlone) {
    const figure = make("figure", "evidence-figure score-figure");
    figure.innerHTML = `
      <div class="scoreboard" aria-label="Diagnostic reasoning scores">
        <div class="score"><strong>74</strong><span>physicians alone</span></div>
        <div class="score"><strong>76</strong><span>physicians with AI</span></div>
        <div class="score"><strong>92</strong><span>AI alone</span></div>
      </div>
      <figcaption>Same cases, diagnostic reasoning score. The collaboration—not raw capability—was the bottleneck.</figcaption>`;
    aiAlone.after(figure);
  }

  const complement = [...articleBody.querySelectorAll("p")].find((p) => p.textContent.replace(/\s+/g, " ").includes("The human omits; the machine invents"));
  if (complement) {
    const figure = make("figure", "faultline");
    figure.setAttribute("aria-label", "Complementary failure modes");
    figure.innerHTML = `
      <div class="human"><b>Human</b><span>omits · forgets · hides bias in gestalt</span></div>
      <div class="machine"><b>Machine</b><span>invents · stays stale · exposes bias in text</span></div>`;
    complement.after(figure);
  }

  if (isOverdrive) {
    const states = [
      { title: "Machine baseline", signal: "41%", detail: "answers invented ≥1 chart fact" },
      { title: "Human baseline", signal: "55%", detail: "of recommended care received" },
      { title: "Error inheritance", signal: "3 roots", detail: "training data · post-training · prompt" },
      { title: "Prompt intervention", signal: "43 → 11%", detail: "invention rate after one sentence" },
      { title: "Team failure", signal: "74 / 76 / 92", detail: "human · team · AI diagnostic scores" },
      { title: "Team success", signal: "Conditional", detail: "task · interface · division of labor" },
      { title: "Proposed protocol", signal: "3 habits", detail: "surface · verify · disagree with evidence" },
      { title: "Four-second question", signal: "What’s missing?", detail: "say what you assume · ask about blanks" }
    ];
    const chapters = [...articleBody.querySelectorAll(".chapter")];
    const matrix = Array.from({ length: 140 }, (_, index) => `<i${index < 57 ? ' class="is-hit"' : ""}></i>`).join("");
    const posters = [
      `<p class="poster-label">140 primary answers</p><strong class="poster-primary">41%</strong><div class="answer-matrix" aria-label="57 of 140 answers invented a chart fact">${matrix}</div><p class="poster-caption">57 invented at least one fact that was not in the chart.</p>`,
      `<p class="poster-label">Different holes · same chart</p><div class="failure-pair"><div><span>Human</span><strong>omits</strong><small>55% of recommended care received</small></div><div><span>Machine</span><strong>invents</strong><small>41% of answers added a fact</small></div></div>`,
      `<p class="poster-label">The inheritance chain</p><div class="root-pipeline"><div><span>01</span><strong>Training data</strong><small>our charts · our stale guidance · our bias</small></div><div><span>02</span><strong>Post-training</strong><small>helpfulness rewards confident completion</small></div><div><span>03</span><strong>Prompt</strong><small>the deployment lever within reach</small></div></div>`,
      `<p class="poster-label">One sentence · same models</p><div class="poster-change"><div><strong>43%</strong><span>bare prompt</span></div><b>→</b><div><strong>11%</strong><span>ask, don’t assume</span></div></div><p class="poster-caption">Behavior moved. Stale knowledge did not.</p>`,
      `<p class="poster-label">Diagnostic reasoning score</p><div class="poster-bars"><div style="--score:.74"><strong>74</strong><i></i><span>human</span></div><div style="--score:.76"><strong>76</strong><i></i><span>team</span></div><div style="--score:.92"><strong>92</strong><i></i><span>AI</span></div></div><p class="poster-caption">Adding a doctor added two points—and subtracted sixteen from the strongest participant.</p>`,
      `<p class="poster-label">Synergy is conditional</p><svg class="synergy-map" viewBox="0 0 360 320" role="img" aria-label="Task, interface, and roles determine whether a team produces synergy"><path d="M180 42 48 265h264Z"/><circle cx="180" cy="186" r="49"/><text x="180" y="190">SYNERGY</text><text x="180" y="25">TASK</text><text x="20" y="290">INTERFACE</text><text x="285" y="290">ROLES</text></svg>`,
      `<p class="poster-label">A collaboration protocol</p><ol class="protocol-sequence"><li><span>01</span><strong>Surface</strong><small>What did the model assume?</small></li><li><span>02</span><strong>Verify</strong><small>Treat each blank as a task.</small></li><li><span>03</span><strong>Disagree with evidence</strong><small>Finding, guideline, lab—not gestalt.</small></li></ol>`,
      `<p class="poster-label">The habit on both sides</p><strong class="poster-question">What are you assuming?</strong><p class="poster-time"><span>4</span> seconds</p>`
    ];

    if (concept === "engine" || concept === "cinematic") {
      chapters.forEach((section, index) => {
        const copy = make("div", "chapter-copy");
        while (section.firstChild) copy.append(section.firstChild);
        const poster = make("aside", `chapter-poster poster-${String(index + 1).padStart(2, "0")}`, posters[index]);
        poster.setAttribute("aria-label", `${states[index].title}: ${states[index].signal}`);
        section.append(poster, copy);
      });
    }

    if (concept === "casefile") {
      hero.prepend(make("div", "case-identity", `<span>CASE 024-AOM</span><span>SYNTHETIC · NO PHI</span><span>REVIEW DRAFT</span>`));
      chapters.forEach((section, index) => {
        section.prepend(make("p", "case-tab", `File ${String(index + 1).padStart(2, "0")} · ${states[index].title}`));
        [...section.querySelectorAll("blockquote,.scroll")].forEach((exhibit, exhibitIndex) => {
          exhibit.dataset.exhibit = `EXHIBIT ${String(index + 1).padStart(2, "0")}.${exhibitIndex + 1}`;
        });
      });
    }

    const consolePanel = make("aside", "journey-console");
    consolePanel.dataset.stage = "0";
    consolePanel.setAttribute("aria-label", "Current evidence stage");
    consolePanel.innerHTML = `
      <header>
        <div><span>Stage 01 / 08</span><strong class="console-title">${states[0].title}</strong></div>
        <button type="button" class="console-toggle" aria-expanded="false" aria-controls="console-content">Open ledger</button>
      </header>
      <div class="console-content" id="console-content">
        <p class="case-number">CASE 024-AOM · SYNTHETIC</p>
        <div class="console-signal" aria-live="polite"><strong>${states[0].signal}</strong><span>${states[0].detail}</span></div>
        <dl class="case-ledger">
          <div><dt>Primary traces</dt><dd>140</dd></div>
          <div><dt>Models</dt><dd>10</dd></div>
          <div><dt>Decision-critical blanks</dt><dd>2</dd></div>
          <div><dt>Scoring passes</dt><dd>2 + adjudication</dd></div>
        </dl>
        <div class="console-progress" aria-hidden="true"><span></span></div>
      </div>`;
    readingShell.append(consolePanel);

    const consoleTitle = consolePanel.querySelector(".console-title");
    const consoleSignal = consolePanel.querySelector(".console-signal strong");
    const consoleDetail = consolePanel.querySelector(".console-signal span");
    const consoleStep = consolePanel.querySelector("header span");
    const consoleMeter = consolePanel.querySelector(".console-progress span");
    const navLinks = [...argumentMap.querySelectorAll("a")];
    const setStage = (index) => {
      const state = states[index];
      document.body.dataset.stage = String(index);
      consolePanel.dataset.stage = String(index);
      consoleTitle.textContent = state.title;
      consoleSignal.textContent = state.signal;
      consoleDetail.textContent = state.detail;
      consoleStep.textContent = `Stage ${String(index + 1).padStart(2, "0")} / 08`;
      consoleMeter.style.transform = `scaleX(${(index + 1) / states.length})`;
      navLinks.forEach((navLink, navIndex) => navLink.toggleAttribute("aria-current", navIndex === index));
    };
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (visible) setStage(chapters.indexOf(visible.target));
    }, { rootMargin: "-18% 0px -62% 0px", threshold: [0, .1, .35] });
    chapters.forEach((section) => observer.observe(section));
    setStage(0);

    const toggle = consolePanel.querySelector(".console-toggle");
    toggle.addEventListener("click", () => {
      const expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      toggle.textContent = expanded ? "Open ledger" : "Close ledger";
      consolePanel.classList.toggle("is-expanded", !expanded);
    });
  }

  const disclosure = [...articleBody.querySelectorAll("p")].find((p) => p.textContent.trim().startsWith("The experiment: one synthetic pediatric chart"));
  const methods = make("details", "methods");
  methods.innerHTML = `<summary>Methods, disclosure, and evidence packet</summary>`;
  if (disclosure) {
    const copy = make("div", "methods-copy", disclosure.innerHTML.replace("at [repo link]", 'in the <a href="../../index.html">local evidence packet</a>'));
    methods.append(copy, make("span", "packet-status", "Public repository link intentionally withheld until the packet is released."));
    const prior = disclosure.previousElementSibling;
    disclosure.remove();
    if (prior?.matches("hr")) prior.remove();
  }

  const endingSection = articleBody.querySelector("#the-four-second-question")?.closest(".chapter");
  if (endingSection) {
    const question = make("section", "final-question", "<p>The four-second habit</p><strong>Compared to whom?</strong>");
    readingShell.after(question, methods);
  } else {
    main.append(methods);
  }

  const updateProgress = () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    const ratio = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
    progress.firstElementChild.style.transform = `scaleX(${ratio})`;
  };
  let frame = 0;
  addEventListener("scroll", () => {
    if (frame) return;
    frame = requestAnimationFrame(() => {
      updateProgress();
      frame = 0;
    });
  }, { passive: true });
  addEventListener("resize", updateProgress, { passive: true });
  updateProgress();
})();
