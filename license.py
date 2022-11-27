import base64
import datetime
import hashlib
import platform
import time

from plist_set import ProcessSettingsClass


class LicenseClass():

    def __init__(self):

        self.release = "beta-0.4"

        self.secondsSinceEpoch = time.time()

        self.params = ProcessSettingsClass()

        # self.hardExpires()
        # self.saveKeyUser("6d93ef3-5fbadf4-28e4d60-c5cc14f","info@jpereira.net" )
        # print(self.betaXpires())
        # self.reset()
        self.updateRelease()
        # self.checkLicense()

    def updateRelease(self):

        oldReleases = ["doomsday-alpha-0.1", "newnormality-beta-0.21", "newnormality-beta-0.29","newnormality-beta-0.3","beta-0.4"]

        if self.params.setting_contains("release"):
            currentRelease = self.params.setting_restore("release")
            if self.release != currentRelease:
                if currentRelease in oldReleases:
                    self.params.save_setting('release', self.release)
                    expire = self.installDate()
                    self.params.save_setting('datecode', expire)
                    self.saveToken()
                    print("update")
        elif self.params.setting_restore("release") is "":
            self.params.save_setting('release', self.release)
        else:
            self.params.save_setting('release', self.release)

    def betaXpires(self):

        epochExpire = datetime.datetime(2021, 12, 31, 0, 0).timestamp()

        # epochExpire = (datetime.datetime(2020, 6, 28, 0, 0) - datetime.datetime(1970, 1, 1)).total_seconds()

        err = self.secondsSinceEpoch - epochExpire

        d1 = time.strftime('%Y-%m-%d', time.localtime(self.secondsSinceEpoch))
        d2 = time.strftime('%Y-%m-%d', time.localtime(epochExpire))

        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")

        dias = abs((d2 - d1).days)

        if err > 0:
            # ha caducado
            note = "Beta expired!"
            return (True, note)

        else:

            note = "Beta " + str(dias) + " days left"
            return (False, note)

    def hardExpires(self):
        # caduca en junio
        if self.secondsSinceEpoch > 1593295991.91:
            quit()

    def reset(self):
        self.params.settings_restore("datecode")
        self.params.settings_restore("user")
        self.params.settings_restore("key")
        self.params.settings_restore("token")

    def hashtoken(self):
        expire = self.params.setting_restore("datecode")
        os = str(platform.system()) + str(platform.release()) + str(platform.version()) + self.release
        # cadena = str(expire).decode('base64')  + os
        #print(str(expire))
        cadena = str(base64.b64encode(bytes(expire, 'utf-8'))) + os

        return hashlib.md5(cadena.encode('utf-8')).hexdigest()

    def saveToken(self):

        token = self.hashtoken()
        self.params.save_setting('token', token)

    def checkToken(self):
        token = self.hashtoken()
        getToken = self.params.setting_restore("token")

        if token == getToken:
            return True
        else:
            return False

    def checkLicense(self):

        expire = None

        if self.params.setting_contains("user") and self.params.setting_contains("key"):
            print("comprueba usuarios")
            x = self.checkKey()
            return x

        else:
            x = self.betaXpires()
            return x
            '''
            if self.params.guicontains("datecode") and self.checkToken():
                
                expire = self.params.guirestore("datecode")
                #x = self.expireTrial( str(expire).decode('base64') ) #esto para el trial
                x = self.betaXpires()
                return x
            else:
                
                expire = self.installDate() #install data esta dando error porque creo que no guarda la fecha del trial
                self.params.guisave('datecode', expire ) 
                self.params.guisave('release', self.release ) 
                self.saveToken()
                return False,"Trial start"
                
            #return str(expire).decode('base64')
            '''

    def saveKeyUser(self, key, user):

        self.params.save_setting('user', base64.b64encode(str(user)))
        self.params.save_setting('key', base64.b64encode(str(key)))

    def getKeyUser(self):

        user = self.params.setting_restore("user")
        key = self.params.setting_restore("key")

        return base64.b64decode(str(user)), base64.b64decode(str(key))

    def installDate(self):

        s = str(self.secondsSinceEpoch)
        o = str(base64.b64encode(bytes(s, 'utf-8')))

        return o

    def expireTrial(self, expire):

        # print(expire)
        month = float(expire) + 2588400
        err = self.secondsSinceEpoch - month

        d1 = time.strftime('%Y-%m-%d', time.localtime(self.secondsSinceEpoch))
        d2 = time.strftime('%Y-%m-%d', time.localtime(month))

        d1 = datetime.strptime(d1, "%Y-%m-%d")
        d2 = datetime.strptime(d2, "%Y-%m-%d")

        dias = abs((d2 - d1).days)

        if err > 0:
            # ha caducado
            note = "Trial expired"
            # self.params.guisave('token', str( self.doToken() ).encode('base64') )
            # print(note)
            return (True, note)

        else:

            note = "Trial " + str(dias) + " days left"
            # print(note)

            return (False, note)

    def createKeyl(self, email):

        o = ""
        for x in email:
            o = o + str(ord(x))

        # md5 = hashlib.md5(o).hexdigest()
        md5 = hashlib.md5(o.encode('utf-8')).hexdigest()

        i = 0
        key = ""
        for x in md5:
            if i <= 6:
                key = key + str(x)
                i = i + 1
            else:
                key = key + "-"
                i = 0

        key = key[:-1]

        return key

    def checkKey(self):
        '''
        email,key = self.getKeyUser()
        
        if key == self.createKeyl(email):
            n = "welcome "+email
            #print(n)
            return False, n
        else:
            n = "Key or mail incorrect"
            #print(n)
            return True, n
        '''
        return True, "Ok"


"""   
if __name__ == "__main__":
    
    LicenseClass()
"""
