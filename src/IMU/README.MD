##IMU Data Logger

Скрипт для считывания данных с IMU-датчика WitMotion и публикации их в шину ros2/imu/raw_data
**Топик** '/imu/data_raw'
**Тип Собщения** 'sensor_msgs/msg/Imu'
#Установка:

Создать виртуальное окружение: python3 -m venv myenv
Активировать: source myenv/bin/activate
Установить зависимости: pip install -r requirements.txt

#Запуск
1) launch IMU.py in terminal;
2) in the second terminal:
source /opt/ros/jazzy/setup.bash
ros2 topic echo /imu/data_raw

