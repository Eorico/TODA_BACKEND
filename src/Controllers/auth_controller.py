from Services.auth_service import signup, login, forgot_password

async def signup_controller(data):
    return await signup(data)

async def login_controller(data):
    return await login(data)

async def forgot_controller(data):
    return await forgot_password(data)