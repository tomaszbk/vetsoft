from datetime import datetime, timedelta

from django.test import TestCase

from app.models import Client, Medicine, Pet, Product, Provider,object_to_querydict


class ClientModelTest(TestCase):
    """Test the client model."""

    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, 54221555232)
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, 54221555232)

        client.update_client({"phone": 54221555232})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, 54221555232)

    def test_cant_create_client_with_invalid_name(self):
        saved, errors = Client.save_client(
            {
                "name": "pepito12",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            },
        )
        self.assertFalse(saved)
        self.assertEqual(errors["name"], "El nombre solo puede contener letras y espacios")
    
    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, 54221555232)

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, 54221555232)

    def test_phone_must_start_with_54(self):
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 221555233,
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        self.assertFalse(saved)
        self.assertEqual(errors["phone"], "El teléfono debe comenzar con 54")
        
    def test_phone_must_be_only_numbers(self):
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54aaa",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        self.assertFalse(saved)
        self.assertEqual(errors["phone"], "El teléfono debe ser un número")
        


    def test_email_must_have_vetsoft_domain(self):
        saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "address": "13 y 44",
                "email": "brujita75@yahoo.com"
            }
        )
        self.assertFalse(saved)
        self.assertEqual(errors["email"], "El email debe ser de dominio vetsoft.com")



class MedicineModelTest(TestCase):
    """Test the medicine model."""

    def test_can_create_and_get_medicine(self):
        Medicine.save_medicine(
            {
                "name": "Ivermectina",
                "description": "Antiparasitario",
                "dose": 1,
            },
        )
        medicines = Medicine.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Ivermectina")
        self.assertEqual(medicines[0].description, "Antiparasitario")
        self.assertEqual(medicines[0].dose, 1)

    def test_cant_create_medicine_with_dose_gratter_than_10(self):
        saved, errors = Medicine.save_medicine(
            {
                "name": "Ivermectina",
                "description": "Antiparasitario",
                "dose": "11",
            },
        )
        self.assertFalse(saved)
        self.assertEqual(errors["dose"], "La dosis debe estar entre 1 y 10.")

    def test_cant_create_medicine_with_dose_less_than_1(self):
        saved, errors = Medicine.save_medicine(
            {
                "name": "Ivermectina",
                "description": "Antiparasitario",
                "dose": "0",
            },
        )
        self.assertFalse(saved)
        self.assertEqual(errors["dose"], "La dosis debe estar entre 1 y 10.")


class PetModelTest(TestCase):
    """Test the pet model."""

    def test_cant_create_pet_with_birthday_today(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        _, errors = Pet.save_pet(
            {
                "name": "Rex",
                "breed": "Labrador",
                "birthday": datetime.now().date(),
                "client": 1,
            },
        )
        self.assertIn("invalid_birthday", errors)

    def test_cant_create_pet_with_future_birthday(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        _, errors = Pet.save_pet(
            {
                "name": "Rex",
                "breed": "Labrador",
                "birthday": datetime.now().date() + timedelta(days=1),
                "client": 1,
            }
        )
        self.assertIn("invalid_birthday", errors)

    def test_can_create_pet(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        is_success, errors = Pet.save_pet(
            {
                "name": "Rex",
                "breed": "Labrador",
                "birthday": datetime.now().date() - timedelta(days=1),
                "client": 1,
            },
        )
        self.assertTrue(is_success)


class ProductModelTest(TestCase):
    """Test the product model."""

    def test_can_create_product(self):
        result = Product.save_product(
            {
                "name": "Pelota",
                "type": "Juguete",
                "price": str(33),
            },
        )

        self.assertEqual(result, (True, None))

    def test_cannot_create_product_with_price_0(self):
        result = Product.save_product(
            {
                "name": "Pelota",
                "type": "Juguete",
                "price": str(0),
            },
        )

        self.assertEqual(
            result,
            (False, {"price": "Por favor ingrese un precio mayor a 0."}),
        )

    def test_cannot_create_product_with_price_negative(self):
        result = Product.save_product(
            {
                "name": "Pelota",
                "type": "Juguete",
                "price": str(-33),
            },
        )

        self.assertEqual(
            result,
            (False, {"price": "Por favor ingrese un precio mayor a 0."}),
        )

    def test_can_create_product_without_price(self):
        result = Product.save_product(
            {
                "name": "Pelota",
                "type": "Juguete",
                "price": "",
            },
        )

        self.assertEqual(
            result,
            (False, {"price": "Por favor ingrese el precio del producto."}),
        )


class ProviderModelTest(TestCase):
    """Test the provider model."""

    def test_can_create_provider(self):
        result = Provider.save_provider(
            {
                "name": "Servicios Veterinarios SA",
                "email": "Serviciosveterinarios@gmail.com",
                "address": "Calle 13 n°1587",
            },
        )

        self.assertEqual(result, (True, None))

    def test_cant_create_provider_without_name(self):
        result = Provider.save_provider(
            {
                "name": "",
                "email": "Serviciosveterinarios@gmail.com",
                "address": "Calle 13 n°1587",
            },
        )
        self.assertEqual(
            result,
            (False, {"name": "Por favor ingrese un nombre"}),
        )

    def test_cant_create_provider_with_invalid_email(self):
        result = Provider.save_provider(
            {
                "name": "Servicios Veterinarios SA",
                "email": "Serviciosveterinariosgmail.com",
                "address": "Calle 13 n°1587",
            },
        )
        self.assertEqual(
            result,
            (False, {"email": "Por favor ingrese un email valido"}),
        )

    def test_cant_create_provider_without_address(self):
        result = Provider.save_provider(
            {
                "name": "Servicios Veterinarios SA",
                "email": "Serviciosveterinarios@gmail.com",
                "address": "",
            },
        )
        self.assertEqual(
            result,
            (False, {"address": "Por favor ingrese una dirección"}),
        )

class ObjectToQueryDictTest(TestCase):
    def test_object_to_querydict(self):
        class MyObject:
            def __init__(self):
                self.name = "John"
                self.age = 30
                self.email = "john@example.com"
                self.city = "New York"

        obj = MyObject()

        query_dict = object_to_querydict(obj)
        
        self.assertEqual(query_dict.get("name"), "John")
        self.assertEqual(query_dict.get("age"), "30")
        self.assertEqual(query_dict.get("city"),"New York")
        self.assertEqual(query_dict.get("email"), "john@example.com")