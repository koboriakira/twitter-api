import logging
import time

from fastapi import FastAPI, Request
from mangum import Mangum

from interface.fastapi_router.tweet.tweet import router as tweet_router
from interface.fastapi_router.user.user import router as user_router

# ログ
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
# if Environment.is_dev():
#     logging.basicConfig(level=logging.DEBUG)

# アプリ設定
app = FastAPI(
    title="Twitter API",
    version="0.0.1",
)
app.include_router(tweet_router, prefix="/tweet", tags=["tweet"])
app.include_router(user_router, prefix="/user", tags=["user"])


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


# ミドルウェア
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):  # noqa: ANN001, ANN201
    start_time = time.time()
    response = await call_next(request)
    process_time = int((time.time() - start_time) * 1000)  # 整数値のミリ秒
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response


handler = Mangum(app, lifespan="off")
