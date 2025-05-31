import asyncio
import random

import numpy as np
from agents import Agent, function_tool
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions
from agents.voice import (
    AudioInput,
    SingleAgentVoiceWorkflow,
    SingleAgentWorkflowCallbacks,
    VoicePipeline,
)

from audio_player import AudioPlayer, record_audio


@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    print(f"[debug] get_weather called with city: {city}")
    choices = ["sunny", "cloudy", "rainy", "snowy"]
    return f"The weather in {city} is {random.choice(choices)}."


french_agent = Agent(
    name="French Tutor",
    handoff_description="A french speaking agent.",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. Speak with a Quebecois French accent, and speak slowly. "
        "You are a helpful French tutor speaking to a beginner French speaker, so try to use simple phrases and to speak "
        "clearly. If the human inserts an English word or phrase into their sentence, try to teach them how to say that "
        "word or phrase in French.",
    ),
    model="gpt-4o-mini",
)

agent = Agent(
    name="Assistant",
    instructions=prompt_with_handoff_instructions(
        "You're speaking to a human, so be polite and concise. If the user speaks in French, handoff to the french agent.",
    ),
    model="gpt-4o-mini",
    handoffs=[french_agent],
    tools=[get_weather],
)


class WorkflowCallbacks(SingleAgentWorkflowCallbacks):
    def on_run(self, workflow: SingleAgentVoiceWorkflow, transcription: str) -> None:
        print(f"[debug] on_run called with transcription: {transcription}")


async def main():
    pipeline = VoicePipeline(
        workflow=SingleAgentVoiceWorkflow(agent, callbacks=WorkflowCallbacks())
    )

    conversing = True
    while conversing:

        audio_input = AudioInput(buffer=record_audio())

        result = await pipeline.run(audio_input)

        with AudioPlayer() as player:
            async for event in result.stream():
                if event.type == "voice_stream_event_audio":
                    player.add_audio(event.data)
                    print("Received audio")
                elif event.type == "voice_stream_event_lifecycle":
                    print(f"Received lifecycle event: {event.event}")

            # Add 1 second of silence to the end of the stream to avoid cutting off the last audio.
            player.add_audio(np.zeros(24000 * 1, dtype=np.int16))
        await asyncio.sleep(0.3)


if __name__ == "__main__":
    asyncio.run(main())
