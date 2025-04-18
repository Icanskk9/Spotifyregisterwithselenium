import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

fake = Faker()

def generate_random_email():
    domains = ["@gmail.com", "@yahoo.com", "@hotmail.com"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return name + random.choice(domains)

def register_spotify_account(password):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://www.spotify.com/id-id/signup/")

    try:
        wait = WebDriverWait(driver, 20)
        email = generate_random_email()
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
        print(f"✔️ Email: {email}")

        next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        time.sleep(2)
        driver.execute_script("arguments[0].click();", next_btn)

        wait.until(EC.presence_of_element_located((By.ID, "new-password")))
        time.sleep(5)
        driver.find_element(By.ID, "new-password").send_keys(password)
        print(f"✔️ Password: {password}")

        next_btn2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        time.sleep(2)
        driver.execute_script("arguments[0].click();", next_btn2)

        wait.until(EC.presence_of_element_located((By.ID, "displayName")))
        name = fake.first_name()
        driver.find_element(By.ID, "displayName").send_keys(name)
        print(f"✔️ Nama: {name}")

        day = str(random.randint(1, 28)).zfill(2)
        month = str(random.randint(1, 12))
        year = str(random.randint(1980, 2005))

        driver.find_element(By.ID, "day").send_keys(day)
        Select(driver.find_element(By.ID, "month")).select_by_value(month)
        driver.find_element(By.ID, "year").send_keys(year)
        print(f"✔️ Lahir: {day}-{month}-{year}")

        checkbox1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "Indicator-sc-hjfusp-0")))
        driver.execute_script("arguments[0].click();", checkbox1)

        next_btn3 = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        time.sleep(2)
        driver.execute_script("arguments[0].click();", next_btn3)

        checkboxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Indicator-sc-1airx73-0")))
        if len(checkboxes) >= 2:
            driver.execute_script("arguments[0].click();", checkboxes[0])
            time.sleep(1)
            driver.execute_script("arguments[0].click();", checkboxes[1])

        signup_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Sign up']")))
        time.sleep(2)
        driver.execute_script("arguments[0].click();", signup_btn)
        print("🎯 Klik tombol Sign up!")

        time.sleep(5)
        current_url = driver.current_url

        if "download/windows" in current_url:
            print("✅ Registrasi berhasil!")
            with open("akun_spotify.txt", "a") as file:
                file.write(f"{email} | {password}\n")
            print("💾 Akun disimpan")
        else:
            print("❌ Gagal redirect ke halaman sukses.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        driver.quit()

# === MAIN LOOP ===
if __name__ == "__main__":
    password = "Password123!"
    jumlah = int(input("Berapa akun Spotify yang ingin dibuat?: "))

    for i in range(jumlah):
        print(f"\n🚀 Membuat akun ke-{i+1}")
        register_spotify_account(password)
        time.sleep(random.randint(1, 5))  # jeda antar akun

    print("\n🎉 Semua akun selesai dibuat!")
