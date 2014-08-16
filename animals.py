class Animal(object):

    def __init__(self, health=10):
        self.health = health
        self.is_alive = True

    def attack(self, target):
        pass

    def receive_hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.health = 0
        self.is_alive = False


class Died(Exception):
    pass


class Shark(Animal):

    def eat(self, target):
        target.receive_hit(damage=5)

    def attack(self, target):
        self.eat(target)


class Weapon(object):
    pass


class LaserMixin(Weapon):

    def shoot(self, target):
        target.receive_hit(5)


class SharkWithLasers(LaserMixin, Shark):

    def attack(self, target):
        self.shoot(target)
        self.eat(target)


class Orca(Animal):

    def eat(self, target):
        target.receive_hit(damage=10)

    def attack(self, target):
        self.eat(target)


class NunchuckMixin(Weapon):

    def hit(self, target):
        target.receive_hit(damage=2)


class OrcaWithNunchucks(NunchuckMixin, Orca):

    def attack(self, target):
        self.hit(target)
        self.eat(target)


class SharkWithNunchucks(NunchuckMixin, Shark):
    pass


class OrcaWithLasers(LaserMixin, Orca):
    pass


class ArmorMixin(object):

    armor_health = 10

    def receive_hit(self, damage):
        """
        Absorb some damage before passing any on to self.health.
        """
        self.armor_health -= damage
        if self.armor_health < 0:
            super(ArmorMixin, self).receive_hit(-self.armor_health)
            self.armor_health = 0


class ArmoredSharkWithLasers(ArmorMixin, SharkWithLasers):
    pass


class ArmoredSharkWithNunchucks(ArmorMixin, SharkWithNunchucks):
    pass


class ArmoredOrcaWithLasers(ArmorMixin, OrcaWithLasers):
    pass


class ArmoredOrcaWithNunchucks(ArmorMixin, OrcaWithNunchucks):
    pass
