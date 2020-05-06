import config
import discord
import asyncio
import logging
import traceback
from datetime import datetime
from reddit_scraper import RedditScraper
from game_deal_manager import GameDealManager

logging.basicConfig(level=logging.INFO)

# TODO: persistent data, log to file


class GratisClient(discord.Client):

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
            if self.__between_6am_and_6pm():
                new_free_deals = manager.find_deals()

                if new_free_deals:
                    for deal in new_free_deals:
                        embed = discord.Embed(
                            title=deal.title[deal.title.find(" ")+1:len(x)],
                            description=deal.title[1:deal.title.find(" ") - 1],
                            url=deal.url
                            color=0x2df228
                        )
                        await self.__send_deals(embed)

                # Sleep for 4 hours and 0 minutes
                await asyncio.sleep(4 * 60 * 60)
            else:
                await asyncio.sleep(1)

    def __between_6am_and_6pm(self):
        """
        Return true if current time is within 6am or 6pm.
        """
        current_time = datetime.now()
        return ((current_time.hour >= 6) or (current_time.hour <= 18)) and (current_time.minute == 0)

    async def __send_deals(self, embed):
        channels_to_send_to = [c for c in self.get_all_channels(
        ) if c.type == discord.ChannelType.text and 'game-deals' in c.name]

        for channel in channels_to_send_to:
            if channel.permissions_for(channel.guild.me).send_messages:
                await channel.send(embed=embed)
            else:
                await channel.send('I don\'t have the permission to send messages in this channel!')


def main():
    client = GratisClient()
    client.run(config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()