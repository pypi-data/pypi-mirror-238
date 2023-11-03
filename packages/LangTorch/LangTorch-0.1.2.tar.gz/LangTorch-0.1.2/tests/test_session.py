import unittest
import sys
sys.path.append("../src")

from langtorch.session import Session

import os
import asyncio
import random
from omegaconf import OmegaConf
from langtorch import TextTensor
import logging

# logging.basicConfig(level=logging.DEBUG)


class TestSession(unittest.TestCase):

    def setUp(self):
        # Create a sample config file for testing
        self.config_path = "test_config.yaml"
        self.config_path2 = "test_config2.yaml"
        OmegaConf.save(OmegaConf.create({"key1": "initial_value"}), self.config_path)
        Session(self.config_path)
        OmegaConf.save(OmegaConf.create({"k": "v"}), self.config_path2)
        Session(self.config_path2)

    def test_syn_async_set_get(self):
        async def async_worker(worker_id):
            logging.debug(f"Worker {worker_id} started.")
            async with Session(self.config_path) as session:
                value = f"async_value_{random.randint(1, 1000)}"
                setattr(session,f"key_{value}",value)
                # await asyncio.sleep(random.uniform(0, 1))  # Sleep for a random time between 0 and 1 seconds
                self.assertEqual(getattr(session, f"key_{value}"), value)
            logging.debug(f"Worker {worker_id} finished.")

        with Session(self.config_path) as session:
            session.key1 = "sync_value"
            self.assertEqual(session.key1, "sync_value")
            passed = False
            try:
                # These async workers should raise RuntimeError
                loop = asyncio.get_event_loop()
                tasks = [loop.create_task(async_worker(i)) for i in range(10)]
                loop.run_until_complete(asyncio.gather(*tasks))
                loop.close()
            except RuntimeError:
                passed = True

            self.assertTrue(passed)
            # These async workers should not raise RuntimeError
            session.close()
            loop = asyncio.get_event_loop()
            tasks = [loop.create_task(async_worker(i)) for i in range(10)]
            loop.run_until_complete(asyncio.gather(*tasks))
            session.open()

        # Running multiple async workers in parallel
        loop = asyncio.get_event_loop()
        tasks = [loop.create_task(async_worker(i)) for i in range(10)]
        loop.run_until_complete(asyncio.gather(*tasks))


        with Session(self.config_path) as session:
            session.key1 = "sync_value"
            self.assertEqual(session.key1, "sync_value")

        # Confirm the value is saved in the file
        config = OmegaConf.load(self.config_path)
        self.assertEqual(config.key1, "sync_value")

    def test_tensor_set_get(self):
        with Session(self.config_path2) as session:
            session.key1 = TextTensor("sync_value")
            self.assertEqual(session.key1, TextTensor("sync_value"))

    def tearDown(self):
        # Cleanup: remove the test config file after each test
        os.remove(self.config_path)
        os.remove(self.config_path2)


if __name__ == '__main__':
    unittest.main()
