 #-*- coding: utf-8 -*-


from openerp import _, api, fields, models

from ftplib import FTP

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
        conexion.retrlines("LIST")"""
        #<<----->>
        fich = open("Prueba_serverFTP.txt","wb")
        conexion.retrbinary("RETR Prueba_serverFTP.txt", fich.write)
        conexion.retrlines("LIST")



        return conexion


