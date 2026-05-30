---
name: codex-claude-academic-skills
description: Chinese-first academic research skills for paper writing, Office document generation, and scientific computing (MATLAB/Python)
triggers:
  - help me write a research paper in Chinese
  - generate academic PPT from my paper
  - create literature review Word document
  - run MATLAB simulation for my experiment
  - polish my paper abstract and introduction
  - make a thesis defense presentation
  - analyze scientific data with Python
  - respond to reviewer comments
---

# Codex Claude Academic Skills

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A collection of three complementary skills for Chinese academic researchers covering paper writing, academic Office document generation, and scientific computing. All skills work in both Claude Code and Codex platforms.

## What This Project Does

This project provides three specialized skills for academic workflows:

1. **research-writing-skill**: Paper writing, editing, and reviewer response in Chinese
2. **office-academic-skill**: Generate editable Word reports and PowerPoint presentations
3. **scientific-toolkit-skill**: Scientific computing with MATLAB/Python and publication-quality figures

The skills are designed to work together across the research pipeline: data analysis → paper writing → presentation generation.

## Installation

### For Claude Code

```bash
# Clone the repository
git clone https://github.com/zLanqing/codex-claude-academic-skills.git

# Install all three skills globally
cd codex-claude-academic-skills
cp -r research-writing-skill ~/.claude/skills/
cp -r office-academic-skill ~/.claude/skills/
cp -r scientific-toolkit-skill ~/.claude/skills/

# Or install via plugin (if supported)
/plugin install zLanqing/codex-claude-academic-skills
```

### For Codex

```bash
# Install to global skills directory
cd codex-claude-academic-skills
cp -r research-writing-skill ~/.codex/skills/
cp -r office-academic-skill ~/.codex/skills/
cp -r scientific-toolkit-skill ~/.codex/skills/

# Or load temporarily with plugin URL
codex --plugin-url https://github.com/zLanqing/codex-claude-academic-skills
```

### Project-Level Installation

Place skill directories in your project root:

```bash
mkdir -p .claude/skills/
cp -r path/to/research-writing-skill .claude/skills/

# Or for Codex
mkdir -p .codex/skills/
cp -r path/to/office-academic-skill .codex/skills/
```

## Skill 1: research-writing-skill

### Core Capabilities

- Write paper sections: abstract, introduction, related work, methods, experiments, discussion, conclusion
- Edit and polish existing drafts for logic, consistency, and terminology
- Generate reviewer response letters (rebuttal)
- Plan paper structure from vague ideas to detailed outlines

### Usage Patterns

**Writing a new section:**

```python
# User prompt example:
# "帮我写一个关于BOTDR传感器的方法章节，已有的实验数据在data.csv"

# The skill will:
# 1. Ask for key information (sensor parameters, measurement setup)
# 2. Check if data.csv exists and analyze it
# 3. Draft the methods section in Chinese
# 4. Preserve English terms: BOTDR, Brillouin scattering, etc.
# 5. Mark inferred vs. confirmed information
```

**Polishing existing text:**

```python
# User provides a Chinese draft:
"""
我们提出了一种新的算法，它很有效，实验结果显著优于传统方法。
"""

# Skill rewrites to:
"""
我们提出了基于小波去噪的 BGS 重构算法。在 100 组实验数据集上，
相比传统高斯拟合方法，本方法的温度测量误差从 ±2.5°C 降低至 ±0.8°C，
空间分辨率从 1m 提升至 0.5m。
"""
# (Removes vague words, adds measurable baselines)
```

**Reviewer response:**

```python
# User: "审稿人说我的实验样本量不够，帮我回复"

# Skill generates structured response:
"""
**Reviewer Comment:**
The sample size (n=30) is insufficient for statistical significance.

**Response:**
感谢审稿人的建议。我们已补充实验至 n=100（新增数据见附录 A）。
更新后的统计检验结果（t-test, p<0.01）已添加至第 4.2 节表 3。
修订稿中已说明样本量选择依据 Cohen's d 效应量计算（d=0.85, power=0.95）。

**Changes in manuscript:**
- Line 203-205: 补充样本量计算依据
- Table 3: 更新统计检验结果
- Appendix A: 新增 70 组实验数据
"""
```

