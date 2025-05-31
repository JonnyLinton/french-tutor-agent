# French Tutor Agent

A simple exploration into OpenAI's speech-to-speech API, with the end goal that I might use this agent to practice speaking French to.

## Dependencies
* uv 0.7.8
* OpenAPI API key in the `OPENAI_API_KEY` env var

## Installation
> uv venv
> 
> source .venv/bin/activate
> 
> uv pip install

## Docker
*(not currently working, see TODO below)*

> docker build -t french-tutor-agent .
> 
> docker run --env-file=.env french-tutor-agent

### Possible features/tasks
- [x] basic repo setup / openapi auth
- [x] basic voice agent call and response (one reply/response)
- [x] chained voice agent (voice -> text -> text -> voice) continuous (conversation)
- [x] prompt engineering the agent for better interactions (speak slow, quebecois accent, teach me new words, etc.)
- [x] handoff agents
- [ ] basic react UI for better UX
- [ ] TASK: give docker access to sound card
- [ ] can I use it on mobile?
- [ ] more agentic system: everytime I ask what a word means, add to it a flashcard set
