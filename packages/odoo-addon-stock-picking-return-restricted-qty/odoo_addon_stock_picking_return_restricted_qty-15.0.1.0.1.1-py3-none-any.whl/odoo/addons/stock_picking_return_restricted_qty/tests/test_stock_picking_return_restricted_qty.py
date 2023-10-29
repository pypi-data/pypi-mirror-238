# Copyright 2020 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests import Form, common


class StockPickingReturnRestrictedQtyTest(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Remove this variable in v16 and put instead:
        # from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT
        DISABLED_MAIL_CONTEXT = {
            "tracking_disable": True,
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **DISABLED_MAIL_CONTEXT))
        partner = cls.env["res.partner"].create({"name": "Test"})
        product = cls.env["product.product"].create(
            {"name": "test_product", "type": "product"}
        )
        picking_type_out = cls.env.ref("stock.picking_type_out")
        stock_location = cls.env.ref("stock.stock_location_stock")
        customer_location = cls.env.ref("stock.stock_location_customers")
        cls.picking = cls.env["stock.picking"].create(
            {
                "partner_id": partner.id,
                "picking_type_id": picking_type_out.id,
                "location_id": stock_location.id,
                "location_dest_id": customer_location.id,
                "move_lines": [
                    (
                        0,
                        0,
                        {
                            "name": product.name,
                            "product_id": product.id,
                            "product_uom_qty": 20,
                            "product_uom": product.uom_id.id,
                            "location_id": stock_location.id,
                            "location_dest_id": customer_location.id,
                        },
                    )
                ],
            }
        )
        cls.picking.action_confirm()
        cls.picking.action_assign()
        cls.picking.move_lines[:1].quantity_done = 20
        cls.picking.button_validate()

    def get_return_picking_wizard(self, picking):
        stock_return_picking_form = Form(
            self.env["stock.return.picking"].with_context(
                active_ids=picking.ids,
                active_id=picking.ids[0],
                active_model="stock.picking",
            )
        )
        return stock_return_picking_form.save()

    def test_return_not_allowed(self):
        """On this test we create a return picking with more quantity
        than the quantity that client have on his hand"""
        return_picking = self.get_return_picking_wizard(self.picking)
        self.assertEqual(return_picking.product_return_moves.quantity, 20)
        return_picking.product_return_moves.quantity = 30
        with self.assertRaises(UserError):
            return_picking._create_returns()

    def test_multiple_return(self):
        """On this test we are going to follow a sequence that a client
        can follow if he tries to return a product"""
        wiz = self.get_return_picking_wizard(self.picking)
        wiz.product_return_moves.quantity = 10
        picking_returned_id = wiz._create_returns()[0]
        picking_returned = self.env["stock.picking"].browse(picking_returned_id)

        wiz = self.get_return_picking_wizard(self.picking)
        self.assertEqual(wiz.product_return_moves.quantity, 10)

        picking_returned._action_done()
        wiz = self.get_return_picking_wizard(self.picking)
        self.assertEqual(wiz.product_return_moves.quantity, 10)

        wiz.product_return_moves.quantity = 80
        with self.assertRaises(UserError):
            wiz.product_return_moves._onchange_quantity()
