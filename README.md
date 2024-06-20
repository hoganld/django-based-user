# A more *based* base user for Django.

`django-based-user` provides a clean minimal starting point for custom Django user models.

## Why?

The Django authentication scheme provides for pluggable user models, and provides both an `AbstractUser` as well as a fairly vanilla `User` model.

The problem with these classes provided by the framework is that they are still too opinionated for my liking.

The primary issue is that the base implementation includes both a `username` and `email` field, and the `username` is required. For many projects, it makes sense to use the email address as the username. The base user model shipped with Django allows you to use `email` as the *login* field, but the `username` is still required. (Thumbs down.)

The secondary issue is that the base user model includes `first_name` and `last_name` fields. These fields are not required, so this is not a major issue, but it is annoying. You may want to use just a single `name` field, or you might choose to store the user's name in a separate `Profile` model or something like that. Or, you might choose to not even collect user's real names at all. I think that should be up to you.

See also: [Falsehoods Programmers Believe About Names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/)

The base user class provided by this package requires only an `email` and `password`, and then a few fields required for compatibility with the Django auth and admin packages, such as `is_staff`, `is_superuser`, `groups`, etc.

## Requirements

- Python 3.9+
- Django 4.2+

`django-based-user` is a tiny package that, unfortunately, has to re-implement a few lines from `django.contrib.auth.models`. Take a look at `based_user.models` and you will see that this file started as a copy/paste of a couple of classes, and then removed a few fields and simplified a few methods accordingly.

The point is, this package follows the upstream code in `django.contrib.auth.models` closely, in order to provide a drop-in replacement for `django.contrib.auth.models.AbstractUser`. Current versions of Django will be supported, and unsupported/EOL versions will be officially unsupported. In reality, the relevant upstream code doesn't often change much, so other versions of Django will probably work just fine.

## Installation

No surprises here. Install from PyPI using `pip` or equivalent:

    pip install django-based-user
    
And that's it. No real need to add the package to `INSTALLED_APPS`, as there are no migrations or templates or static files to be collected.

## B.Y.O.U. (Bring your own user)

Because Django makes it so easy to start with a custom user model, and so painful to switch to one later on, I think that a custom user model class is a clear example of PAGNI (Probably Are Gonna Need It). For that reason, this package provides only an abstract base user class, and an associated model manager class. You have to inherit the base class into your own custom model, but it can be as simple as this:

    from based_user.models import BasedUser
    
    class User(BasedUser):
        pass
        
## License

Distributed under the MIT license. See `LICENSE` for more information.
        
## Contributing

The point of this package is to provide a minimal, unopinionated baseline for custom Django user model implementations. As such, the scope will remain necessarily constrained. Don't expect much to be added in terms of bells and whistles, as those tend to be opinionated. That said, bug fixes and other improvements are welcome. Follow the usual process:

1. [Fork the project](https://github.com/hoganld/django-based-user/fork)
2. Create your own feature branch (`git checkout -b feature/foobar`)
3. Commit you changes (`git commit -am "Add more foobar"`)
4. Push to the branch (`git push origin feature/foobar`)
5. Create a new Pull Request

## Code of Conduct

You have heard of the Golden Rule. Taleb's [Silver Rule](https://www.goodreads.com/book/show/36064445-skin-in-the-game) is more robust.

*"Do not treat others the way you would not like them to treat you."*

## Based?

The name is a joke. Wordplay makes me smile. All is well.
