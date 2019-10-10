# -*- coding: utf-8 -*-


from openerp import _, api, fields, models
from openerp.exceptions import Warning
import logging
from pprint import pprint
_logger = logging.getLogger(__name__)




class supplier(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner']

    codigo_provedor = fields.Char('Código EDI')
    # codigo_dir_fact = fields.Char('Código Facturacion')
    # codigo_dir_entrega = fields.Char('Código Dirección entrega')

class product_exi(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    product_exist = fields.Text(string='Default Terms and Conditions', translate=True)


class ediversaOrder(models.Model):
    _name = 'ediversa.order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'ediversa Orders'

    _rec_name = 'subject'

    subject = fields.Char('Subject', size=128)
    email = fields.Char('Email', size=128)
    attach = fields.Text('Attachment')

    @api.multi
    def confirm(self):
        res = []
        vals = {}
        ftx = []
        lin = []
        pialin = []
        imdlin = []
        nadiv = []
        naddp = []
        nadsu = []
        nadms = []
        qtylin = []
        moalin = []
        alclin = []
        prilin = []
        tax = []

        res = self.env['ir.attachment'].search_read(domain=[
            ('res_model', '=', 'ediversa.order'),
            ('res_id', '=', self.id),
        ], fields=['datas_fname', 'index_content'], limit=1)
        self.attach = res[0]['index_content']
        if self.attach:
            array = self.attach.split('\n')
            if array:
                for line in array:
                    _logger.warn('===>line %r' % line)
                    item = line.split('|')
                    _logger.warn('===>item %r' % item)

                    if item[0] == 'ORD':
                        if not len(item) == 3:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'ord_num_doc': item[1],
                            'ord_tipo_doc': item[2],
                            'ord_fun_mensaje': item[3],
                        })

                        if vals["ord_tipo_doc"] == '220':
                            _logger.info("pedido normal")
                        else:
                            False
                        if vals["ord_tipo_doc"] == '22E':
                            _logger.info("propuesta de pedido")
                        else:
                            False
                        if vals["ord_tipo_doc"] == '221':
                            _logger.info("pedido abierto")
                        else:
                            False
                        if vals["ord_tipo_doc"] == '224':
                            _logger.info("pedido urgente ")
                        else:
                            False

                        if vals["ord_tipo_doc"] == '226':
                            _logger.info("pedido parcial que cancela un pedido abierto ")
                        else:
                            False

                        if vals["ord_tipo_doc"] == '227':
                            _logger.info("pedido consignacion ")
                        else:
                            False

                        if vals["ord_tipo_doc"] == 'YB1':
                            _logger.info("pedido cross dock")
                        else:
                            False

                        if vals["ord_tipo_doc"] == 'YB1':
                            _logger.info("pedido cross dock")
                        else:
                            False

                        if vals["ord_fun_mensaje"] == '9':
                            _logger.info("original")
                        else:
                            False

                        if vals["ord_fun_mensaje"] == 's':
                            _logger.info("sustitucion")
                        else:
                            False

                        if vals["ord_fun_mensaje"] == '16':
                            _logger.info("propuesta")
                        else:
                            False

                    if item[0] == 'DTM':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'dtm_fecha_emi_ped': item[1],
                            'dtm_fecha_entre': item[2] if len(item) >= 3 else False,
                            'dtm_fecha_limite_entre': item[3] if len(item) >= 4 else False,
                            'dtm_ultima_fecha_entre': item[4] if len(item) >= 5 else False,
                            'dtm_primera_fecha_entre': item[5] if len(item) >= 6 else False,
                            'dtm_fecha_liquidacion': item[6] if len(item) >= 7 else False,
                            'dtm_fecha_recogida_carga': item[7] if len(item) >= 8 else False,
                            'dtm_fecha_entre_programada': item[8] if len(item) >= 9 else False,
                        })

                    if item[0] == 'PAI':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'pai_forma_pago': item[1],
                        })
                        if vals["pai_forma_pago"] == '42':
                            _logger.info("cuenta bancaria")
                        else:
                            False
                        if vals["pai_forma_pago"] == '14E':
                            _logger.info("giro bancario")
                        else:
                            False
                        if vals["pai_forma_pago"] == '10':
                            _logger.info("efectivo")
                        else:
                            False
                        if vals["pai_forma_pago"] == '20':
                            _logger.info("cheque")
                        else:
                            False
                        if vals["pai_forma_pago"] == '60':
                            _logger.info("pagare")
                        else:
                            False

                    if item[0] == 'ALI':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'ali_info_pedido': item[1],
                        })

                        if vals["ali_info_pedido"] == '81E':
                            _logger.info("facturar pero no rebastecer")
                        else:
                            False
                        if vals["ali_info_pedido"] == '82E':
                            _logger.info("enviar pero no facturar")
                        else:
                            False
                        if vals["ali_info_pedido"] == '83E':
                            _logger.info("entregar  el pedido entero")
                        else:
                            False
                        if vals["ali_info_pedido"] == '61E':
                            _logger.info("pedidos agrupados de palets de cross-Dock")
                        else:
                            False
                        if vals["ali_info_pedido"] == 'x1':
                            _logger.info("si envio parcial-cancelacion del resto")
                        else:
                            False
                        if vals["ali_info_pedido"] == 'x2':
                            _logger.info("si envio parcial entrega del resto")
                        else:
                            False
                        if vals["ali_info_pedido"] == 'x41':
                            _logger.info("reserva realizada por el consumidor final")
                        else:
                            False
                        if vals["ali_info_pedido"] == 'x42':
                            _logger.info("mercancia de reaprovisionamiento a tienda")
                        else:
                            False
                        if vals["ali_info_pedido"] == 'x43':
                            _logger.info("stock de seguridad")
                        else:
                            False

                    if item[0] == 'FTX':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline = ({
                            'ftx_info_gral': item[1],
                            'ftx_info_codificada': item[2] if len(item) >= 3 else False,
                            'ftx_texto_libre': item[3] if len(item) >= 4 else False,
                        })
                        ftx.append(xline)
                        for f in ftx:
                            if f.has_key('fix_info_gral'):
                                # _logger.info("=>fix_info_gral",
                                #              f["fix_info_gral"])

                                if f["ftx_info_gral'"] == 'DEL':
                                    _logger.info("infromacion de entrega")
                                else:
                                    False
                                if f["ftx_info_gral'"] == 'PUR':
                                    _logger.info("infromacion de compra")
                                else:
                                    False
                                if f["ftx_info_gral'"] == 'INV':
                                    _logger.info("informacion de facturacion")
                                else:
                                    False
                                if f["ftx_info_gral'"] == 'ZZZ':
                                    _logger.info("definicion mutua")
                                else:
                                    False
                                if f["ftx_info_gral'"] == 'AAI':
                                    _logger.info("informacion general")
                                else:
                                    False
                                if f["ftx_info_gral'"] == 'SUR':
                                    _logger.info("nota del proveedor")
                                else:
                                    False
                                if f["ftx_info_gral'"] == 'AAB':
                                    _logger.info("condiciones de pago")
                                else:
                                    False

                                if f["ftx_info_codificada"] == '001':
                                    _logger.info("liquidacion por venta")
                                else:
                                    False
                                if f["ftx_info_codificada"] == '002':
                                    _logger.info("liquidacion manual")
                                else:
                                    False

                        vals.update({'ftx_row': ftx})
                        # _logger.warn('===>f %r' % f)
                        # _logger.warn('===>vals %r' % vals)

                    if item[0] == 'RFF':
                        vals.update({
                            'rff_temporada': item[1] if len(item) >= 2 else False,
                            'rff_num_propuesta': item[2] if len(item) >= 3 else False,
                            'rff_codigo_uneco': item[3] if len(item) >= 4 else False,
                            'rff_num_pedido': item[4] if len(item) >= 5 else False,
                            'rff_num_albaran': item[5] if len(item) >= 6 else False,
                        })
                    if item[0] == 'NADMS':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline=[{
                            'nadms_punto_oper_emisor_men': item[1],
                            'nadms_nombre': item[2] if len(item) >= 3 else False,
                            'nadms_direccion': item[3] if len(item) >= 4 else False,
                            'nadms_poblacion': item[4] if len(item) >= 5 else False,
                            'nadms_cp': item[5] if len(item) >= 6 else False,
                            'nadms_nif': item[6] if len(item) >= 7 else False,
                        }]
                        nadms.append(xline)
                        for f in nadms:
                            for p in f:
                                if p['nadms_punto_oper_emisor_men'] != '0':
                                    _logger.info("#######################codigo interno del cliente")
                                else:
                                    False
                        vals.update({'nadms_row':nadms})

                    if item[0] == 'NADMR':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'nadmr_punto_oper_receptor_men': item[1],
                        })
                    if item[0] == 'NADSU':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline=[{
                            'nadsu_punto_oper_proveedor': item[1],
                            'nadsu_cod_interno_proveedor': item[2] if len(item) >= 3 else False,
                            'nadsu_cod_interno_proveedor1': item[3] if len(item) >= 4 else False,
                        }]
                        nadsu.append(xline)
                        for f in nadsu:
                            for p in f:
                                if p["nadsu_punto_oper_proveedor"] != '0':
                                    _logger.info("#########################codigo interno del proveedor")
                                else:
                                    False
                        vals.update({'nadsu_row':nadsu})

                    if item[0] == 'NADBY':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'nadby_punto_oper_comprador': item[1],
                            'nadby_departamento': item[2] if len(item) >= 3 else False,
                            'nadby_num_reposicion': item[3] if len(item) >= 4 else False,
                            'nadby_cod_sucursal': item[4] if len(item) >= 5 else False,
                            'nadby_nombre': item[5] if len(item) >= 6 else False,
                            'nadby_direccion': item[6] if len(item) >= 7 else False,
                            'nadby_poblacion': item[7] if len(item) >= 8 else False,
                            'nadby_cp': item[8] if len(item) >= 9 else False,
                            'nadby_nif': item[9] if len(item) >= 10 else False,
                        })
                    if item[0] == 'NADDP':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline=[{
                            'naddp_punto_entrega': item[1],
                            'naddp_puerta_entrega_mercancia': item[2] if len(item) >= 3 else False,
                            'naddp_nombre': item[3] if len(item) >= 4 else False,
                            'naddp_direccion': item[4] if len(item) >= 5 else False,
                            'naddp_poblacion': item[5] if len(item) >= 6 else False,
                            'naddp_cp': item[6] if len(item) >= 7 else False,
                        }]
                        naddp.append(xline)
                        for f in naddp:
                            for p in f:
                                if p["naddp_punto_entrega"] != '0':
                                    _logger.info("############################ direccion de entrega")
                                else:
                                    False
                        vals.update({'naddp_row':naddp})

                    if item[0] == 'NADIV':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline = [{
                            'nadiv_punto_oper_fac': item[1],
                            'nadiv_codigo_uneco': item[2] if len(item) >= 3 else False,
                            'nadiv_nombre': item[3] if len(item) >= 4 else False,
                            'nadiv_direccion': item[4] if len(item) >= 5 else False,
                            'nadiv_poblacion': item[5] if len(item) >= 6 else False,
                            'nadiv_cp': item[6] if len(item) >= 7 else False,
                            'nadiv_nif': item[7] if len(item) >= 8 else False,
                        }]
                        nadiv.append(xline)
                        for f in nadiv:
                            for p in f:
                                if p["nadiv_punto_oper_fac"] != '0':
                                    _logger.info("############################ direccion de la factura")
                                else:
                                    False
                        vals.update({'nadiv_row':nadiv})



                    if item[0] == 'NADPR':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'nadpr_punto_oper_emisor_pago': item[1],
                        })

                    if item[0] == 'NADUD':
                        vals.update({
                            'nadud_punto_oper_cliente_final': item[1] if len(item) >= 2 else False,
                            'nadud_nombre': item[2] if len(item) >= 3 else False,
                            'nadud_direccion': item[3] if len(item) >= 4 else False,
                            'nadud_poblacion': item[4] if len(item) >= 5 else False,
                            'nadud_cp': item[5] if len(item) >= 6 else False,
                            'nadud_cheque': item[6] if len(item) >= 7 else False,
                            'nadud_reserva': item[7] if len(item) >= 8 else False,
                            'nadud_provincia': item[8] if len(item) >= 9 else False,
                        })

                    

                    if item[0] == 'TAX':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline=[{
                            'tax_tipo_impuesto': item[1],
                            'tax_porcentaje_impuesto': item[2] if len(item) >= 3 else False,
                            'tax_importe_impuesto': item[3] if len(item) >= 4 else False,
                        }]
                        tax.append(xline)
                        for f in tax:
                            print ("###################################f de tax",f)
                            for p in f:
                                print("#################################p de tax",p)
                            if p["tax_porcentaje_impuesto"] != '0':
                                _logger.info("porcentaje")
                            else:
                                False
                            if p.has_key('tax_tipo_impuesto'):
                                if p["tax_tipo_impuesto"] == 'VAT':
                                    _logger.info("iva")
                                else:
                                    False

                                if p["tax_tipo_impuesto"] == 'IGI':
                                    _logger.info("igic")
                                else:
                                    False
                        vals.update({'tax_row': tax})



                    if item[0] == 'CUX':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'cux_tipo_moneda': item[1],
                        })

                        if vals["cux_tipo_moneda"] == 'EUR':
                            _logger.info(" euro")
                        else:
                            False

                        if vals["cux_tipo_moneda"] == 'USD':
                            _logger.info("dolar")
                        else:
                            False


                    if item[0] == 'PAT':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'pat_cal_condicion_pago': item[1],
                            'pat_referencia_tiempo_pago': item[2] if len(item) >= 3 else False,
                            'pat_tipo_periodo': item[3] if len(item) >= 4 else False,
                            'pat_numero_dias': item[4] if len(item) >= 5 else False,
                            'pat_importe_pago': item[5] if len(item) >= 6 else False,
                        })

                        if vals["pat_cal_condicion_pago"] == '10E':
                            _logger.info("pago unico")
                        else:
                            False

                        if vals["pat_referencia_tiempo_pago"] == '5':
                            _logger.info("despues de fecha factura")
                        else:
                            False

                        if vals["pat_referencia_tiempo_pago"] == '29':
                            _logger.info(
                                "desde que la mercancia se entrega al destino final")
                        else:
                            False

                        if vals["pat_tipo_periodo"] == 'D':
                            _logger.info("dias")
                        else:
                            False

                    if item[0] == 'TDT':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'tdt_medio_tranporte_mercancia': item[1],
                        })

                        if vals["tdt_medio_tranporte_mercancia"] == '10':
                            _logger.info("matutino")
                        else:
                            False
                        if vals["tdt_medio_tranporte_mercancia"] == '20':
                            _logger.info("ferroviario")
                        else:
                            False
                        if vals["tdt_medio_tranporte_mercancia"] == '30':
                            _logger.info("por carretera")
                        else:
                            False
                        if vals["tdt_medio_tranporte_mercancia"] == '40':
                            _logger.info("transporte aereo")
                        else:
                            False

                    if item[0] == 'TOD':
                        vals.update({
                            'tod_condiciones_entrega': item[1] if len(item) >= 2 else False,
                            'tod_responsable_trasporte': item[2] if len(item) >= 3 else False,
                            'tod_lugar_entrega': item[3] if len(item) >= 4 else False,
                            'tod_punto_operacional_entrega': item[4] if len(item) >= 5 else False,
                            'tod_codigo_interno_lugar_entrega': item[5] if len(item) >= 6 else False,
                        })

                        if vals["tod_condiciones_entrega"] == 'CIF':
                            _logger.info("coste, seguro, flete en el destino")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'CIP':
                            _logger.info("flete, porte,  seguro hasta destino")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'CPT':
                            _logger.info("flete, porte, pagado hasta destino")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'DAF':
                            _logger.info("entrega en la frontera lugar indicado")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'EXW':
                            _logger.info("en la fabrica")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'FCA':
                            _logger.info("franco en el trasporte-punto indicado")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'RYF':
                            _logger.info("reponer y facturar")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == '01E':
                            _logger.info(
                                "contar con la parte receptora antes de la entrega")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == '02E':
                            _logger.info("enviar mercancia entrega urgente")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == '03E':
                            _logger.info("condiciones de entrega especiales")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == '04E':
                            _logger.info("efectivo a la entrega")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'CFR':
                            _logger.info("coste y flete")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'DDP':
                            _logger.info("entregado con aranceles pagados hasta destino")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'DDU':
                            _logger.info("entregado aranceles sin pagar")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'DEQ':
                            _logger.info(
                                "entregado en el muelle aranceles pagados, puerto indicado")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'DES':
                            _logger.info(
                                "entregado en el barco- puerto de destino indicado")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'FAS':
                            _logger.info("franco al lado del barco")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'FOA':
                            _logger.info("aereopurto- nombres dek aereopuerto de salida")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'FOB':
                            _logger.info("free on board nombre del puerto del embarque")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'FOR':
                            _logger.info(
                                "franco en el ferrocarril- punto de salida indicado")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'FNA':
                            _logger.info("facturar y no reponer")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'RNF':
                            _logger.info("reponer y no facturar")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'COM':
                            _logger.info("servir pedido completo")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'RD':
                            _logger.info("recogida por el emisor del pedido")
                        else:
                            False
                        if vals["tod_condiciones_entrega"] == 'EP':
                            _logger.info("metodo de pago. en este caso es cuando se especifica el siguiete campo(portes)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == 'PP':
                            _logger.info("transporte a cargo del proveedor(portes pagados)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == 'X1E':
                            _logger.info("transporte a cargo del proveedor(portes pagados)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == 'PU':
                            _logger.info("transporte a cargo del comprador(portes debidos)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == 'PD':
                            _logger.info("transporte a cargo del comprador(portes debidos)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == 'CC':
                            _logger.info("transporte a cargo del comprador(portes debidos)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == 'X2E':
                            _logger.info("transporte a cargo del comprador(portes debidos)")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == '4':
                            _logger.info("recogida por el cliente")
                        else:
                            False
                        if vals["tod_responsable_trasporte"] == '10E':
                            _logger.info("entregado por el proveedor)")
                        else:
                            False

                    if item[0] == 'ALC':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'alc_secuencia': item[1] if len(item) >= 2 else False,
                            'alc_tipo_desc': item[2],
                            'alc_porcentaje_desc': item[3] if len(item) >= 4 else False,
                            'alc_cal': item[4],
                            'alc_importe_desc': item[5] if len(item) >= 6 else False,
                        })

                        if vals["alc_tipo_desc"] == 'EAB':
                            _logger.info("descuento por pronto pago")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'TD':
                            _logger.info("descuento comercial")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'DI':
                            _logger.info("descuento")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'AA':
                            _logger.info("abono por publicidad")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'EAA':
                            _logger.info("abono por compra anticipada")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'FA':
                            _logger.info("abono por flete")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'FG':
                            _logger.info("costes financieros")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'GRB':
                            _logger.info("crecimiento del negocio")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'ADR':
                            _logger.info("otros servicios")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'DDA':
                            _logger.info("descuentos/abonos del distribuidor")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'PAE':
                            _logger.info("descuento promocional")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'ADN':
                            _logger.info(
                                "reparacion de  remplazo de embalaje/paquete retornable roto")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'PAD':
                            _logger.info("abono procional")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'PI':
                            _logger.info("descuento de recogida")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'VAB':
                            _logger.info("descuento por volumen")
                        else:
                            False
                        if vals["alc_tipo_desc"] == 'ADO':
                            _logger.info("logistica eficente")
                        else:
                            False
                        if vals["alc_cal"] == 'A':
                            _logger.info("descuento")
                        else:
                            False
                        if vals["alc_cal"] == 'C':
                            _logger.info("cargo")
                        else:
                            False

                    if item[0] == 'LIN':
                        product_ban = str(item[1])

                        xline = [{
                            'lin_cod_normalizado': item[1] if len(item) >= 2 else False,
                            'lin_tipo_cod': item[2] if len(item) >= 3 else False,
                            'lin_num_correctivo_linea_detalle': item[3] if len(item) >= 4 else False,
                        }]
                        lin.append(xline)
                        for f in lin:
                            for p in f:
                                if p.has_key('lin_tipo_cod'):
                                    if p["lin_tipo_cod"] == 'EN':
                                        _logger.info("EAN13")
                                    else:
                                        False
                                    if p["lin_tipo_cod"] == 'UP':
                                        _logger.info("upc")
                                    else:
                                        False
                        vals.update({'lin_row': lin})

                    if item[0] == 'PIALIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        xline = [{
                            'pialin_calificador': item[1],
                            'pialin_ref_articulo': item[2],
                        }]
                        pialin.append(xline)
                        for f in pialin:
                            for p in f:
                                _logger.info ("########################p",p)
                            _logger.info ("########################f",f)
                            if p["pialin_ref_articulo"] != '0':
                                _logger.info("codigo interno del articulo")
                            else:
                                False
                                _logger.info ("########################pialin_ref_articulo", f["pialin_ref_articulo"])
                            if p.has_key('pialin_calificador'):
                                if p["pialin_calificador"] == 'SA':
                                    _logger.info("codigo interno del articulopor el proveedor")
                                else:
                                    False
                                if p["pialin_calificador"] == 'IN':
                                    _logger.info("codigo interno del comprador")
                                else:
                                    False
                                if p["pialin_calificador"] == 'SN':
                                    _logger.info("numero de serie")
                                else:
                                    False
                                if p["pialin_calificador"] == 'ADU':
                                    _logger.info("codigo de la unidad del embalaje")
                                else:
                                    False
                                if p["pialin_calificador"] == 'MN':
                                    _logger.info("identificacion del modelo del fabricante")
                                else:
                                    False
                                if p["pialin_calificador"] == 'DW':
                                    _logger.info("identificacion interna del provedor del dibujo")
                                else:
                                    False
                                if p["pialin_calificador"] == 'PV':
                                    _logger.info("variable promocional")
                                else:
                                    False
                                if p["pialin_calificador"] == 'GB':
                                    _logger.info("go de grupo producto interno")
                                else:
                                    False
                                if p["pialin_calificador"] == 'AT':
                                    _logger.info("numero de busqueda para el precio")
                                else:
                                    False
                        vals.update({'pialin_row': pialin})

                    if item[0] == 'IMDLIN':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline = ({
                            'imdlin_calificador': item[1],
                            'imdlin_caracteristica': item[2] if len(item) >= 3 else False,
                            'imdlin_descripcion_codificada': item[3] if len(item) >= 4 else False,
                            'imdlin_descripcion _libre': item[4] if len(item) >= 5 else False,
                        })
                        imdlin.append(xline)
                        for f in imdlin:
                            if f.has_key('imdlin_calificador'):
                                # _logger.info("=>imdlin_calificador",
                                #              f["imdlin_calificador"])

                                if f["imdlin_calificador"] == 'F':
                                    _logger.info("desripcion con texto libre")
                                else:
                                    False
                                if f["imdlin_calificador"] == 'C':
                                    _logger.info("descripcion codificada")
                                else:
                                    False
                                if f["imdlin_calificador"] == 'E':
                                    _logger.info("descripcion corta")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'M':
                                    _logger.info("mercancia")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'DSC':
                                    _logger.info("mercancia")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'BRN':
                                    _logger.info(
                                        "marca utilizada por el suministrador")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'UPS':
                                    _logger.info(
                                        "tamaño u horma del articulo")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'UP5':
                                    _logger.info(
                                        "tamaño u horma del articulo")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'U03':
                                    _logger.info(
                                        "nombre del dibujo del articulo")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == '38':
                                    _logger.info("estilo para libros")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == '79':
                                    _logger.info("familia para peliculas")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == '86':
                                    _logger.info("estilo para libros")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'STE':
                                    _logger.info(
                                        "referencia interna del proveedor")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == '35':
                                    _logger.info("color")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == '98':
                                    _logger.info("talla")
                                else:
                                    False
                                if f["imdlin_caracteristica"] == 'MD':
                                    _logger.info(
                                        "descripcion del material")
                                else:
                                    False
                                if f["imdlin_descripcion_codificada"] == 'CU':
                                    _logger.info(
                                        "el articulo fcaturado es la unidad de consumo")
                                else:
                                    False
                                if f["imdlin_descripcion_codificada"] == 'DU':
                                    _logger.info(
                                        "el articulo factrado es la unidad de envio")
                                else:
                                    False
                        vals.update({'imdlin_row': imdlin})

                    if item[0] == 'MEALIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'mealin_dimension': item[1],
                            'mealin_codigo_significado_medida': item[2] if len(item) >= 3 else False,
                            'mealin_especificador_medida': item[3] if len(item) >= 4 else False,
                            'mealin_valor_medida': item[4],

                        })

                        if vals["mealin_dimension"] == 'AAA':
                            _logger.info("peso neto unitario")
                        else:
                            False
                        if vals["mealin_dimension"] == 'AAB':
                            _logger.info("peso bruto unitario")
                        else:
                            False
                        if vals["mealin_dimension"] == 'ULY':
                            _logger.info("numero de cajas por manto")
                        else:
                            False
                        if vals["mealin_dimension"] == 'LAY':
                            _logger.info("numero de  mantos por palet")
                        else:
                            False
                        if vals["mealin_codigo_significado_medida"] == '3':
                            _logger.info("aproximadamente")
                        else:
                            False
                        if vals["mealin_codigo_significado_medida"] == '4':
                            _logger.info("igual")
                        else:
                            False
                        if vals["mealin_especificador_medida"] == 'KGM':
                            _logger.info("kilogramos")
                        else:
                            False
                        if vals["mealin_especificador_medida"] == 'PCE':
                            _logger.info("unidades")
                        else:
                            False

                    if item[0] == 'QTYLIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        if item[1] == '21':
                            xline = [{
                                'qtylin_product': product_ban or '',
                                'qtylin_unidad_medida': item[1],
                                'qtylin_cantidad_expresada': item[2],
                                'qtylin_especificador_unidad': item[3] if len(item) >= 4 else False,
                            }]
                            qtylin.append(xline)
                       

                    vals.update({'qtylin_row': qtylin})
                    # print("#############################p",p)

                    if item[0] == 'DTMLIN':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'dtmlin_fecha_min_cad': item[1],
                            'dtmlin_entregar_antes_de': item[2] if len(item) >= 3 else False,
                        })

                    if item[0] == 'MOALIN':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline = ({
                            'moalin_importe_total_linea': item[1],
                        })
                        moalin.append(xline)
                        vals.update({'moalin_row': moalin})

                    if item[0] == 'FTXLIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'ftxlin_texto_libre': item[1],
                            'ftxlin_calificador': item[2],
                        })

                        if vals["ftxlin_calificador"] == 'AAK':
                            _logger.info("cantidad de medida de articulos")
                        else:
                            False
                        if vals["ftxlin_calificador"] == 'ZZZ':
                            _logger.info("definicion mutua")
                        else:
                            False

                    if item[0] == 'PRILIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        xline = ({
                            'prilin_calificador_tipo_precio': item[1],
                            'prilin_precio_unitario': item[2],
                            'prilin_especificador_precio': item[3] if len(item) >= 4 else False,
                            'prilin_calificador_unidad': item[4] if len(item) >= 5 else False,
                        })
                        prilin.append(xline)
                        for f in prilin:
                            if f.has_key('prilin_calificador_tipo_precio'):
                                # _logger.info(
                                #     "=>prilin_calificador_tipo_precio", f["prilin_calificador_tipo_precio"])

                                if f["prilin_calificador_tipo_precio"] == 'AAA':
                                    _logger.info(
                                        "precio neto unitario(con descuentos y cargos, sin impuestos)")
                                else:
                                    False
                                if f["prilin_calificador_tipo_precio"] == 'AAB':
                                    _logger.info(
                                        "precio bruto unitario(sin descuentos, cargos e impuestos)")
                                else:
                                    False
                                if f["prilin_calificador_tipo_precio"] == 'INF':
                                    _logger.info("precio a titulo informativo")
                                else:
                                    False
                                if f["prilin_especificador_precio"] == 'CU':
                                    _logger.info("por unidadd de consumo o de medida")
                                else:
                                    False
                                if f["prilin_especificador_precio"] == 'LBL':
                                    _logger.info("precio de etiqueta")
                                else:
                                    False
                                if f["prilin_calificador_unidad"] == 'KGM':
                                    _logger.info("kilogramos")
                                else:
                                    False
                                if f["prilin_calificador_unidad"] == 'PCE':
                                    _logger.info("unidades")
                                else:
                                    False
                                if f["prilin_calificador_unidad"] == 'LTR':
                                    _logger.info("litros")
                                else:
                                    False
                                if f["prilin_calificador_unidad"] == 'MTR':
                                    _logger.info("metros")
                                else:
                                    False
                        vals.update({'prilin_row': prilin})

                    if item[0] == 'PACLIN':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'paclin_num_bultos_palet': item[1] if len(item) >= 2 else False,
                            'paclin_tipo_embalaje': item[2],
                        })

                        if vals["paclin_tipo_embalaje"] == '08':
                            _logger.info("palet sin retorno")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '09':
                            _logger.info("palet retornable")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '200':
                            _logger.info("Palet  ISO 0 ‐ 1/2 EURO Palet ( 80 x 60 cm)")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '201':
                            _logger.info("Palet  ISO 1 ‐ 1/1 EURO Palet ( 80 x 120 cm)")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '202':
                            _logger.info("Palet  ISO 2 (100 x 120 cm) ")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '203':
                            _logger.info("Palet  1/4 EURO (60 x 40 cm)")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '204':
                            _logger.info("Palet  1/8 EURO (40 x 30 cm)")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'cs':
                            _logger.info("Caja.Un embalaje tipo caja ")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'PK':
                            _logger.info("Númer o de bultos")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'CT':
                            _logger.info("Caja de cartón")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'X1':
                            _logger.info("Palet genérico ")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'X2':
                            _logger.info("Palet /  caja")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'RCA':
                            _logger.info(" Jaula")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'DPE':
                            _logger.info("Emba laje de presentación ")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'SW':
                            _logger.info("Retrac ctilado")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == 'BX':
                            _logger.info("Caja ta pada ")
                        else:
                            False
                        if vals["paclin_tipo_embalaje"] == '999':
                            _logger.info("Palet  1/4")
                        else:
                            False

                    if item[0] == 'LOCLIN':
                        vals.update({
                            'loclin_codigo_punto_entrega': item[1] if len(item) >= 2 else False,
                            'loclin_cantidad_destinada': item[2] if len(item) >= 3 else False,
                            'loclin_cantidad_solicitada': item[3] if len(item) >= 4 else False,
                            'loclin_unidad_expresada_cantidad_destinada': item[4] if len(item) >= 5 else False,
                            'loclin_unidad_expresada_cantidad_solicitada': item[5] if len(item) >= 6 else False,
                            'loclin_departamento': item[6] if len(item) >= 7 else False,
                            'loclin_punto_venta': item[7] if len(item) >= 8 else False,
                        })

                    if item[0] == 'TAXLIN':
                        if not len(item) == 3:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'taxlin_tipo_impuesto': item[1],
                            'taxlin_porcentaje': item[2],
                            'taxlin_importe_impuesto': item[3],
                        })

                        if vals["taxlin_tipo_impuesto"] == 'VAT':
                            _logger.info("IVA")
                        else:
                            False
                        if vals["taxlin_tipo_impuesto"] == 'IGI':
                            _logger.info(" IGIC")
                        else:
                            False
                        if vals["taxlin_tipo_impuesto"] == 'EXT':
                            _logger.info("exento de impuestos ")
                        else:
                            False
                        if vals["taxlin_tipo_impuesto"] == 'RE':
                            _logger.info(" Recargo de equivalencia ")
                        else:
                            False
                        if vals["taxlin_tipo_impuesto"] == 'ACT':
                            _logger.info(" Impuest to de alcoholes  ")
                        else:
                            False
                        if vals["taxlin_tipo_impuesto"] == 'RET':
                            _logger.info("Retención por servicios profesionales ")
                        else:
                            False


                    if item[0] == 'ALCLIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        xline = ({
                            'alclin_indicador_descuento': item[1],
                            'alclin_secuencia_descuento': item[2] if len(item) >= 3 else False,
                            'alclin_tipo_descuento': item[3],
                            'alclin_cantidad': item[4] if len(item) >= 5 else False,
                            'alclin_porcentaje_descuento_sobre_precio': item[5] if len(item) >= 6 else False,
                            'alclin_importe_descuento': item[6] if len(item) >= 7 else False,
                            'alclin_porcentaje_descuento_sobre_precio': item[7] if len(item) >= 8 else False,
                        })
                        alclin.append(xline)
                        for f in alclin:
                            if f.has_key('alclin_indicador_descuento'):
                                # _logger.info(
                                #     "=>alclin_indicador_descuento", f["alclin_indicador_descuento"])

                                if f["alclin_indicador_descuento"] == 'A':
                                    _logger.info("Descuento")
                                else:
                                    False
                                if f["alclin_indicador_descuento"] == 'C':
                                    _logger.info("Cargo")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'EAB':
                                    _logger.info("De escuentos por pronto pa ago ")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'TD':
                                    _logger.info("descuento comercial ")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'FC':
                                    _logger.info("Cargo por fletes ")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'PC':
                                    _logger.info("Cargo por embalajes")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'SH':
                                    _logger.info(" Cargo por montajes")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'IN':
                                    _logger.info("Cargo por seguros")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'CW':
                                    _logger.info("Descuento por contenedor o envase retornado ")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'RAD':
                                    _logger.info("Cargo por contenedor o envase retornado")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'ABH':
                                    _logger.info("Ra appel (descuento por volumen)")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'ACQ':
                                    _logger.info("Royalties")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'FI':
                                    _logger.info("Cargo financiero ")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'ADO':
                                    _logger.info("logística eficiente")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'PAD':
                                    _logger.info(" Abono promocional")
                                else:
                                    False
                                if f["alclin_tipo_descuento"] == 'DI':
                                    _logger.info(" Descuento ")
                                else:
                                    False
                        vals.update({'alclin_row': alclin})

                    if item[0] == 'MOARES':
                        vals.update({
                            'moares_importe_neto_pedido': item[1] if len(item) >= 2 else False,
                            'moares_importe_bruto_pedido': item[2] if len(item) >= 3 else False,
                            'moares_importe_total_impuestos': item[3] if len(item) >= 4 else False,
                            'moares_importe_total_pagar': item[4] if len(item) >= 5 else False,
                            'moares_base_imponible_total': item[5] if len(item) >= 6 else False,
                        })

                    if item[0] == 'CNTRES':
                        vals.update({
                            'cntres_num_paquetes_embalajes': item[1] if len(item) >= 2 else False,
                            'cntres_total_palets_envio': item[2] if len(item) >= 3 else False,
                            'cntres_importe_articulos': item[3] if len(item) >= 4 else False,
                            'cntres_num_lineas_detalle': item[4] if len(item) >= 5 else False,
                            'cntres_peso_bruto_total_pedido': item[5] if len(item) >= 6 else False,
                        })

                        # if item[0] == 'NADSU':
                        # if not len(item) == 1:
                        #     Warning(('Please fixing manual'))
                        # vals.update({
                        #     'nadsu_punto_oper_proveedor': item[1],
                        #     'nadsu_cod_interno_proveedor': item[2] if len(item) >= 3 else False,
                        #     'nadsu_cod_interno_proveedor1': item[3] if len(item) >= 4 else False,
                        # })

        # _logger.warn('==> first line principio del mensaje %r' % vals)
        pprint(vals)
        return vals

    @api.multi
    def create_sale_order(self):
        line_list = []
        line_qty = []
        line_tax = []
        vals = self.confirm()




        if vals.has_key('nadiv_row'):
            for nadiv in vals['nadiv_row']:
                # print("#################nadsu",nadsu)
                for nadi in nadiv:
                    if nadi.has_key('nadiv_punto_oper_fac'):
                        # print("##################################nad", nad)
                        factu_recordset = self.env['res.partner'].search([
                            ('codigo_provedor', '=', str(nadi['nadiv_punto_oper_fac'])),
                             ('type', '=', 'invoice')
                             ])
                        # print("#######################################partner_recordset",partner_recordset)
                        #if not factu_recordset:
                           #post_vars = {'subject': 'Mensaje', 'body': _('The code not exists %r' % str(nad['nadiv_punto_oper_fac'])), }  # noqa
                           # self.message_post(type="notification", subtype="mt_comment", **post_vars)  # noqa
                        #for record in factu_recordset:
                            #print("#######################################record",record)


        if vals.has_key('naddp_row'):
            for nadd in vals['naddp_row']:
                # print("#################nadsu",nadsu)
                for nad in nadd:
                    if nad.has_key('naddp_punto_entrega'):
                        # print("##################################nad", nad)
                        dir_recordset = self.env['res.partner'].search([
                            ('codigo_provedor', '=', str(nad['naddp_punto_entrega'])),
                             ('type', '=', 'delivery')
                             ])
                        # print("#######################################partner_recordset",partner_recordset)
                        if not factu_recordset:
                            post_vars = {'subject': 'Mensaje', 'body': _('The code not exists %r' % str(nad['naddp_punto_entrega'])), }  # noqa
                            self.message_post(type="notification", subtype="mt_comment", **post_vars)  # noqa
                        for record in dir_recordset:
                            print("#######################################record",record)



       
        if vals.has_key('nadms_row'):
            for nadsu in vals['nadms_row']:
                # print("#################nadsu",nadsu)
                for nad in nadsu:
                    if nad.has_key('nadms_punto_oper_emisor_men'):
                        # print("##################################nad", nad)
                        partner_recordset = self.env['res.partner'].search([
                            ('codigo_provedor', '=', str(nad['nadms_punto_oper_emisor_men'])),
                            ('type', '=', 'contact')
                            ])
                        # print("#######################################partner_recordset",partner_recordset)
                        if not partner_recordset:
                            post_vars = {'subject': 'Mensaje', 'body': _('The code not exists %r' % str(nad['nadms_punto_oper_emisor_men'])), }  # noqa
                            self.message_post(type="notification", subtype="mt_comment", **post_vars)  # noqa
                        for record in partner_recordset:
                            print("#######################################record",record)

        qty_list = []
        product_uom_qty = 0.00
        if vals.has_key('lin_row'):
            for line in vals['lin_row']:
                for l in line:
                    if l.has_key('lin_cod_normalizado'):
                        product_recordset = self.env['product.product'].search([
                            ('barcode', '=', str(l['lin_cod_normalizado']))])
                        for qty_row in vals['qtylin_row']:
                            for qty_l in qty_row:
                                print "========>qty_l", qty_l
                                if qty_l.has_key('qtylin_cantidad_expresada') and l['lin_cod_normalizado'] == qty_l['qtylin_product']:
                                    product_uom_qty = float(qty_l['qtylin_cantidad_expresada'])
                                    qty_list.append([l['lin_cod_normalizado'], product_uom_qty])
                        print("#######################################product_uom_qty", product_uom_qty)
                        if not product_recordset:
                            post_vars = {'subject': 'Mensaje', 'body': _('The code not exists %r' % str(l['lin_cod_normalizado'])), }  # noqa
                            self.message_post(type="notification", subtype="mt_comment", **post_vars)  # noqa
                            print("#######################################post_var", post_vars)
                        for record in product_recordset:
                            # print("#######################################product_recordset",product_recordset)
                            for qty in qty_list:
                                discount = self.env['sale.order.line'].getDiscount(partner_recordset.id, product_recordset.id)
                                if qty[0] == record.barcode:
                                    product_qty = qty[1]
                                    xline = (0, 0, {
                                        'product_id': product_recordset.id,
                                        'product_uom_qty': product_qty,
                                        'discount': discount,
                                        # 'tax_id': [(4, tax_recordset.id)],
                                        'name': '{}'.format(product_recordset.name),  # noqa
                                        'price_unit': product_recordset.lst_price})
                                    print("#####################################xline", xline)
                                    line_list.append(xline)
                            # print("######################################line_list",line_list)
                        if not partner_recordset:
                            print "partner_recordset", partner_recordset
                            raise Warning(_('The partner can not be found!'))
                        order = {
                                'partner_id': partner_recordset.id,
                                #'partner_invoice_id' : factu_recordset.id,
                                'partner_shipping.id' : dir_recordset.id,
                                'order_line': [line for line in line_list],
                                 }
                        # print("####################################order", order)
                    # else:
                    #     post_vars = {'subject': 'Mensaje', 'body': _('The code not exists %r' % str(l['lin_cod_normalizado'])), }  # noqa
                    #     self.message_post(type="notification", subtype="mt_comment", **post_vars)  # noqa

            sale_obj = self.env['sale.order']
            sale_id = sale_obj.create(order)
            _logger.info('El ID de la nueva orden de venta es %s' % sale_id)
        pprint(vals)