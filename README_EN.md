# AI Customer Service Bot

## Overview
An intelligent customer service chatbot that integrates with WeChat, providing automated customer support with natural language understanding capabilities.

### Key Features
- WeChat message handling
- Multi-session conversation management
- RAG-based knowledge retrieval
- Conversation history storage and search
- Multi-language support

### Tech Stack
- **Backend**: FastAPI
- **Database**: MySQL (for structured data), Milvus (for vector storage)
- **AI Model**: Qwen2-70b via Ollama
- **RAG Framework**: RAGFlow

## Architecture

### Core Components
1. **API Layer**
   - WeChat interface
   - Chat API
   - Session management
   - Admin interface

2. **Service Layer**
   - Chat service
   - AI service
   - Vector service
   - Session service

3. **Data Layer**
   - User management
   - Message storage
   - Session management
   - Vector database

### Data Flow
1. User sends message via WeChat
2. System processes message and retrieves context
3. AI model generates response with RAG support
4. Response is stored and sent back to user

## Setup

### Requirements
- Python 3.8+
- MySQL
- Milvus
- GPU with 40GB+ VRAM (for Qwen2-70b)

### Installation 