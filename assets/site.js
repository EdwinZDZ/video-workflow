/* Video Workflow — showcase behaviour
   视频工作流 — 展示页交互
   No dependencies. State lives in one object; both the specimen and the
   coverage explorer read from it. */

(function () {
  "use strict";

  var kit = window.FONTKIT;
  if (!kit) {
    return;
  }

  var FAMILY_META = {
    Inter: {
      roleEn: "Interface and captions",
      roleZh: "界面与字幕",
      sample: "Every lesson deserves a clear voice.",
      noteEn: "Neutral grotesque with a generous x-height. The default for captions, UI and anything that has to stay legible at 24 px.",
      noteZh: "中性无衬线，字腔开阔。字幕、界面，以及所有必须在 24 px 仍清晰可读的文字，都从它开始。",
      slug: "inter",
    },
    Lora: {
      roleEn: "Editorial and quotations",
      roleZh: "编辑排版与引文",
      sample: "Slow down. Explain it properly.",
      noteEn: "A serif with brush roots. Use it for the one sentence you want the viewer to remember, not for running text.",
      noteZh: "带毛笔笔意的衬线体。留给那句希望观众记住的话，而不是大段正文。",
      slug: "lora",
    },
    Oswald: {
      roleEn: "Titles and lower thirds",
      roleZh: "标题与下三分之一",
      sample: "MAKE IT CLEAR",
      noteEn: "Condensed display: a big voice in a small horizontal footprint. Built for titles that must not crowd the frame.",
      noteZh: "压缩展示体：声量大、占地小。适合不能挤占画面的标题与下三分之一。",
      slug: "oswald",
    },
    Caveat: {
      roleEn: "Annotations and callouts",
      roleZh: "批注与提示",
      sample: "watch this part",
      noteEn: "Handwritten and informal, one step away from the script. Pairs with an arrow, never with a paragraph.",
      noteZh: "手写、非正式，像是从讲稿边上长出来的。配箭头使用，不要配整段文字。",
      slug: "caveat",
    },
    "IBM Plex Mono": {
      roleEn: "Code and terminal",
      roleZh: "代码与终端",
      sample: "npm run captions -- --lang zh",
      noteEn: "Monospaced with a 0.6 em advance. Commands, filenames and timecodes line up without manual spacing.",
      noteZh: "等宽字体，0.6 em 字宽。命令、文件名与时间码天然对齐，不必手工加空格。",
      slug: "ibmplexmono",
    },
  };

  var BLOCKS = [
    { id: "basic-latin", label: "Basic Latin", zh: "基本拉丁", range: "U+0020–007E" },
    { id: "latin-1", label: "Latin-1 Supplement", zh: "拉丁-1 补充", range: "U+00A0–00FF" },
    { id: "latin-ext-a", label: "Latin Extended-A", zh: "拉丁扩展-A", range: "U+0100–017F" },
    { id: "greek", label: "Greek and Coptic", zh: "希腊与科普特", range: "U+0370–03FF" },
    { id: "cyrillic", label: "Cyrillic", zh: "西里尔", range: "U+0400–04FF" },
    { id: "cjk", label: "CJK Unified Ideographs", zh: "中日韩统一表意文字", range: "U+4E00–9FFF" },
  ];

  var CJK_SAMPLE = "中文字幕示例第一课你好世界";

  var state = {
    family: "Inter",
    weight: "Regular",
    size: 76,
    block: "basic-latin",
  };

  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function familyByName(name) {
    return kit.families.filter(function (family) {
      return family.name === name;
    })[0];
  }

  function latinCore(family) {
    return (
      family.blocks["basic-latin"].covered +
      family.blocks["latin-1"].covered +
      family.blocks["latin-ext-a"].covered
    );
  }

  function formatBytes(bytes) {
    if (bytes >= 1024 * 1024) {
      return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    }
    return Math.round(bytes / 1024) + " KB";
  }

  function familyStack(name) {
    return '"' + name + '", "PingFang SC", "Microsoft YaHei", "Noto Sans SC", sans-serif';
  }

  function blockById(id) {
    return BLOCKS.filter(function (block) {
      return block.id === id;
    })[0];
  }

  function buildStack() {
    var host = $("#stackList");
    if (!host) {
      return;
    }
    kit.families.forEach(function (family, index) {
      var meta = FAMILY_META[family.name];
      var button = document.createElement("button");
      button.type = "button";
      button.dataset.family = family.name;
      button.innerHTML =
        '<span class="idx">0' + (index + 1) + "</span>" +
        '<span class="face"></span>' +
        '<span class="role"></span>';
      var face = button.querySelector(".face");
      face.textContent = family.name;
      face.style.fontFamily = familyStack(family.name);
      button.querySelector(".role").textContent = meta.roleEn;
      button.addEventListener("click", function () {
        selectFamily(family.name);
        var section = $("#type");
        if (section) {
          section.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
      host.appendChild(button);
    });
  }

  function buildFamilyList() {
    var host = $("#familyList");
    if (!host) {
      return;
    }
    kit.families.forEach(function (family, index) {
      var meta = FAMILY_META[family.name];
      var button = document.createElement("button");
      button.type = "button";
      button.dataset.family = family.name;
      button.setAttribute("aria-pressed", family.name === state.family ? "true" : "false");
      button.innerHTML =
        '<span class="idx">0' + (index + 1) + "</span>" +
        '<span class="name"></span>' +
        '<span class="role">' + meta.roleEn + '<br><span class="zh" lang="zh-CN">' + meta.roleZh + "</span></span>";
      var name = button.querySelector(".name");
      name.textContent = family.name;
      name.style.fontFamily = familyStack(family.name);
      button.addEventListener("click", function () {
        selectFamily(family.name);
      });
      host.appendChild(button);
    });
  }

  function selectFamily(name) {
    var family = familyByName(name);
    if (!family) {
      return;
    }
    var meta = FAMILY_META[name];
    state.family = name;
    state.weight = "Regular";

    document.querySelectorAll("#familyList button").forEach(function (button) {
      button.setAttribute("aria-pressed", button.dataset.family === name ? "true" : "false");
    });

    var stageName = $("#stageName");
    stageName.textContent = name;
    stageName.style.fontFamily = familyStack(name);

    $("#stageRole").innerHTML = meta.roleEn + ' <span class="zh" lang="zh-CN">' + meta.roleZh + "</span>";

    var bytes = family.files.reduce(function (total, file) {
      return total + file.bytes;
    }, 0);
    $("#stageMeta").innerHTML =
      "<b>" + family.files.length + "</b> files · " + formatBytes(bytes) + "<br>" +
      "400 / 700 · " + family.files[0].license + "<br>" +
      "Latin " + latinCore(family) + "/319 · CJK 0";

    $("#noteEn").textContent = meta.noteEn;
    $("#noteZh").textContent = meta.noteZh;

    $("#previewInput").value = meta.sample;
    $("#previewText").textContent = meta.sample;

    var regular = family.files.filter(function (file) {
      return file.style === "Regular";
    })[0] || family.files[0];
    var bold = family.files.filter(function (file) {
      return file.style === "Bold";
    })[0] || regular;

    $("#downloadRegular").href = "fonts/" + regular.file;
    $("#downloadBold").href = "fonts/" + bold.file;
    $("#specimenLink").href = "docs/previews/specimen-" + meta.slug + ".png";

    document.querySelectorAll(".weights button").forEach(function (button) {
      button.setAttribute("aria-pressed", button.dataset.weight === "Regular" ? "true" : "false");
    });

    renderPreview();
    renderCoverage();
    renderGlyphs();
    renderTable();
  }

  function renderPreview() {
    var family = familyByName(state.family);
    var meta = FAMILY_META[state.family];
    var weightClass = state.weight === "Bold" ? 700 : 400;
    var text = $("#previewInput").value || meta.sample;

    var preview = $("#previewText");
    preview.textContent = text;
    preview.style.fontFamily = familyStack(state.family);
    preview.style.fontWeight = String(weightClass);
    preview.style.fontSize = state.size + "px";

    $("#sizeValue").value = state.size;
    $("#sizeValue").textContent = state.size;
    $("#previewSpec").textContent = state.family + " — " + state.weight + " " + weightClass;
    $("#previewCoverage").textContent = "LATIN " + latinCore(family) + "/319 · CJK 0";
  }

  function renderTable() {
    var body = $("#fontTable tbody");
    if (!body) {
      return;
    }
    body.innerHTML = "";
    kit.families.forEach(function (family) {
      family.files.forEach(function (file) {
        var row = document.createElement("tr");
        var latin = latinCore(family);
        row.innerHTML =
          '<td class="file"><a href="fonts/' + file.file + '" download>' + file.file + "</a></td>" +
          "<td>" + family.name + "</td>" +
          '<td class="num">' + file.weightClass + "</td>" +
          '<td class="num">' + formatBytes(file.bytes) + "</td>" +
          '<td class="num">' + file.glyphs.toLocaleString("en-US") + "</td>" +
          '<td class="num">' + file.mapped.toLocaleString("en-US") + "</td>" +
          '<td class="num">' + latin + "/319</td>" +
          '<td class="num"><span class="pill accent">0</span></td>' +
          '<td><span class="pill">' + file.license + "</span></td>";
        body.appendChild(row);
      });
    });
  }

  function renderCoverage() {
    var host = $("#coverageTable");
    if (!host) {
      return;
    }
    var family = familyByName(state.family);
    var head =
      '<div class="row head"><span>Block / 区块</span><span>Coverage / 覆盖率</span><span>Count / 字数</span></div>';
    var rows = BLOCKS.map(function (block) {
      var data = family.blocks[block.id];
      var zero = data.covered === 0;
      var pct = ((data.covered / data.total) * 100).toFixed(1);
      var value = zero
        ? '<span class="pill accent">0</span>/' + data.total.toLocaleString("en-US")
        : "<b>" + data.covered + "</b>/" + data.total.toLocaleString("en-US");
      return (
        '<div class="row">' +
        '<div class="face block">' + block.label + "<small>" + block.zh + " · " + block.range + "</small></div>" +
        '<div class="bar' + (zero ? " zero" : "") + '" role="img" aria-label="' + pct + ' percent"><i style="width:' + pct + '%"></i></div>' +
        '<div class="value">' + value + "</div>" +
        "</div>"
      );
    }).join("");
    host.innerHTML = head + rows;
  }

  function buildTabs() {
    var host = $("#blockTabs");
    if (!host) {
      return;
    }
    BLOCKS.forEach(function (block) {
      var button = document.createElement("button");
      button.type = "button";
      button.setAttribute("role", "tab");
      button.dataset.block = block.id;
      button.textContent = block.label.replace(" Supplement", "").replace(" Unified Ideographs", "");
      button.title = block.label + " / " + block.zh;
      button.setAttribute("aria-selected", block.id === state.block ? "true" : "false");
      button.addEventListener("click", function () {
        state.block = block.id;
        document.querySelectorAll("#blockTabs button").forEach(function (tab) {
          tab.setAttribute("aria-selected", tab.dataset.block === block.id ? "true" : "false");
        });
        renderGlyphs();
      });
      host.appendChild(button);
    });
  }

  function renderGlyphs() {
    var family = familyByName(state.family);
    var block = blockById(state.block);
    var grid = $("#glyphGrid");
    var data = family.blocks[state.block];
    var note = $("#fallbackNote");

    grid.innerHTML = "";
    grid.classList.remove("fallback");
    $("#glyphTitle").textContent = block.label + " · " + block.zh;

    if (state.block === "cjk") {
      note.hidden = false;
      grid.classList.add("fallback");
      CJK_SAMPLE.split("").forEach(function (char) {
        var cell = document.createElement("span");
        cell.textContent = char;
        cell.style.fontFamily = familyStack(state.family);
        grid.appendChild(cell);
      });
      $("#glyphCount").textContent = "0 / " + data.total.toLocaleString("en-US") + " · fallback";
      return;
    }

    note.hidden = true;
    var chars = family.chars[state.block] || [];
    chars.forEach(function (cp) {
      if (cp === 0x20 || cp === 0xa0) {
        return;
      }
      var cell = document.createElement("span");
      cell.textContent = String.fromCodePoint(cp);
      cell.style.fontFamily = familyStack(state.family);
      cell.title = "U+" + cp.toString(16).toUpperCase().padStart(4, "0");
      grid.appendChild(cell);
    });
    $("#glyphCount").textContent = data.covered + " / " + data.total;
  }

  function bindControls() {
    $("#previewInput").addEventListener("input", function (event) {
      $("#previewText").textContent = event.target.value || FAMILY_META[state.family].sample;
    });

    $("#sizeRange").addEventListener("input", function (event) {
      state.size = Number(event.target.value);
      renderPreview();
    });

    document.querySelectorAll(".weights button").forEach(function (button) {
      button.addEventListener("click", function () {
        state.weight = button.dataset.weight;
        document.querySelectorAll(".weights button").forEach(function (other) {
          other.setAttribute("aria-pressed", other === button ? "true" : "false");
        });
        renderPreview();
      });
    });
  }

  function bindScrollState() {
    var header = $(".site-header");
    var links = Array.prototype.slice.call(document.querySelectorAll('.nav a[href^="#"]'));
    var sections = links.map(function (link) {
      return document.querySelector(link.getAttribute("href"));
    }).filter(Boolean);

    function onScroll() {
      if (header) {
        header.classList.toggle("is-scrolled", window.scrollY > 8);
      }
      var current = "";
      sections.forEach(function (section) {
        if (section.getBoundingClientRect().top <= 140) {
          current = "#" + section.id;
        }
      });
      links.forEach(function (link) {
        link.classList.toggle("is-active", link.getAttribute("href") === current);
      });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  buildStack();
  buildFamilyList();
  buildTabs();
  bindControls();
  bindScrollState();
  selectFamily("Inter");
})();
