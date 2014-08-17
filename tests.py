import animals
import unittest


class TestAnimal(unittest.TestCase):

    def test_receive_hit(self):
        animal = animals.Animal()
        animal.receive_hit(1)
        self.assertTrue(animal.is_alive)
        animal.receive_hit(8)
        self.assertTrue(animal.is_alive)
        animal.receive_hit(1)
        self.assertFalse(animal.is_alive)

    def test_die(self):
        animal = animals.Animal()
        self.assertTrue(animal.is_alive)
        animal.die()
        self.assertFalse(animal.is_alive)

    def test_attack(self):
        animal = animals.Animal()
        target = animals.Animal(99)
        animal.attack(target)
        self.assertEqual(target.health, 99)


class TestShark(unittest.TestCase):

    def test_eat(self):
        shark = animals.Shark()
        animal = animals.Animal(100)
        shark.eat(animal)
        self.assertEqual(animal.health, 95)

    def test_attack(self):
        shark = animals.Shark()
        animal = animals.Animal(100)
        shark.attack(animal)
        self.assertEqual(animal.health, 95)


class TestOrca(unittest.TestCase):

    def test_eat(self):
        orca = animals.Orca()
        animal = animals.Animal(100)
        orca.eat(animal)
        self.assertEqual(animal.health, 90)

    def test_attack(self):
        orca = animals.Orca()
        animal = animals.Animal(100)
        orca.attack(animal)
        self.assertEqual(animal.health, 90)


class TestSharkWithLasers(unittest.TestCase):

    def test_attack(self):
        animal = animals.Animal(100)
        shark = animals.SharkWithLasers()
        shark.attack(animal)
        self.assertEqual(animal.health, 85.0)


class TestOrcaWithNunchucks(unittest.TestCase):

    def test_attack(self):
        animal = animals.Animal(100)
        orca = animals.OrcaWithNunchucks()
        orca.attack(animal)
        self.assertEqual(animal.health, 88)


class TestArmorProxy(unittest.TestCase):

    def test_receive_hit(self):
        inner = animals.Shark(health=10)
        shark = animals.ArmorProxy(wearer=inner)

        shark.receive_hit(9)
        self.assertEqual(shark.health, inner.health, 10)
        self.assertEqual(shark.armor_health, 1)

        shark.receive_hit(1)
        self.assertEqual(shark.health, inner.health, 10)
        self.assertEqual(shark.armor_health, 0)

        shark.receive_hit(1)
        self.assertEqual(shark.health, inner.health, 9)
        self.assertEqual(shark.armor_health, 0)

        shark.receive_hit(9)
        self.assertEqual(shark.health, inner.health, 0)
        self.assertEqual(shark.armor_health, 0)
        self.assertFalse(shark.is_alive)
        self.assertEqual(shark.is_alive, inner.is_alive)
