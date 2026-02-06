from django.db import models

class Student(models.Model):
    serial_no = models.IntegerField(unique=True, editable=False)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    course = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.serial_no:
            last = Student.objects.order_by('-serial_no').first()
            self.serial_no = 1 if not last else last.serial_no + 1
        super().save(*args, **kwargs)

    @classmethod
    def create_student(cls, name, age, course):
        return cls.objects.create(name=name, age=age, course=course)

    def update_student(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course
        self.save()

    def delete_student(self):
        self.delete()

    @classmethod
    def reorder_serials(cls):
        students = cls.objects.order_by('id')
        for index, student in enumerate(students, start=1):
            student.serial_no = index
            student.save(update_fields=["serial_no"])

    def __str__(self):
        return self.name