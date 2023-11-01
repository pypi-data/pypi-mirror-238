from setuptools import setup

VERSION = '0.1.5' 
DESCRIPTION = 'Paquete de notificaciones'
LONG_DESCRIPTION = 'Paquete de canales de notificaciones de kemok'

# Configurando
setup(
        name="notificationspackageke", 
        version=VERSION,
        author="Carlos Pacheco",
        license='MIT',
        author_email="carlos.pacheco@kemok.io",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url='https://github.com/Kemok-Repos/notification-service',
        packages=['notificationmethods']
)