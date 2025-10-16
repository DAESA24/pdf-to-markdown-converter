# Claude Code Configuration - Podcast Processor CLI Tool

## Project Context

**Project Name**: podcast-processor-cli-tool
**Development Method**: BMAD (Breakthrough Method for AI-driven Agile Development)
**Framework**: Pydantic AI (Production-ready Python agent framework)
**Current Phase**: Planning - Ready for BMAD Implementation

## Project Overview

This project creates a Claude Code sub-agent that automates the transcription of Spotify podcast episodes using OpenAI Whisper API, outputting structured markdown files with timestamps, metadata, and navigation features.

### Core Problem
Manual podcast transcription is time-consuming, inaccurate, and lacks structured formatting for easy consumption and reference.

### Solution Approach
**Workflow**: Spotify URL → Audio Download → Whisper API → Structured Markdown Output

**Key Innovation**: Integration of Pydantic AI framework for production-ready agent development with full type safety and robust error handling.

## Development Guidelines

### BMAD Phase Workflow
The project follows BMAD methodology with three phases:

1. **Explore Phase** (Next): Research Spotify API, Whisper integration, and Pydantic AI patterns
2. **Plan Phase**: Design comprehensive agent architecture with API orchestration
3. **Execute Phase**: Implement production-ready CLI tool with comprehensive testing

### Key Development Principles
- **Type Safety First**: Leverage Pydantic AI's type system for robust development
- **Production Ready**: Built-in observability, error handling, and evaluation systems
- **API Orchestration**: Seamless integration between Spotify API and Whisper API
- **Structured Output**: Consistent markdown formatting with YAML frontmatter

## Technical Requirements

### Pydantic AI Framework Integration

#### **Core Data Models**
```python
class PodcastRequest(BaseModel):
    spotify_url: HttpUrl
    output_format: Literal["markdown", "json"] = "markdown"
    include_timestamps: bool = True
    language: str = "en"

class TranscriptionResult(BaseModel):
    text: str
    confidence: float
    duration: float
    segments: List[TranscriptionSegment]

class TranscriptionSegment(BaseModel):
    start_time: float
    end_time: float
    text: str
    confidence: float
```

#### **Agent Tool Architecture**
```python
@agent.tool
def download_audio(spotify_url: str) -> AudioFile:
    # Spotify API integration with error handling

@agent.tool
def transcribe_audio(audio_file: AudioFile) -> TranscriptionResult:
    # Whisper API with retry logic

@agent.tool
def format_transcript(result: TranscriptionResult) -> MarkdownDocument:
    # Structured markdown generation
```

### Technology Stack
- **Framework**: Pydantic AI (V1+ with API stability)
- **APIs**: Spotify API + OpenAI Whisper API
- **Language**: Python with full type safety
- **Package Management**: UV (high-performance Python package manager)
- **Observability**: Pydantic Logfire for monitoring and debugging
- **Integration**: Claude Code sub-agent CLI interface

### Output Specifications

#### **Markdown Format Structure**
```yaml
---
title: "Podcast Episode Title"
podcast_name: "Podcast Series Name"
episode_number: "Episode #123"
spotify_url: "https://open.spotify.com/episode/..."
transcription_date: "2025-09-17"
duration: "45:32"
file_size: "42.3 MB"
language: "en"
quality: "high"
---
```

#### **Content Organization**
- Episode summary with auto-generated key topics
- Speaker identification (Host/Guest with icons)
- Timestamp-based sections with navigation links
- Quality indicators and confidence scores
- Clickable navigation for quick reference

#### **File Naming Convention**
```
[podcast-name]-ep[###]-[episode-title-slug]-transcript-YYYY-MM-DD.md
```

## File Structure Context

```
podcast-processor-cli-tool/
├── .bmad-core/              # BMAD framework (75 files)
├── .claude/                 # Claude Code integration
├── drews-artifacts/         # Project planning and checkpoints
│   ├── spotify-podcast-transcription-checkpoint-2025-09-17.md
│   └── spotify-podcast-transcription-checkpoint-2025-09-18.md
├── src/                     # Source code (TBD)
├── tests/                   # Test suites (TBD)
├── CLAUDE.md               # This configuration file
└── README.md               # Repository overview
```

## Development Context for Claude

### Current Status
- ✅ BMAD framework installed with complete agent ecosystem
- ✅ Claude Code integration configured
- ✅ Repository setup with GitHub integration
- ✅ Comprehensive project planning and requirements documentation
- ✅ Pydantic AI framework analysis and integration strategy complete

