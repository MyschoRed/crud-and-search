from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q

from .models import Student


def index(request):
    students = Student.objects.all()
    query = ''

    if request.method == 'POST':
        if 'add' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            Student.objects.create(name=name, email=email)
            messages.success(request, "Student added successfully")

        elif 'update' in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            email = request.POST.get('email')

            update_student = Student.objects.get(id=id)
            update_student.name = name
            update_student.email = email
            update_student.save()

            messages.success(request, 'Student updated successfully')

        elif 'delete' in request.POST:
            id = request.POST.get('id')
            Student.objects.get(id=id).delete()

            messages.success(request, 'Student deleted successfully')

        elif 'search' in request.POST:
            if request.POST.get('searchqueryname'):
                query = request.POST.get('searchqueryname')
                students = Student.objects.filter(Q(name__icontains=query))
                # students = Student.objects.filter(Q(name__icontains=query) | Q(email__icontains=query))  # for fulltext search
            elif request.POST.get('searchqueryemail'):
                query = request.POST.get('searchqueryemail')
                students = Student.objects.filter(Q(email__icontains=query))


    ctx = {
        'students': students,
        'query': query
    }
    return render(request, 'index.html', ctx)

# Class Based View alternative
# from django.views.generic import TemplateView
# class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        students = Student.objects.all()
        query = ''
        context['students'] = students
        context['query'] = query
        return context

    def post(self, request, *args, **kwargs):
        students = Student.objects.all()
        query = ''

        if 'add' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            Student.objects.create(name=name, email=email)
            messages.success(request, "Študent úspešne pridaný")

        elif 'update' in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            email = request.POST.get('email')

            update_student = Student.objects.get(id=id)
            update_student.name = name
            update_student.email = email
            update_student.save()

            messages.success(request, 'Študent úspešne aktualizovaný')

        elif 'delete' in request.POST:
            id = request.POST.get('id')
            Student.objects.get(id=id).delete()

            messages.success(request, 'Študent úspešne vymazaný')

        elif 'search' in request.POST:
            if request.POST.get('searchqueryname'):
                query = request.POST.get('searchqueryname')
                students = Student.objects.filter(Q(name__icontains=query))
            elif request.POST.get('searchqueryemail'):
                query = request.POST.get('searchqueryemail')
                students = Student.objects.filter(Q(email__icontains=query))

        context = {
            'students': students,
            'query': query
        }
        return self.render_to_response(context)