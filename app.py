from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
import sys

from models import Base, Operator 
from utils import engine, SessionLocal 

from ui_login import LoginForm
from ui_product_master import ProductMasterForm
from ui_goods_receiving import GoodsReceivingForm
from ui_sales import SalesForm

main_window_instance = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(200, 200, 400, 300)

        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)

        btn_product = QPushButton("Product Master")
        btn_product.clicked.connect(self.open_product)
        layout.addWidget(btn_product)

        btn_goods = QPushButton("Goods Receiving")
        btn_goods.clicked.connect(self.open_goods)
        layout.addWidget(btn_goods)

        btn_sales = QPushButton("Sales Entry")
        btn_sales.clicked.connect(self.open_sales)
        layout.addWidget(btn_sales)

        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.product_form = None
        self.goods_form = None
        self.sales_form = None

    def open_product(self):
        if self.product_form is None:
            self.product_form = ProductMasterForm()
        self.product_form.show()
        if self.product_form.isMinimized():
            self.product_form.showNormal()
        self.product_form.activateWindow()

    def open_goods(self):
        if self.goods_form is None:
            self.goods_form = GoodsReceivingForm()
        self.goods_form.show()
        if self.goods_form.isMinimized():
            self.goods_form.showNormal()
        self.goods_form.activateWindow()

    def open_sales(self):
        if self.sales_form is None:
            self.sales_form = SalesForm()
        self.sales_form.show()
        if self.sales_form.isMinimized():
            self.sales_form.showNormal()
        self.sales_form.activateWindow()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    
    Base.metadata.create_all(bind=engine)

    
    session = SessionLocal()
    try:
        
        admin_user = session.query(Operator).filter_by(username='admin').first()
        if not admin_user:
            session.add(Operator(username='admin', password='adminpass'))
            print("Added default admin user.")
        
        
        regular_user = session.query(Operator).filter_by(username='user').first()
        if not regular_user:
            session.add(Operator(username='user', password='userpass'))
            print("Added default user.")
            
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error ensuring default users: {e}")
    finally:
        session.close()

    def on_login_success_callback():
        global main_window_instance
        main_window_instance = MainWindow()
        main_window_instance.show()

    login_window = LoginForm(on_login_success=on_login_success_callback)
    login_window.show()

    sys.exit(app.exec())
