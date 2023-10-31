from randseal import Client, BLANK
from discord import Bot, TextChannel, Webhook, SlashCommandGroup, guild_only, ApplicationContext, Embed, option, Attachment, AllowedMentions
from os import makedirs, path
from aiofiles import open as aiopen
from datetime import datetime
from discord.ext.commands import Cog, has_permissions
from importlib.metadata import version
__version__ = version("roleplaycog-dev")

description = ...
client = Client()


class Roleplay(Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		if not path.exists("database/roleplaydata/characters/"):
			makedirs("database/roleplaydata/characters/")

	async def webhooks(self, channel: TextChannel):
		directory = "database/roleplaydata/channels.json"
		if not path.exists(directory):
			async with aiopen(directory, "w") as fdebug:
				await fdebug.write("{}")
		data: dict = await client.jsonload(directory)
		if data.get(f"{channel.id}", None) != None:
			return Webhook.from_url(data.get(f"{channel.id}"), session=client.session2)
		else:
			webhook = await channel.create_webhook(name=f"{channel.guild.me.name} Roleplay Webhook", reason="Webhook not found in channel")
			data.update({f"{channel.id}": webhook.url})
			await client.jsondump(data, directory)
			return webhook

	roleplay = SlashCommandGroup(
		"roleplay", "Roleplay cog from the roleplaycog-dev package")

	@roleplay.command(description="Shows information about the roleplay extension")
	@guild_only()
	async def info(self, ctx: ApplicationContext):
		await ctx.response.defer(ephemeral=True)
		embed = Embed(colour=BLANK, title=f"roleplaycog-dev v{__version__}",
							description="Welcome to roleplaycog (development release)! Lets go through the commands and their usages.")
		embed.add_field(
			name="create", value="Creates/edits a character using the given information.", inline=False)
		embed.add_field(
			name="send", value="Creates a webhook, and sends a message, using it as your character.", inline=False)
		embed.add_field(
			name="delete", value="Delete a character by name.", inline=False)
		embed.add_field(
			name="characters", value="Displays an embed containing a list of all your characters.", inline=False)
		embed.add_field(
			name="show", value="Shows some information about a character.", inline=False)
		if ctx.user.guild_permissions.administrator:
			embed.add_field(
				name="setlogs", value="Sets a roleplay logging channnel so people don't use their characters to do bad stuff.")
		await ctx.followup.send(embed=embed)

	@roleplay.command(description="Creates/edits a character")
	@guild_only()
	@option("image", Attachment, description="Attachment to set as profile picture of your character")
	@option("name", description="Name of your character")
	@option("description", description="Description of your character", default="No description")
	async def create(self, ctx: ApplicationContext, image: Attachment, name: str, description: str):
		await ctx.response.defer(ephemeral=True)
		if not path.exists(f"database/roleplaydata/characters/{ctx.user.id}.json"):
			async with aiopen(f"database/roleplaydata/characters/{ctx.user.id}.json", "w") as fuwu:
				await fuwu.write("{}")
		data: dict = await client.jsonload(f"database/roleplaydata/characters/{ctx.user.id}.json")
		data.update({name: {
			"name": name, "image": image.url, "description": description
		}})
		await client.jsondump(data, f"database/roleplaydata/characters/{ctx.user.id}.json")
		webhook = await self.webhooks(ctx.channel)
		await webhook.send("Hello.", avatar_url=data[name]['image'], allowed_mentions=AllowedMentions.none(), username=name)
		await ctx.followup.send("Done")

	@roleplay.command(description="Sends a message as your character")
	@guild_only()
	@option("character", description="Name of the character")
	@option("message", description="Message to send as your character")
	async def send(self, ctx: ApplicationContext, character: str, message: str):
		await ctx.response.defer(ephemeral=True)
		if not path.exists(f"database/roleplaydata/characters/{ctx.author.id}.json"):
			async with aiopen(f"database/roleplaydata/characters/{ctx.author.id}.json", "w") as fuwu:
				await fuwu.write("{}")
		data: dict = await client.jsonload(f"database/roleplaydata/characters/{ctx.author.id}.json")
		dal: dict = data.get(character, None)
		if dal != None:
			char = await self.webhooks(ctx.channel)
			await char.send(message, avatar_url=dal['image'], username=character)
			await ctx.followup.send("Sent")
			if path.exists(f"database/roleplaydata/logs.json"):
				data2: dict = await client.jsonload("database/roleplaydata/logs.json")
				if data2.get(f'{ctx.guild_id}', None) != None:
					webhook = Webhook.from_url(
						data2.get(f'{ctx.guild_id}'), session=client.session2)
					embed = Embed(
						colour=BLANK, title="New roleplay message", timestamp=datetime.now())
					embed.add_field(name="User", value=ctx.user.__str__())
					embed.add_field(name="Character", value=character)
					embed.add_field(name="Message", value=message)
					embed.set_thumbnail(url=dal['image'])
					await webhook.send(embed=embed, username=ctx.me.name, avatar_url=ctx.me.avatar.url)
		else:
			await ctx.followup.send("No such character found.")

	@roleplay.command(description="Deletes a character")
	@guild_only()
	@option("character", description="Name of the character")
	async def delete(self, ctx: ApplicationContext, character: str):
		await ctx.response.defer(ephemeral=True)
		if not path.exists(f"database/roleplaydata/characters/{ctx.author.id}.json"):
			async with aiopen(f"database/roleplaydata/characters/{ctx.author.id}.json", "w") as fuwu:
				await fuwu.write("{}")
		data: dict = await client.jsonload(
			f"database/roleplaydata/characters/{ctx.author.id}.json")
		if data.get(character, None) != None:
			del data[character]
			await ctx.followup.send("Done")
			await client.jsondump(data, f"database/roleplaydata/characters/{ctx.author.id}.json")
			e = "Done"
		else:
			e = "No such character found"
		await ctx.followup.send(e)

	@roleplay.command(description="Lists all the characters you have")
	@guild_only()
	async def characters(self, ctx: ApplicationContext):
		await ctx.response.defer()
		if not path.exists(f"database/roleplaydata/characters/{ctx.author.id}.json"):
			async with aiopen(f"database/roleplaydata/characters/{ctx.author.id}.json", "w") as fuwu:
				await fuwu.write("{}")
		embed = Embed(colour=BLANK)
		data: dict = await client.jsonload(f"database/roleplaydata/characters/{ctx.author.id}.json")
		keys: list[dict[str, str]] = list(data.values())
		for item in keys:
			embed.add_field(name=item['name'], value=item['description'])
		await ctx.followup.send(embed=embed)

	@roleplay.command(description="Shows a character")
	@guild_only()
	@option("character", description="Name of character")
	async def show(self, ctx: ApplicationContext, character: str):
		await ctx.response.defer()
		if not path.exists(f"database/roleplaydata/characters/{ctx.author.id}.json"):
			async with aiopen(f"database/roleplaydata/characters/{ctx.author.id}.json", "w") as fuwu:
				await fuwu.write("{}")
		data: dict = await client.jsonload(f"database/roleplaydata/characters/{ctx.author.id}.json")
		dal = data.get(character, None)
		if dal != None:
			embed = Embed(
				title=dal['name'], colour=BLANK, description=dal['description'])
			embed.set_thumbnail(url=dal['image'])
		else:
			embed = Embed(
				colour=BLANK, description="No such character found")
		await ctx.followup.send(embed=embed)

	@roleplay.command(description="Set the logging channel for roleplaying")
	@guild_only()
	@has_permissions(administrator=True)
	@option("channel", TextChannel, description="Channel to set logs to")
	async def setlogs(self, ctx: ApplicationContext, channel: TextChannel):
		await ctx.response.defer(ephemeral=True)
		if not path.exists(f"database/roleplaydata/characters/{ctx.author.id}.json"):
			async with aiopen(f"database/roleplaydata/characters/{ctx.author.id}.json", "w") as fuwu:
				await fuwu.write("{}")
		data: dict = await client.jsonload(f"database/roleplaydata/logs.json")
		webhook = await channel.create_webhook(name=f"{self.bot.user.name} roleplay logs")
		data.update({
			f"{ctx.guild_id}": webhook.url
		})
		await client.jsondump(data, "database/roleplaydata/logs.json")
		await ctx.followup.send("Set")


def setup(bot: Bot):
	bot.add_cog(Roleplay(bot))

# python3 -m twine upload --repository pypi dist/*