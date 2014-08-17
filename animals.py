class Animal(object):

    def __init__(self, health=10, skill=10, weapon=None):
        self.health = health
        self.skill = skill
        self.is_alive = True
        self.weapon = weapon

    def attack(self, target):
        pass
        # if self.weapon is not None:
        #     self.weapon.attack(target)

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
        if self.weapon is not None:
            self.weapon.attack(target)
        self.eat(target)


class Weapon(object):
    pass


class LaserMixin(Weapon):

    def shoot(self, target):
        damage = self.calculate_damage(target)
        target.receive_hit(damage)

    def calculate_damage(self, target):
        # Expects to be mixed in to a class with `skill`
        skill_modifier = 1 + (0.1 * self.skill)
        return 5 * skill_modifier


class Laser(LaserMixin):

    # Temporary hack to get at owner's skill
    @property
    def skill(self):
        return self.owner.skill

    def attack(self, target):
        self.shoot(target)


def SharkWithLasers(*args, **kwargs):
    # TODO remove this factory
    shark = Shark(*args, **kwargs)
    shark.weapon = Laser()
    shark.weapon.owner = shark  # TODO remove


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

    # Another approach to refactoring:
    # Haven't rewritten Nunchucks yet, instead override attack().

    def attack(self, target):
        NunchuckMixin.hit(self, target)
        Shark.attack(self, target)


class OrcaWithLasers(LaserMixin, Orca):
    pass


class ArmorProxy(object):

    armor_health = 10

    def __init__(self, wearer):
        self.wearer = wearer

    def receive_hit(self, damage):
        """
        Absorb some damage before passing any on to self.health.
        """
        self.armor_health -= damage
        if self.armor_health < 0:
            self.wearer.receive_hit(-self.armor_health)
            self.armor_health = 0

    def __getattr__(self, name):
        return getattr(self.wearer, name)
