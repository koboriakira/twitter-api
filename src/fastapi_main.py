import logging
import time

from fastapi import FastAPI, Request
from mangum import Mangum

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
# app.include_router(projects.router, prefix="/projects", tags=["projects"])
# app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
# app.include_router(healthcheck.router, prefix="/healthcheck", tags=["healthcheck"])
# app.include_router(music.router, prefix="/music", tags=["music"])
# app.include_router(webclip.router, prefix="/webclip", tags=["webclip"])
# app.include_router(video.router, prefix="/video", tags=["video"])
# app.include_router(prowrestling.router, prefix="/prowrestling", tags=["prowrestling"])
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
# app.include_router(task.router, prefix="/task", tags=["tasks"])
# app.include_router(page.router, prefix="/page", tags=["page"])
# app.include_router(books.router, prefix="/books", tags=["books"])


# handler = Mangum(app, lifespan="off")


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
