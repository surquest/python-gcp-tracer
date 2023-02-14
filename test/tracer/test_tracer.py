# import external modules
import pytest
from starlette.requests import Request
from starlette.datastructures import Headers

# import internal modules
from surquest.GCP.tracer import Tracer


class TestTracer:
    ERRORS = {
        "value": "Wrong value: Expected: `{}`, Actual: `{}`",
        "type": "Wrong type: Expected: `{}`, Actual: `{}`"
    }

    @pytest.mark.parametrize(
        "property,expected",
        [
            ("project_id", {"type": str, "minLen": 5}),
            ("trace", {"type": str, "minLen": 8}),
            ("trace_id", {"type": str, "minLen": 8}),
            ("span_id", {"type": int, "minLen": 8}),
            ("flags", {"type": str, "minLen": 2})
        ]
    )
    def test__traces_properties(self, property, expected):
        tracer = Tracer()

        attribute = getattr(tracer, property)

        assert expected.get("type") == type(attribute), \
            self.ERRORS.get("type").format(
                str,
                type(attribute)
            )

        if expected.get("type") == str:
            assert expected.get("minLen") < len(attribute), \
                self.ERRORS.get("value").format(
                    expected.get("minLen"),
                    len(attribute)
                )

    @pytest.mark.parametrize(
        "trace,expected",
        [
            (
                "4ab5b3118c3e7cad6fef2b9376ecb9b0",
                {
                    "trace_id": "4ab5b3118c3e7cad6fef2b9376ecb9b0",
                    "span_id": None,
                    "flags": "o=1"
                }
            ),
            (
                "4ab5b3118c3e7cad6fef2b9376ecb9b0/2141214",
                {
                    "trace_id": "4ab5b3118c3e7cad6fef2b9376ecb9b0",
                    "span_id": "2141214",
                    "flags": "o=1"
                }
            ),
            (
                "4ab5b3118c3e7cad6fef2b9376ecb9b0/2141214;o=0",
                {
                    "trace_id": "4ab5b3118c3e7cad6fef2b9376ecb9b0",
                    "span_id": "2141214",
                    "flags": "o=0"
                }
            )
        ]
    )
    def test__get_context(self, trace, expected):
        """Method tests the _get_context method of the Tracer class

        :param trace: The trace
        :type trace: str
        :param expected: The expected result
        :type expected: dict
        """

        request = Request(
            {
                "type": "http",
                "path": "/my/path",
                "headers": Headers({
                    "x-cloud-trace-context": trace
                }).raw,
                "http_version": "1.1",
                "method": "GET",
                "scheme": "https",
                "client": ("127.0.0.1", 8080),
                "server": ("www.example.com", 443),
            }
        )

        tracer = Tracer(request=request)
        ctx = tracer._get_context(request)
        assert dict == type(ctx), self.ERRORS.get("type").format(
            dict,
            type(ctx)
        )

        assert expected.get("trace_id") == ctx.get("trace_id"), \
            self.ERRORS.get("value").format(
                expected.get("trace_id"),
                ctx.get("trace_id")
            )

        if expected.get("span_id") is not None:
            assert expected.get("span_id") == ctx.get("span_id"), \
                self.ERRORS.get("value").format(
                    expected.get("span_id"),
                    ctx.get("span_id")
                )

        assert expected.get("flags") == ctx.get("flags"), \
            self.ERRORS.get("value").format(
                expected.get("flags"),
                ctx.get("flags")
            )