### Immediate Next Steps
1. **Begin BMAD Planning Phase**: Use orchestrator to coordinate analyst/PM/architect agents
2. **Pydantic AI Setup**: Install framework and configure development environment
3. **API Research**: Deep dive into Spotify API and Whisper API integration patterns
4. **Architecture Design**: Create comprehensive system design with error handling
5. **Implementation Planning**: Break down development into manageable stories

### BMAD Integration Commands
```bash
# Activate orchestrator for full planning workflow
@bmad-orchestrator
*plan

# Jump directly to specific agents
@bmad-orchestrator
*agent analyst    # For API research and requirements gathering
*agent pm         # For CLI interface and user experience design
*agent architect  # For system architecture and technical design
*agent dev        # For implementation planning and development
```

## Success Metrics

### MVP Success Criteria
- **Functionality**: Successfully process Spotify podcast URLs into formatted markdown
- **Quality**: 95%+ transcription accuracy with proper speaker identification
- **Reliability**: Robust error handling for API failures and edge cases
- **Integration**: Seamless Claude Code sub-agent CLI interface
- **Performance**: Process typical 45-minute podcast in under 10 minutes

### Learning Objectives
- Master Pydantic AI framework patterns for production-ready agent development
- Establish reliable multi-API orchestration patterns (Spotify + Whisper)
- Develop advanced Claude Code sub-agent integration techniques
- Create reusable templates for AI agent CLI tool development

## Key Technical Decisions Made

### Framework Selection: Pydantic AI
**Rationale**:
- Production-ready framework with API stability
- Full type safety for robust development
- Built-in observability and error handling
- Model-agnostic support for future flexibility
- Perfect alignment with CLI tool development patterns

### API Strategy: OpenAI Whisper over Otter.ai
**Rationale**:
- Official API with excellent documentation
- Superior accuracy for podcast-length content
- Reliable developer access and predictable pricing
- Strong integration patterns with Pydantic AI

### Output Format: Structured Markdown
**Rationale**:
- Human-readable and machine-parseable
- Excellent for documentation and content management
- SEO-friendly for web publishing
- Compatible with existing workflow tools

## Agent Behavior Guidelines

### When Working on This Project
1. **Check Development Phase**: Always verify current BMAD phase and appropriate next steps
2. **Leverage Type Safety**: Use Pydantic AI's type system extensively for code generation
3. **Prioritize Production Quality**: Focus on error handling, observability, and user experience
4. **Document Decisions**: Maintain clear architectural decision records in project artifacts

### BMAD Workflow Integration
- **Planning Phase**: Use analyst for API research, PM for requirements, architect for design
- **Development Phase**: Use scrum master for story breakdown, dev for implementation
- **Quality Phase**: Use QA for testing strategy and validation

### Key Files to Reference
- `drews-artifacts/spotify-podcast-transcription-checkpoint-2025-09-18.md` - Complete project context and planning
- `.bmad-core/` - BMAD framework files for methodology guidance
- API documentation and integration patterns from research phase

## Error Handling & Quality Assurance

### Multi-Layer Validation Strategy
- **Input Validation**: Type-safe URL validation and format checking
- **API Error Handling**: Robust retry logic with exponential backoff
- **Quality Assessment**: Confidence scoring and transcription validation
- **Output Verification**: Structured data validation before file creation

### Observability & Monitoring
- **Pydantic Logfire**: Built-in logging and debugging capabilities
- **Performance Metrics**: API response times, processing duration, success rates
- **Quality Metrics**: Transcription confidence, speaker identification accuracy
- **User Experience**: CLI feedback and progress indicators

## Integration Patterns

### Claude Code Sub-Agent Interface
```bash
# Future CLI usage pattern
claude-podcast-transcribe https://open.spotify.com/episode/xyz123

# With options
claude-podcast-transcribe https://open.spotify.com/episode/xyz123 --format markdown --timestamps true
```

### Development Environment
- **Package Manager**: UV for high-performance dependency management
- **Type Checking**: Pylance integration for maximum IDE context
- **Code Generation**: GitHub Copilot enhancement through structured patterns
- **Testing**: Comprehensive test suite with API mocking and validation

---

**Project Goal**: Create a production-ready podcast transcription tool that demonstrates advanced Pydantic AI patterns while solving real content processing needs through intelligent automation.