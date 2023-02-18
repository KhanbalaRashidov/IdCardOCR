import os
from mrz_reader import mrz_reader
import common
from PIL import Image


mrz_reader=mrz_reader()
mrz_reader.load()



def getIdentityText(img):
    txt,face=mrz_reader.predict(img=img)
    common.resizeImage(img=img)
    idCard=common.getImage(img=img)
    #os.remove(img)
    print(txt)
    line1=txt[0:30]
    line2=txt[30:60]
    line3=txt[60:90]
    
    documentype=line1[0]
    
    countryCode=line1[2:5]
    
    documentNo=line1[5:14]
    
    identityNo=common.removeJunk(line1[15:30])
    
    dateOfBirth=common.getDate(common.removeJunk(line2[0:6]))
    
    gender=line2[7]
    
    expireDate=common.getDate(line2[8:14])
    
    nationality=common.countries[line2[15:18]]
    
    surnameIndex=line3[0:30].find('<<')
    lastName=line3[0:surnameIndex]
    
    givenName=line3[surnameIndex+2:30]
    givenIndex=givenName.find('<')
    firstName=givenName[0:givenIndex]+' '+ common.removeJunk(givenName[givenIndex+1:30])
    
    return {
        "documentTye":documentype,
        "countryCode":countryCode,
        "documentNo":documentNo,
        "identityNo":identityNo,
        "dateOfBirth":dateOfBirth,
        "expireDate":expireDate,
        "gender":gender,
        "nationality":nationality,
        "firstName":firstName,
        "lastName":lastName,
        "mrz":txt,
        "idCardImage":idCard,
    }