### Key Principles

- **Chinese-first**: Explanations, body text in Chinese; preserve English for paper titles, formulas, variable names, software commands, citations
- **No fabrication**: Never invent DOI, journal names, experimental values, or figure numbers
- **Source marking**: Label claims as "from user", "inferred", "suggested extension", or "original text"
- **Measurable claims**: Replace "significant improvement" with "error reduced from X to Y"

### Reference Files

The skill includes built-in references under `paper-writing/`:

```
references/
├── section_rhetorical_moves/
│   ├── abstract.md          # IMRaD structure for abstracts
│   ├── introduction.md      # Hook → Gap → Contribution pattern
│   ├── methods.md           # Replicability checklist
│   └── results.md           # Figure-first narrative
├── writing_checklists/
│   ├── before_submission.md # Pre-submission self-check
│   └── revision_guide.md    # Responding to major revisions
├── figure_templates/
│   └── multi_panel.md       # Standards for composite figures
└── brainstorming_guide.md   # From idea to paper blueprint
```

## Skill 2: office-academic-skill

### Core Capabilities

**Word Documents:**
- PDF → structured literature review report (.docx)
- Generate editable reports with headings, tables, figure placeholders, citations
- Version-controlled editing of existing .docx files

**PowerPoint Presentations:**
- Literature report slides, group meeting presentations
- Thesis defense slides (proposal, mid-term, final defense)
- Scientific poster presentations, outreach slides

### Usage Patterns

**Generate literature report from PDF:**

```python
# User: "把这篇论文转成文献阅读报告"
# Uploads: paper.pdf

# Skill workflow:
# 1. Extract text and figures from PDF
# 2. Generate structured report.docx:

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Title
title = doc.add_heading('文献阅读报告', level=1)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Metadata section
doc.add_heading('基本信息', level=2)
table = doc.add_table(rows=4, cols=2)
table.cell(0, 0).text = '标题'
table.cell(0, 1).text = 'Distributed Optical Fiber Sensing Using BOTDR'
table.cell(1, 0).text = '作者'
table.cell(1, 1).text = 'Zhang, Y., et al.'
table.cell(2, 0).text = '期刊'
table.cell(2, 1).text = 'J. Lightwave Tech., 2023, 41(5), 1234-1245'
table.cell(3, 0).text = 'DOI'
table.cell(3, 1).text = '10.1109/JLT.2023.1234567'

# Main sections
doc.add_heading('研究背景', level=2)
doc.add_paragraph('【来源: 论文第1节】分布式光纤传感技术...')

doc.add_heading('核心方法', level=2)
doc.add_paragraph('【来源: 论文图2及第3.1节】本文提出...')
doc.add_paragraph('[图2占位符: BOTDR系统示意图]')

doc.add_heading('实验结果', level=2)
doc.add_paragraph('【来源: 论文表1】在50km光纤上测试...')

doc.add_heading('个人评价', level=2)
doc.add_paragraph('【评价】优点: 空间分辨率达到0.5m；局限: 仅测试单模光纤...')

doc.save('文献报告_BOTDR_2023.docx')
```

**Create thesis defense PPT:**

```python
# User: "用我的论文PDF生成答辩PPT，用学校模板template.pptx"

# Skill workflow:
from pptx import Presentation
from pptx.util import Inches, Pt

# 1. Clone template master slides
template = Presentation('template.pptx')
prs = Presentation()
prs.slide_master = template.slide_master  # Preserve school branding

# 2. Extract paper structure
# Reads paper.pdf → sections, figures, key results

# 3. Generate slides with action titles
slide = prs.slides.add_slide(prs.slide_layouts[1])
title = slide.shapes.title
title.text = 'BOTDR空间分辨率提升至0.5m'  # Conclusion, not topic

# Add figure placeholder
left = Inches(1)
top = Inches(2)
pic_placeholder = slide.shapes.add_textbox(left, top, Inches(8), Inches(4))
pic_placeholder.text = '[插入论文图3: 分辨率对比实验结果]'

# Add source annotation
source = slide.shapes.add_textbox(Inches(0.5), Inches(6.5), Inches(9), Inches(0.3))
source.text = '数据来源: 论文第4.2节, 表2'
source.text_frame.paragraphs[0].font.size = Pt(10)

prs.save('答辩PPT_初稿.pptx')

# 4. Run overflow check (built-in script)
# python references/thesis-defense-pptx/scripts/check_text_overflow.py 答辩PPT_初稿.pptx
```

