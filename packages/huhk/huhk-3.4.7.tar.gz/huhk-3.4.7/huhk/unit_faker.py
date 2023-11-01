from faker import Faker


class MyFaker(Faker):
    def __init__(self):
        super().__init__(locale='zh_CN')
        self.model = "自动化测试"

    def phone(self):
        return self.phone_number()

    def mobile(self):
        return self.phone_number()

    def str(self):
        return self.model + self.word()

    def string(self):
        return self.model + self.word() + self.numerify()

    def int(self, *args, **kwargs):
        return self.random_int(*args, **kwargs)

    def int2(self, min=1, max=99):
        return self.random_int(min, max)

    def int3(self, min=1, max=999):
        return self.random_int(min, max)


if __name__ == '__main__':
    out = MyFaker().int(1, 8)
    print(out)

