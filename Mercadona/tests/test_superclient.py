import unittest
import logging

from application.models.client import Client
from application.models.superclient import SuperClient



class SuperClientTests(unittest.TestCase):

    #Test de création d'instance.

    def test_creation_instance(self):
        super_client = SuperClient(role="SuperClient", identifiant="client123", password_hash="hashed_password", salt="salt",
                               nom="Poe", prenom="Mickael", email="mickaelpoe@example.com", date_naissance="1990-01-01",
                               genre="Masculin")
        self.assertEqual(super_client.role, "SuperClient")
        self.assertEqual(super_client.identifiant, "client123")
        self.assertEqual(super_client.password_hash, "hashed_password")
        self.assertEqual(super_client.salt, "salt")
        self.assertEqual(super_client.nom, "Poe")
        self.assertEqual(super_client.prenom, "Mickael")
        self.assertEqual(super_client.email, "mickaelpoe@example.com")
        self.assertEqual(super_client.date_naissance, "1990-01-01")
        self.assertEqual(super_client.genre, "Masculin")

    # Test des méthodes héritées de la classe Client.
    def test_methodes_heritees(self):
        super_client = SuperClient(role="SuperClient", identifiant="client123", password_hash="hashed_password", salt="salt",
                               nom="Poe", prenom="Mickael", email="mickaelpoe@example.com", date_naissance="1990-01-01",
                               genre="Masculin")

        self.assertTrue(super_client.is_authorized("SuperClient"))
        self.assertTrue(super_client.is_active())
        self.assertFalse(super_client.is_anonymous())
        self.assertEqual(super_client.get_id(), str(super_client.id))
        self.assertTrue(super_client.has_role("SuperClient"))





    # Test des attributs spécifiques à SuperClient.
    def test_attributs_specifiques(self):
        super_client = SuperClient(role="SuperClient", identifiant="client123", password_hash="hashed_password", salt="salt",
                               nom="Poe", prenom="Mickael", email="mickaelpoe@example.com", date_naissance="1990-01-01",
                               genre="Masculin")
        self.assertEqual(super_client.role, "SuperClient")
        self.assertEqual(super_client.identifiant, "client123")
        self.assertEqual(super_client.password_hash, "hashed_password")
        self.assertEqual(super_client.salt, "salt")


    # Test des relations avec d'autres modèles.
    def test_relations(self):
        super_client = SuperClient(role="SuperClient", identifiant="client123", password_hash="hashed_password", salt="salt",
                               nom="Poe", prenom="Mickael", email="mickaelpoe@example.com", date_naissance="1990-01-01",
                               genre="Masculin")
        client = Client(nom="Jane", prenom="Doe", email="jane.doe@example.com", date_naissance="1995-05-05", genre="F")

        super_client.client = client

        self.assertEqual(super_client.client, client)
        self.assertEqual(client.superclient, super_client)

if __name__ == '__main__':
    unittest.main()