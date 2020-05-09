def merchant(user):
    if user.is_anonymous:
        return False
    return user.profile.is_student or merchant()



def manager(user):
        if user.is_anonymous:
            return False
        return user.profile.is_manager or user.is_superuser