**Edit existing PowerPoint:**

```python
# User: "把第5页的标题改成中文，图表移到右边"

from pptx import Presentation

prs = Presentation('答辩PPT_初稿.pptx')
slide = prs.slides[4]  # 0-indexed

# Change title
slide.shapes.title.text = '实验验证与结果分析'

# Move figure to right half
for shape in slide.shapes:
    if shape.has_text_frame and '[插入论文图' in shape.text:
        shape.left = Inches(5)
        shape.top = Inches(1.5)
        shape.width = Inches(4)

prs.save('答辩PPT_修订.pptx')
```

### PPT Quality Standards

The skill enforces these rules:

1. **Action titles**: "温度测量误差降低60%" not "实验结果"
2. **One idea per slide**: No bullet-point essays
3. **Figure-driven**: Technical claims backed by charts/equations
4. **Scientific rigor**: Axes labels, units, legends, data sources
5. **Academic aesthetics**: White/neutral backgrounds, color for emphasis only

### Built-in Tools

Under `references/`:

```
office-docx/
├── ooxml_validator.py       # Check DOCX against Office Open XML schema
└── schemas/                 # XSD schemas for validation

office-pptx/
├── pptx_structure.md        # PPTX OOXML anatomy
└── layout_examples/         # Common academic slide layouts

thesis-defense-pptx/scripts/
├── extract_thesis_context.py   # Parse LaTeX/PDF for key content
├── clone_template.py           # Preserve master slide styles
├── export_slides_png.py        # Slide → PNG for review
└── check_text_overflow.py      # Detect text box overflow
```

## Skill 3: scientific-toolkit-skill

### Core Capabilities

**MATLAB/Octave:**
- Signal/image processing, FFT, filtering, matrix operations
- Simulation, numerical methods
- Publication-quality figure export

**Python Scientific Stack:**
- **NumPy, SciPy**: Numerical computing, optimization
- **pandas**: Data manipulation and analysis
- **matplotlib, seaborn**: Publication-grade plots
- **scikit-learn**: Machine learning (classification, regression, clustering, PCA)
- **statsmodels**: Statistical modeling, time series
- **SymPy**: Symbolic math, equation derivation
- **QuTiP**: Quantum optics simulations
- **pymatgen**: Materials science (crystal structures, band structure)
- **TimesFM**: Time series forecasting
- **NetworkX**: Graph and network analysis
- **Astropy**: Astronomical/optical imaging data

**Literature & Citations:**
- Search: arXiv, PubMed, CrossRef, Semantic Scholar, OpenAlex
- DOI → BibTeX conversion, citation validation

### Usage Patterns

**MATLAB signal processing:**

