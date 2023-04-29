from rest_framework.exceptions import ValidationError


class CommentBodyValidator:

    def __call__(self, value):
        words = list(self.get_all_badwords())
        for word in words:
            if word in value:
                raise ValidationError('Ваш комментарий содержит нецензурные слова')

    @staticmethod
    def get_all_badwords():
        with open('comments/words.txt', 'r', encoding='utf-8') as file:
            return map(lambda row: row.rstrip('\n'), file.readlines())


class CommentImagesValidator:

    def __call__(self, value):
        if len(value) > 5:
            raise ValidationError('За один раз можно отправлять не больше 5 картинок')


