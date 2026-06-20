import time
import csv
from datetime import datetime
from witmotion import IMU

PORT = '/dev/ttyUSB0'
BAUD = 38400
CSV_FILE = 'imu_data_log.csv'


def main():
    print(f"[*] Подключение к IMU на порту {PORT} (baud_rate = {BAUD})...")
    try:
        imu = IMU(path=PORT, baudrate=BAUD)
    except Exception as e:
        print(f"[!] Ошибка подключения: {e}")
        return

    with open(CSV_FILE, mode='w', newline='') as f:
        writer = csv.writer(f)
        # Пишем шапку CSV
        writer.writerow(['timestamp', 'accel_x', 'accel_y', 'accel_z',
                         'gyro_x', 'gyro_y', 'gyro_z',
                         'roll', 'pitch', 'yaw'])

        print("[*] Соединение установлено")
        try:
            while True:
                #данные
                accel = imu.get_acceleration()
                gyro = imu.get_angular_velocity()
                angle = imu.get_angle()

                #Ждем данные
                if accel is None or gyro is None or angle is None:
                    time.sleep(0.01)
                    continue

                # Генерируем таймстемп
                ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

                # Печатать в терминал
                print(f"[{ts}] "
                      f"Accel(g): {accel[0]:5.2f} {accel[1]:5.2f} {accel[2]:5.2f} | "
                      f"Gyro(°/s): {gyro[0]:7.2f} {gyro[1]:7.2f} {gyro[2]:7.2f} | "
                      f"Angle(°): {angle[0]:6.2f} {angle[1]:6.2f} {angle[2]:6.2f}")

                # Пишем данные в CSV лог
                writer.writerow([ts, *accel, *gyro, *angle])

                # Частота опроса (0.05 сек = 20 Гц)
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\n[*] Остановка записи")
        finally:
            imu.close()
            print(f"[*] Лог успешно сохранен в файл: {CSV_FILE}")


if __name__ == '__main__':
    main()