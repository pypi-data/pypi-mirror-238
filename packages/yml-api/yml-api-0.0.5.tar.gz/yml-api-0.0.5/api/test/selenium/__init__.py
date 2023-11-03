# -*- coding: utf-8 -*-
import os
import json
import warnings
from django.apps import apps
from django.db import connection
from django.conf import settings
from django.core.management import call_command
from django.contrib.staticfiles.testing import LiveServerTestCase
from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.contrib.auth.models import User
from django.core.cache import cache
from .browser import Browser
from subprocess import DEVNULL, check_call
from django.core.servers.basehttp import WSGIServer
import os
import signal
from subprocess import Popen, PIPE


WSGIServer.handle_error = lambda *args, **kwargs: None


class ContextManager:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class TestStaticFilesHandler(StaticFilesHandler):
    def _middleware_chain(self, request):
        from django.http import HttpResponse
        return HttpResponse()


# StaticLiveServerTestCase
class SeleniumTestCase(LiveServerTestCase):

    FROM_STEP = None
    HEADLESS = True
    EXPLAIN = False
    RESTORE = None
    LOG_ACTION = False

    static_handler = TestStaticFilesHandler

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_count = 0
        self.current_username = None
        warnings.filterwarnings('ignore')

        self._url = '/app/dashboard/login/'
        self._execute = 1
        self._step = 0
        self._adverb = 0

    @classmethod
    def setUpClass(cls):
        cache.clear()
        super().setUpClass()
        cls.browser = Browser(cls.live_server_url, slowly=SeleniumTestCase.EXPLAIN, headless=SeleniumTestCase.HEADLESS)
        cls.browser.open('/')
        for app_label in settings.INSTALLED_APPS:
            app_module = __import__(app_label)
            app_dir = os.path.dirname(app_module.__file__)
            fixture_path = os.path.join(app_dir, 'fixtures', 'test.json')
            if os.path.exists(fixture_path):
                call_command('loaddata', fixture_path)
        settings.DEBUG = True

    def explain(self, action, text, *texts):
        if SeleniumTestCase.EXPLAIN:
            adverbs = 'e então', 'em seguida', 'na sequência', 'dando continuidade', 'dopois', 'logo', 'a seguir'
            if action == 'enter':
                phrases = f'preencha o campo {text}',
            elif action == 'choose':
                phrases = f'escolha uma opção para {text}',
            elif action == 'check':
                phrases = f'marque a opção {text}',
            elif action == 'check_radio':
                phrases = f'marque a opção {text}',
            elif action == 'see':
                phrases = f'veja o texto {text}',
            elif action == 'see_message':
                phrases = f'veja a mensagem {text}',
            elif action == 'look_at_popup_window':
                phrases = f'observe a janela interna',
            elif action == 'look_at':
                phrases = f'olhe para o texto {text}',
            elif action == 'look_at_panel':
                phrases = f'olhe para o painel {text}',
            elif action == 'click_menu':
                phrases = [f'clique no menu {text}']
                for text in texts:
                    phrases.append(text)
            elif action == 'search_menu':
                phrases = f'busque por {text}',
            elif action == 'click':
                phrases = f'clique em {text}',
            for phrase in phrases:
                adverb = adverbs[self._adverb]
                self._adverb = (self._adverb + 1) % len(adverbs)
                self.say('{}, {}'.format(adverb, phrase))

    def say(self, text):
        if SeleniumTestCase.EXPLAIN:
            os.system('say "{}"'.format(text))

    def create_superuser(self, username, password):
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, None, password)

    def wait(self, seconds=1):
        self.browser.wait(seconds)

    def open(self, url='/api/v1/login/'):
        if url == '/':
            self.say('acesse o sistema')
        self.browser.open(url)
        self._url = url

    def slow(self, slowly=False):
        self.browser.slow(slowly)

    def reload(self):
        self.browser.reload()

    def home(self):
        self.browser.open('/api/v1/dashboard/')

    def enter(self, name, value, submit=False, count=5):
        self.explain('enter', name)
        self.browser.enter(name, value, submit, count)

    def choose(self, name, value, count=5):
        self.explain('choose', name)
        self.browser.choose(name, value, count)

    def dont_see_error_message(self):
        self.browser.dont_see_error_message(self)

    def see(self, text, flag=True, count=5):
        self.explain('see', text)
        self.browser.see(text, flag, count)

    def see_message(self, text, count=10):
        self.explain('see_message', text)
        self.browser.see_message(text, count)

    def see_dialog(self, count=5):
        self.explain('look_at_popup_window', None)
        self.browser.see_dialog(count)
        return ContextManager()

    def look_at(self, text, count=5):
        self.explain('look_at', text)
        self.browser.look_at(text, count)
        return ContextManager()

    def search_menu(self, text):
        self.explain('search_menu', text)
        self.browser.search_menu(text)

    def click(self, text):
        self.explain('click', text)
        self.browser.click(text)

    def click_cell(self, i, j):
        self.browser.click_cell(i, j)

    def check_cell(self, i, j):
        self.wait(0.5)
        self.browser.check_cell(i, j)
        self.wait(0.5)

    def submit_form(self, wait=False):
        self.click('Enviar')
        if 0 and wait:
            self.wait_form()

    def wait_form(self):
        self.browser.wait_start()
        self.browser.wait_finish()
        self.wait()

    def step(self, description=None):
        if self._step > 1 and self._execute:
            self.save()
        if SeleniumTestCase.RESTORE and self.step_file_exists(SeleniumTestCase.RESTORE) and self._execute:
            print('Creating development database from existing step {}'.format(SeleniumTestCase.RESTORE))
            self.create_dev_database(self.step_file_exists(SeleniumTestCase.RESTORE))
            self._execute = 0
            return False
        self._step += 1
        if SeleniumTestCase.FROM_STEP:
            if self._step == SeleniumTestCase.FROM_STEP:
                self.load(self._step)
                self._execute = 2
                return False
            else:
                self._execute = 2 if self._execute > 1 else 0

        if self._execute:
            description = 'Executando passo {}{}'.format(self._step, ' ({})'.format(description) if description else '')
            if SeleniumTestCase.EXPLAIN:
                self.say(description)
            else:
                print(description)
        return self._execute

    def login(self, username, password):
        self.current_username = username
        if '/login/' not in self.browser.current_url and '/token/' not in self.browser.current_url:
            self.open('/api/v1/login/')
        self.enter('Nome do usuário', username)
        self.enter('Senha', password)
        self.submit_form()
        self.wait()

    def logout(self):
        self.browser.logout(self.current_username)
        self.current_username = None

    def tearDown(self):
        self.save()
        if SeleniumTestCase.LOG_ACTION:
            SeleniumTestCase.LOG_ACTION = 2
            self.reload()
            input('Logging the actions in the terminal. Type any key to exit!\n\n')
        return super().tearDown()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.browser.close()
        cls.browser.quit()
        cls.browser.service.stop()

    def postgres_parameters(self):
        dbhost = settings.DATABASES['default']['HOST']
        dbuser = settings.DATABASES['default']['USER']
        dbport = settings.DATABASES['default']['PORT']
        dbparam = '-U {} -h {} -p {}'.format(dbuser, dbhost, dbport)
        return dbparam

    def create_dev_database(self, fname=None):
        dbname = settings.DATABASES['default']['NAME']
        if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
            if os.path.exists('db.sqlite3'):
                os.unlink('db.sqlite3')
            os.system('sqlite3 db.sqlite3 "VACUUM;"')
            if fname:
                os.system('cat {} | sqlite3 db.sqlite3'.format(fname, dbname))
            else:
                os.system('sqlite3 {} ".dump" | sqlite3 db.sqlite3'.format(dbname))
        elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
            dbparam = self.postgres_parameters()
            dbname2 = dbname[5:]
            os.system('dropdb {} --if-exists {}'.format(dbparam, dbname2))
            os.system('createdb {} {}'.format(dbparam, dbname2))
            if fname:
                os.system('pg_dump {} --schema-only -d {} | psql {} -q -d {} > /dev/null'.format(dbparam, dbname, dbparam, dbname2))
                os.system('cat {} | psql {} -q -d {} > /dev/null'.format(fname, dbparam, dbname2))
            else:
                os.system('pg_dump {} -d {} | psql {} -q -d {} > /dev/null'.format(dbparam, dbname, dbparam, dbname2))

    def save(self):
        if SeleniumTestCase.RESTORE == self._step:
            print('Creating development database from step {}'.format(self._step))
            self.create_dev_database()
            self._execute = 0
        if self._execute:
            print('Saving step {}'.format(self._step))
            os.makedirs('.steps', exist_ok=True)
            dbname = settings.DATABASES['default']['NAME']
            fname = '{}.sql'.format(os.path.join('.steps', str(self._step)))
            if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
                cmd = 'sqlite3 {} ".dump" > {}'.format(dbname, fname)
                if 'memory' not in cmd:
                    os.system(cmd)
            elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
                cmd = 'pg_dump {} -d {} --inserts --data-only --no-owner -f {}'.format(
                    self.postgres_parameters(), dbname, fname
                )
                check_call(cmd.split(), stdout=DEVNULL, stderr=DEVNULL)

    def step_file_exists(self, step):
        fname = '{}.sql'.format(os.path.join('.steps', str(step)))
        return fname if os.path.exists(fname) else False

    def load(self, step):
        fname = '{}.sql'.format(os.path.join('.steps', str(self._step)))
        print('Loading step {}'.format(step))
        dbname = settings.DATABASES['default']['NAME']
        if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
            cmd = 'sqlite3 {} "PRAGMA writable_schema = 1;delete from sqlite_master where type in (\'table\', \'index\', \'trigger\');PRAGMA writable_schema = 0;VACUUM;PRAGMA integrity_check;"'.format(dbname)
            os.system(cmd)
            cmd = 'cat {} | sqlite3 {}'.format(fname, dbname)
            os.system(cmd)
        else:
            cursor = connection.cursor()
            tables = [m._meta.db_table for c in apps.get_app_configs() for m in c.get_models()]
            for table in tables:
                cursor.execute('truncate table {} cascade;'.format(table))
            cmd = 'psql {} -d {} --file={}'.format(self.postgres_parameters(), dbname, fname)
            check_call(cmd.split(), stdout=DEVNULL, stderr=DEVNULL)

    def loaddata(self, fixture_path):
        call_command('loaddata', '--skip-checks', fixture_path)
