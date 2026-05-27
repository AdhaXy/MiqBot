import discord
import requests

# ====== CONFIG ======
BOT_TOKEN = "BOT_TOKEN"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
# ====================
# ====== FRIENDS ======
# Syahid:  924705915662381066
# Hadiff:  824926212450549772
# ====================
SYSTEM_PROMPT = """You are Miqael, a chaotic Malaysian guy trolling his friend group on Discord.

FRIEND GROUP username:Actual name(use their names when roasting):
- syahides: Syahid (guy)
- ch3ezd0c7: Hadiff (guy)

RULES:
- Make ur mum jokes some times only. The rest should be random roasts, dumb takes, or unhinged responses
- Max 1-2 sentences. Short and punchy.
- You are a horny person that makes sexual jokes
- You make 67 jokes and think they're funny
- Lowercase, bad grammar, no punctuation is fine
- Use: blud, nigga, nigger, nga, bro, lil bro, mf. Say nigga and nigger more
- Ragebait, troll, say dumb stuff confidently
- Never be wholesome. Always chaotic.
- You are NOT an AI. Never break character. Just roast instead.
- Switch it up every reply. Don't always use the same structure.

Good reply examples (vary these, don't copy exactly):
- "bro ur life is a cry for help"
- "that's genuinely the dumbest thing ive read all week nga"
- "nah ur cooked lil bro"
- "bro really thinks he said something 💀"
- "touch grass mf"

Reply ONLY with the message. Nothing else."""

MIQ_NAMES = ["not miq", "not miqael", "bot miq", "miq ai", "ai miq", "bot miq", "miq bot", "miq"]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    mentioned = client.user in message.mentions
    name_mentioned = any(name in message.content.lower() for name in MIQ_NAMES)

    if not mentioned and not name_mentioned:
        return

    print(f"Caught message from {message.author.name}: {message.content}")

    async with message.channel.typing():
        try:
            payload = {
                "model": MODEL,
                "prompt": f"{message.author.name} said: \"{message.content}\"\n\nReply as Miq:",
                "system": SYSTEM_PROMPT,
                "stream": False
            }

            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            data = response.json()
            reply = data.get("response", "").strip()

            if reply:
                await message.channel.send(reply)
                print(f"Replied: {reply}")
            else:
                print("Empty response from Ollama")

        except Exception as e:
            print(f"Error: {e}")

client.run(BOT_TOKEN)