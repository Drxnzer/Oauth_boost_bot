import asyncio
import discord
from discord.ext import commands,tasks
from discord import app_commands
import tls_client
import threading
import os
import requests
from base64 import b64encode
import json
import random
import string
import shutil
from typing import Optional
from datetime import datetime
import secrets
from pystyle import Center, Colorate, Colors
from colorama import init, Fore, Style
import pystyle
from pystyle import Write, Colors
import time
from discord import app_commands, app_commands 
from datetime import datetime, timezone

import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime


def clear_file(file_path):
    try:
        with open(file_path, "w") as file:
            file.truncate(0)  
    except FileNotFoundError:
        pass

try:
    os.system("cls")
except:
    pass

with open("config.json") as f:
    config = json.load(f)
intents = discord.Intents.all()

def clear_file(file_path):
    try:
        with open(file_path, "w") as file:
            file.truncate(0)  
    except FileNotFoundError:
        pass

try:
    os.system("cls")
except:
    pass

ascii_art = """
██╗     ██╗   ██╗███╗   ██╗ █████╗ ██████╗ ███╗   ███╗ █████╗ ██████╗ ████████╗
██║     ██║   ██║████╗  ██║██╔══██╗██╔══██╗████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝
██║     ██║   ██║██╔██╗ ██║███████║██████╔╝██╔████╔██║███████║██████╔╝   ██║   
██║     ██║   ██║██║╚██╗██║██╔══██║██╔══██╗██║╚██╔╝██║██╔══██║██╔══██╗   ██║   
███████╗╚██████╔╝██║ ╚████║██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║██║  ██║   ██║   
╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
"""
print(Colorate.Horizontal(Colors.yellow_to_green, Center.XCenter(ascii_art)))
text = "Engine-Status   = Started"
text1 = "Command-Loaded   = True"
text2 = "Creator   = Lunarmart"

print(Colorate.Horizontal(Colors.yellow_to_green, Center.XCenter(text)))
print(Colorate.Horizontal(Colors.yellow_to_green, Center.XCenter(text1)))
print(Colorate.Horizontal(Colors.yellow_to_green, Center.XCenter(text2)))
print("")

with open('config.json', 'r') as config_file:
     config = json.load(config_file)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
BUILD_NUMBER = 165486
CV = "108.0.0.0"
BOT_TOKEN = config['BOT_TOKEN']
CLIENT_SECRET = config['CLIENT_SECRET']
CLIENT_ID = config['CLIENT_ID']
REDIRECT_URI = "http://localhost:8080"
API_ENDPOINT = 'https://canary.discord.com/api/v9'
AUTH_URL = f"https://canary.discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds.join"
ALLOWED_USER_IDS = config["ALLOWED_USER_IDS"]

WEBHOOK_URL = config["webhook"] 
SUPER_PROPERTIES = b64encode(
    json.dumps(
        {
            "os": "Windows",
            "browser": "Chrome",
            "device": "PC",
            "system_locale": "en-GB",
            "browser_user_agent": USER_AGENT,
            "browser_version": CV,
            "os_version": "10",
            "referrer": "https://discord.com/channels/@me",
            "referring_domain": "discord.com",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": BUILD_NUMBER,
            "client_event_source": None
        },
        separators=(',', ':')).encode()).decode()

def get_headers(token):
    headers = {
        "Authorization": token,
        "Origin": "https://canary.discord.com",
        "Accept": "*/*",
        "X-Discord-Locale": "en-GB",
        "X-Super-Properties": SUPER_PROPERTIES,
        "User-Agent": USER_AGENT,
        "Referer": "https://canary.discord.com/channels/@me",
        "X-Debug-Options": "bugReporterEnabled",
        "Content-Type": "application/json"
    }
    return headers

def exchange_code(code):
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(f"{API_ENDPOINT}/oauth2/token",
                      data=data,
                      headers=headers)
    if r.status_code in (200, 201, 204):
        return r.json()
    else:
        return False

def add_to_guild(access_token, userID, guild):
    url = f"{API_ENDPOINT}/guilds/{guild}/members/{userID}"
    botToken = BOT_TOKEN
    data = {
        "access_token": access_token,
    }
    headers = {
        "Authorization": f"Bot {botToken}",
        'Content-Type': 'application/json'
    }
    r = requests.put(url=url, headers=headers, json=data)
    return r.status_code

