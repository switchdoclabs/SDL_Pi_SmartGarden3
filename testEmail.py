import sendemail
  
import config
import readJSON

readJSON.readJSON("")
config.SWDEBUG = True
print("config.mailUser", config.mailUser)
print("config.notifyAddress=", config.notifyAddress)
print("config.fromAddress=", config.fromAddress)
print("config.mailPassword=", config.mailPassword)

sendemail.sendEmail("test", "Test SmartGarden3 Email", "From Smart Garden 3 down.", config.notifyAddress,  config.fromAddress, "");
