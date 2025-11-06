from django.db import models
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_all_lexers,get_lexer_by_name
from pygments.styles import get_all_styles

# Создание списка языков программирования
LEXERS = [item for item in get_all_lexers() if item[1]]
# Список выбора языка программирования
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# Создание списка выбора стиля подсветки
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    # Писать ли номера строк
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User',related_name='snippets', on_delete=models.CASCADE)
    # Html код для отображения его на отдельной странице.
    highlighted = models.TextField()

    # Переопределяем метод сохранения для генерации HTML с покрашеным примером кода.
    def save(self, *args, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        options = {'title': self.title } if self.title else {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        #Вызываем радительский метод сохранения в бд
        super(Snippet, self).save(*args, **kwargs)
    # Сортировка.
    class Meta:
        ordering = ['created']