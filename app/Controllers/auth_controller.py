from Services.auth_service import AuthService

async def signup_controller(data):
    return await AuthService.signup(data)

async def login_controller(data):
    return await AuthService.login(data)

async def forgot_controller(data):
    return await AuthService.forgot_password(data)

async def verify_code_controller(data):
    return await AuthService.verify_code(data)

async def reset_password_controller(data):
    return await AuthService.reset_password(data)