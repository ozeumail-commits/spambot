import discord
from discord.ext import commands
from discord.ui import View, Button
import os
from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# Intents の設定
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 固定メッセージ本文
FIXED_MESSAGE = """@everyone @here
# 荒らしおめでとうございます🎉
# ここはおぜうの集いによって荒らされました‼️‼️‼️‼️‼️
キミも今すぐおぜうの集いに参加し、最高の荒らしライフを楽しもう！
# おぜうの集いに参加すると…❓
## ・フォロワーが増える!!
## ・何かあった時に守ってもらえる!!
## ・仲間が増える!!
## ・より楽しく快適なネットライフを送れる!!
## ・知名度が上がる!!
# ⬇️参加はこちらをクリック
## discord.gg/ozeuozeu

ついでにおぜうのTwitterフォローもよろしくね！
https://x.com/ozeusabu
 https://imgur.com/a/5OKmtuG
  (https://media.discordapp.net/attachments/1421665302491435108/1422017936771645530/2025-09-11_1.45.32.webp?ex=68db24e7&is=68d9d367&hm=fa8ede681d9b25d1df3d4658536d9e5968f39645f03f95a2eba357d4fb85bc48&=&format=webp&width=812&height=1211)
  https://i.imgur.com/NbBGFcf.mp4
   (https://media.discordapp.net/attachments/1421665302491435108/1422017937283354665/2025-09-14_14.46.00.webp?ex=68db24e8&is=68d9d368&hm=82f81b12ed5db30ce992ec91b64f40b6547bc519d00a52da0076b97785e61d9e&=&format=webp&width=900&height=1211)
   
 ( https://media.discordapp.net/attachments/1421665302491435108/1422018058247077989/NbBGFcf_2.gif?ex=68db2504&is=68d9d384&hm=89a4eeab8f1cbc6c0d324bb701bbc76f0d5a7c6008f9099a9605699363f91df3&=&width=1281&height=540 )
"""

class SpamView(View):
    def __init__(self, user: discord.User):
        super().__init__(timeout=None)
        self.user = user
        self.add_item(Button(
            label="⚠️ スパム送信 ⚠️",
            style=discord.ButtonStyle.danger,
            custom_id="spam_button"
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """ボタンを押せるのはコマンド送信者だけ"""
        return interaction.user.id == self.user.id

@bot.event
async def on_ready():
    print(f"✅ 起動完了: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ スラッシュコマンド {len(synced)} 個同期しました")
    except Exception as e:
        print(f"同期エラー: {e}")

@bot.tree.command(name="spam", description="固定メッセージスパム")
async def spam(interaction: discord.Interaction):
    """スパムボタンを表示するコマンド"""
    await interaction.response.send_message(
        "⚠️ 固定メッセージスパム ⚠️\n下のボタンを押すと固定メッセージが送信されます。",
        view=SpamView(interaction.user),
        ephemeral=True  # 他人には見えない
    )

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data.get("custom_id") == "spam_button":
            # メンション有効に設定
            allowed_mentions = discord.AllowedMentions(everyone=True)

            # 最初のレスポンス（全体に1回目の送信）
            await interaction.response.send_message(
                FIXED_MESSAGE,
                allowed_mentions=allowed_mentions
            )

            # 残り5回を followup で送信
            for _ in range(5):
                await interaction.followup.send(
                    FIXED_MESSAGE,
                    allowed_mentions=allowed_mentions
                )


# Replit Secrets に保存したトークンを取得して起動
keep_alive()
bot.run(os.getenv("DISCORD_TOKEN"))
