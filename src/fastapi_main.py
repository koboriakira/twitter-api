import logging
import time

from fastapi import FastAPI, Request
from mangum import Mangum

from interface.fastapi_router.tweet.tweet import router as tweet_router

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
    return response
    # try:

    # except:
    #     ErrorReporter().execute()
    #     raise


handler = Mangum(app, lifespan="off")
