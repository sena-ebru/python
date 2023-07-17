#!/usr/bin/env python
# coding: utf-8

# In[6]:


import platform
import psutil
import subprocess

def get_computer_specs():
    # İşletim sistemi bilgileri
    os_name = platform.system()
    os_version = platform.release()

    # CPU bilgileri
    cpu_name = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count(logical=True)

    # RAM (bellek) bilgisi
    mem = psutil.virtual_memory()
    total_ram = mem.total / (1024 ** 3)
    available_ram = mem.available / (1024 ** 3)
    used_ram = mem.used / (1024 ** 3)
    ram_percentage = mem.percent

    # Bilgisayar modeli ve markası
    try:
        if os_name == "Windows":
            computer_info = subprocess.check_output(["wmic", "computersystem", "get", "manufacturer, model"]).decode().strip()
            brand, model = [item.strip() for item in computer_info.split("\n")[1:-1]]
        else:
            model = " Tulpar T7 V20.2"
            brand = "MONSTER"
    except:
        model = "Tulpar T7 V20.2"
        brand = "MONSTER"

    print("İşletim Sistemi: {} {}".format(os_name, os_version))
    print("İşlemci: {}".format(cpu_name))
    print("CPU Çekirdek Sayısı: {}".format(cpu_cores))
    print("CPU İş Parçacığı Sayısı: {}".format(cpu_threads))
    print("RAM (Toplam): {:.2f} GB".format(total_ram))
    print("RAM (Kullanılabilir): {:.2f} GB".format(available_ram))
    print("RAM Kullanımı: {:.2f} GB ({}%)".format(used_ram, ram_percentage))
    print("Bilgisayar Markası: {}".format(brand))
    print("Bilgisayar Modeli: {}".format(model))

if __name__ == "__main__":
    get_computer_specs()


# In[ ]:




