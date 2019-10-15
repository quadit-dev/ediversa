# -*- coding: utf-8 -*-
# CONTEXTO, LISTA Y RELACIONALES PARA TOMAR LOS VALORES DE LOS PRODUCTOS

from openerp import _, api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import base64
from datetime import datetime
# TRABAJAR CON LOS EXCEL
import xlsxwriter
import time

import tempfile

# SOLUCIONA CUALQUIER ERROR DE ENCODING (CARACTERES ESPECIALES)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


class export_factura_txt(models.Model):
    _name = 'export.factura.txt'
    _description = 'Exportar Factura'


    @api.model
    def default_get(self,values):
        res = super(export_factura_txt,self).default_get(values)
        active_id = self._context.get('active_ids')
        invoice_id = self.env['account.invoice'].browse(active_id)
        for invoice in invoice_id:
            #line_list = []
            for line in invoice.invoice_line_ids:
                print ("<<<<------------>>>",line.name)




        res.update({
                'inv_numdoc':invoice.number,
                'nadsco':invoice.user_id.codigo_provedor,
                'nadsco_name':invoice.user_id.name,
                'nadbco':invoice.partner_id.codigo_provedor,
                'nadbco_name':invoice.partner_id.name,
                'nadbco_direc':invoice.partner_id.street,
                'nadbco_prov':invoice.partner_id.state_id.name,
                'nadbco_cp':invoice.partner_id.zip,
                'nadbco_nif':invoice.partner_id.vat,
                'nadsu_cod_prove':invoice.user_id.codigo_provedor,
                'nadby_cod_cliente':invoice.partner_id.codigo_provedor,
                'nadbii':invoice.user_id.codigo_provedor,
                'nadbii_name':invoice.user_id.name,
                'nadms':invoice.partner_id.codigo_provedor,
                'nadmr':invoice.user_id.codigo_provedor,
                'nadpe':invoice.partner_id.codigo_provedor,
                'nadpe_name':invoice.partner_id.name,
                })

        return res

    datas_fname = fields.Char('File Name', size=256)
    download_file = fields.Boolean('Descargar Archivo')
    dtm_creacion = fields.Datetime ('Fecha creacion',
        readonly = False,
        select = True ,
        default = lambda self: fields.datetime.now ())
    inv_numdoc = fields.Char('Numero de factura', size=256)
    inv_tipo = fields.Selection([
        ('380', 'Factura comercial'),
        ('381', 'Nota de adono'),
        ('325', 'Factura pro-forma'),
        ('383', 'Nota de cargo'),
        ('384', 'Factura Corregida'),
        ('385', 'Factura recapitulada'),
        ('389', 'Autofactura')],
        'Tipo de documento')
    inv_funcion = fields.Selection([
        ('9', 'Original'),
        ('5', 'Sustitucion'),
        ('7', 'Duplicado'),
        ('43', 'Transmisión adcional'),
        ('31', 'Copia'),
        ('2', 'Adición (Complementaria)')],
        'Función del mensaje')



    pai = fields.Selection([
        ('20', 'Cheque'),
        ('42', 'A una cuenta bancaria'),
        ('60', 'Pagaré'),
        ('14E', 'Giro de banco'),
        ('10', 'En efectivo')],
        'Instruccion de pago')

    ali = fields.Selection([
        ('1A', 'Devolución de la mercancía'),
        ('2A', 'Bonificacion por volumen'),
        ('3A', 'Diferencias (precio,cantidad,etc.)'),
        ('78E', 'Devolucion de la mercancia'),
        ('79E', 'Discrepancias o ajustes'),
        ('80E', 'Bonificaciones anuales (Rappel)')],
        'Condiciones especiales')

    rff_cali = fields.Selection([
        ('DQ', 'Numero de albaran en papel'),
        ('ON', 'Numero de pedido'),
        ('AAN', 'Numero de planificacion de entregas')],
        'Referencias', required=True)
    rff_referencia = fields.Char('Referencia del documento')
    rff_fecha = fields.Datetime ('Fecha referencia',
        readonly = False, select = True,
        default = lambda self: fields.datetime.now ())
    nadsco = fields.Char('codigo EDI emisor')
    nadsco_name = fields.Char('nombre emisor')
    nadbco = fields.Char('codigo EDI receptor')
    nadbco_name = fields.Char('codigo EDI receptor')
    nadbco_direc = fields.Char('street')
    nadbco_prov = fields.Char('prov')
    nadbco_cp = fields.Char('cp')
    nadbco_nif = fields.Char('nif')
    nadsu_cod_prove = fields.Char('codigo EDI Proveedor')
    nadby_cod_cliente = fields.Char('codigo EDI Cliente')
    nadbii = fields.Char('codigo EDI emisor de factura')
    nadbii_name = fields.Char('codigo EDI emisor de factura nombre')
    nadiv = fields.Many2one('res.partner',string = 'Receptor de factura')
    naddp = fields.Many2one('res.partner',string = 'Receptor de mercancia')
    nadms = fields.Char('Codigo EDI del emisor del mensaje')
    nadpe = fields.Char('receptor del pago')
    nadpe_name = fields.Char('receptor del pago nombre')

    cux_coin = fields.Selection([
        ('EUR', 'Euro'),
        ('USD', 'Dolar')],
        'Codigo de moneda', required=True)
    cux_cali = fields.Selection([
        ('4', 'Divisa de la factura'),
        ('10', 'Divisa del precio'),
        ('11', 'Divisa del pago')],
        'Calificador de la divisa', required=True)

    pat_cali = fields.Selection([
        ('1', 'Básico'),
        ('21', 'Varios vencimientos'),
        ('35', 'Pago único')],
        'Condiciones de pago')
    pat_ven = fields.Datetime ('Fecha de vencimiento',
        readonly = False, select = True,
        default = lambda self: fields.datetime.now ())
    pat_import = fields.Float('Importe del vencimiento')
    pat_efect = fields.Datetime ('Fecha de efectiva',
        readonly = False, select = True,
        default = lambda self: fields.datetime.now ())
    pat_referencia = fields.Selection([
        ('5', 'Después de la fecha factura'),
        ('72', 'Fecha de pago'),
        ('29', 'Depués de la fecha de entrega'),
        ('68', 'Fecha de valor')],
        'Referencia de tiempo de pago')
    pat_periodo = fields.Selection([
        ('D', 'Días'),
        ('M', 'Meses')],
        'Tipo de periodo')
    pat_numero = fields.Integer('Numero de días o meses')
    pat_entrega = fields.Datetime ('Fecha de entrega',
        readonly = False,
        select = True,
        default = lambda self: fields.datetime.now ())


    moares_neto = fields.Integer('Importe neto de la factura')
    moares_bruto = fields.Integer('Importe bruto')
    moares_base = fields.Integer('Base imponible')
    moares_total = fields.Integer('Importe total de la factura')
    moares_impuestos = fields.Integer('Total de impuestos')
    moares_descuentos = fields.Integer('Total de descuentos globales')
    moares_cargos = fields.Integer('Total de cargos globales')
    moares_debido = fields.Integer('Importe total a pagar')
    lin_tipo_cod = fields.Selection([
            ('EN', 'EAN13'),
            ('UP', 'UPC'),
            ('SRV','Número único de acuerdo con la estructura'),
            ('IB','Número normalizado de publicación')],
            'Tipo de codificacion', required=True, default="EN")
    imdlin_cali_cod = fields.Selection([
        ('M', 'Mercancía'),
        ('C', 'Material consignado'),
        ('38','EStilo, Para libros'),
        ('79','Familia,Para peliculas'),
        ('86','Estilo, Para discos'),
        ('98','Talla'),
        ('UP5','Tamaño u horma del artículo'),
        ('U03','Nombre del dibujo del articulo'),
        ('DSC','Mercancia DSC')],
        'Calificador de descripcion', required=True, default="M")
    qtylin_cal = fields.Selection([
        ('46', 'Cantidad entregada'),
        ('47', 'Cantidad facturada'),
        ('61', 'Cantida de devolución'),
        ('15E','Cantidad de mercancia'),
        ('12','Cantidad enviada por el proovedor'),
        ('59','Número de unidades de consumo')],
        'Calificador de cantidad', required=True, default="47")
    qtylin_uni = fields.Selection([
        ('KGM', 'Kilogramos'),
        ('PCE', 'Unidades'),
        ('LTR', 'Litros'),
        ('UN','Unidad de consumo'),
        ('NAR','Numero de artículo'),
        ('EA','Cada'),
        ('MTQ','Metro cúbico'),
        ('TNE','Tonelada'),
        ('MTR','Metro')],
        'Especificador de la unidad de medida', required=True, default="PCE")
    taxres_tipo = fields.Selection([
        ('VAT', 'IVA'),
        ('IGI', 'IGIC'),
        ('EXT', 'Exento de impuesto'),
        ('ACT', 'Impuesto de alcoholes'),
        ('RE', 'Recargo de equivalencia'),
        ('ENV', 'Punto verde')],
        'Calificador de tipo de impuesto')
    taxres_porcentaje = fields.Integer('Porcentaje del impuesto aplicar')
    taxres_importe = fields.Integer('Suma total de los importes del impuesto')
    taxres_base = fields.Integer('Importe monetario de la base imponible')
    taxres_total = fields.Integer('Importe del impuesto')
    taxres_dis = fields.Integer(
        'Disposición nacional que da lugar a la exención del IVA')
    taxres_categoria = fields.Selection([
        ('E', 'Exento de impuestos'),
        ('ES1', 'Se aplica el régimen especial del criterio de caja')],
        'Categoría del impuesto')


    file = fields.Binary('Layout')
    download_file = fields.Boolean('Descargar Archivo')
    cadena_decoding = fields.Text('Binario sin encoding')
    type = fields.Selection([('txt', 'TXT')], 'Tipo Exportacion',
                            required=False, )

    _defaults = {
        'download_file': False,
        'type': 'txt',
    }

    @api.multi
    def export_txt_file(self,picking_ids):
        print("_________________________-----",picking_ids)
        document_txt = ""
        #split de fecha creacion
        split_creacion = self.dtm_creacion.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_creacion = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]  # noqa

        #split de fecha referencia
        split_creacion = self.rff_fecha.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_referencia = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]  # noqa

        #split de fecha pat_ve,
        split_creacion = self.pat_ven.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_pat_ven = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]  # noqa

        #split de fecha pat_efec,
        split_creacion = self.pat_efect.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_pat_ref = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]  # noqa

        #split de fecha pat_ent,
        split_creacion = self.pat_entrega.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_pat_ent = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]  # noqa

        sl = "\n"

        document_txt = document_txt+"invoic_d_93a_un_ean007"
        # =>Cabecera
        campo_inv = "%s|%s|%s|%s" % (
                "INV", self.inv_numdoc, self.inv_tipo, self.inv_funcion)
        document_txt = document_txt+ sl + campo_inv
        campo_dtm = "%s|%s" % (
                "DTM", date_creacion)
        document_txt = document_txt+ sl + campo_dtm
        if self.pai:
            campo_pai = "%s|%s" % (
                "PAI", self.pai)
            document_txt = document_txt+ sl + campo_pai

        if self.ali:
            campo_ali = "%s|%s" % (
                "ALI", self.ali)
            document_txt = document_txt+ sl + campo_ali

        campo_rff = "%s|%s|%s|%s" % (
                "RFF", self.rff_cali,self.rff_referencia,date_referencia)

        document_txt = document_txt+ sl + campo_rff

        campo_nadsco ="%s|%s|%s" % (
                "NADSCO",self.nadsco,self.nadsco_name)

        document_txt = document_txt+ sl + campo_nadsco

        campo_nadbco ="%s|%s|%s|%s|%s|%s|%s" % (
                "NADBCO",self.nadbco,self.nadbco_name,self.nadbco_direc,
                self.nadbco_prov, self.nadbco_cp, self.nadbco_nif)

        document_txt = document_txt+ sl + campo_nadbco

        campo_nadsu="%s|%s|%s" % (
                "NADSU",self.nadsu_cod_prove,self.nadsco_name)

        document_txt = document_txt+ sl + campo_nadsu

        campo_nadby="%s|%s|%s" % (
                "NADBY",self.nadby_cod_cliente,self.nadbco_name)

        document_txt = document_txt+ sl + campo_nadby

        campo_nadii="%s|%s|%s" % (
                "NADII",self.nadbii, self.nadbii_name)

        document_txt = document_txt+ sl + campo_nadii

        campo_nadiv="%s|%s|%s||||%s" % (
                "NADIV",self.nadiv.codigo_provedor, self.nadiv.name,
                self.nadiv.vat)

        document_txt = document_txt+ sl + campo_nadiv

        campo_nadms="%s|%s" % (
                "NADMS",self.nadms)

        document_txt = document_txt+ sl + campo_nadms

        campo_nadmr="%s|%s|%s|||||%s" % (
                "NADMR",self.nadiv.codigo_provedor, self.nadiv.name,
                self.nadiv.vat)

        document_txt = document_txt+ sl + campo_nadmr

        campo_naddp="%s|%s|%s|%s|%s|%s||%s" % (
                "NADDP",self.naddp.codigo_provedor, self.naddp.name,
                self.naddp.street,self.naddp.state_id.name, self.naddp.zip,
                self.naddp.vat)

        document_txt = document_txt+ sl + campo_naddp

        campo_nadpr  ="%s|%s|%s||||%s" % (
                "NADPR",self.nadiv.codigo_provedor, self.nadiv.name,
                self.nadiv.vat)

        document_txt = document_txt+ sl + campo_nadpr

        campo_nadpe  ="%s|%s|%s" % (
                "NADPE",self.nadpe, self.nadpe_name)

        document_txt = document_txt+ sl + campo_nadpe

        campo_cux = "%s|%s|%s" % (
                "CUX", self.cux_coin,self.cux_cali)

        document_txt = document_txt+ sl + campo_cux


        if self.pat_cali:
            campo_pat = "%s|%s|%s|%s|%s|%s|%s|%s|%s" % (
                "PAT", self.pat_cali,date_pat_ven,
                self.pat_import,date_pat_ref,
                self.pat_referencia,
                self.pat_periodo,self.pat_numero,date_pat_ent)
            document_txt = document_txt+ sl + campo_pat

        # =>Fin Cabecera

        # => Cuepo

        for move in self.env['account.invoice'].browse(
            picking_ids).invoice_line_ids:
            campo_lin = "%s|%s|%s|%s" % (
                "LIN", move.product_id.barcode,self.lin_tipo_cod,"1")
            document_txt = document_txt+ sl + campo_lin
            campo_pialin = "%s|%s" % (
                "PIALIN" , move.product_id.barcode)
            document_txt = document_txt+ sl + campo_pialin
            campo_imdlin = "%s|%s|%s|%s" % (
                "IMDLIN",  move.product_id.name,self.imdlin_cali_cod,"F")
            document_txt = document_txt+ sl + campo_imdlin
            campo_qtylin = "%s|%s|%s|%s" % (
                "QTYLIN",self.qtylin_cal,move.quantity,
                self.qtylin_uni)
            document_txt = document_txt+ sl + campo_qtylin


        # =>Resumen

        campo_cntres = "%s|%s" % (
                "CNTRES", "2")


        document_txt = document_txt+ sl + campo_cntres

        # =>Fin Resumen

        #creamos el archivo txt
        file_name = 'desdav.txt'
        date = datetime.now().strftime('%d-%m-%Y')
        datas_fname = "Factura "+str(date)+".txt"  # Nombre del Archivo


        #abrimos el archivo txt especificando en que ruta de la maquina
        # se guardara

        with open('/tmp/'+file_name, 'w+') as f:
            #le asiganamos que informacion guardara
            f.write(document_txt)
        f.close()
        with open('/tmp/'+file_name, 'r+') as r:
            print "rrrrrrrrrrr", r
            self.write({
                        'cadena_decoding': document_txt,
                        'datas_fname': datas_fname,
                        'file': base64.b64encode(r.read()),
                        'download_file': True})
            print "f.read()", r.read()
        r.close()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.factura.txt',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }



    @api.multi
    def process_export(self,):
        if self.type == 'txt':
            active_ids = self._context.get('active_ids', False)
            result = self.export_txt_file(active_ids)
            print("ahahahahaha____------------->>>>>>>",result)
            return result




