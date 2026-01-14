from fastapi import FastAPI
from router import admin_router,login_router,service_router,user_router

app = FastAPI()
app.mount("/auth",login_router.login_app)
app.mount("/admin",admin_router.admin_main_app)
app.mount("/user",user_router.user_main_app)
app.mount("/service",service_router.service)