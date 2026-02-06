import json
from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator
from .models import Student


class StudentAPI(View):

    def get(self, request):
        students = Student.objects.all().order_by('serial_no')

        page_number = request.GET.get('page', 1)
        paginator = Paginator(students, 5)
        page_obj = paginator.get_page(page_number)

        data = list(page_obj.object_list.values("id", "serial_no", "name", "age", "course"))

        return JsonResponse({
            "students": data,
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "page_size": paginator.per_page
        }, status=200)


    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data.get("name")
            age = data.get("age")
            course = data.get("course")

            if not name or not age or not course:
                return JsonResponse({"error": "All fields required"}, status=400)

            student = Student.create_student(name.strip(), int(age), course.strip())

            return JsonResponse({"message": "Student created", "id": student.id}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

   
    def put(self, request, id=None):
        try:
            if not id:
                return JsonResponse({"error": "Student ID required"}, status=400)

            data = json.loads(request.body)
            name = data.get("name")
            age = data.get("age")
            course = data.get("course")

            if not name or not age or not course:
                return JsonResponse({"error": "All fields required"}, status=400)

            student = Student.objects.get(id=id)
            student.update_student(name.strip(), int(age), course.strip())

            return JsonResponse({"message": "Student updated"}, status=200)

        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

   
    def delete(self, request, id=None):
        try:
            if not id:
                return JsonResponse({"error": "Student ID required"}, status=400)

            student = Student.objects.get(id=id)
            student.delete_student()

            Student.reorder_serials()  

            return JsonResponse({"message": "Student deleted"}, status=200)

        except Student.DoesNotExist:
            return JsonResponse({"error": "Student not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)