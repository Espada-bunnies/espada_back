from rest_framework.exceptions import ValidationError


class BodyValidator:
    def __call__(self, value):
        words = list(self.get_all_badwords())
        for word in words:
            if word in value:
                raise ValidationError("Текст содержит нецензурные слова")

    @staticmethod
    def get_all_badwords():
        with open(
            "./words.txt", "r", encoding="utf-8"
        ) as file:
            return map(lambda row: row.rstrip("\n"), file.readlines())


class ImagesValidator:
    def __call__(self, value):
        if len(value) > 5:
            raise ValidationError("За один раз можно отправлять не больше 5 картинок")
