def add_user_role(request):
    return {'user_role': request.user.role.role_name if request.user.is_authenticated else None}