# A more based base user for Django.

`django-based-user` provides a clean minimal starting point for custom Django user models.

## Why?

The Django authentication scheme provides for pluggable user models, and provides both an `AbstractUser` as well as a fairly vanilla `User` model.

The problem with these classes provided by the framework is that they are still too opinionated for my liking.

The primary issue is that the base implementation includes both a `username` and `email` field, and the `username` is required. For many projects, it makes sense to use the email address as the username. The base user model shipped with Django allows you to use `email` as the *login* field, but the `username` is still required. (Thumbs down.)

The secondary issue is that the base user model includes `first_name` and `last_name` fields. These fields are not required, so this is not a major issue, but it is annoying. You may want to use just a single `name` field, or you might choose to store the user's name in a separate `Profile` model or something like that. Or, you might choose to not even collect user's real names at all. The point is, I think that should be up to you.

See also: [Falsehoods Programmers Believe About Names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/)

The base user class provided by this package requires only an `email` and `password`, and then a few fields required for compatibility with the Django auth and admin packages, such as `is_staff`, `is_superuser`, `groups`, etc.

## B.Y.O.U. (Bring your own user)

This package only provides an abstract base class for a custom user model, and an associated model manager class.

Because Django makes it so easy to start with a custom user model, and so painful to switch to one later on, I think that a custom user model class is a clear example of PAGNI (Probably Are Gonna Need It). For that reason, this package does not provide a concrete user model. You have to inherit the base class into your own custom model, but it can be as simple as this:

    from based_user.models import BasedUser
    
    class User(BasedUser):
        pass
        
        
## Based?

The name is a joke, not a political statement. Wordplay makes me smile. All is well.