```matlab
% User: "帮我用MATLAB分析这个BOTDR信号，提取BGS并计算温度"

% Skill generates:
% === BOTDR Signal Analysis ===
% Parameters (用户需确认):
fs = 1e9;              % 采样率 [Hz] - 来源: 用户确认
fiber_length = 50e3;   % 光纤长度 [m] - 来源: 用户确认
v_B0 = 10.86e9;        % 参考Brillouin频移 [Hz] - 来源: 文献默认值 (SMF-28)
C_T = 1.0e6;           % 温度系数 [Hz/°C] - 来源: 文献默认值

% Load signal
data = load('botdr_signal.mat');
raw_signal = data.raw;  % [时间 x 频率扫描]

% Extract BGS (Brillouin Gain Spectrum)
[n_points, n_freq] = size(raw_signal);
freq_axis = linspace(10.5e9, 11.5e9, n_freq);  % 频率扫描范围 [Hz]

BGS_peak_freq = zeros(n_points, 1);
for i = 1:n_points
    [~, peak_idx] = max(raw_signal(i, :));
    BGS_peak_freq(i) = freq_axis(peak_idx);
end

% Convert to temperature
delta_v_B = BGS_peak_freq - v_B0;  % 频移差 [Hz]
temperature = delta_v_B / C_T;      % 温度 [°C]

% Calculate spatial resolution
spatial_res = 0.5 * 3e8 / fs;  % = c/(2*fs) [m]

% Plot results
figure('Position', [100, 100, 800, 600]);

subplot(2,1,1);
plot(1:n_points, BGS_peak_freq/1e9, 'LineWidth', 1.5);
xlabel('测量点', 'FontSize', 12);
ylabel('Brillouin频移 (GHz)', 'FontSize', 12);
title('沿光纤的BGS频移分布', 'FontSize', 14);
grid on;

subplot(2,1,2);
plot((1:n_points)*spatial_res/1000, temperature, 'LineWidth', 1.5);
xlabel('距离 (km)', 'FontSize', 12);
ylabel('温度 (°C)', 'FontSize', 12);
title(sprintf('温度分布 (空间分辨率: %.2f m)', spatial_res), 'FontSize', 14);
grid on;

% Export figure for paper
print('BGS_temperature_profile.png', '-dpng', '-r300');

% 【注释】未编造数据，所有物理量已标注来源
```

**Python data analysis with scikit-learn:**

```python
# User: "用机器学习分类这些光谱数据，特征在features.csv，标签在labels.csv"

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
features = pd.read_csv('features.csv')  # 假设每行是一个光谱样本
labels = pd.read_csv('labels.csv').values.ravel()

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42, stratify=labels
)

# Preprocessing
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model training with grid search
param_grid = {
    'C': [0.1, 1, 10, 100],
    'gamma': ['scale', 'auto', 0.001, 0.01],
    'kernel': ['rbf', 'linear']
}

svm = SVC(random_state=42)
grid_search = GridSearchCV(svm, param_grid, cv=5, scoring='f1_macro', n_jobs=-1)
grid_search.fit(X_train_scaled, y_train)

# Best model
best_model = grid_search.best_estimator_
print(f"最佳参数: {grid_search.best_params_}")
print(f"交叉验证F1分数: {grid_search.best_score_:.3f}")

# Evaluate on test set
y_pred = best_model.predict(X_test_scaled)
print("\n测试集分类报告:")
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=np.unique(labels), 
            yticklabels=np.unique(labels))
plt.xlabel('预测标签', fontsize=12)
plt.ylabel('真实标签', fontsize=12)
plt.title('混淆矩阵 (SVM分类器)', fontsize=14)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300)

# 【注释】模型参数通过网格搜索确定，避免主观设定
# 【注释】数据来源: features.csv, labels.csv (用户提供)
```

**Publication-quality matplotlib figure:**

```python
# User: "生成一个双Y轴图，左边是温度，右边是应变"

import matplotlib.pyplot as plt
import numpy as np

# 【用户需提供】实际数据
distance = np.linspace(0, 50, 100)  # km
temperature = 25 + 5*np.sin(2*np.pi*distance/10)  # °C - 示例数据
strain = 100 + 50*np.cos(2*np.pi*distance/15)    # με - 示例数据

# Create figure with publication settings
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'Arial',
    'axes.linewidth': 1.2,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'lines.linewidth': 1.5
})

fig, ax1 = plt.subplots(figsize=(7, 4))

# Left y-axis: Temperature
color_temp = 'tab:red'
ax1.set_xlabel('Distance (km)', fontsize=12)
ax1.set_ylabel('Temperature (°C)', color=color_temp, fontsize=12)
line1 = ax1.plot(distance, temperature, color=color_temp, label='Temperature')
ax1.tick_params(axis='y', labelcolor=color_temp)
ax1.grid(True, alpha=0.3)

# Right y-axis: Strain
ax2 = ax1.twinx()
color_strain = 'tab:blue'
ax2.set_ylabel('Strain (με)', color=color_strain, fontsize=12)
line2 = ax2.plot(distance, strain, color=color_strain, linestyle='--', label='Strain')
ax2.tick_params(axis='y', labelcolor=color_strain)

# Combined legend
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', frameon=True, fontsize=10)

plt.title('Temperature and Strain Distribution along Fiber', fontsize=13, pad=10)
plt.tight_layout()
plt.savefig('dual_axis_plot.pdf', dpi=300, bbox_inches='tight')
plt.savefig('dual_axis_plot.png', dpi=300, bbox_inches='tight')

# 【注释】图表符合期刊要求: 矢量PDF + 高分辨率PNG备份
```

