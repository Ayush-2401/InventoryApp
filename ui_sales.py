from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtGui import QIntValidator, QDoubleValidator
from utils import SessionLocal
from models import Sale, Product


class SalesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Entry")
        self.setGeometry(100, 100, 400, 450)

        main_layout = QVBoxLayout() # This is your main layout
        main_layout.setSpacing(10)

        # Pass main_layout to _create_line_edit so it can add to it
        self.product_id_input = self._create_line_edit("Product ID:", main_layout)
        self.product_id_input.setValidator(QIntValidator(1, 9999999))

        self.customer_name_input = self._create_line_edit("Customer Name:", main_layout)

        self.quantity_input = self._create_line_edit("Quantity:", main_layout)
        self.quantity_input.setValidator(QDoubleValidator(0.01, 9999999.0, 2))

        self.unit_input = self._create_line_edit("Unit:", main_layout)
        self.unit_input.setPlaceholderText("e.g., pcs, kg, L")

        self.rate_input = self._create_line_edit("Rate per unit:", main_layout)
        self.rate_input.setValidator(QDoubleValidator(0.01, 9999999.0, 2))

        save_btn = QPushButton("Save Sale")
        save_btn.clicked.connect(self.save_sale)
        main_layout.addWidget(save_btn)

        self.setLayout(main_layout) # This sets the main layout for the QWidget

    # Modified _create_line_edit to accept the parent_layout
    def _create_line_edit(self, label_text, parent_layout):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"Enter {label_text.replace(':', '').strip()}")
        layout.addWidget(label)
        layout.addWidget(line_edit)
        parent_layout.addLayout(layout) # Add to the passed main_layout
        return line_edit

    def save_sale(self):
        session = SessionLocal()
        try:
            product_id = int(self.product_id_input.text()) if self.product_id_input.text() else 0
            quantity = float(self.quantity_input.text()) if self.quantity_input.text() else 0.0
            rate = float(self.rate_input.text()) if self.rate_input.text() else 0.0
            customer_name = self.customer_name_input.text().strip()
            unit = self.unit_input.text().strip()

            if not product_id or product_id <= 0:
                QMessageBox.critical(self, "Input Error", "Please enter a valid Product ID.")
                return
            if not customer_name:
                QMessageBox.critical(self, "Input Error", "Customer Name is mandatory.")
                return
            if quantity <= 0:
                QMessageBox.critical(self, "Input Error", "Quantity must be greater than zero.")
                return
            if rate <= 0:
                QMessageBox.critical(self, "Input Error", "Rate must be greater than zero.")
                return
            if not unit:
                QMessageBox.critical(self, "Input Error", "Unit is mandatory.")
                return

        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers for Product ID, Quantity, and Rate.")
            return
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred during input parsing: {e}")
            return

        try:
            product = session.query(Product).filter_by(id=product_id).first()

            if not product:
                QMessageBox.critical(self, "Error", f"Product with ID {product_id} does not exist in product master.")
                return

            if product.stock_quantity < quantity:
                QMessageBox.warning(self, "Stock Alert", f"Insufficient stock for {product.product_name}. Available: {product.stock_quantity}, Requested: {quantity}")
                return

            sub_total = quantity * rate
            product_tax_percentage = product.tax
            tax_amount = (sub_total * product_tax_percentage) / 100
            total_sale_amount = sub_total + tax_amount

            sale = Sale(
                product_id=product_id,
                customer_name=customer_name,
                quantity=quantity,
                unit=unit,
                rate=rate,
                total_rate=total_sale_amount,
                tax=product_tax_percentage
            )
            session.add(sale)
            product.stock_quantity -= quantity
            session.add(product)
            session.commit()
            QMessageBox.information(self, "Success", f"Sale recorded successfully for {product.product_name}! Remaining stock: {product.stock_quantity}")
            self.clear_form()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save sale record: {e}")
        finally:
            session.close()

    def clear_form(self):
        self.product_id_input.clear()
        self.customer_name_input.clear()
        self.quantity_input.clear()
        self.unit_input.clear()
        self.rate_input.clear()