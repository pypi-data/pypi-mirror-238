from wallaroo.logs import LogEntry, LogEntries
import json
import unittest


class TestLogEntries(unittest.TestCase):
    def setUp(self):
        with open("unit_tests/outputs/ccfraud_output.json", "r") as fp:
            self.ccfraud_output = json.loads(fp.read())
        with open("unit_tests/outputs/lazyadam_output.json", "r") as fp:
            self.lazyadam_output = json.loads(fp.read())
        with open("unit_tests/outputs/some_output.json", "r") as fp:
            self.some_output = json.loads(fp.read())
        with open("unit_tests/outputs/pipeline_output.json", "r") as fp:
            self.pipeline_output = json.loads(fp.read())

    def test_pipeline_row(self):
        entry = LogEntry(self.pipeline_output)
        self.assertEqual(entry.elapsed, 688600)
        self.assertEqual(entry.model_name, "noop-py")
        self.assertEqual(entry.model_version, "c4915677-b6d4-4ea1-82a0-05c6d0171cd4")
        self.assertAlmostEqual(entry.output[0][0][0], 1.23)

    def test_default_tensor(self):
        entry = LogEntry(self.ccfraud_output)
        self.assertEqual(entry.model_version, "2021-05-01")
        self.assertEqual(entry.model_name, "ccfraud")
        self.assertEqual(len(entry.input[0]), 29)
        self.assertAlmostEqual(entry.output[0][0][0], 0.00149741768)

    def test_nondefault_tensor(self):
        entry = LogEntry(self.lazyadam_output)
        self.assertEqual(entry.model_version, "version")
        self.assertEqual(entry.model_name, "lazyadam")
        self.assertEqual(len(entry.input[0]), 784)
        self.assertAlmostEqual(entry.output[0][0][0], 0.1137351095676)

    def test_multiple_inputs(self):
        # We don't support this case yet but some models we've seen have it

        entry = LogEntry(self.some_output)
        self.assertEqual(entry.model_version, "xx1")
        self.assertEqual(entry.model_name, "foo")
        self.assertEqual(len(entry.input), 3)
        self.assertEqual(len(entry.input["tensor_1"][0]), 4)
        self.assertEqual(len(entry.input["tensor_2"][0]), 3)
        self.assertEqual(len(entry.input["tensor_3"][0]), 2)
        self.assertAlmostEqual(entry.output[0][0][0], 0.00149741768)

    def test_log_entries(self):
        # Just make sure it creates a string
        entries = LogEntries(
            [
                LogEntry(self.ccfraud_output),
                LogEntry(self.lazyadam_output),
                LogEntry(self.some_output),
            ]
        )
        self.assertIsNotNone(entries)

        # Random blob of html without sploding
        html = entries._repr_html_()
        print(html)
        self.assertTrue(len(html) > 5000)
