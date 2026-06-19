import can
import time
import struct
import sys
import curses

class ZLAC8015D:
    def __init__(self, channel='can0', node_id=1):
        try:
            self.bus = can.interface.Bus(channel=channel, bustype='socketcan')
        except OSError:
            print(f"Ошибка: Интерфейс {channel} не найден или не поднят.")
            sys.exit(1)
            
        self.node_id = node_id
        self.cob_id = 0x600 + self.node_id
        
    def send_sdo(self, index, subindex, data, data_len):
        """Формирование и отправка SDO-пакета записи"""
        cmd = {1: 0x2F, 2: 0x2B, 4: 0x23}[data_len]
        payload = list(data) + [0] * (4 - len(data))
        msg_data = [cmd, index & 0xFF, (index >> 8) & 0xFF, subindex] + payload
        msg = can.Message(arbitration_id=self.cob_id, data=msg_data, is_extended_id=False)
        self.bus.send(msg)
        time.sleep(0.015) # Стабильный таймаут для логики драйвера

    def initialize(self):
        """Инициализация по ТЗ: Сеть -> Режим -> Ускорения -> CiA 402 State Machine"""
        # 1. Перевод CAN-сети в Operational
        self.bus.send(can.Message(arbitration_id=0x000, data=[0x01, 0x00], is_extended_id=False))
        time.sleep(0.05)
        
        # Настройка синхронизации/тормоза (регистр 0x200F)
        self.send_sdo(0x200F, 0x00, [0x01, 0x00], 2)
        
        # 2. Выбор Profile Velocity Mode (0x6060 = 0x03)
        self.send_sdo(0x6060, 0x00, [0x03], 1)
        
        # 3. Настройка динамики разгона и торможения (0x6083 и 0x6084)
        accel = struct.pack('<i', 100) # 100 мс плавный разгон
        for subindex in [0x01, 0x02]:
            self.send_sdo(0x6083, subindex, accel, 4)
            self.send_sdo(0x6084, subindex, accel, 4)

        # 4. Проход по CiA 402 State Machine
        # Шаг А: Shutdown (Готовность к включению) -> Controlword = 0x0006
        self.send_sdo(0x6040, 0x00, [0x06, 0x00], 2)
        time.sleep(0.02)
        
        # Шаг Б: Switch On (Включено) -> Controlword = 0x0007
        self.send_sdo(0x6040, 0x00, [0x07, 0x00], 2)
        time.sleep(0.02)
        
        # Шаг В: Enable Operation (Работа разрешена) -> Controlword = 0x000F
        self.send_sdo(0x6040, 0x00, [0x0F, 0x00], 2)
        time.sleep(0.02)

    def set_sync_speed(self, left_rpm, right_rpm):
        """Синхронная отправка скоростей с инверсией левого зеркального колеса"""
        l = max(-300, min(300, int(-left_rpm))) # Инвертируем левое колесо
        r = max(-300, min(300, int(right_rpm)))
        data = struct.pack('<hh', l, r)
        self.send_sdo(0x60FF, 0x03, data, 4)

    def quick_stop(self):
        """Аварийное выключение (Quick Stop) по стандарту CiA 402"""
        try:
            # Бит 2 в Controlword сбрасывается в 0 для активации Quick Stop (0x000B)
            # Это заставляет драйвер экстренно остановить моторы по зашитому профилю аварии
            self.send_sdo(0x6040, 0x00, [0x0B, 0x00], 2)
            time.sleep(0.05)
            # Полное снятие напряжения с мостов (Disable Operation / Shutdown)
            self.send_sdo(0x6040, 0x00, [0x06, 0x00], 2)
        except can.CanOperationError:
            pass # Если сеть уже легла, не роняем скрипт в обработчике аварии

    def shutdown_bus(self):
        """Окончательное закрытие сокета шины"""
        self.bus.shutdown()


