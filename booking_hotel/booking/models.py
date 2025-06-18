from django.db import models

# Create your models here.
class Room(models.Model):   # Модель комнаты
    description = models.TextField()    # Описание комнаты
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)  # Цены за ночь max_digits - всего можно записать до 10 цифр в числе, decimal_places- это сколько цифр после запятой
    added_at = models.DateTimeField(auto_now_add=True)  #Автодобавление даты создания


class Booking(models.Model):
    room = models.ForeignKey(   #ForeignKey-связь один ко многим(то есть создаю ссылку на другую таблицу(модель) в бд)
        Room,   # На какую модель(таблицу) ссылаемся
        on_delete=models.CASCADE,   # Нужно если комнату удалят, то и удалятся все связанные бронирования
        related_name='bookings'    # Позвонляет из комнаты(Room) получить все её бронирования
    )
    date_start = models.DateField() # Дата начала бронирования
    date_end = models.DateField()   # Дата окончания бронирования

    class Meta:
        ordering = ['date_start']   # Сортировка бронирования по date_start
