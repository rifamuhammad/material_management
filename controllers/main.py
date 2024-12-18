from odoo import http
from odoo.http import request
import json

class MaterialController(http.Controller):

    @http.route('/api/materials', type='http', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        domain = []
        if kwargs.get('material_type'):
            domain.append(('material_type', '=', kwargs.get('material_type')))
            
        materials = request.env['material.registration'].search_read(
            domain=domain,
            fields=['material_code', 'material_name', 'material_type', 
                   'material_buy_price', 'supplier_id']
        )
        return json.dumps(materials)

    @http.route('/api/materials', type='json', auth='user', methods=['POST'])
    def create_material(self, **kwargs):
        try:
            material = request.env['material.registration'].create({
                'material_code': kwargs.get('material_code'),
                'material_name': kwargs.get('material_name'),
                'material_type': kwargs.get('material_type'),
                'material_buy_price': float(kwargs.get('material_buy_price')),
                'supplier_id': int(kwargs.get('supplier_id'))
            })
            return {
                'status': 'success',
                'id': material.id
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    @http.route('/api/materials/<int:material_id>', type='json', auth='user', methods=['PUT'])
    def update_material(self, material_id, **kwargs):
        try:
            material = request.env['material.registration'].browse(material_id)
            if not material.exists():
                return {'status': 'error', 'message': 'Material not found'}
            
            material.write({
                'material_name': kwargs.get('material_name', material.material_name),
                'material_type': kwargs.get('material_type', material.material_type),
                'material_buy_price': float(kwargs.get('material_buy_price', material.material_buy_price)),
                'supplier_id': int(kwargs.get('supplier_id', material.supplier_id.id))
            })
            return {'status': 'success'}
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    @http.route('/api/materials/<int:material_id>', type='http', auth='user', methods=['DELETE'])
    def delete_material(self, material_id):
        try:
            material = request.env['material.registration'].browse(material_id)
            if not material.exists():
                return json.dumps({'status': 'error', 'message': 'Material not found'})
            
            material.unlink()
            return json.dumps({'status': 'success'})
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'message': str(e)
            })