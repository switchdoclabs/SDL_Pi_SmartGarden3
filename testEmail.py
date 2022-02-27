import sendemail
  
import config
import readJSON

readJSON.readJSON("")
config.SWDEBUG = True
print("config.mailUser", config.mailUser)
print("config.notifyAddress=", config.notifyAddress)
print("config.fromAddress=", config.fromAddress)
print("config.mailPassword=", config.mailPassword)

sendemail.sendEmail("test", "Test SmartGarden3 Email", "From SmartGarden 3 test.", config.notifyAddress,  config.fromAddress, "");
