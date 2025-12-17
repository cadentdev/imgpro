# From Bash to Python: Creating the ImgPro PRD


How we used AI to explore options, make architectural decisions, and create a comprehensive Product Requirements Document before writing any code.

---

## Introduction

Sometimes the best projects start with a simple question that leads you somewhere completely unexpected. We began by asking our AI assistant about testing tools for a bash script—and ended up creating an entirely new Python application with a comprehensive product roadmap. This article shows how a conversation with an AI coding assistant can help you explore options, challenge assumptions, and make better architectural decisions. You'll see that we didn't march straight toward our goal; instead, we wandered, questioned, and refined our thinking. That exploration process wasn't wasted time—it was essential to understanding what we really needed to build.

This article covers the first two commits in the ImgPro project:
- **Commit 1**: Initial commit (`.gitignore`, `LICENSE`, `README.md`)
- **Commit 2**: Create PRD (`PRD.md` and chat log documentation)

By the end, you'll see how we used AI assistance to move from "How do I test this bash script?" to a well-planned Python project—before writing a single line of code.

---

## The Starting Point: A Complex Bash Script

Our journey didn't start with Python. It started with a question about testing a complex bash script called `resize_images.sh`. This script handled image resizing for web projects, but it had several challenges:

- **External dependencies**: Required ImageMagick, GraphicsMagick, or macOS's `sips` tool
- **Platform inconsistencies**: Different tools behaved differently across systems
- **Testing complexity**: Bash scripts are notoriously difficult to test
- **Limited error handling**: Shell scripting has inherent limitations for robust error messages
- **Maintenance burden**: 300+ lines of bash with complex logic for tool detection and fallbacks

The original question to our AI assistant (Cascade, built into the Windsurf IDE) was: *"What do you recommend for bash script testing tools?"*

> **What is Windsurf?** Windsurf is an IDE based on VSCode that includes Cascade, an AI coding assistant. Cascade supports multiple AI models and can help with everything from architecture decisions to writing code. We also use Claude (both in the IDE and web versions) and other AI tools throughout development.

---

## The Exploration Process

### Step 1: Understanding the Testing Options

Cascade analyzed the bash script and recommended several testing frameworks:

1. **Bats (Bash Automated Testing System)** - Simple syntax, good for our use case
2. **ShellSpec** - More sophisticated with BDD-style syntax
3. **shUnit2** - Lightweight but older

This was helpful, but it led to a bigger question: *Should we even be using bash for this?*

### Step 2: Questioning the Approach

Instead of immediately diving into testing tools, we asked: *"What are the advantages and disadvantages of re-implementing this script in Python?"*

This is a key moment in AI-assisted development. **Don't just accept the first solution—ask your AI to help you evaluate alternatives.** The AI provided a detailed comparison:

**Python + Pillow Advantages:**
- Eliminate external dependencies (just `pip install pillow`)
- Better error handling with try/except blocks
- Cross-platform consistency
- Easier testing with pytest
- More maintainable code
- Larger developer community

**Python Disadvantages:**
- Potentially slower than native ImageMagick
- Requires Python runtime (not just bash)
- Higher memory usage for large images
- More setup for end users

> **Why Pillow?** Pillow is one of the most popular and widely supported Python image processing libraries. It's a friendly fork of PIL (Python Imaging Library) with excellent documentation and active maintenance.

### Step 3: Expanding the Vision

The conversation then took an interesting turn. We asked: *"Could I write a Python script that also included a web server?"*

This opened up new possibilities:
- A web interface for non-technical users
- Visual configuration and preview
- Batch processing with progress bars
- Mobile-friendly interface

But we didn't get distracted by the shiny new features. Instead, we focused on the **core use case**.

---

## Defining the Core Use Case

We explained our primary need:

> "I have a set of images for an 11ty-based website where I need to generate thumbnails for a 'lightbox' arrangement, then the same image at high resolution for full-screen display. I'd like to use the `img srcset` attribute to create a set of images at various resolutions."

This led to a specific example:

```bash
scale_image --width 300,600,900,1200 --input image_base_name.jpg --quality 90
```

Should create:
```
image_base_name_300.jpg
image_base_name_600.jpg
image_base_name_900.jpg
image_base_name_1200.jpg
```