**DOI to BibTeX:**

```python
# User: "把这个DOI转成BibTeX: 10.1109/JLT.2023.1234567"

import requests

doi = "10.1109/JLT.2023.1234567"
url = f"https://doi.org/{doi}"
headers = {"Accept": "application/x-bibtex"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    bibtex = response.text
    print(bibtex)
    
    # Save to file
    with open('reference.bib', 'w', encoding='utf-8') as f:
        f.write(bibtex)
else:
    print(f"错误: 无法获取DOI {doi} 的元数据 (状态码: {response.status_code})")
    
# 【注释】不编造BibTeX，仅从DOI.org获取真实元数据
```

### Domain Focus

The skill is optimized for:

- Optics, optoelectronics, optical communications, fiber sensing
- BOTDR/BOTDA, Brillouin gain spectrum (BGS), stimulated scattering
- Spectroscopy, detector data, sensor time series
- Calibration, uncertainty quantification

### Reference Documentation

Over 20 sub-modules under `references/scientific-skills/`:

```
matlab_octave/
├── signal_processing.md     # FFT, filtering, convolution
├── figure_export.md         # Export settings for journals
└── numerical_methods.md     # ODE solvers, optimization

python_libraries/
├── matplotlib_templates.md  # Plot styles for Nature/IEEE
├── sklearn_workflows.md     # ML pipelines, hyperparameter tuning
├── statsmodels_guide.md     # Regression, ANOVA, time series
└── scipy_optimization.md    # Curve fitting, global optimization

literature_tools/
├── arxiv_search.md          # API usage, metadata extraction
├── crossref_api.md          # DOI resolution, citation data
└── bibtex_management.md     # Parsing, validation, deduplication
```

## Cross-Skill Workflows

### Example 1: Complete Research Pipeline

```python
# Step 1: Data analysis (scientific-toolkit-skill)
# User: "分析BOTDR数据并生成温度分布图"
# → Generates: temperature_profile.png, analysis_results.csv

# Step 2: Write paper (research-writing-skill)
# User: "用这个图写实验结果章节"
# → Drafts: results_section.md (Chinese, with figure reference)

# Step 3: Create presentation (office-academic-skill)
# User: "把结果章节做成答辩PPT"
# → Generates: defense_slides.pptx (includes temperature_profile.png)
```

### Example 2: Literature to Presentation

```python
# Step 1: Extract literature (office-academic-skill)
# User: "把这5篇PDF转成综述Word文档"
# → Generates: literature_review.docx

# Step 2: Create group meeting slides (office-academic-skill)
# User: "用综述做组会PPT"
# → Generates: group_meeting.pptx (with citations)

# Step 3: Prepare speaker notes (research-writing-skill)
# User: "给每页PPT写讲稿"
# → Adds speaker notes in Chinese to group_meeting.pptx
```

## Configuration

### Environment Variables

```bash
# For literature search APIs (optional)
export SEMANTIC_SCHOLAR_API_KEY=your_key_here
export PUBMED_API_KEY=your_key_here

# For figure export paths
export PAPER_FIGURES_DIR=./figures

# For Office document templates
export PPT_TEMPLATE_PATH=./templates/school_template.pptx
export WORD_TEMPLATE_PATH=./templates/report_template.docx
```

### Skill Configuration Files

Each skill includes a `SKILL.md` with customizable parameters:

```yaml
# research-writing-skill/SKILL.md
defaults:
  language: zh-CN
  preserve_english: true
  evidence_labels: true
  allow_fabrication: false

# office-academic-skill/SKILL.md
ppt_standards:
  action_titles: true
  one_idea_per_slide: true
  max_text_length: 50  # words per text box
  require_sources: true

# scientific-toolkit-skill/SKILL.md
plotting:
  default_dpi: 300
  default_format: [pdf, png]
  font_family: Arial
  color_scheme: scientific
```

