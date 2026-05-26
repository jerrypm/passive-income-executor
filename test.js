import { OpenRouter } from "@openrouter/sdk";

const client = new OpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY,
});

async function main() {
  try {
    const res = await client.chat.completions.create({
      model: "openai/gpt-4o-mini",
      messages: [
        { role: "user", content: "Kasih 3 ide passive income yang realistis" }
      ],
    });

    console.log(res.choices[0].message.content);
  } catch (err) {
    console.error("ERROR:", err);
  }
}

main();
