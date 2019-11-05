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
        fichero = open("Prueba_serverFTP2.txt","w")
        fichero.writelines("Esta es una prueba de la conexion a un servidor FTP")
        fichero.close()

        fichero = open("Prueba_serverFTP2.txt","rb")
        conexion.storbinary("STOR Prueba_serverFTP2.txt", fichero)
        conexion.retrlines("LIST")
        #<<----->>
        #fp = tempfile.TemporaryFile()
        file = open('Prueba_serverFTP3.txt', 'wb')
        conexion.retrbinary('RETR %s' % 'Prueba_serverFTP2.txt', file.write)
        file.close()
        file = open('Prueba_serverFTP3.txt', 'r')
        print(file.read())
        file.close

        return conexion

""" Tarea para mañana:
Separar los metodos conexion, subir archivo y descargar
por el momento solo contare 3 metodos
primero modificar el modulo de orders el cual crea una orden
por lo tanto debere crear un metodo que descargue el archivo
y sea capaz de cargarlo desde el widzard y no por el adjunto."""


