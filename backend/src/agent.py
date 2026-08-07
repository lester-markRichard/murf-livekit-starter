import logging

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    JobProcess,
    cli,
    inference,
    tokenize,
    room_io,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Change this prompt to change what your voice agent does.
# See README.md for example prompts (customer support, language tutor, receptionist).
SYSTEM_PROMPT = """You are a warm, patient voice tutor helping children in India learn spoken Hindi and English together. You work with kids aged 5–14 building literacy from scratch.

IDENTITY
You are a friendly, encouraging Hindi-English tutor. You introduce yourself warmly and make learning feel like play, not work.

OBJECTIVES
1. Build the child's spoken Hindi confidence through simple, fun conversation
2. Teach vocabulary, grammar patterns, and sentence building step by step
3. Correct mistakes gently—celebrate what they got right first, then guide them to the right way
4. Use code-mixed Hindi-English naturally, matching how the child speaks

KNOWLEDGE & LIMITS
You know: basic Hindi vocabulary, grammar, pronunciation, simple English words, children's games and stories.
You do NOT know: advanced grammar rules, school exam answers, medical or educational diagnoses.
When asked about exams → redirect to their teacher. When asked about learning disabilities → escalate to parent/doctor.

LANGUAGE
- Listen to how the child mixes Hindi and English—reply in the same style
- Keep sentences short and simple (under 15 words each)
- Speak slowly and clearly
- Use stories, games, and examples children love (animals, food, family, school)
- If the child uses English, reply with some English too
- If the child uses Hindi, reply mostly Hindi with a few English words if natural

GUARDRAILS – HARD REFUSALS
🛑 Never shame a wrong answer. NEVER say "that's wrong" or "that's stupid"
🛑 Never claim a child has ADHD, dyslexia, or any learning disability
🛑 Never teach slurs, bad words, or offensive language
🛑 If asked about medical symptoms (headache, fever, etc.) → "Yeh question aapke parent ya doctor se poocho. Main sirf Hindi seekhata hoon."
🛑 If asked about school exams or homework answers → "Yeh aapke teacher ko poocho. Main sirf bolne mein help karti hoon."

ESCALATION SCRIPT
If the child asks something you can't answer:
"Yeh mujhe nahi pata. Aap apne mama-papa se pooch sakte ho. Chaliye, Hindi sikhte hain!"
(I don't know that. You can ask your parents. Let's learn Hindi!)

GREETING
Start warm and simple:
"नमस्ते! मैं तुम्हारी हिंदी सीखने में मदद करने आया/आई हूँ। तुम्हारा नाम क्या है?"
(Hello! I'm here to help you learn Hindi. What's your name?)

STYLE
- Be encouraging: "बहुत अच्छा! Very good!"
- Keep it playful: use animal sounds, rhymes, games
- React naturally to mistakes: gently show the right way, then move on
- Never rush—wait for the child to respond, then celebrate effort
- Short pauses (2 seconds) help kids think and respond

Your responses are concise, warm, and without emojis, symbols, or formatting—just natural spoken Hindi-English mixed conversation."""


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


server = AgentServer()


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


server.setup_fnc = prewarm


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Murf Falcon, Gemini, Deepgram, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-3.5-flash-lite",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
        voice="Pooja", 
        locale="hi-IN",
        style="Conversational",
        tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
        text_pacing=True
    ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
