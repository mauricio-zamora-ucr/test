"""
Tests básicos para la aplicación
Verifica que las funcionalidades principales funcionen correctamente
"""
import unittest
from database.connection import DatabaseConnection
from controllers.producto_controller import ProductoController
from controllers.venta_controller import VentaController
from models.producto import Producto
from models.venta import Venta
import os


class TestProductoController(unittest.TestCase):
    """Tests para el controlador de productos"""
    
    @classmethod
    def setUpClass(cls):
        """Se ejecuta antes de todos los tests"""
        # Usar BD de prueba
        os.environ['DB_PATH'] = ':memory:'
        DatabaseConnection.create_tables()
    
    def test_crear_producto(self):
        """Test crear un producto"""
        resultado = ProductoController.crear_producto(
            "TEST001", "Producto Test", 99.99, 10, "Descripción test"
        )
        self.assertTrue(resultado['exito'])
        self.assertIn('id', resultado)
    
    def test_crear_producto_sin_codigo(self):
        """Test crear producto sin código (debe fallar)"""
        resultado = ProductoController.crear_producto(
            "", "Producto", 99.99, 10, ""
        )
        self.assertFalse(resultado['exito'])
    
    def test_crear_producto_precio_negativo(self):
        """Test crear producto con precio negativo (debe fallar)"""
        resultado = ProductoController.crear_producto(
            "TEST002", "Producto", -10, 10, ""
        )
        self.assertFalse(resultado['exito'])
    
    def test_obtener_todos_productos(self):
        """Test obtener todos los productos"""
        # Crear un producto primero
        ProductoController.crear_producto("OBT001", "Producto 1", 50.0, 5, "")
        
        resultado = ProductoController.obtener_todos_productos()
        self.assertTrue(resultado['exito'])
        self.assertIsInstance(resultado['datos'], list)
        self.assertGreater(len(resultado['datos']), 0)
    
    def test_actualizar_producto(self):
        """Test actualizar un producto"""
        # Crear producto
        res_crear = ProductoController.crear_producto(
            "UPD001", "Producto Original", 100.0, 10, "Original"
        )
        producto_id = res_crear['id']
        
        # Actualizar
        resultado = ProductoController.actualizar_producto(
            producto_id, "UPD001", "Producto Actualizado", 150.0, 20, "Actualizado"
        )
        self.assertTrue(resultado['exito'])
    
    def test_eliminar_producto(self):
        """Test eliminar un producto"""
        # Crear producto
        res_crear = ProductoController.crear_producto(
            "DEL001", "Producto a Borrar", 50.0, 5, ""
        )
        producto_id = res_crear['id']
        
        # Eliminar
        resultado = ProductoController.eliminar_producto(producto_id)
        self.assertTrue(resultado['exito'])


class TestVentaController(unittest.TestCase):
    """Tests para el controlador de ventas"""
    
    @classmethod
    def setUpClass(cls):
        """Se ejecuta antes de todos los tests"""
        DatabaseConnection.create_tables()
        
        # Crear un producto de prueba
        ProductoController.crear_producto(
            "VTEST001", "Producto Venta Test", 99.99, 100, "Producto para ventas"
        )
    
    def test_crear_venta(self):
        """Test crear una venta"""
        resultado = VentaController.crear_venta(1, 5, 99.99)
        self.assertTrue(resultado['exito'])
        self.assertIn('id', resultado)
    
    def test_crear_venta_cantidad_negativa(self):
        """Test crear venta con cantidad negativa (debe fallar)"""
        resultado = VentaController.crear_venta(1, -1, 99.99)
        self.assertFalse(resultado['exito'])
    
    def test_crear_venta_stock_insuficiente(self):
        """Test crear venta con stock insuficiente (debe fallar)"""
        resultado = VentaController.crear_venta(1, 999, 99.99)
        self.assertFalse(resultado['exito'])
    
    def test_obtener_todas_ventas(self):
        """Test obtener todas las ventas"""
        # Crear una venta primero
        VentaController.crear_venta(1, 2, 50.0)
        
        resultado = VentaController.obtener_todas_ventas()
        self.assertTrue(resultado['exito'])
        self.assertIsInstance(resultado['datos'], list)
    
    def test_eliminar_venta(self):
        """Test eliminar una venta"""
        # Crear venta
        res_crear = VentaController.crear_venta(1, 1, 99.99)
        if res_crear['exito']:
            venta_id = res_crear['id']
            # Eliminar
            resultado = VentaController.eliminar_venta(venta_id)
            self.assertTrue(resultado['exito'])


class TestModels(unittest.TestCase):
    """Tests para los modelos"""
    
    @classmethod
    def setUpClass(cls):
        """Se ejecuta antes de todos los tests"""
        DatabaseConnection.create_tables()
    
    def test_producto_obtener_por_codigo(self):
        """Test obtener producto por código"""
        Producto.crear("TEST_COD", "Test Código", 100, 10)
        producto_id = Producto.obtener_por_codigo("TEST_COD")
        self.assertIsNotNone(producto_id)
    
    def test_venta_obtener_total(self):
        """Test obtener total de ventas"""
        total = Venta.obtener_total_ventas()
        self.assertIsInstance(total, (int, float))
        self.assertGreaterEqual(total, 0)


def run_tests():
    """Ejecuta todos los tests"""
    print("\\n" + "="*60)
    print("EJECUTANDO TESTS")
    print("="*60 + "\\n")
    
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestProductoController))
    suite.addTests(loader.loadTestsFromTestCase(TestVentaController))
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\\n" + "="*60)
    if result.wasSuccessful():
        print("✅ TODOS LOS TESTS PASARON")
    else:
        print(f"❌ {len(result.failures)} fallos, {len(result.errors)} errores")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
