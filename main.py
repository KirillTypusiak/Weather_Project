from modules import application, main_window
from utils import load_cities

def main():
    try:
        load_cities()  # Завантажуємо міста один раз при старті програми
        main_window.show()
        application.exec()
    except Exception as error:
        print(f"помилка {error}")
    
if __name__ == "__main__":
    main()
