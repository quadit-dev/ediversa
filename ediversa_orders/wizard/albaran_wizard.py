# -*- coding: utf-8 -*-


from openerp import _, api, fields, models

from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import SUPERUSER_ID
from openerp.exceptions import UserError

from datetime import datetime
import logging
_logger = logging.getLogger(__name__)   

import base64
# TRABAJAR CON LOS EXCEL
import xlsxwriter
import time

import tempfile

# SOLUCIONA CUALQUIER ERROR DE ENCODING (CARACTERES ESPECIALES)
import sys
reload(sys)
sys.setdefaultencoding('utf8')

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    id_bultos = fields.Selection([('1','1'),
                                  ('2','2')], 'Tipo', default="1")

class StockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'
    
    id_bultos = fields.Selection([('1','1'),
                                  ('2','2')], 'Tipo', default="1")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

class product_exi(models.Model):
    _inherit = ['sale.order']

class res_partner(models.Model):
    _inherit = 'res.partner'

    code_nadby = fields.Char('Codigo EDI Facturacion')
    code_naddp = fields.Char('Codigo EDI Direccion Entrega')

class export_albaran_txt(models.Model):
    _name = 'export.albaran.txt'
    _description = 'Exportar Albaran'

    @api.model
    def default_get(self,values):
        pack_op_obj = self.pool['stock.pack.operation']
        data_obj = self.pool['ir.model.data']
        validate = True

        res = super(export_albaran_txt,self).default_get(values)
        active_id = self._context.get('active_ids')
        picking_id = self.env['stock.picking'].browse(active_id)
        cont_cntres = 0
        for picking in picking_id:
            validate = True
            for move in picking.pack_operation_product_ids:
                cont_cntres = cont_cntres+1
                if not move.id_bultos:
                    validate = False
            if not validate:
                raise UserError(_('Agregar numero de bultos en cada producto'))

            code_ddp = picking.partner_id.codigo_provedor
            code_dby = picking.sale_id.cod_edi_cli
            for child in picking.partner_id:
                # if child.code_naddp:
                #     code_ddp = child.code_naddp
                # if child.code_nadby:
                #     code_dby = picking.sale_id.cod_edi_cli
                res.update({
                    'bgm_num_doc':picking.name,
                    'naddp_cod_entrega': code_ddp,
                    'nadby_cod_cliente': code_dby,
                    'dtm_entrega':picking.min_date,
                    'rff_referencia':picking.order_reference,
                    'rff_fecha':picking.sale_id.date_order,
                    'nadms_cod_emisor_mens':picking.company_id.partner_id.codigo_provedor,  # noqa
                    'nadmr_cod_emisor_mens':picking.partner_id.codigo_provedor,
                    'nadsu_cod_prove':picking.company_id.partner_id.codigo_provedor,  # noqa
                    'pac_num_embalajes':picking.number_of_packages,
                    'cntres_lines':cont_cntres
                    })
        return res

    datas_fname = fields.Char('File Name', size=256)
    bgm_num_doc = fields.Char('Numero de aviso de expedicion', size=256)
    bgm_tip_doc = fields.Selection([
        ('351', 'Aviso de Expedición'),
        ('YA5', 'Aviso de expedición de Cross Docking')],
        "Tipo de documento", required=True, default="351")
    bgm_fun_men = fields.Selection([
        ('9', 'Original'),
        ('5', 'Reemplazo'),
        ('7', 'Duplicado'),
        ('1', 'Cancelacion')],
        "Funcion del Mensaje", required=True, default="9")
    #dtm_entrega = fields.Char('Fecha entrega')
    dtm_creacion = fields.Datetime ('Fecha creacion', readonly = False,
        select = True, default = lambda self: fields.datetime.now ())
    ali_info = fields.Selection([
        ('X6', 'Si especificar la matrícula'),
        ('X7', 'No se va a especificar la matrícula'),
        ('164', 'Última entrega del pedido'),
        ('165', 'Quedan entregas parciales del pedido')],
        'Información Adicional',default="X6")
    rff_cali = fields.Selection([
        ('DQ', 'Numero de albaran en papel'),
        ('ON', 'Numero de pedido'),
        ('AAN', 'Numero de planificacion de entregas')],
        'Referencias', required=True, default="ON")
    rff_referencia = fields.Char('Referencia del documento')
    rff_fecha = fields.Char('Fecha de referecia')
    nadms_cod_emisor_mens = fields.Char('codigo EDI emisor')
    nadmr_cod_emisor_mens = fields.Char('codigo EDI receptor')
    nadsu_cod_prove = fields.Char('codigo EDI Proveedor')
    nadby_cod_cliente = fields.Char('codigo EDI Cliente')
    naddp_cod_entrega = fields.Char('codigo EDI punto de entrega')
    cps_empacado = fields.Selection([
        ('1', 'Nivel de envio'),
        ('2', 'segundo nivel'),
        ('3', 'tercer nivel')],
        'secuencia de empacado')
    cps_predecesor = fields.Selection([
        ('2', '1'),
        ('3', '2')],
        'Predecesor')
    pac_num_embalajes = fields.Char('Numero de bultos', readonly=True)
    pac_tipo_unidad = fields.Selection([
        ('CT', 'Caja de cartón'),
        ('BX', 'Caja tapada'),
        ('CHB', 'CHEP Jaula'),
        ('CS', 'Caja rígida'),
        ('PK', 'Paquete / Embalaje'),
        ('SL', 'Placa de plástico (hoja de embalaje)'),
        ('RO', 'rollo'),
        ('SW ', 'Retractilado'),
        ('09', 'Palet retornable'),
        ('08', 'Palet no retornablea'),
        ('200', 'Palet ISO 0 – 1/2 (80 x 60 cm)'),
        ('201', 'Palet ISO 1 (80 x 120 cm)'),
        ('202', 'Palet ISO 2 (100 x 120 cm)'),
        ('203', 'Palet 1/4 EURO (60 x 40 cm)'),
        ('204', 'Palet 1/8 EURO (40 x 30 cm)'),
        ('210', 'Palet del mayorista'),
        ('211', 'Palet (80 x 100 cm)'),
        ('212', 'Palet (60 x 100 cm)')],
        'Tipo Embalaje', required=True, default="CT")

    pac_tipo_unidad_palet = fields.Selection([
        ('CT', 'Caja de cartón'),
        ('BX', 'Caja tapada'),
        ('CHB', 'CHEP Jaula'),
        ('CS', 'Caja rígida'),
        ('PK', 'Paquete / Embalaje'),
        ('SL', 'Placa de plástico (hoja de embalaje)'),
        ('RO', 'rollo'),
        ('SW ', 'Retractilado'),
        ('09', 'Palet retornable'),
        ('08', 'Palet no retornablea'),
        ('200', 'Palet ISO 0 – 1/2 (80 x 60 cm)'),
        ('201', 'Palet ISO 1 (80 x 120 cm)'),
        ('202', 'Palet ISO 2 (100 x 120 cm)'),
        ('203', 'Palet 1/4 EURO (60 x 40 cm)'),
        ('204', 'Palet 1/8 EURO (40 x 30 cm)'),
        ('210', 'Palet del mayorista'),
        ('211', 'Palet (80 x 100 cm)'),
        ('212', 'Palet (60 x 100 cm)')],
        'Tipo Embalaje Palet', required=True, default="201")
    pci_marcaje = fields.Char('SSCC', default='33E', readonly=True)
    pci_calificador = fields.Char('Calificador', default='BJ', readonly=True)
    pci_num_iden = fields.Char('Matricula')
    lin_cod_prod = fields.Char('Codigo Producto')
    lin_tipo_cod = fields.Selection([
        ('EN', 'EAN13'),
        ('UP', 'UPC')],
        'Tipo de codificacion', required=True, default="EN")
    pialin_cod_int_prove = fields.Char('Codigo Interno proveedor')
    imdlin_descripcion = fields.Char('Descripcion del articulo')
    imdlin_cali_cod = fields.Selection([
        ('F', 'Descripcion texto Libre'),
        ('C', 'Descripcion Codificada')],
        'Calificador de descripcion', required=True, default="F")

    qtylin_cali_cant = fields.Selection([
        ('12', 'Cantidad enviada (no incluye la mercancía sin cargo)'),
        ('21', 'Cantidad solicitada por el comprador (no incluye la mercancía sin cargo)'),  # noqa
        ('59', 'Unidades de consumo contenidas en esta unidad de embalaje'),
        ('192', 'Cantidad de mercancía sin cargo'),
        ('45E', 'Cantidad de unidades en agrupación superior')],
        'Calificador de cantidad', required=True, default="12")
    qtylin_cantidad = fields.Char('Cantidad')
    cntres_lines = fields.Char('Lineas de producto')
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
    def export_txt_file(self, picking_ids):
        document_txt = ""
        #split de fecha creacion
        split_creacion = self.dtm_creacion.split('-')
        split_creacion_dia = split_creacion[2].split(' ')
        date_creacion = split_creacion[0]+split_creacion[1]+split_creacion_dia[0]  # noqa

        #split fecha de entrega
        split_entrega = self.env['stock.picking'].browse(picking_ids).min_date.split('-')  # noqa
        split_entrega_dia = split_entrega[2].split(' ')
        date_entrega = split_entrega[0]+ split_entrega[1]+ split_entrega_dia[0]

        #split de referencia
        """La operacion del split es correcta
        solo que en la orden debe de efectuarse de manera correcta si no
        mostrara error"""
        split_referencia  = self.env['stock.picking'].browse(picking_ids).sale_id.date_order.split('-')  # noqa
        split_referencia_dia = split_referencia[2].split(' ')
        date_referencia = split_referencia[0]+ split_referencia[1]+ split_referencia_dia[0]  # noqa
        date = datetime.now().strftime('%d-%m-%Y')
        datas_fname = "Albaran "+str(date)+".txt"  # Nombre del Archivo
        sl = "\n"
        # =>Cabecera
        for picking in self.env['stock.picking'].browse(picking_ids):
            campo_bgm = "%s|%s|%s|%s" % (
                "BGM", picking.name, self.bgm_tip_doc, self.bgm_fun_men)
            campo_dtm = "%s|%s|%s" % (
                "DTM", date_creacion, date_entrega )
            campo_ali = "%s|%s" % (
                "ALI", self.ali_info)
            """if hasattr(picking,'picking.order_reference'):
                campo_rff = "%s|%s|%s|%s" % (
                "RFF", self.rff_cali, picking.order_reference, date_referencia)
            else:
                campo_rff = "%s|%s" % (
                "RFF", self.rff_cali)"""
            campo_rff = "%s|%s|%s|%s" % (
                "RFF", self.rff_cali, self.rff_referencia, date_referencia)

            campo_nadms = "%s|%s" % (
                "NADMS", picking.company_id.partner_id.codigo_provedor)
            campo_nadmr = "%s|%s" % (
                "NADMR", picking.partner_id.codigo_provedor)
            campo_nadsu = "%s|%s" % (
                "NADSU", picking.company_id.partner_id.codigo_provedor)
            campo_nadby = "%s|%s||%s" % (
                "NADBY", self.nadby_cod_cliente, picking.sale_id.cod_dep)
            campo_naddp = "%s|%s" % (
                "NADDP", self.naddp_cod_entrega)
        # =>Fin Cabecera

        # =>Cuerpo
        body = ""
        cabecera = ""
        final = ""
        cont_1 = 1
        cont_2 = 0
        cont_1_pac = 1
        cont_2_pac = 0
        contador_cntres = 0
        contador_bulto = 0

        for move in self.env['stock.picking'].browse(
                picking_ids).pack_operation_product_ids:
            if contador_bulto == 0:
                campo_cps = "%s|%s" % (
                    "CPS", str(cont_1))
                campo_pac = "%s|%s" % (
                    "PAC", str(cont_1_pac))
                cabecera += campo_cps +  sl + campo_pac + sl
                cont_1 = cont_1+1
                cont_2 = cont_2+1
                campo_cps = "%s|%s|%s" % (
                    "CPS", str(cont_1), "1")
                campo_pac = "%s|%s|%s" % (
                    "PAC", str(cont_1_pac),  self.pac_tipo_unidad_palet)
                cabecera += campo_cps +  sl + campo_pac
                cont_1 = cont_1+1
                cont_2 = cont_2+1
            campo_pci = "%s|%s|%s|" % (
                "PCI", self.pci_marcaje, self.pci_calificador)
            contador_cntres = contador_cntres+1
            campo_cps = False

            if move.id_bultos > contador_bulto:
                campo_cps = "%s|%s|%s" % (
                    "CPS", str(cont_1), str(cont_2))
                campo_pac = "%s|%s|%s|%s" % (
                    "PAC", "1", self.pac_tipo_unidad, "52")
                campo_pci = "%s|%s|%s|" % (
                    "PCI", self.pci_marcaje, self.pci_calificador)
                cont_1 = cont_1+1
                cont_2 = cont_2+1
                contador_bulto= move.id_bultos

            campo_lin = "%s|%s|%s" % (
                "LIN", move.product_id.barcode, self.lin_tipo_cod)
            campo_pialin = "%s|%s|%s" % (
                "PIALIN" ," ", move.product_id.barcode)
            campo_imdlin = "%s|%s|%s" % (
                "IMDLIN", self.imdlin_cali_cod, move.product_id.name)
            cont_1_pac = cont_1_pac+1
            cont_2_pac = cont_2_pac+1
            campo_qtylin = "%s|%s|%s" % (
                "QTYLIN", self.qtylin_cali_cant, int(move.qty_done))
            if contador_bulto == 1:
                body += campo_pci + sl + campo_lin + sl + \
                    campo_pialin + sl + \
                    campo_imdlin + sl + campo_qtylin + sl
            else:
                if campo_cps:
                    body += campo_cps + sl + campo_pac + sl + campo_pci + \
                        sl + campo_lin + sl + campo_pialin + sl + \
                        campo_imdlin + sl + campo_qtylin + sl
                else:
                    body += campo_lin + sl + campo_pialin + sl + \
                        campo_imdlin + sl + campo_qtylin + sl
        
        campo_cntres = "%s|%s" % (
                    "CNTRES", str(contador_cntres))

        ##Moficando como llena la opcion ALI en el documento TXT
        if self.ali_info:
            document_txt = document_txt+"desadv_d_96a_un_ean005" + sl + \
                campo_bgm + sl + campo_dtm + sl + campo_ali + sl + \
                campo_rff + sl + campo_nadms + sl + campo_nadmr + sl + \
                campo_nadsu + sl + campo_nadby + sl + campo_naddp + sl + \
                cabecera  + sl + body + campo_cntres+ sl
        else:
            document_txt = document_txt+"desadv_d_96a_un_ean005" + sl + \
            campo_bgm + sl + campo_dtm + sl + campo_rff + sl + campo_nadms + \
            sl + campo_nadmr + sl + campo_nadsu + sl + campo_nadby + sl + \
            campo_naddp + sl + cabecera  + sl + body + campo_cntres+ sl


        # =>Fin cuerpo
        # time.sleep(10)
        #creamos el archivo txt
        file_name = 'desdav.txt'
        #abrimos el archivo txt especificando en
        #que ruta de la maquina se guardara
        with open('/tmp/'+file_name, 'w+') as f:
            #le asiganamos que informacion guardara
            f.write(document_txt)
        f.close()
        with open('/tmp/'+file_name, 'r+') as r:
            self.write({
                        'cadena_decoding': document_txt,
                        'datas_fname': datas_fname,
                        'file': base64.b64encode(r.read()),
                        'download_file': True})
        r.close()
        m = '/tmp/'+file_name
        ftp_obj = self.env['ediversa.ftp']
        ftp_ids = ftp_obj.search([])
        conn = ftp_ids.subir_archivo(f,m,datas_fname,picking.name,"ALB")
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'export.albaran.txt',
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
            return result
