import os
import datetime


def logger(path):


  def _logger(old_function):
    def new_function(*args, **kwargs):
      data = f'''Дата и время: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\nФункция {old_function.__name__}:\n'''
      with open(path,'a') as f:
        if args and kwargs:
          data += f'Параметры функции:\n args = {args}\n kwargs = {kwargs.values()}\n'
        elif args:
          data += f'Параметры: {args}\n'
        elif kwargs:
          data += f'Параметры: {kwargs}\n'
        else:
          data += 'Функция без параметров\n'
        data += f'Результат функции: {old_function(*args, **kwargs)}\n\n'
        f.write(data)
      return old_function(*args, **kwargs)
    return new_function
  return _logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()