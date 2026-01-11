from openai import OpenAI

client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Reply with OK"}],
    max_tokens=5
)

print(resp.choices[0].message.content)
