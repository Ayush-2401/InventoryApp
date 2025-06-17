from PySide6.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PySide6.QtGui import QDoubleValidator, QIntValidator
from utils import SessionLocal
from models import Product

class ProductMasterForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product Master Form")
        self.setGeometry(100, 100, 400, 600)

        main_layout = QVBoxLayout() # This is your main layout

        # Pass main_layout to _create_line_edit so it can add to it
        self.barcode_input = self._create_line_edit("Barcode:", main_layout)
        self.sku_input = self._create_line_edit("SKU ID:", main_layout)
        self.category_input = self._create_line_edit("Category:", main_layout)
        self.subcategory_input = self._create_line_edit("Subcategory:", main_layout)
        self.product_name_input = self._create_line_edit("Product Name:", main_layout)

        main_layout.addWidget(QLabel("Description:"))
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Enter product description (max 255 chars)")
        main_layout.addWidget(self.description_input)

        self.tax_input = self._create_line_edit("Tax (%):", main_layout)
        self.tax_input.setValidator(QDoubleValidator(0.0, 100.0, 2))

        self.price_input = self._create_line_edit("Price:", main_layout)
        self.price_input.setValidator(QDoubleValidator(0.0, 9999999.0, 2))

        self.unit_input = self._create_line_edit("Default Unit of Measurement:", main_layout)
        self.unit_input.setPlaceholderText("e.g., pcs, kg, L, box")

        self.image_path_label = QLabel("No image selected")
        upload_image_btn = QPushButton("Upload Image")
        upload_image_btn.clicked.connect(self.upload_image)

        image_layout = QHBoxLayout()
        image_layout.addWidget(upload_image_btn)
        image_layout.addWidget(self.image_path_label)
        main_layout.addLayout(image_layout)

        save_btn = QPushButton("Save Product")
        save_btn.clicked.connect(self.save_product)
        main_layout.addWidget(save_btn)

        self.setLayout(main_layout) # This sets the main layout for the QWidget
        self.image_path = ""

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

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Product Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)")
        if file_path:
            self.image_path = file_path
            self.image_path_label.setText(f"Image: {file_path.split('/')[-1]}")
            QMessageBox.information(self, "Image Selected", f"Image path saved: {self.image_path}")
        else:
            self.image_path = ""
            self.image_path_label.setText("No image selected")

    def save_product(self):
        barcode = self.barcode_input.text().strip()
        sku_id = self.sku_input.text().strip()
        category = self.category_input.text().strip()
        subcategory = self.subcategory_input.text().strip()
        product_name = self.product_name_input.text().strip()
        description = self.description_input.toPlainText().strip()
        unit = self.unit_input.text().strip()

        if not product_name:
            QMessageBox.critical(self, "Input Error", "Product Name is mandatory.")
            return
        if not barcode and not sku_id:
             QMessageBox.critical(self, "Input Error", "Either Barcode or SKU ID is mandatory.")
             return

        try:
            tax = float(self.tax_input.text()) if self.tax_input.text() else 0.0
            price = float(self.price_input.text()) if self.price_input.text() else 0.0
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Please enter valid numbers for Tax and Price.")
            return

        session = SessionLocal()
        try:
            if barcode and session.query(Product).filter_by(barcode=barcode).first():
                QMessageBox.critical(self, "Duplicate Error", "A product with this barcode already exists.")
                return
            if sku_id and session.query(Product).filter_by(sku_id=sku_id).first():
                QMessageBox.critical(self, "Duplicate Error", "A product with this SKU ID already exists.")
                return

            product = Product(
                barcode=barcode,
                sku_id=sku_id,
                category=category,
                subcategory=subcategory,
                product_name=product_name,
                description=description,
                tax=tax,
                price=price,
                unit=unit,
                image_path=self.image_path,
                stock_quantity=0.0
            )
            session.add(product)
            session.commit()
            QMessageBox.information(self, "Success", "Product saved successfully!")
            self.clear_form()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save product: {e}")
        finally:
            session.close()

    def clear_form(self):
        self.barcode_input.clear()
        self.sku_input.clear()
        self.category_input.clear()
        self.subcategory_input.clear()
        self.product_name_input.clear()
        self.description_input.clear()
        self.tax_input.clear()
        self.price_input.clear()
        self.unit_input.clear()
        self.image_path = ""
        self.image_path_label.setText("No image selected")