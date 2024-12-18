from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
import json

class TestMaterial(TransactionCase):

    def setUp(self):
        super(TestMaterial, self).setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'supplier_rank': 1
        })
        
        self.material_data = {
            'material_code': 'TEST001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'material_buy_price': 150.0,
            'supplier_id': self.supplier.id
        }

    def test_create_material(self):
        # Test normal creation
        material = self.env['material.registration'].create(self.material_data)
        self.assertTrue(material.id)
        self.assertEqual(material.material_code, 'TEST001')

        # Test price constraint
        with self.assertRaises(ValidationError):
            self.material_data['material_buy_price'] = 50.0
            self.env['material.registration'].create(self.material_data)

    def test_unique_material_code(self):
        # Create first material
        self.env['material.registration'].create(self.material_data)

        # Try to create material with same code
        with self.assertRaises(Exception):
            self.env['material.registration'].create(self.material_data)

    def test_update_material(self):
        material = self.env['material.registration'].create(self.material_data)
        
        # Test valid update
        material.write({
            'material_name': 'Updated Material',
            'material_buy_price': 200.0
        })
        self.assertEqual(material.material_name, 'Updated Material')
        self.assertEqual(material.material_buy_price, 200.0)

        # Test invalid price update
        with self.assertRaises(ValidationError):
            material.write({
                'material_buy_price': 50.0
            })

    def test_delete_material(self):
        material = self.env['material.registration'].create(self.material_data)
        material_id = material.id
        
        # Test deletion
        material.unlink()
        self.assertFalse(self.env['material.registration'].browse(material_id).exists())