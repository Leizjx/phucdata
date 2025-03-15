# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import mysql.connector

# Cấu hình Chrome (chạy ẩn)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Chạy ẩn trình duyệt

# Khởi tạo trình duyệt
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Truy cập NetTruyen
url = "https://nettruyenrr.com/"
driver.get(url)

# Kết nối MySQL
try:
    print(" Kết nối MySQL...")
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # XAMPP mặc định không có mật khẩu
        database="story"
    )
    cursor = connection.cursor()

    # Chờ danh sách truyện xuất hiện
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "item")))

    # Lấy danh sách truyện
    stories = driver.find_elements(By.CLASS_NAME, "item")

    for story in stories:
        try:
            # Lấy tên truyện
            name = story.find_element(By.CLASS_NAME, "jtip").text.strip()

            # Lấy chapter mới nhất
            chapter_text = story.find_element(By.CLASS_NAME, "chapter").text.strip()
            chapter_number = int(''.join(filter(str.isdigit, chapter_text)))  # Lấy số từ chuỗi

            print(f" {name} - Chapter {chapter_number}")

            # Lưu vào MySQL
            sql = "INSERT INTO story (title, chapter) VALUES (%s, %s)"
            cursor.execute(sql, (name, chapter_number))

        except Exception as e:
            print(f" Lỗi lấy dữ liệu: {e}")
            continue

    # Lưu thay đổi vào MySQL
    connection.commit()
    print(" Dữ liệu đã lưu vào MySQL!")

except mysql.connector.Error as error:
    print(f" Lỗi kết nối MySQL: {error}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print(" Đã đóng kết nối MySQL.")

# Đóng trình duyệt
driver.quit()
