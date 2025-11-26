from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_welcome_message(verify_link: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Підтвердження Email</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background-color: #4CAF50; padding: 30px 40px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">
                                o4ki.com.ua
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 40px 20px 40px;">
                            <h2 style="margin: 0 0 20px 0; color: #333333; font-size: 24px;">
                                Вітаємо!
                            </h2>
                            <p style="margin: 0 0 20px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                Ви успішно зареєструвалися на o4ki.com.ua.
                            </p>
                            <p style="margin: 0 0 30px 0; color: #666666; font-size: 16px; line-height: 1.6;">
                                Для завершення реєстрації та підтвердження вашої електронної пошти, будь ласка, натисніть на кнопку нижче:
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Button -->
                    <tr>
                        <td style="padding: 0 40px 40px 40px;" align="center">
                            <table cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td style="border-radius: 4px; background-color: #4CAF50;">
                                        <a href="{verify_link}" style="display: inline-block; padding: 16px 40px; font-size: 16px; color: #ffffff; text-decoration: none; font-weight: bold;">
                                            Підтвердити Email
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Alternative Link -->
                    <tr>
                        <td style="padding: 0 40px 40px 40px;">
                            <p style="margin: 0; color: #999999; font-size: 14px; line-height: 1.6; text-align: center;">
                                Якщо кнопка не працює, скопіюйте це посилання у ваш браузер:
                            </p>
                            <p style="margin: 10px 0 0 0; text-align: center;">
                                <a href="{verify_link}" style="color: #4CAF50; font-size: 14px; word-break: break-all;">
                                    {verify_link}
                                </a>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f9f9f9; padding: 30px 40px; text-align: center; border-top: 1px solid #eeeeee;">
                            <p style="margin: 0; color: #999999; font-size: 13px; line-height: 1.6;">
                                Якщо ви не реєструвалися на o4ki.com.ua, проігноруйте цей лист.
                            </p>
                            <p style="margin: 10px 0 0 0; color: #999999; font-size: 13px;">
                                © 2024 o4ki.com.ua. Всі права захищені.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""