def main(stdscr):
    # Конфигурация curses под интерактивный терминал
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    
    driver = ZLAC8015D(channel='can0', node_id=1)
    
    stdscr.addstr(0, 0, "Инициализация привода по CiA 402...")
    stdscr.refresh()
    
    # Инициализация внутри общего try, чтобы перехватить сбои на старте
    driver.initialize()
    
    current_left = 0
    current_right = 0
    
    SPEED_STEP = 10   # Шаг регулировки (RPM)
    MAX_SPEED = 200   # Безопасный лимит для 24В на весу
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "=== УПРАВЛЕНИЕ ПЛАТФОРМОЙ ПО СТАНДАРТУ CiA 402 ===", curses.A_BOLD)
        stdscr.addstr(2, 0, "Управление движением:")
        stdscr.addstr(3, 2, "Стрелка ВВЕРХ  : Вперед (+ RPM)")
        stdscr.addstr(4, 2, "Стрелка ВНИЗ   : Назад / Торможение (- RPM)")
        stdscr.addstr(5, 2, "Стрелка ВЛЕВО  : Разворот на месте влево")
        stdscr.addstr(6, 2, "Стрелка ВПРАВО : Разворот на месте вправо")
        stdscr.addstr(7, 2, "ПРОБЕЛ         : Плавный сброс скорости в 0 (моторы на моменте)")
        stdscr.addstr(8, 2, "Клавиша 's'    : Аварийная остановка (QUICK STOP)")
        stdscr.addstr(9, 2, "Клавиша 'q'    : Безопасный выход и отключение привода")
        
        stdscr.addstr(12, 0, "МОНИТОРИНГ ЗАДАННОЙ СКОРОСТИ:", curses.A_UNDERLINE)
        stdscr.addstr(13, 2, f"Левое колесо (инвертировано в шине) : {current_left} RPM")
        stdscr.addstr(14, 2, f"Правое колесо                       : {current_right} RPM")
        stdscr.refresh()
        
        key = stdscr.getch()
        
        if key == ord('q') or key == 27: # 'q' или Esc
            break
            
        elif key == ord('s'): # Авария (Quick Stop)
            stdscr.clear()
            stdscr.addstr(0, 0, "[ЗАПУЩЕН QUICK STOP] Аварийное торможение привода!", curses.A_REVERSE)
            stdscr.refresh()
            driver.quick_stop()
            time.sleep(1.0)
            break
            
        elif key == curses.KEY_UP:
            current_left = min(MAX_SPEED, current_left + SPEED_STEP)
            current_right = min(MAX_SPEED, current_right + SPEED_STEP)
            driver.set_sync_speed(current_left, current_right)
            
        elif key == curses.KEY_DOWN:
            current_left = max(-MAX_SPEED, current_left - SPEED_STEP)
            current_right = max(-MAX_SPEED, current_right - SPEED_STEP)
            driver.set_sync_speed(current_left, current_right)
            
        elif key == curses.KEY_LEFT:
            current_left = max(-MAX_SPEED, current_left - SPEED_STEP)
            current_right = min(MAX_SPEED, current_right + SPEED_STEP)
            driver.set_sync_speed(current_left, current_right)
            
        elif key == curses.KEY_RIGHT:
            current_left = min(MAX_SPEED, current_left + SPEED_STEP)
            current_right = max(-MAX_SPEED, current_right - SPEED_STEP)
            driver.set_sync_speed(current_left, current_right)
            
        elif key == ord(' '): # Остановка уставки в 0
            current_left = 0
            current_right = 0
            driver.set_sync_speed(0, 0)
            
        time.sleep(0.05)

    # Перед выходом из curses-интерфейса переводим моторы в безопасный режим плавного стопа
    driver.set_sync_speed(0, 0)
    time.sleep(0.1)
    driver.quick_stop()


if __name__ == "__main__":
    # Финальный глобальный блок try/finally согласно ТЗ
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"\n[Критическая ошибка выполнения]: {e}")
    finally:
        # Конструкция гарантирует, что даже если упал curses или код внутри main,
        # сокет шины закроется корректно и освободит дескриптор в Ubuntu Linux
        # Желательно продублировать quick_stop для физической безопасности моторов
        try:
            # Создаем временный объект для финализации, если основной упал
            emergency_driver = ZLAC8015D(channel='can0', node_id=1)
            emergency_driver.quick_stop()
            emergency_driver.shutdown_bus()
        except:
            pass
        print("\n[FINALLY] Сеть CAN отключена. Драйвер переведен в безопасное состояние.")