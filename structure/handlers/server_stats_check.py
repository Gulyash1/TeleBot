import os
import time
import psutil
from aiogram import Router
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

stats_router = Router()

START_TIME = time.time()

ALLOWED_USERS = {
    int(os.getenv('ADMIN_ID'))
}


@stats_router.message(lambda msg: msg.text == "/stats")
async def stats_handler(msg: Message):

    if msg.from_user.id not in ALLOWED_USERS:
        return

    # --- CPU ---
    cpu = psutil.cpu_percent(interval=0.5)

    # --- RAM ---
    mem = psutil.virtual_memory()

    # --- DISK ---
    disk = psutil.disk_usage("/")

    # --- UPTIME ---
    uptime_seconds = int(time.time() - START_TIME)
    uptime = time.strftime("%H:%M:%S", time.gmtime(uptime_seconds))

    # --- PROCESS INFO (бот) ---
    process = psutil.Process(os.getpid())
    proc_mem = process.memory_info().rss / 1024 / 1024

    text = (
        "<b>Server Stats</b>\n\n"
        f"CPU: {cpu}%\n"
        f"RAM: {mem.percent}% ({mem.used // 1024**2} / {mem.total // 1024**2} MB)\n"
        f"Disk: {disk.percent}% ({disk.used // 1024**3} / {disk.total // 1024**3} GB)\n\n"
        f"Bot RAM: {proc_mem:.1f} MB\n"
        f"Uptime: {uptime}"
    )

    await msg.answer(text, parse_mode="HTML")