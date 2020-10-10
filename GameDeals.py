import config
import discord
import asyncio
import logging
import traceback
from image_scraper import preview_image
from datetime import datetime
from reddit_scraper import RedditScraper
from game_deal_manager import GameDealManager

logging.basicConfig(level=logging.INFO)

# TODO: persistent data, log to file


class GameDealsClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.get_deals())

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.content in ['gd.info', 'gd.i']:
            description = 'Game Deals is a bot that helps you know the latest discounts on videogames you\'ll keep forever in your library!'
            embed = discord.Embed(title='Bot Information', description=description, colour=0xa865e3) \
                .add_field(name='Developer', value='[<REDDIT_USERNAME>](https://github.com/AJMC2OO2)')
            await message.channel.send(embed=embed)
        elif message.content in ['gd.help', 'gd.h']:
            embed = discord.Embed(title='Game Deals Commands', colour=0xa865e3) \
                .add_field(name='gd.info', value='Display bot information.', inline=False) \
                .add_field(name='gd.help', value='Display the commands menu.')
            await message.channel.send(embed=embed)

    async def on_error(event, *args, **kwargs):
        message = args[0]
        logging.warning(traceback.format_exc())

    async def get_deals(self):
        await self.wait_until_ready()

        reddit = RedditScraper()
        manager = GameDealManager(reddit)
        channel = self.get_channel(config.DISCORD_CHANNEL_ID)

        while not self.is_closed():
            free_deals = manager.find_deals()
            new_free_deals = []

            if free_deals:
                for deal in free_deals:
                    time = datetime.fromtimestamp(deal.created_utc)
                    diff = datetime.utcnow() - time
                    diff = diff.total_seconds()
                    if diff < 5 * 60:
                        new_free_deals.append(deal)
                    else:
                        continue

                for deal in new_free_deals:
                    embed = discord.Embed(
                        title=deal.title[deal.title.find(
                            "]")+2:len(deal.title)],
                        description=deal.title[1:deal.title.find("]")],
                        url=deal.url,
                        color=0xa865e3
                    )
                    embed.set_image(url=preview_image(deal.url))
                    await self.__send_deals(embed)
                    new_free_deals.remove(deal)
                    await asyncio.sleep(10 * 60)

    async def __send_deals(self, embed):
        channels_to_send_to = [c for c in self.get_all_channels(
        ) if c.type == discord.ChannelType.text and 'game-deals' in c.name]

        for channel in channels_to_send_to:
            if channel.permissions_for(channel.guild.me).send_messages:
                await channel.send(embed=embed)
            else:
                await channel.send('I don\'t have the permission to send messages in this channel!')


def main():
    client = GameDealsClient()
    client.run(config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
