import unittest

import redis

from kameleon.emulator.e32900t20d import E32900T20D

# need docker run -d --name redis -p 6379:6379 redis:latest to work

class TestE32900T20D(unittest.TestCase):
    def setUp(self) -> None:
        self._redis_A = redis.Redis("127.0.0.1", 6379)
        self._redis_B = redis.Redis("127.0.0.1", 6379)

        self.lora_A = E32900T20D(self._redis_A)
        self.lora_B = E32900T20D(self._redis_B)

    def test_send_recv(self):
        expected = b"hello"
        self.lora_A.send_frame(expected)

        result = self.lora_B.recv_frame()

        self.assertEqual(result, expected)

    def test_lenght(self):
        self.lora_A.send_frame(b"hello")

        expected = 5
        result = self.lora_B.recv_frame_length()

        self.assertEqual(result, expected)

    def test_send_recv_2(self):
        expected = [b"hello", b"bonjour"]
        for m in expected:
            self.lora_A.send_frame(m)

        result = [self.lora_B.recv_frame(), self.lora_B.recv_frame()]

        self.assertEqual(result, expected)