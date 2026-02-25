import logging
import os

def configurar_logs():
    if not os.path.exists('logs'):
        os.makedirs('logs')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S' ,
        handlers=[
            logging.FileHandler("logs/clinica.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logging.info("=== Sistema de Logs Iniciado ===")
    