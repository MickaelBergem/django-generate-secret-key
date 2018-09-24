from django.core.management.base import BaseCommand
import os
import string


class Command(BaseCommand):
    """
    Generate a Django secret key in `secretkey.txt` if none exists
    """
    args = 'secretkey.txt'
    help = 'Generate a Django secret key'
    can_import_settings = False
    leave_locale_alone = True

    # Where to create the key if no parameter is given
    # This will be monkey-patched when runnning the tests
    BASE_DIR = os.getcwd()

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace',
            action='store_true',
            dest='replace',
            default=False,
            help='Replace the existing key'
        )
        parser.add_argument(
            'filename',
            default='secretkey.txt',
            nargs='?',
            help='Secret file name'
        )

    def handle(self, *args, **options):

        if len(args) > 1:
            self.stderr.write("Please provide only one file name (or none).")
            return

        key_filepath = os.path.join(self.BASE_DIR, options['filename'])

        try:
            existing_key = open(key_filepath).read().strip()
            # Key not empty ?
            if existing_key and not options['replace']:
                self.stderr.write("There is already a secret key in `{}`".format(key_filename))
                return
        except IOError:
            # No key found
            pass

        import random
        generated_key = ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation)
                                 for _ in range(50)])
        secret = open(key_filepath, 'w')
        secret.write(generated_key)
        secret.close()
