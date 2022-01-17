# send text
import sendemail
  
import config
import readJSON

readJSON.readJSON("")
config.SWDEBUG = True
print("config.mailUser", config.mailUser)
print("config.textnotifyAddress=", config.textnotifyAddress)
print("config.fromAddress=", config.fromAddress)
print("config.mailPassword=", config.mailPassword)

sendemail.sendEmail("test", "Test SmartGarden3 Email", "From SmartGarden3 .", config.textnotifyAddress,  config.fromAddress, "");
