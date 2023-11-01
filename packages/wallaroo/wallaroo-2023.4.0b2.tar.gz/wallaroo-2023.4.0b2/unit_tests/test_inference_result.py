import datetime
import json
import math
import pprint
import unittest

from wallaroo.inference_result import InferenceResult
from wallaroo.inference_decode import decode_inference_result
from . import testutil

import numpy  # type: ignore


class TestInferenceResult(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        # Truncate time to the millisecond
        self.now = self.now.replace(
            microsecond=math.floor(self.now.microsecond / 1000) * 1000
        )
        self.gql_client = testutil.new_gql_client(endpoint="http://api-lb/v1/graphql")

        with open("unit_tests/outputs/ccfraud_output.json", "r") as fp:
            self.ccfraud_output = json.loads(fp.read())
        with open("unit_tests/outputs/lazyadam_output.json", "r") as fp:
            self.lazyadam_output = json.loads(fp.read())
        with open("unit_tests/outputs/some_output.json", "r") as fp:
            self.some_output = json.loads(fp.read())
        with open("unit_tests/outputs/pipeline_output.json", "r") as fp:
            self.pipeline_output = json.loads(fp.read())
        with open("unit_tests/outputs/day5_output.json", "r") as fp:
            self.day5_output = json.loads(fp.read())

        self.timed_pipeline_response = {
            "model_name": "noop-py-post",
            "model_version": "65c791c9-e138-47ec-bcf2-6877336d4968",
            "pipeline_id": "noop-pipe65c791c9-e138-47ec-bcf2-6877336d4968",
            "outputs": [
                {
                    "Json": {
                        "v": 1,
                        "dim": [1],
                        "data": [
                            {
                                "tensor_fields": ["tensor"],
                                "tensor": {
                                    "outputs": [
                                        {
                                            "Float": {
                                                "v": 1,
                                                "dim": [1, 2],
                                                "data": [1.4, 2.5],
                                            }
                                        }
                                    ]
                                },
                            }
                        ],
                    }
                }
            ],
            "elapsed": [5, 467900],
            "time": int(self.now.timestamp() * 1000),
            "original_data": {"tensor": [[1.0, 2.0]]},
            "check_failures": [],
        }

    def test_without_gql_client(self):
        result = {
            "model_name": "kerasccfraud",
            "model_version": "21400ff8-0862-4c9f-a00d-41164fcabf1e",
            "pipeline_id": "a-b-test-c78dab93-02d6-4d42-92a5-01c1970f4319",
            "outputs": [{"Float": {"v": 1, "dim": [1, 1], "data": [0.1]}}],
            "elapsed": [0, 149902],
            "time": int(self.now.timestamp() * 1000),
            "original_data": {
                "tensor": [
                    [
                        1.0678324729342086,
                        0.21778102664937624,
                        -1.7115145261843976,
                        0.6822857209662413,
                        1.0138553066742804,
                        -0.43350000129006655,
                        0.7395859436561657,
                        -0.28828395953577357,
                        -0.44726268795990787,
                        0.5146124987725894,
                        0.3791316964287545,
                        0.5190619748123175,
                        -0.4904593221655364,
                        1.1656456468728569,
                        -0.9776307444180006,
                        -0.6322198962519854,
                        -0.6891477694494687,
                        0.17833178574255615,
                        0.1397992467197424,
                        -0.35542206494183326,
                        0.4394217876939808,
                        1.4588397511627804,
                        -0.3886829614721505,
                        0.4353492889350186,
                        1.7420053483337177,
                        -0.4434654615252943,
                        -0.15157478906219238,
                        -0.26684517248765616,
                        -1.454961775612449,
                    ]
                ]
            },
        }

        inference = InferenceResult(None, result)

        self.assertEqual(self.now, inference.timestamp())
        self.assertEqual(datetime.timedelta(microseconds=150), inference.time_elapsed())
        self.assertEqual(
            {
                "tensor": [
                    [
                        1.0678324729342086,
                        0.21778102664937624,
                        -1.7115145261843976,
                        0.6822857209662413,
                        1.0138553066742804,
                        -0.43350000129006655,
                        0.7395859436561657,
                        -0.28828395953577357,
                        -0.44726268795990787,
                        0.5146124987725894,
                        0.3791316964287545,
                        0.5190619748123175,
                        -0.4904593221655364,
                        1.1656456468728569,
                        -0.9776307444180006,
                        -0.6322198962519854,
                        -0.6891477694494687,
                        0.17833178574255615,
                        0.1397992467197424,
                        -0.35542206494183326,
                        0.4394217876939808,
                        1.4588397511627804,
                        -0.3886829614721505,
                        0.4353492889350186,
                        1.7420053483337177,
                        -0.4434654615252943,
                        -0.15157478906219238,
                        -0.26684517248765616,
                        -1.454961775612449,
                    ]
                ]
            },
            inference.input_data(),
        )
        self.assertEqual(repr(inference), f"InferenceResult({pprint.pformat(result)})")
        self.assertEqual(
            numpy.ndarray(shape=(1, 1), buffer=numpy.array([0.1])), inference.data()[0]
        )
        self.assertEqual(
            ("kerasccfraud", "21400ff8-0862-4c9f-a00d-41164fcabf1e"),
            inference.model_version(),
        )

    def test_full_response(self):
        result = {
            "model_name": "kerasccfraud",
            "model_version": "21400ff8-0862-4c9f-a00d-41164fcabf1e",
            "pipeline_id": "a-b-test-c78dab93-02d6-4d42-92a5-01c1970f4319",
            "outputs": [{"Float": {"v": 1, "dim": [1, 1], "data": [0.1]}}],
            "elapsed": [0, 149902],
            "time": int(self.now.timestamp() * 1000),
            "original_data": {
                "tensor": [
                    [
                        1.0678324729342086,
                        0.21778102664937624,
                        -1.7115145261843976,
                        0.6822857209662413,
                        1.0138553066742804,
                        -0.43350000129006655,
                        0.7395859436561657,
                        -0.28828395953577357,
                        -0.44726268795990787,
                        0.5146124987725894,
                        0.3791316964287545,
                        0.5190619748123175,
                        -0.4904593221655364,
                        1.1656456468728569,
                        -0.9776307444180006,
                        -0.6322198962519854,
                        -0.6891477694494687,
                        0.17833178574255615,
                        0.1397992467197424,
                        -0.35542206494183326,
                        0.4394217876939808,
                        1.4588397511627804,
                        -0.3886829614721505,
                        0.4353492889350186,
                        1.7420053483337177,
                        -0.4434654615252943,
                        -0.15157478906219238,
                        -0.26684517248765616,
                        -1.454961775612449,
                    ]
                ]
            },
        }

        inference = InferenceResult(self.gql_client, result)

        self.assertEqual(self.now, inference.timestamp())
        self.assertEqual(datetime.timedelta(microseconds=150), inference.time_elapsed())
        self.assertEqual(
            {
                "tensor": [
                    [
                        1.0678324729342086,
                        0.21778102664937624,
                        -1.7115145261843976,
                        0.6822857209662413,
                        1.0138553066742804,
                        -0.43350000129006655,
                        0.7395859436561657,
                        -0.28828395953577357,
                        -0.44726268795990787,
                        0.5146124987725894,
                        0.3791316964287545,
                        0.5190619748123175,
                        -0.4904593221655364,
                        1.1656456468728569,
                        -0.9776307444180006,
                        -0.6322198962519854,
                        -0.6891477694494687,
                        0.17833178574255615,
                        0.1397992467197424,
                        -0.35542206494183326,
                        0.4394217876939808,
                        1.4588397511627804,
                        -0.3886829614721505,
                        0.4353492889350186,
                        1.7420053483337177,
                        -0.4434654615252943,
                        -0.15157478906219238,
                        -0.26684517248765616,
                        -1.454961775612449,
                    ]
                ]
            },
            inference.input_data(),
        )
        self.assertEqual(repr(inference), f"InferenceResult({pprint.pformat(result)})")
        self.assertEqual(
            numpy.ndarray(shape=(1, 1), buffer=numpy.array([0.1])), inference.data()[0]
        )
        self.assertEqual(
            ("kerasccfraud", "21400ff8-0862-4c9f-a00d-41164fcabf1e"),
            inference.model_version(),
        )

    def test_pipeline_response_no_client(self):
        result = self.timed_pipeline_response
        inference = InferenceResult(None, result)
        self.assertEqual(self.now, inference.timestamp())
        expect = numpy.ndarray(shape=(1, 2), buffer=numpy.array([1.4, 2.5]))
        numpy.testing.assert_almost_equal(expect, inference.data()[0], 5)

    def test_shallow_pipeline_no_client(self):
        result = {
            "model_name": "kerasccfraud",
            "model_version": "53ed2516-e5c2-4f56-bf07-87636a22aa48",
            "pipeline_id": "a-b-test-ab3ae00e-0797-4137-b648-9c3149948e16",
            "outputs": [
                {"Float": {"v": 1, "dim": [1, 1], "data": [0.001497417688369751]}}
            ],
            "elapsed": [10, 175800],
            "time": int(self.now.timestamp() * 1000),
            "original_data": {
                "tensor": [
                    [
                        1.0678324729342086,
                        0.21778102664937624,
                        -1.7115145261843976,
                        0.6822857209662413,
                        1.0138553066742804,
                        -0.43350000129006655,
                        0.7395859436561657,
                        -0.28828395953577357,
                        -0.44726268795990787,
                        0.5146124987725894,
                        0.3791316964287545,
                        0.5190619748123175,
                        -0.4904593221655364,
                        1.1656456468728569,
                        -0.9776307444180006,
                        -0.6322198962519854,
                        -0.6891477694494687,
                        0.17833178574255615,
                        0.1397992467197424,
                        -0.35542206494183326,
                        0.4394217876939808,
                        1.4588397511627804,
                        -0.3886829614721505,
                        0.4353492889350186,
                        1.7420053483337177,
                        -0.4434654615252943,
                        -0.15157478906219238,
                        -0.26684517248765616,
                        -1.454961775612449,
                    ]
                ],
                "card_type": "silver",
            },
            "check_failures": [],
        }
        inference = InferenceResult(None, result)
        self.assertEqual(self.now, inference.timestamp())
        expect = numpy.ndarray(shape=(1, 1), buffer=numpy.array([0.00149741]))
        numpy.testing.assert_almost_equal(expect, inference.data()[0], 5)

    def test_ccfraud_data(self):
        inference = InferenceResult(None, self.ccfraud_output)
        expect = numpy.ndarray(shape=(1, 1), buffer=numpy.array([0.00149741]))
        numpy.testing.assert_almost_equal(expect, inference.data()[0], 5)

    def test_lazyadam_data(self):
        inference = InferenceResult(None, self.lazyadam_output)
        expect = numpy.ndarray(
            shape=(1, 10),
            buffer=numpy.array(
                [
                    [
                        0.11373511,
                        0.0931812,
                        0.11534489,
                        0.08846594,
                        0.08157939,
                        0.0981674,
                        0.10186929,
                        0.0926488,
                        0.11743077,
                        0.09757723,
                    ]
                ]
            ),
        )
        numpy.testing.assert_almost_equal(expect, inference.data()[0], 5)

    def test_pipeline_data(self):
        inference = InferenceResult(None, self.pipeline_output)
        expect = numpy.ndarray(shape=(1, 2), buffer=numpy.array([1.23, 2.34]))
        numpy.testing.assert_almost_equal(expect, inference.data()[0], 5)

    def test_day5_data(self):
        inference = InferenceResult(None, self.day5_output)
        expect = numpy.ndarray(shape=(1, 1), buffer=numpy.array([[6.68025519]]))
        numpy.testing.assert_almost_equal(expect, inference.data(), 5)

    def test_bad_dict(self):
        with self.assertRaises(KeyError):
            InferenceResult(None, {"x": 3})

    def test_bad_data_type(self):
        result = {
            "model_name": "noop-py-post",
            "model_version": "65c791c9-e138-47ec-bcf2-6877336d4968",
            "pipeline_id": "noop-pipe65c791c9-e138-47ec-bcf2-6877336d4968",
            "outputs": [
                {
                    "Foo": {
                        "v": 1,
                    },
                }
            ],
            "elapsed": [20, 467900],
            "time": int(self.now.timestamp() * 1000),
            "original_data": {"tensor": [[1.0, 2.0]]},
            "check_failures": [],
        }

        with self.assertRaises(RuntimeError) as ex:
            InferenceResult(None, result)
        self.assertTrue("Unsupported type" in str(ex.exception))

    def test_multi_row_output(self):
        multi_row_output = {
            "outputs": [
                {"Int64": {"data": [0, 0, 1, 1, 0, 0, 1, 1, 0], "dim": [9], "v": 1}},
                {
                    "Float": {
                        "data": [
                            0.9994155168533325,
                            0.0005844831466674805,
                            0.9791371822357178,
                            0.020862817764282227,
                            0.004281818866729736,
                            0.9957181811332703,
                            0.007074475288391113,
                            0.9929255247116089,
                            0.998551070690155,
                            0.0014489293098449707,
                            0.9985581040382385,
                            0.0014418959617614746,
                            0.18509161472320557,
                            0.8149083852767944,
                            0.08718907833099365,
                            0.9128109216690063,
                            0.9992682337760925,
                            0.0007317662239074707,
                        ],
                        "dim": [9, 2],
                        "v": 1,
                    }
                },
            ]
        }
        print(decode_inference_result(multi_row_output))

    def test_bad_data_key(self):
        result = self.timed_pipeline_response

        # hide the data key
        del result["outputs"][0]["Json"]["data"]

        with self.assertRaises(RuntimeError) as ex:
            InferenceResult(None, result)
        self.assertTrue("Output does not look like numpy")

    def test_inference_data_has_expected_dtype(self):
        result = {
            "model_name": "kerasccfraud",
            "model_version": "53ed2516-e5c2-4f56-bf07-87636a22aa48",
            "pipeline_id": "a-b-test-ab3ae00e-0797-4137-b648-9c3149948e16",
            "outputs": [
                {"Int64": {"data": [0, 0, 1, 1, 0, 0, 1, 1, 0], "dim": [9], "v": 1}},
                {
                    "Float": {
                        "data": [
                            0.9994155168533325,
                            0.0005844831466674805,
                            0.9791371822357178,
                            0.020862817764282227,
                            0.004281818866729736,
                            0.9957181811332703,
                            0.007074475288391113,
                            0.9929255247116089,
                            0.998551070690155,
                            0.0014489293098449707,
                            0.9985581040382385,
                            0.0014418959617614746,
                            0.18509161472320557,
                            0.8149083852767944,
                            0.08718907833099365,
                            0.9128109216690063,
                            0.9992682337760925,
                            0.0007317662239074707,
                        ],
                        "dim": [9, 2],
                        "v": 1,
                    }
                },
            ],
            "elapsed": [15, 175800],
            "time": int(self.now.timestamp() * 1000),
            "original_data": {
                "tensor": [
                    [
                        1.0678324729342086,
                        0.21778102664937624,
                        -1.7115145261843976,
                        0.6822857209662413,
                        1.0138553066742804,
                        -0.43350000129006655,
                        0.7395859436561657,
                        -0.28828395953577357,
                        -0.44726268795990787,
                        0.5146124987725894,
                        0.3791316964287545,
                        0.5190619748123175,
                        -0.4904593221655364,
                        1.1656456468728569,
                        -0.9776307444180006,
                        -0.6322198962519854,
                        -0.6891477694494687,
                        0.17833178574255615,
                        0.1397992467197424,
                        -0.35542206494183326,
                        0.4394217876939808,
                        1.4588397511627804,
                        -0.3886829614721505,
                        0.4353492889350186,
                        1.7420053483337177,
                        -0.4434654615252943,
                        -0.15157478906219238,
                        -0.26684517248765616,
                        -1.454961775612449,
                    ]
                ],
                "card_type": "silver",
            },
            "check_failures": [],
        }
        inference = InferenceResult(None, result)
        infer_data = inference.data()
        self.assertEqual(numpy.int64, type(infer_data[0][1]))
        self.assertEqual(numpy.float64, type(infer_data[1][1][0]))

    def test_pyomo_inference_data_has_expected_dtype(self):
        result = {
            "model_name": "pyomo",
            "model_version": "d64f71ee-35a0-4c56-9ef0-8f965e445b77",
            "pipeline_name": "noop-pipe44141798-138b-4465-9f78-01dc99981340",
            "outputs": [
                {
                    "Json": {
                        "v": 1,
                        "dim": [1],
                        "data": [
                            {
                                "tensor": [
                                    {
                                        "Float": {
                                            "v": 1,
                                            "dim": [1, 2],
                                            "data": [1.0, 2.0],
                                        }
                                    }
                                ],
                                "glpk": "0.4.6",
                            }
                        ],
                    }
                }
            ],
            "elapsed": [0, 179219],
            "time": 1666890213354,
            "original_data": {"tensor": [[1.0, 2.0]]},
            "check_failures": [],
            "shadow_data": {},
        }

        inference = InferenceResult(None, result)
        infer_data = inference.data()
        self.assertEqual(numpy.float64, type(infer_data[0][0][1]))