def rename(token, guild, nickname):
    headers = get_headers(token)
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    r = client.patch(
        f"https://canary.discord.com/api/v9/guilds/{guild}/members/@me",
        json={"nick": nickname})
    if r.status_code in (200, 201, 204):
        return "ok"
    else:
        return "error"

def authorizer(token, guild, nickname):
    headers = get_headers(token)
    r = requests.post(AUTH_URL, headers=headers, json={"authorize": "true"})
    if r.status_code in (200, 201, 204):
        location = r.json()['location']
        code = location.replace("http://localhost:8080?code=", "")
        exchange = exchange_code(code)
        access_token = exchange['access_token']
        userid = get_user(access_token)
        add_to_guild(access_token, userid, guild)
        if nickname:
            threading.Thread(target=rename, args=(token, guild, nickname)).start()
        return "ok"

def get_user(access: str):
    endp = "https://canary.discord.com/api/v9/users/@me"
    r = requests.get(endp, headers={"Authorization": f"Bearer {access}"})
    rjson = r.json()
    return rjson['id']

def main(token, guild, nickname=None):
    authorizer(token, guild, nickname)
    headers = get_headers(token)
    client = tls_client.Session(client_identifier="firefox_102")
    client.headers.update(headers)
    r = client.get(
        f"https://canary.discord.com/api/v9/users/@me/guilds/premium/subscription-slots"
    )
    idk = r.json()
    for x in idk:
        id_ = x['id']
        payload = {"user_premium_guild_subscription_slot_ids": [id_]}
        r = client.put(
            f"https://canary.discord.com/api/v9/guilds/{guild}/premium/subscriptions",
            json=payload)
        if r.status_code in (200, 201, 204):
            print(f"[+] Boosted {guild}")

            if nickname:
                rename(token, guild, nickname)

    return "ok"

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

