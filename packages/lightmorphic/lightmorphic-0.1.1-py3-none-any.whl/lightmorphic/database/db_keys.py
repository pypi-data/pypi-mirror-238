def appid():
    appid='appid='+input('''The OpenWeather One Call API is used to retrive the city specific weather data.
The value you enter is not recorded, saved or transmitted.
So each time you call the OpenWeather One Call API you will have to enter it manually at the promt.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Enter the value of your private OpenWeather One Call API:''')
    return appid


if __name__ == '__main__':
    print("The db_keys's main module is running")
else:
    pass
