##IMU Data Logger

Скрипт для считывания данных с IMU-датчика WitMotion и записи их в CSV-файл в формате timestamp, accel_x/accel_y/accel_z, gyro_x/gyro_y/gyro_z, roll, pitch, yaw.

#Установка:

Создать виртуальное окружение: python3 -m venv myenv
Активировать: source myenv/bin/activate
Установить зависимости: pip install -r requirements.txt

#Запуск
`python3 imu_logger.py