**This is the moment where the project crystallized.** We had a clear, specific use case that would drive all our decisions.

---

## The Requirements Discovery Process

Instead of jumping straight to code, Cascade asked us **10 detailed questions** about requirements:

1. **Image Dimensions & Aspect Ratio**: Resize by width, height, or both? What about upscaling?
2. **Output Organization**: Where should files go? How should they be named?
3. **Input Handling**: Single file, multiple files, or directories?
4. **Image Format Support**: JPEG only, or multiple formats?
5. **Quality & Optimization**: How to handle quality settings? Strip EXIF data?
6. **Error Handling**: What happens when processing fails?
7. **Responsive Image Workflow**: Just create files, or generate HTML/JSON too?
8. **Performance & Feedback**: Progress bars? Verbose mode?
9. **Configuration & Presets**: Config files? Named presets?
10. **Future Extensibility**: What features might we add later?

**This is a best practice in software development**: Understand the requirements before writing code. The AI helped us think through edge cases and decisions we hadn't considered.

---

## Creating the Product Requirements Document (PRD)

After answering the questions, we asked Cascade to create a PRD. 

> **What is a PRD?** A Product Requirements Document (PRD) is a comprehensive specification that covers use cases, user personas, functional requirements, technical constraints, and future plans. Importantly, **a PRD should not include actual code**—it's about *what* to build and *why*, not *how* to implement it.

### Our PRD Structure

The PRD Cascade created included:

1. **Executive Summary** - One-paragraph overview of the tool
2. **Goals & Objectives** - What we're building and why
3. **User Personas** - Who will use this tool (web developers, content managers, social media managers)
4. **Functional Requirements** - Detailed specifications for each feature
5. **CLI Interface** - Command syntax and examples
6. **Error Handling** - How to handle failures gracefully
7. **Non-Functional Requirements** - Performance, compatibility, reliability
8. **Technical Constraints** - Dependencies and limitations
9. **Future Enhancements** - Roadmap for versions 1.1 through 2.0
10. **Open Questions** - Decisions still to be made

### Key Decisions Captured in the PRD

**Version 1.0 Scope (Minimal Viable Product):**
- Single file input only (batch processing in v1.1)
- JPEG only (other formats in v1.3)
- Resize by width OR height, not both (advanced modes in v1.2)
- Strip EXIF by default (preserve option in v1.4)
- Default quality of 90
- Output to `./resized/` directory by default

**Future Enhancements:**
- v1.1: Batch processing
- v1.2: Advanced resizing (crop modes, fit modes)
- v1.3: Format support (PNG, WebP, AVIF)
- v1.4: Metadata options
- v1.5: Responsive web features (generate HTML srcset)
- v1.6: Configuration files
- v2.0: Advanced features (watermarking, filters)

This phased approach meant we could ship something useful quickly while having a clear roadmap for future development.

---

## The Initial Commit: Setting Up the Repository

Before creating the PRD, we made our initial commit with three essential files:

### 1. `.gitignore`
A comprehensive Python `.gitignore` file that excludes:
- Python bytecode (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `.env`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`)
- Build artifacts

> **Why is `.gitignore` important?** Using a version control system like Git is essential when developing with AI agents! Git tracks changes, allows you to experiment safely, and makes collaboration possible. If you need help with Git, ask your AI assistant to guide you through the process.

### 2. `LICENSE`
We included an MIT License, which is:
- Permissive (allows commercial and private use)
- Simple and widely understood
- Compatible with most other licenses

### 3. `README.md`
A minimal README that would be expanded later. Starting with a README from day one is good practice—it forces you to articulate what your project is about.

---

## The Second Commit: Documenting the PRD and Process

The second commit added two critical files:

### 1. `PRD.md` (422 lines)
The comprehensive Product Requirements Document described above. This became our north star for development.

### 2. `devlog/bash_script_testing_tools.md` (492 lines)
This is the **complete chat log** from our conversation with Cascade. We saved this because:

- **Transparency**: Shows our thought process and decision-making
- **Reference**: We can review why we made certain choices
- **Learning**: Others can see how to use AI effectively for planning
- **Context**: Future contributors can understand the project's origins

**Saving your AI conversations is a best practice.** They provide valuable context and show your reasoning process.

---

## Key Lessons for AI-Assisted Development

### 1. Start with Questions, Not Code

We spent significant time exploring options and asking questions before writing any code. This prevented us from building the wrong thing.

### 2. Use AI to Evaluate Trade-offs

The AI helped us compare bash vs. Python objectively, listing pros and cons we might not have considered.

### 3. Define Requirements Before Implementation

The PRD gave us a clear specification to work from. This made subsequent development much more focused.

### 4. Embrace the Non-Linear Path

We started asking about bash testing tools and ended up creating a Python project with a web interface on the roadmap. That's okay! The exploration helped us find the right solution.

### 5. Document Your Decisions

Both the PRD and the saved chat log provide context for future work. When we (or others) come back to this project, we'll understand *why* we made these choices.

### 6. Version Your Requirements

By committing the PRD to Git, we can track how requirements evolve over time. This is especially valuable when working with AI, as you can reference specific versions of your requirements in future conversations.

### 7. Think in Phases

The PRD's versioned roadmap (v1.0, v1.1, etc.) gave us permission to ship something simple first, knowing we had a plan for future enhancements.

---

## What We Built in These Two Commits

Let's be clear: **We didn't write any actual code yet.** These two commits contain:

- Project infrastructure (`.gitignore`, `LICENSE`, `README.md`)
- A comprehensive PRD (422 lines)
- Documentation of our decision-making process (492 lines)

That's **914 lines of planning and documentation** before a single line of Python code.

This might seem like a lot of overhead, but it paid off in several ways:

1. **Clear direction**: We knew exactly what to build
2. **Scope control**: We defined what was in v1.0 and what wasn't
3. **Shared understanding**: Anyone reading the PRD would understand the project
4. **Decision record**: We documented *why* we chose Python over bash
5. **Future roadmap**: We had a clear plan for enhancements

---

## Tools and Techniques Used

### AI Tools
- **Cascade** (in Windsurf IDE): Primary AI assistant for exploration and planning
- **Claude**: Additional AI assistance (both IDE and web versions)

### Development Tools
- **Git**: Version control for tracking changes
- **Markdown**: Documentation format for PRD and chat logs
- **GitHub**: Repository hosting (planned for wiki)

### Methodologies
- **Requirements-driven development**: Define requirements before coding
- **Iterative exploration**: Ask questions, evaluate options, refine understanding
- **Documentation-first**: Write the PRD before the code
- **Version planning**: Define MVP and future enhancements upfront

---

## Next Steps

In the next article, we'll cover how we took this PRD and implemented the first version of the `imagepro` tool, including:

- Setting up the Python project structure
- Implementing the CLI with argparse
- Using Pillow for image processing
- Writing the resize functionality
- Testing our implementation

But for now, we have a solid foundation: a clear understanding of what we're building, why we're building it, and how it will evolve over time.

---

## Try It Yourself

If you're learning to develop with AI assistance, try this exercise:

1. **Think of a simple tool you'd like to build** (it doesn't have to be complex)
2. **Ask your AI assistant to help you explore options** (like we did with bash vs. Python)
3. **Have the AI ask you requirements questions** (prompt it to interview you about your use case)
4. **Create a simple PRD** (it doesn't need to be as detailed as ours)
5. **Save your chat log** (you'll appreciate having this context later)
6. **Commit everything to Git** (before writing any code)

This process will help you think through your project more clearly and give you a better foundation for development.

---

## Resources

- **ImgPro Repository**: [github.com/cadentdev/imagepro](https://github.com/cadentdev/imagepro)
- **Pillow Documentation**: [pillow.readthedocs.io](https://pillow.readthedocs.io/)
- **Windsurf IDE**: [codeium.com/windsurf](https://codeium.com/windsurf)
- **Git Basics**: Ask your AI assistant to teach you!

---

**Next Article**: [Part 2: Implementing the First Version - From PRD to Working Code](#) *(coming soon)*

---

*This article is part of our "Building in Public" series, where we document the entire development process of ImgPro, including the messy parts, the detours, and the lessons learned. We hope it helps you on your own coding journey!*
