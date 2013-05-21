'''Tests the rpc middleware and utilities. It uses the calculator example.'''
from pulsar import Config, get_actor
from pulsar.apps import MultiApp
from pulsar.apps.wsgi import WSGIServer
from pulsar.apps.tasks import TaskQueue
from pulsar.apps.test import unittest, run_on_arbiter


def dummy(environ, start_response):
    start_response('200 OK', [])
    yield [b'dummy']
    
class MultiWsgi(MultiApp):
    cfg = Config(bind=':0', rpc_bind=':0', bla='foo')
    
    def build(self):
        yield self.new_app(WSGIServer, callable=dummy)
        yield self.new_app(WSGIServer, 'rpc', callable=dummy)
    

class TestMultiApp(unittest.TestCase):
    
    def create(self, **params):
        # create the application
        return MultiWsgi(**params)
    
    def testApp(self):
        app = self.create()
        self.assertTrue(app)
        apps = app.apps()
        self.assertEqual(len(apps), 2)
        
    def testConfig(self):
        app = self.create(bind=':9999', unz='whatz')
        self.assertTrue(app)
        self.assertEqual(len(app.cfg.params), 4)
        apps = app.apps()
        self.assertEqual(len(app.cfg.params), 2)
        self.assertEqual(app.cfg.bla, 'foo')
        self.assertEqual(app.cfg.unz, 'whatz')
        self.assertEqual(app.cfg.bind, ':9999')
        
    def testBacklog(self):
        app = self.create(backlog=22, name='pippo')
        self.assertEqual(app.name, 'pippo')
        self.assertEqual(app.cfg.backlog, 22)
        apps = app.apps()
        self.assertEqual(app.cfg.backlog, 22)
        self.assertNotEqual(app.cfg.rpc_backlog, 22)
        app1 = apps[0]
        self.assertEqual(app1.name, 'pippo')
        self.assertEqual(app1.cfg.backlog, 22)
        app2 = apps[1]
        self.assertEqual(app2.name, 'rpc_pippo')
        self.assertNotEqual(app2.cfg.backlog, 22)
        self.assertEqual(app2.cfg.backlog,
                         app2.cfg.settings['backlog'].default)
        
    def testName(self):
        app = self.create()
        self.assertEqual(app.name, 'multiwsgi')
        app = self.create(name='bla')
        self.assertEqual(app.name, 'bla')
        apps = app.apps()
        self.assertEqual(apps[0].name, 'bla')
        self.assertEqual(apps[1].name, 'rpc_bla')
        
    @run_on_arbiter
    def testInstall(self):
        arbiter = get_actor()
        app = self.create(name='pluto')
        self.assertTrue(app)
        self.assertFalse(arbiter.get_actor('pluto'))
        self.assertFalse(arbiter.get_actor('rpc_pluto'))
        # create the application
        app.start()
        monitor1 = arbiter.get_actor('pluto')
        self.assertTrue(monitor1)
        self.assertTrue(monitor1.is_monitor())
        monitor2 = arbiter.get_actor('rpc_pluto')
        self.assertTrue(monitor2)
        self.assertTrue(monitor2.is_monitor())
        yield monitor1.stop()
        yield monitor2.stop()
        yield None
        
    def test_config_copy(self):
        app = self.create()
        self.assertTrue(app)
        apps = app.apps()
        rpc = apps[1]
        cfg = rpc.cfg.copy()
        self.assertEqual(cfg.prefix, rpc.cfg.prefix)
        for name in cfg:
            self.assertTrue(name in rpc.cfg)
        