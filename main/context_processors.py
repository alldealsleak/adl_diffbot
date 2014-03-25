from .models import Company


def get_companies(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return context