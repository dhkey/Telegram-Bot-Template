import asyncio
import structlog
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_reader import get_config, BotConfig, LogConfig, DatabaseConfig
from logs import get_structlog_config
from structlog.typing import FilteringBoundLogger
from dispatcher import dp
from databaseConnection import connection
import handlers

async def main():
    
    log_config: LogConfig = get_config(model=LogConfig, root_key="logs")
    structlog.configure(**get_structlog_config(log_config))

    bot_config: BotConfig = get_config(model=BotConfig, root_key="bot")

    bot = Bot(
        token=bot_config.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    logger: FilteringBoundLogger = structlog.get_logger()
    await logger.ainfo("Starting the bot...")

    @dp.startup()
    async def onSturtup():
        await logger.ainfo("BOT ::: Started ✅")

    @dp.shutdown()
    async def onShutdown():
        connection.closeConnection()

    try:
        await dp.start_polling(bot, skip_updates=False)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
