     #-*- coding: utf-8 -*-


from openerp import _, api, fields, models
import tempfile
from ftplib import FTP
from io import StringIO

class ediversaFTP(models.Model):
    _name = 'ediversa.ftp'
    _description = 'ediversa FTP'

    name_ftp = fields.Char('Nombre del FTP',required=True)
    ruta_ftp = fields.Char('Ruta del FTP',required=True)
    carpeta = fields.Char('Carpta FTP', required=True)
    usuario_ftp = fields.Char('Usuario FTP', required=True)
    contrasenia_ftp = fields.Char('Contraseña FTP',required=True)


    @api.multi
    def test(self):
        print("PROBANDO METODOO -------------------------->>>>>>>>>>",
            self.name_ftp)
        server = self.ruta_ftp
        user = self.usuario_ftp
        passw = self.contrasenia_ftp
        try:
            conexion = FTP(server)
            conexion.login(user,passw)
            print "[+] Conexion establecida correctamente"
        except Exception,e:
            print "[-] No se pudo establecerla conexion al servidor" + str(e)

        #Crear y subir un archivo por FTP
        """fichero = open("Prueba_serverFTP.txt","w")
        fichero.writelines("Esta es una prueba de la conexion a un servidor FTP")
        fichero.close()

        fich = open("Prueba_serverFTP.txt","rb")
        conexion.storbinary("STOR Prueba_serverFTP.txt", fich)
        conexion.retrlines("LIST")
        #<<----->>"""
        #fp = tempfile.TemporaryFile()
        r = StringIO()
        #fich = open("Prueba_serverFTP.txt","wb")
        #fich = BytesIO(FtpFile(conexion, "Prueba_serverFTP.txt").read(10240))
        conexion.retrbinary('RETR Prueba_serverFTP.txt', r.write)
        info = r.getvalue().decode()
        splits = info.split('|')

        tickers = [x for x in splits if 'N\r\n' in x]
        tickers = [x.strip('N\r\n') for x in tickers]
        print ("-------------------------",info.read())
        conexion.retrlines("LIST")


        return conexion