## Common Patterns

### Pattern 1: Annotate Data Sources

All three skills mark information origins:

```python
# In Word reports:
"【来源: 论文图3】空间分辨率为0.5m"

# In Python code comments:
# 【来源: 用户确认】采样率 fs = 1e9 Hz

# In paper text:
"温度系数取 1.0 MHz/°C（文献默认值，参考[3]）"
```

### Pattern 2: Avoid Fabrication

```python
# ❌ Wrong:
"根据Smith et al. (2020, doi:10.xxxx/made_up) 的研究..."

# ✅ Correct:
"【需要补充引用】根据文献，BOTDR温度系数通常为1.0 MHz/°C"
"【建议用户确认】该结论需要文献支持，请提供DOI或论文PDF"
```

### Pattern 3: Chinese Explanations, English Technicalities

```python
# In paper:
"本文提出了基于 wavelet denoising 的 Brillouin gain spectrum (BGS) 重构方法。"
# 中文句子 + English method names

# In code:
# 使用 Savitzky-Golay filter 平滑信号
signal_smooth = savgol_filter(signal, window_length=11, polyorder=3)

# In PPT:
slide.title.text = "基于小波去噪的BGS重构算法"  # Chinese title
# Figure caption: "Wavelet denoising results (db4, level 3)"  # English caption
```

## Troubleshooting

### Issue: Skills Not Loaded

```bash
# Check skill directories exist
ls ~/.claude/skills/research-writing-skill
ls ~/.codex/skills/office-academic-skill

# Verify SKILL.md is present
cat ~/.claude/skills/scientific-toolkit-skill/SKILL.md

# Reload skills (platform-specific)
/reload skills  # In Claude Code
codex --reload-skills  # In Codex CLI
```

### Issue: MATLAB Code Not Running

```bash
# Check Octave compatibility (if MATLAB not available)
octave --version

# Install signal processing package (Octave)
octave --eval "pkg install -forge signal"
octave --eval "pkg load signal"

# Run MATLAB script with Octave
octave --eval "run('botdr_analysis.m')"
```

### Issue: Python Package Missing

```bash
# Install scientific stack
pip install numpy scipy pandas matplotlib seaborn scikit-learn statsmodels

# For quantum optics
pip install qutip

# For materials science
pip install pymatgen

# For time series forecasting
pip install timesfm

# Verify imports
python -c "import matplotlib; import sklearn; import statsmodels; print('OK')"
```

### Issue: PowerPoint Text Overflow

```bash
# Use built-in overflow checker
cd ~/.claude/skills/office-academic-skill/references/thesis-defense-pptx/scripts
python check_text_overflow.py /path/to/presentation.pptx

# Output shows slides with overflowing text boxes
# Slide 5, Shape "TextBox 3": Text exceeds box by 12 lines

# Fix: Reduce text or enlarge box
from pptx import Presentation
prs = Presentation('presentation.pptx')
slide = prs.slides[4]
shape = slide.shapes[2]  # TextBox 3
shape.height = Inches(3)  # Increase height
prs.save('presentation_fixed.pptx')
```

### Issue: DOI Lookup Fails

```python
# Fallback to manual BibTeX
# If DOI API is down, use CrossRef REST API

import requests

doi = "10.1109/JLT.2023.1234567"
url = f"https://api.crossref.org/works/{doi}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()['message']
    # Extract metadata manually
    author = data['author'][0]['family']
    title = data['title'][0]
    print(f"Author: {author}, Title: {title}")
else:
    print("【建议】请手动从期刊网站复制BibTeX条目")
```

### Issue: Figure Quality Too Low

```python
# For MATLAB: Increase export resolution
print('figure.png', '-dpng', '-r600');  % 600 DPI for print

# For Python: Use vector formats
plt.savefig('figure.pdf', format='pdf', bbox_inches='tight')  # Vector
plt.savefig('figure.eps', format='eps', bbox_inches='tight')  # For LaTeX

# Check font embedding (for journals)
import matplotlib
