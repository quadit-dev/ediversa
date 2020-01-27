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

    product_exist = fields.Text(string='Default Terms and Conditions',
                                translate=True)


class ediversaOrder(models.Model):
    _name = 'ediversa.order'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = 'ediversa Orders'

    _rec_name = 'subject'

    subject = fields.Char('Subject', size=128)
    email = fields.Char('Email', size=128)
    attach = fields.Text('Attachment')
    dtm_creacion = fields.Datetime ('Fecha creacion',
        readonly = False,
        select = True ,
        default = lambda self: fields.datetime.now ())

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
                    item = line.split('|')

                    if item[0] == 'ORD':
                        if not len(item) == 3:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'ord_num_doc': item[1],
                            'ord_tipo_doc': item[2],
                            'ord_fun_mensaje': item[3],
                        })

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

                    if item[0] == 'ALI':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'ali_info_pedido': item[1],
                        })

                    if item[0] == 'FTX':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline = ({
                            'ftx_info_gral': item[1],
                            'ftx_info_codificada': item[2] if len(item) >= 3 else False,
                            'ftx_texto_libre': item[3] if len(item) >= 4 else False,
                        })
                        ftx.append(xline)
                        vals.update({'ftx_row': ftx})

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
                        xline = [{
                            'nadms_punto_oper_emisor_men': item[1],
                            'nadms_nombre': item[2] if len(item) >= 3 else False,
                            'nadms_direccion': item[3] if len(item) >= 4 else False,
                            'nadms_poblacion': item[4] if len(item) >= 5 else False,
                            'nadms_cp': item[5] if len(item) >= 6 else False,
                            'nadms_nif': item[6] if len(item) >= 7 else False,
                        }]
                        nadms.append(xline)
                        vals.update({'nadms_row': nadms})

                    if item[0] == 'NADMR':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'nadmr_punto_oper_receptor_men': item[1],
                        })
                    if item[0] == 'NADSU':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        xline = [{
                            'nadsu_punto_oper_proveedor': item[1],
                            'nadsu_cod_interno_proveedor': item[2] if len(item) >= 3 else False,
                            'nadsu_cod_interno_proveedor1': item[3] if len(item) >= 4 else False,
                        }]
                        nadsu.append(xline)
                        vals.update({'nadsu_row': nadsu})

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
                        xline = [{
                            'naddp_punto_entrega': item[1],
                            'naddp_puerta_entrega_mercancia': item[2] if len(item) >= 3 else False,
                            'naddp_nombre': item[3] if len(item) >= 4 else False,
                            'naddp_direccion': item[4] if len(item) >= 5 else False,
                            'naddp_poblacion': item[5] if len(item) >= 6 else False,
                            'naddp_cp': item[6] if len(item) >= 7 else False,
                        }]
                        naddp.append(xline)
                        vals.update({'naddp_row': naddp})

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
                        vals.update({'nadiv_row': nadiv})

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
                        xline = [{
                            'tax_tipo_impuesto': item[1],
                            'tax_porcentaje_impuesto': item[2] if len(item) >= 3 else False,
                            'tax_importe_impuesto': item[3] if len(item) >= 4 else False,
                        }]
                        tax.append(xline)
                        vals.update({'tax_row': tax})

                    if item[0] == 'CUX':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'cux_tipo_moneda': item[1],
                        })

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

                    if item[0] == 'TDT':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'tdt_medio_tranporte_mercancia': item[1],
                        })

                    if item[0] == 'TOD':
                        vals.update({
                            'tod_condiciones_entrega': item[1] if len(item) >= 2 else False,
                            'tod_responsable_trasporte': item[2] if len(item) >= 3 else False,
                            'tod_lugar_entrega': item[3] if len(item) >= 4 else False,
                            'tod_punto_operacional_entrega': item[4] if len(item) >= 5 else False,
                            'tod_codigo_interno_lugar_entrega': item[5] if len(item) >= 6 else False,
                        })

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

                    if item[0] == 'LIN':
                        product_ban = str(item[1])

                        xline = [{
                            'lin_cod_normalizado': item[1] if len(item) >= 2 else False,
                            'lin_tipo_cod': item[2] if len(item) >= 3 else False,
                            'lin_num_correctivo_linea_detalle': item[3] if len(item) >= 4 else False,
                        }]
                        lin.append(xline)
                        vals.update({'lin_row': lin})

                    if item[0] == 'PIALIN':
                        if not len(item) == 2:
                            Warning(('Please fixing manual'))
                        xline = [{
                            'pialin_calificador': item[1],
                            'pialin_ref_articulo': item[2],
                        }]
                        pialin.append(xline)
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
                        vals.update({'prilin_row': prilin})

                    if item[0] == 'PACLIN':
                        if not len(item) == 1:
                            Warning(('Please fixing manual'))
                        vals.update({
                            'paclin_num_bultos_palet': item[1] if len(item) >= 2 else False,
                            'paclin_tipo_embalaje': item[2],
                        })

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

        return vals

    @api.multi
    def create_sale_order(self):
        line_list = []
        line_qty = []
        line_tax = []
        vals = self.confirm()

        if vals.has_key('nadiv_row'):
            for nadiv in vals['nadiv_row']:
                for nadi in nadiv:
                    if nadi.has_key('nadiv_punto_oper_fac'):
                        factu_recordset = self.env['res.partner'].search([
                            ('codigo_provedor', '=', str(
                                nadi['nadiv_punto_oper_fac'])),
                            ('type', '=', 'invoice')
                        ])

        if vals.has_key('naddp_row'):
            for nadd in vals['naddp_row']:
                for nad in nadd:
                    if nad.has_key('naddp_punto_entrega'):
                        #print("========================================>nad", nad)
                        dir_recordset = self.env['res.partner'].search([
                            ('codigo_provedor', '=', str(
                                nad['naddp_punto_entrega']))
                            #,('type', '=', 'delivery')
                        ])
                        if not dir_recordset:
                            raise Warning("Falta el codigo de entrega")
                            post_vars = {'subject': 'Mensaje', 'body': _('El codigo para entrega no existe %r' % str(nad['naddp_punto_entrega'])), }  # noqa
                            self.message_post(type="notification", subtype="mt_comment", **post_vars)  # noqa

        if vals.has_key('nadms_row'):
            for nadsu in vals['nadms_row']:
                for nad in nadsu:
                    if nad.has_key('nadms_punto_oper_emisor_men'):
                        partner_recordset = self.env['res.partner'].search([
                            ('codigo_provedor', '=', str(
                                nad['nadms_punto_oper_emisor_men'])),
                            ('type', '=', 'contact')
                        ])
                        if not partner_recordset:
                            post_vars = {'subject': 'Mensaje', 'body': _('El codigo de cliente2 no existe %r' % str(nad['nadms_punto_oper_emisor_men'])), }  # noqa
                            self.message_post(type="notification", subtype="mt_comment", **post_vars)

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
                                if qty_l.has_key('qtylin_cantidad_expresada') and l['lin_cod_normalizado'] == qty_l['qtylin_product']:
                                    product_uom_qty = float(
                                        qty_l['qtylin_cantidad_expresada'])
                                    qty_list.append(
                                        [l['lin_cod_normalizado'], product_uom_qty])
                        if not product_recordset:
                            post_vars = {'subject': 'Mensaje', 'body': _('The code not exists %r' % str(l['lin_cod_normalizado'])), }  # noqa
                            self.message_post(type="notification", subtype="mt_comment", **post_vars)
                        for record in product_recordset:
                            for qty in qty_list:
                                discount = self.env['sale.order.line'].getDiscount(
                                    partner_recordset.id, product_recordset.id)
                                if qty[0] == record.barcode:
                                    product_qty = qty[1]
                                    xline = (0, 0, {
                                        'product_id': product_recordset.id,
                                        'discount': discount,
                                        'product_uom': 1,
                                        'product_uom_qty': product_qty,
                                        # 'tax_id': [(4, tax_recordset.id)],
                                        'name': '{}'.format(product_recordset.name),
                                        'price_unit': product_recordset.lst_price})
                                    line_list.append(xline)
                        if not partner_recordset:
                            print "partner_recordset", partner_recordset
                            raise Warning(_('The partner can not be found!'))
                        #print("========================================>nombre",dir_recordset.name)
                        #print("========================================>id",dir_recordset.id)
                        order = {
                            'partner_id': partner_recordset.id,
                            # 'partner_invoice_id' : factu_recordset.id,
                            'partner_shipping_id': dir_recordset.id,
                            'order_line': [line for line in line_list],
                        }
            sale_obj = self.env['sale.order']
            sale_id = sale_obj.create(order)
            _logger.info('El ID de la nueva orden de venta es %s' % sale_id)
        pprint(vals)