def generate_key(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    activity = discord.Activity(type=discord.ActivityType.watching, name=".gg/lunarmart")
    await bot.change_presence(activity=activity)

def is_allowed_user():
    async def predicate(interaction: discord.Interaction):
        if str(interaction.user.id) in config["ALLOWED_USER_IDS"]:  # Convert interaction.user.id to string
            return True
        embed = discord.Embed(title="Permission Denied", description="You are not allowed to use this command.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return False
    return app_commands.check(predicate)

from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

@bot.tree.command(name="boost")
@is_allowed_user()
async def boost(
    interaction: discord.Interaction,
    guild_id: str,
    num_tokens: int,
    token_type: str,
    nickname: str = None
):
    if not guild_id or num_tokens <= 0:
        embed = discord.Embed(title="Invalid Arguments", description="Please provide a valid server ID and the number of boosts.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    if token_type not in ["1m", "3m"]:
        embed = discord.Embed(title="Invalid Token Type", description="Please specify '1m' for 1-month tokens or '3m' for 3-month tokens.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    file_name = f"{token_type}tokens.txt"

    try:
        with open(file_name, "r") as f:
            tokens = f.readlines()
    except FileNotFoundError:
        embed = discord.Embed(title="File Not Found", description=f"The file {file_name} does not exist.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    if len(tokens) < num_tokens:
        embed = discord.Embed(title="Insufficient Tokens", description=f"Not enough tokens available. Requested: {num_tokens}, Available: {len(tokens)}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    await interaction.response.send_message(f"Starting to apply {2 * num_tokens} boost(s) to server ID: {guild_id}. This may take a while...")

    successful_boosts = 0
    used_tokens = []

    for i in range(num_tokens):
        token = tokens[i].strip()
        if ":" in token:
            try:
                token = token.split(":")[2]
            except IndexError:
                await interaction.followup.send(f"Invalid token format: {token}")
                continue

        result = await interaction.client.loop.run_in_executor(executor, main, token, guild_id, nickname)

        if result == "ok":
            successful_boosts += 1
            used_tokens.append(tokens[i])

    remaining_tokens = tokens[num_tokens:]
    with open(file_name, "w") as f:
        f.writelines(remaining_tokens)

    if successful_boosts == num_tokens:
        embed = discord.Embed(title="Boosting Completed", description=f"Successfully applied boost(s) to server ID: {guild_id} with no failures.", color=discord.Color.green())
    else:
        embed = discord.Embed(title="Boosting Partial Success", description=f"Applied {successful_boosts} boost(s) to server ID: {guild_id}. Some tokens may have failed.", color=discord.Color.orange())

    await interaction.followup.send(embed=embed)

    if used_tokens:
        dm_embed = discord.Embed(
            title="Tokens Used for Boosting",
            description="Here are the tokens used to successfully boost the server:",
            color=discord.Color.blue()
        )
        dm_embed.add_field(name="Tokens", value="\n".join(used_tokens), inline=False)

        try:
            await interaction.user.send(embed=dm_embed)
        except discord.Forbidden:
            await interaction.followup.send("Could not send DM with the used tokens. The user may have DMs disabled.")

@bot.tree.command(name="add_token")
@is_allowed_user()
@app_commands.describe(token="The token to add", token_type="The type of token ('1m' for 1-month tokens, '3m' for 3-month tokens)")
async def add_token(interaction: discord.Interaction, token: str, token_type: str):
    if not token or token_type not in ["1m", "3m"]:
        embed = discord.Embed(title="Missing or Invalid Arguments", description="Please provide the required token and specify the type ('1m' or '3m').", color=discord.Color.red())
        embed.add_field(name="Command Usage", value="/add_token <token> <token_type>")
        await interaction.response.send_message(embed=embed)
        return

    file_name = f"{token_type}tokens.txt"

    with open(file_name, "a") as f:
        f.write(f"{token}\n")
    await interaction.response.send_message(f"Token added to {file_name}: {token}")

@bot.tree.command(name="remove_token")
@is_allowed_user()
@app_commands.describe(token="The token to remove", token_type="The type of token ('1m' for 1-month tokens, '3m' for 3-month tokens)")
async def remove_token(interaction: discord.Interaction, token: str, token_type: str):
    if not token or token_type not in ["1m", "3m"]:
        embed = discord.Embed(title="Missing or Invalid Arguments", description="Please provide the required token and specify the type ('1m' or '3m').", color=discord.Color.red())
        embed.add_field(name="Command Usage", value="/remove_token <token> <token_type>")
        await interaction.response.send_message(embed=embed)
        return

    file_name = f"{token_type}tokens.txt"

    with open(file_name, "r") as f:
        tokens = f.readlines()
    tokens = [t.strip() for t in tokens if t.strip() != token]
    with open(file_name, "w") as f:
        f.write("\n".join(tokens) + "\n")
    await interaction.response.send_message(f"Token removed from {file_name}: {token}")

@bot.tree.command(name="list_tokens")
@is_allowed_user()
@app_commands.describe(token_type="The type of tokens to list ('1m' for 1-month tokens, '3m' for 3-month tokens)")
async def list_tokens(interaction: discord.Interaction, token_type: str):
    if token_type not in ["1m", "3m"]:
        embed = discord.Embed(title="Invalid Token Type", description="Please specify '1m' for 1-month tokens or '3m' for 3-month tokens.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    file_name = f"{token_type}tokens.txt"

    try:
        with open(file_name, "r") as f:
            tokens = f.readlines()
    except FileNotFoundError:
        embed = discord.Embed(title="File Not Found", description=f"The file {file_name} does not exist.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    if tokens:

        await interaction.response.send_message(content="Listing tokens...", ephemeral=True)

        def split_into_chunks(text_list, max_length=4096):
            current_chunk = ""
            for line in text_list:
                if len(current_chunk) + len(line) > max_length:
                    yield current_chunk
                    current_chunk = line
                else:
                    current_chunk += line
            if current_chunk:
                yield current_chunk

        for chunk in split_into_chunks(tokens):
            embed = discord.Embed(
                title=f"{token_type.upper()} Tokens",
                description=chunk,
                color=discord.Color.blue()
            )
            await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(title=f"{token_type.upper()} Tokens", description="No tokens found.", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="file_restock")
@is_allowed_user()
@app_commands.describe(file="The file containing tokens to restock", token_type="The type of tokens to restock ('1m' for 1-month tokens, '3m' for 3-month tokens)")
async def file_restock(interaction: discord.Interaction, file: discord.Attachment, token_type: str):
    if token_type not in ["1m", "3m"]:
        embed = discord.Embed(title="Invalid Token Type", description="Please specify '1m' for 1-month tokens or '3m' for 3-month tokens.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    try:
        file_content = await file.read()

        content_str = file_content.decode('utf-8').strip()
        tokens = [line.strip() for line in content_str.splitlines() if line.strip()]
    except Exception as e:
        embed = discord.Embed(title="File Error", description=f"Failed to read the file: {str(e)}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    file_name = f"{token_type}tokens.txt"

    with open(file_name, "a") as f:

        for token in tokens:
            f.write(f"{token}\n")

    await interaction.response.send_message(f"Tokens restocked from {file.filename} to {file_name}")

@bot.tree.command(name="stock")
async def stock(interaction: discord.Interaction):
    try:
        with open("1mtokens.txt", "r") as f:
            one_month_tokens = len(f.readlines())
            print(f"1-Month Tokens Counted: {one_month_tokens}")  
    except FileNotFoundError:
        one_month_tokens = 0
        print("1-Month Tokens File Not Found")  

    try:
        with open("3mtokens.txt", "r") as f:
            three_month_tokens = len(f.readlines())
            print(f"3-Month Tokens Counted: {three_month_tokens}")  
    except FileNotFoundError:
        three_month_tokens = 0
        print("3-Month Tokens File Not Found")  

    embed = discord.Embed(
        title="Token Stock",
        description="Current token stock levels:",
        color=discord.Color.green()
    )
    embed.add_field(name="1-Month Tokens", value=str(one_month_tokens), inline=False)
    embed.add_field(name="3-Month Tokens", value=str(three_month_tokens), inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="cleartokens")
@is_allowed_user()
@app_commands.describe(token_type="The type of tokens to clear ('1m' for 1-month tokens, '3m' for 3-month tokens)")
async def cleartokens(interaction: discord.Interaction, token_type: str):
    if token_type not in ["1m", "3m"]:
        embed = discord.Embed(title="Invalid Token Type", description="Please specify '1m' for 1-month tokens or '3m' for 3-month tokens.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    file_name = f"{token_type}tokens.txt"

    try:

        open(file_name, "w").close()
        embed = discord.Embed(title="Tokens Cleared", description=f"All tokens in {file_name} have been cleared.", color=discord.Color.green())
    except Exception as e:
        embed = discord.Embed(title="Error", description=f"Failed to clear tokens: {str(e)}", color=discord.Color.red())

    await interaction.response.send_message(embed=embed)

def load_suggestion_channel():
    try:
        with open('suggestion_channel.json', 'r') as f:
            data = json.load(f)
            return data.get('channel_id')
    except FileNotFoundError:
        return None

def save_suggestion_channel(channel_id):
    with open('suggestion_channel.json', 'w') as f:
        json.dump({'channel_id': channel_id}, f)

@bot.tree.command(name="setsuggestionchannel")
@is_allowed_user()
@app_commands.describe(channel="The channel where suggestions will be sent.")
@commands.has_permissions(administrator=True)
async def set_suggestion_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    save_suggestion_channel(channel.id)
    await interaction.response.send_message(f"Suggestion channel set to {channel.mention}", ephemeral=True)

@bot.tree.command(name="suggest")
@app_commands.describe(suggestion="Your suggestion or feedback.")
async def suggest(interaction: discord.Interaction, suggestion: str):
    suggestion_channel_id = load_suggestion_channel()
    if suggestion_channel_id:
        suggestion_channel = bot.get_channel(suggestion_channel_id)
        if suggestion_channel:
            embed = discord.Embed(title="New Suggestion", description=suggestion, color=discord.Color.blue())
            embed.set_footer(text=f"Suggested by {interaction.user}", icon_url=interaction.user.avatar.url)

            message = await suggestion_channel.send(embed=embed)

            await message.add_reaction("✅")  
            await message.add_reaction("❌")  

            await interaction.response.send_message("Thanks for your suggestion!", ephemeral=True)
        else:
            await interaction.response.send_message("Sorry, I couldn't find the suggestion channel.", ephemeral=True)
    else:
        await interaction.response.send_message("Suggestion channel has not been set yet.", ephemeral=True)

@set_suggestion_channel.error
async def set_suggestion_channel_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingPermissions):
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)

async def process_token(token, server_id):
    await asyncio.sleep(2)  
    return True  

@bot.tree.command(name='redeem', description="Redeem tokens using a key")
@app_commands.describe(
    key="The key for redeeming tokens",
    server_id="The server ID where tokens will join",
    remove_bot="Remove the bot after completing the process (yes or no)",
    nickname="The new nickname for the tokens"
)
async def redeem_tokens(interaction: discord.Interaction, key: str, server_id: str, remove_bot: Optional[str] = None, nickname: Optional[str] = None):
    key_folder = os.path.join("genned_stocks", key)

    if not os.path.exists(key_folder):
        await interaction.response.send_message("Invalid key! Please check and try again.")
        return

    token_files = [f for f in os.listdir(key_folder) if f.endswith('tokens.txt')]
    if not token_files:
        await interaction.response.send_message("No tokens found for the provided key.")
        return

    tokens_used = 0
    failed_tokens = 0
    failed_token_list = []
    successful_tokens = []
    joined_tokens = 0
    boosted_tokens = 0

    processing_embed = discord.Embed(
        title="Key has been redeemed.",
        description=f"Processing boost for server ID: {server_id}",
        color=discord.Color.orange()
    )
    processing_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1282004413308866594/1283104825223151648/ezgif-3-1177cb2f1e.gif")
    processing_embed.set_image(url="https://cdn.discordapp.com/attachments/1282004413308866594/1283104825810096170/a_d5fed0a75e31f4d7eb86b42d5bd055b8.gif")

    await interaction.response.defer()

    processing_message = await interaction.followup.send(embed=processing_embed, wait=True)

    for token_file in token_files:
        with open(os.path.join(key_folder, token_file), 'r') as f:
            tokens = f.readlines()

        for token in tokens:
            token = token.strip()
            parts = token.split(":")
            if len(parts) < 3:
                failed_tokens += 1
                failed_token_list.append(token)
                continue

            token = parts[2]
            tokens_used += 1
            try:
                threading.Thread(target=main, args=(token, server_id)).start()
                successful_tokens.append(token)
                joined_tokens += 1

                updated_embed = discord.Embed(
                    title="Processing your order…",
                    description=f"Using {joined_tokens} Tokens",
                    color=discord.Color.orange()
                )
                updated_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1282004413308866594/1283104825223151648/ezgif-3-1177cb2f1e.gif")
                updated_embed.set_image(url="https://cdn.discordapp.com/attachments/1282004413308866594/1283104825810096170/a_d5fed0a75e31f4d7eb86b42d5bd055b8.gif")

                await processing_message.edit(embed=updated_embed)

                boosted = main(token, server_id)  
                if boosted:
                    boosted_tokens += 1

                    updated_embed = discord.Embed(
                        title="Processing",
                        description=f"Boosted Using {joined_tokens}",
                        color=discord.Color.green()
                    )
                    updated_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1282004413308866594/1283104825223151648/ezgif-3-1177cb2f1e.gif")
                    updated_embed.set_image(url="https://cdn.discordapp.com/attachments/1282004413308866594/1283104825810096170/a_d5fed0a75e31f4d7eb86b42d5bd055b8.gif")
                    await processing_message.edit(embed=updated_embed)

            except Exception as e:
                failed_tokens += 1
                failed_token_list.append(token)
                print(f"Error processing token {token}: {e}")

    # Define messages before using them in webhook_payload
    successful_tokens_message = '\n'.join(successful_tokens) if successful_tokens else "None"
    failed_tokens_message = '\n'.join(failed_token_list) if failed_token_list else "None"

    # Change nickname for the tokens if provided
    if nickname:
        try:
            # Implement the actual nickname change logic here
            await interaction.followup.send(f"Nickname for tokens changed to {nickname}.")
        except Exception as e:
            await interaction.followup.send(f"Failed to change nickname: {e}")

    # Prepare timestamp using timezone-aware datetime
    timestamp = datetime.now(timezone.utc).isoformat()

    webhook_payload = {
        "content": None,  
        "embeds": [
            {
                "title": "We have boosted a server successfully.",
                "color": 0x00FF00,  
                "fields": [
                    {"name": "Success", "value": f"{joined_tokens}", "inline": True},
                    {"name": "Failed", "value": f"{failed_tokens}", "inline": True},
                    {"name": "Elapsed Time", "value": "2.91 seconds", "inline": False},  
                    {"name": "Bio", "value": "[Boosted by](https://discord.gg/s0)", "inline": True},
                    {
                        "name": "Order Information",
                        "value": f"**Boost Amount:** {joined_tokens}\n**Server Invite:** g3",
                        "inline": False
                    },
                    {
                        "name": "Succeeded Tokens",
                        "value": successful_tokens_message,
                        "inline": False
                    },
                    {
                        "name": "Failed Tokens",
                        "value": failed_tokens_message,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Order Completed, Contact for support",
                },
                "timestamp": timestamp
            }
        ]
    }

    # Ensure WEBHOOK_URL is set
    if WEBHOOK_URL:
        response = requests.post(WEBHOOK_URL, json=webhook_payload)
        if response.status_code >= 400:
            print(f"Failed to send webhook: {response.status_code} - {response.text}")
    else:
        print("WEBHOOK_URL is not set.")

    # Send a DM to the user with the list of tokens used for boosting
    try:
        dm_message = f"Tokens used for boosting:\n{successful_tokens_message}"
        await interaction.user.send(dm_message)
    except Exception as e:
        await interaction.followup.send(f"Failed to send DM: {e}")

    # Remove the bot from the server if requested
    if remove_bot and remove_bot.lower() == 'yes':
        try:
            await interaction.guild.leave()
        except Exception as e:
            await interaction.followup.send(f"Failed to remove the bot from the server: {e}")

    # Remove the folder containing the tokens
    try:
        shutil.rmtree(key_folder)
    except Exception as e:
        await interaction.followup.send(f"Failed to remove token folder: {e}")
        return

    await interaction.followup.send(f"Tokens have been redeemed and added to server ID: {server_id}")



@bot.tree.command(name="give-token")
@is_allowed_user()
@app_commands.describe(
    amount="The number of tokens to give",
    token_type="The type of tokens ('1m' for 1-month, '3m' for 3-month)",
    user="The user to give the tokens to"
)
async def give_token(interaction: discord.Interaction, amount: int, token_type: str, user: discord.User):
    if not token_type in ["1m", "3m"]:
        embed = discord.Embed(title="Invalid Token Type", description="Please specify '1m' for 1-month tokens or '3m' for 3-month tokens.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    if amount <= 0:
        embed = discord.Embed(title="Invalid Amount", description="Please specify a valid number of tokens.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    file_name = f"{token_type}tokens.txt"
    try:
        with open(file_name, "r") as f:
            tokens = f.readlines()
    except FileNotFoundError:
        embed = discord.Embed(title="File Not Found", description=f"The file {file_name} does not exist.", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    if len(tokens) < amount:
        embed = discord.Embed(title="Insufficient Tokens", description=f"Not enough tokens available. Required: {amount}, Available: {len(tokens)}", color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
        return

    tokens_to_give = tokens[:amount]

    remaining_tokens = tokens[amount:]
    with open(file_name, "w") as f:
        f.writelines(remaining_tokens)

    tokens_str = ''.join(tokens_to_give)
    embed = discord.Embed(title="Tokens Received", description=f"You have received {amount} token(s) of type {token_type}.", color=discord.Color.green())
    embed.add_field(name="Tokens", value=f"```\n{tokens_str}\n```", inline=False)

    try:
        await user.send(embed=embed)
        confirmation_message = f"Successfully sent {amount} token(s) of type {token_type} to {user.mention}."
    except discord.Forbidden:
        confirmation_message = f"Failed to send tokens to {user.mention}. They might have DMs disabled."

    admin_embed = discord.Embed(title="Tokens Given", description=confirmation_message, color=discord.Color.green())
    await interaction.response.send_message(embed=admin_embed)

@bot.tree.command(name='makekeys', description="Generate keys and send them to your DM")
@is_allowed_user()
@app_commands.describe(amount="The number of tokens", typ="The type of tokens: '1m' or '3m'", keys="The number of keys to generate (default is 1)")
async def gen_tokens(interaction: discord.Interaction, amount: int, typ: str, keys: int = 1):
    if typ not in ["1m", "3m"]:
        await interaction.response.send_message("Invalid type! Please use either '1m' or '3m'")
        return

    filename = '1mtokens.txt' if typ == '1m' else '3mtokens.txt'
    genned_stocks_dir = "genned_stocks"

    if not os.path.exists(genned_stocks_dir):
        os.makedirs(genned_stocks_dir)

    with open(filename, 'r') as f:
        lines = f.readlines()

    total_tokens_required = amount * keys
    if len(lines) < total_tokens_required:
        await interaction.response.send_message(f"Not enough tokens in {typ} stock to generate {total_tokens_required} tokens.")
        return

    keys_generated = []
    for _ in range(keys):
        key = f"KEY-LUNARMART-{secrets.token_hex(5)}"
        key_folder = os.path.join(genned_stocks_dir, key)

        if not os.path.exists(key_folder):
            os.makedirs(key_folder)

        with open(os.path.join(key_folder, f"{typ}tokens.txt"), 'w') as f:
            f.writelines(lines[:amount])
            lines = lines[amount:]

        keys_generated.append(key)

    with open(filename, 'w') as f:
        f.writelines(lines)

    keys_file_path = os.path.join(genned_stocks_dir, 'genned_keys.txt')
    with open(keys_file_path, 'w') as keys_file:
        keys_file.write("\n".join(keys_generated))

    user = await bot.fetch_user(interaction.user.id)
    await user.send("Here are your keys:", file=discord.File(keys_file_path))
    await interaction.response.send_message(f"Generated {amount * keys} tokens of {typ} type and sent {keys} key(s) to your DM with a file containing the keys.")

@bot.tree.command(name='extract-tokens', description="Extract tokens from the generated key")
@app_commands.describe(key="The key from which you want to extract tokens")
async def extract_tokens(interaction: discord.Interaction, key: str):
    key_folder = os.path.join("genned_stocks", key)

    if not os.path.exists(key_folder):
        await interaction.response.send_message("Invalid key! Please check and try again.")
        return

    token_files = [f for f in os.listdir(key_folder) if f.endswith('tokens.txt')]

    if not token_files:
        await interaction.response.send_message("No tokens found for the provided key.")
        return

    all_tokens = []
    for token_file in token_files:
        with open(os.path.join(key_folder, token_file), 'r') as f:
            tokens = f.readlines()
            all_tokens.extend(tokens)

    token_text = '\n'.join(all_tokens)

    if len(token_text) > 2000:  

        tokens_file_path = os.path.join(key_folder, f"{key}_tokens.txt")
        with open(tokens_file_path, 'w') as tokens_file:
            tokens_file.write(token_text)

        await interaction.response.send_message("The tokens have been extracted and are sent as a file:")
        await interaction.followup.send(file=discord.File(tokens_file_path))
    else:

        await interaction.response.send_message(f"Tokens extracted:\n```{token_text}```")

    try:
        shutil.rmtree(key_folder)  
        await interaction.followup.send("The key and associated tokens have been successfully deleted.")
    except Exception as e:
        await interaction.followup.send(f"Failed to delete the key folder. Error: {str(e)}")

@bot.tree.command(name='start_stock_update', description="Start live stock updates for tokens.")
@app_commands.describe(channel_id="The channel ID to send live stock updates.")
async def start_stock_update(interaction: discord.Interaction, channel_id: str):

    channel = bot.get_channel(int(channel_id))
    if not channel:
        await interaction.response.send_message("Invalid channel ID!")
        return

    live_stock_update.start(channel_id)
    await interaction.response.send_message(f"Live stock updates started in channel <#{channel_id}>.")

@bot.tree.command(name='stop_stock_update', description="Stop live stock updates.")
async def stop_stock_update(interaction: discord.Interaction):

    live_stock_update.stop()
    await interaction.response.send_message("Live stock updates stopped.")

@tasks.loop(hours=1)  
async def live_stock_update(channel_id):

    channel = bot.get_channel(int(channel_id))
    if not channel:
        print(f"Channel with ID {channel_id} not found.")
        return

    token_file_1m = os.path.join("1mtokens.txt")
    token_file_3m = os.path.join("3mtokens.txt")

    stock_1m = count_tokens_in_file(token_file_1m)
    stock_3m = count_tokens_in_file(token_file_3m)

    stock_embed = discord.Embed(
        title="Live Token Stock Update",
        description="Here is the current stock of tokens:",
        color=discord.Color.green()
    )
    stock_embed.add_field(name="1-Month Nitro Tokens", value=f"{stock_1m} tokens available", inline=False)
    stock_embed.add_field(name="3-Months Nitro Tokens", value=f"{stock_3m} tokens available", inline=False)

    await channel.send(embed=stock_embed)

def count_tokens_in_file(file_path):
    """Helper function to count the number of tokens in a given file."""
    if not os.path.exists(file_path):
        return 0  

    with open(file_path, 'r') as file:
        tokens = file.readlines()

    return len(tokens)  

@bot.tree.command(name='listkeys', description="List all generated keys")
@is_allowed_user()
async def list_keys(interaction: discord.Interaction):
    genned_stocks_dir = "genned_stocks"
    keys_file_path = os.path.join(genned_stocks_dir, 'genned_keys.txt')

    if not os.path.exists(keys_file_path):
        await interaction.response.send_message("No keys have been generated yet.")
        return

    with open(keys_file_path, 'r') as keys_file:
        keys = keys_file.read().splitlines()

    if not keys:
        await interaction.response.send_message("No keys have been generated yet.")
        return

    if len(keys) > 10:  
        user = await bot.fetch_user(interaction.user.id)
        await user.send("Here are the currently generated keys:\n" + "\n".join(keys))
        await interaction.response.send_message("The list of keys has been sent to your DMs.")
    else:

        await interaction.response.send_message("Here are the currently generated keys:\n" + "\n".join(keys))

@bot.tree.command(name='removekeys', description="Remove keys and their tokens")
@is_allowed_user()
@app_commands.describe(keys_to_remove="The number of keys to remove (or 'all' to remove all keys)")
async def remove_keys(interaction: discord.Interaction, keys_to_remove: str):
    genned_stocks_dir = "genned_stocks"

    if not os.path.exists(genned_stocks_dir):
        await interaction.response.send_message("No keys found to remove.")
        return

    keys_file_path = os.path.join(genned_stocks_dir, 'genned_keys.txt')

    if not os.path.exists(keys_file_path):
        await interaction.response.send_message("No keys found to remove.")
        return

    with open(keys_file_path, 'r') as keys_file:
        keys = keys_file.read().splitlines()

    if keys_to_remove.lower() == "all":

        for key in keys:
            key_folder = os.path.join(genned_stocks_dir, key)
            if os.path.exists(key_folder):
                shutil.rmtree(key_folder)

        with open(keys_file_path, 'w') as keys_file:
            keys_file.write("")

        await interaction.response.send_message(f"All keys have been successfully removed.")
    else:
        try:
            keys_to_remove = int(keys_to_remove)
        except ValueError:
            await interaction.response.send_message("Invalid input. Please provide a number or 'all' to remove all keys.")
            return

        if keys_to_remove > len(keys):
            await interaction.response.send_message(f"There are only {len(keys)} keys available to remove.")
            return

        keys_to_delete = keys[:keys_to_remove]
        for key in keys_to_delete:
            key_folder = os.path.join(genned_stocks_dir, key)
            if os.path.exists(key_folder):
                shutil.rmtree(key_folder)

        with open(keys_file_path, 'w') as keys_file:
            keys_file.write("\n".join(keys[keys_to_remove:]))

        await interaction.response.send_message(f"Removed {keys_to_remove} key(s) successfully.")

bot.run(BOT_TOKEN)
