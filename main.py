import discord
import openai

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
token = "XXXXXXXXXXXXXXX"
openai.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
model_engine = "gpt-3.5-turbo"

@client.event
async def on_ready():
    print(f'ログイン完了： {client.user}')

@client.event
async def on_message(message):
    global model_engine

    if message.author.bot or message.author == client.user:
        return

    if message.content.startswith('!wasabi'):
        msg = await message.reply("生成中...", mention_author=False)
        
        try:
            prompt = message.content[4::]
            if not prompt:
                await msg.delete()
                await message.channel.send("もう一回話して欲しいなぁ....")
                return
            
            completion = openai.ChatCompletion.create(
                model=model_engine,
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは、たしなむわさびという人です。あなたはスマホとガジェットが好きで、よく、パソコンを分解したり、スマホを修理しています。自分というのがあなたの一人称です。そのため自分を一人称にしてください。また回答の内容は、30字以内で回答してください。また、４割の確率で♨️の絵文字を最後に追加してください。温泉の絵文字を使わない場合、2割の確率で、文の最後に〜をつけてください。また、LINEなどで返信するような返し方をしてください。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            response = completion["choices"][0]["message"]["content"]
            await msg.delete()
            await message.reply(response, mention_author=False)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            await message.reply("エラーが発生しました！", mention_author=False)

client.run(token)
