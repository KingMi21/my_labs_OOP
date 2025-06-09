from injector import Injector, LifeStyle
from example import LoggerProtocol, DatabaseProtocol, EmailServiceProtocol, ConsoleLogger, MockDatabase, \
    MockEmailService, FileLogger, SqlDatabase, SmtpEmailService

COLORING = "\033[{}m{}\033[0m"


def colorize(text: str, color_code: int) -> str:
    return COLORING.format(color_code, text)


def configure_production(di_container: Injector) -> None:
    di_container.register(LoggerProtocol, ConsoleLogger, LifeStyle.SINGLETON)
    di_container.register(DatabaseProtocol, SqlDatabase, LifeStyle.SCOPED,
                          params={'connection_string': 'server=prod;db=app'})
    di_container.register(EmailServiceProtocol, SmtpEmailService, LifeStyle.PER_REQUEST,
                          params={'smtp_server': 'smtp.example.com'})


def configure_testing(di_container: Injector) -> None:
    di_container.register(LoggerProtocol, FileLogger, LifeStyle.SINGLETON,
                          params={'filename': 'test.log'})
    di_container.register(DatabaseProtocol, MockDatabase, LifeStyle.SCOPED)
    di_container.register(EmailServiceProtocol, MockEmailService, LifeStyle.PER_REQUEST)


def demonstrate_lifecycles(di_container: Injector) -> None:
    # Логгер - Singleton
    logger1 = di_container.get_instance(LoggerProtocol)
    logger1.log(colorize("Приложение запущено", 32))

    with di_container.scope():
        logger2 = di_container.get_instance(LoggerProtocol)
        print(colorize(f"Один и тот же экземпляр логгера внутри и вне области видимости: {logger1 is logger2}", 33))

        # База данных - Scoped
        db1 = di_container.get_instance(DatabaseProtocol)
        print(db1.query("SELECT * FROM users"))

        # Email сервис - PerRequest
        email1 = di_container.get_instance(EmailServiceProtocol)
        print(email1.send("user@example.com", "Тест", "Привет"))

        db2 = di_container.get_instance(DatabaseProtocol)
        print(colorize(f"Один и тот же экземпляр базы данных внутри области видимости: {db1 is db2}", 33))

    db3 = di_container.get_instance(DatabaseProtocol)
    print(colorize(f"Разные экземпляры базы данных вне области видимости: {db1 is db3}", 33))

    if di_container._registrations[EmailServiceProtocol]['life_style'] == LifeStyle.PER_REQUEST:
        with di_container.scope():
            email2 = di_container.get_instance(EmailServiceProtocol)
            email3 = di_container.get_instance(EmailServiceProtocol)
            print(colorize(f"Разные экземпляры email сервиса с PerRequest: {email2 is email3}", 33))


def demonstrate_test_config(di_container: Injector) -> None:
    logger = di_container.get_instance(LoggerProtocol)
    logger.log("Тестовая конфигурация запущена")

    with di_container.scope():
        db = di_container.get_instance(DatabaseProtocol)
        print(db.query("SELECT * FROM users"))

        email = di_container.get_instance(EmailServiceProtocol)
        print(email.send("test@example.com", "Тест", "Привет"))


if __name__ == "__main__":
    production_injector = Injector()
    configure_production(production_injector)
    demonstrate_lifecycles(production_injector)

    test_injector = Injector()
    configure_testing(test_injector)
    demonstrate_test_config(test_injector)
