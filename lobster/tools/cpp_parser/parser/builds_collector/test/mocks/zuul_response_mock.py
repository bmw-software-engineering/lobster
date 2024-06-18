from typing import Dict


def return_zuul_build(uuid: str, build_result: str, project_name: str) -> Dict:
    """Return test zuul builds with values set accordingly to function parameters
    Parameters
    ----------
    uuid: str
        uuid of the ZuulBuild to generate
    build_result: str
        result of the ZuulBuild to generate
    project_name: str
        project of the ZuulBuild to generate
    Returns
    -------
    Dict
        Content of a Zuulbuild
    """

    return {
        "uuid": uuid,
        "job_name": "bazel-build-and-test-with-cache-upload",
        "result": build_result,
        "start_time": "2020-12-07T09:56:30",
        "end_time": "2020-12-07T12:17:33",
        "duration": 8463.461946,
        "voting": True,
        "log_url": "https://cc-ci.bmwgroup.net/logs/t/ddad/swh/zuul-trusted-ddad/38/1338/c366ac4340521bf9340ff3a8f63266242a3bb31e/post-independent/bazel-build-and-test-with-cache-upload/31f1da8/",
        "node_name": None,
        "error_detail": None,
        "final": True,
        "artifacts": [
            {
                "name": "Zuul Manifest",
                "url": "https://cc-ci.bmwgroup.net/logs/t/ddad/swh/zuul-trusted-ddad/38/1338/c366ac4340521bf9340ff3a8f63266242a3bb31e/post-independent/bazel-build-and-test-with-cache-upload/31f1da8/zuul-manifest.json",
                "metadata": {"type": "zuul_manifest"},
            }
        ],
        "provides": [],
        "project": project_name,
        "branch": "master",
        "pipeline": "post-independent",
        "change": 1338,
        "patchset": "c366ac4340521bf9340ff3a8f63266242a3bb31e",
        "ref": "refs/pull/1338/head",
        "newrev": None,
        "ref_url": "https://cc-github.bmwgroup.net/swh/zuul-trusted-ddad/pull/1338",
        "event_id": "15512a00-3872-11eb-8b32-3b6c8a129920",
        "buildset": {"uuid": "55d3dd6d0afb4e319526a4718200cf4a"},
    }


RESPONSE = [
    {
        "uuid": "31f1da8735dc41989bb34e56ab9caa62",
        "job_name": "bazel-build-and-test-with-cache-upload",
        "result": "FAILURE",
        "held": False,
        "start_time": "2020-12-07T09:56:30",
        "end_time": "2020-12-07T12:17:33",
        "duration": 8463.461946,
        "voting": True,
        "log_url": "https://cc-ci.bmwgroup.net/logs/t/ddad/swh/zuul-trusted-ddad/38/1338/c366ac4340521bf9340ff3a8f63266242a3bb31e/post-independent/bazel-build-and-test-with-cache-upload/31f1da8/",
        "node_name": None,
        "error_detail": None,
        "final": True,
        "artifacts": [
            {
                "name": "Zuul Manifest",
                "url": "https://cc-ci.bmwgroup.net/logs/t/ddad/swh/zuul-trusted-ddad/38/1338/c366ac4340521bf9340ff3a8f63266242a3bb31e/post-independent/bazel-build-and-test-with-cache-upload/31f1da8/zuul-manifest.json",
                "metadata": {"type": "zuul_manifest"},
            }
        ],
        "provides": [],
        "project": "swh/zuul-trusted-ddad",
        "branch": "master",
        "pipeline": "post-independent",
        "change": 1338,
        "patchset": "c366ac4340521bf9340ff3a8f63266242a3bb31e",
        "ref": "refs/pull/1338/head",
        "newrev": None,
        "ref_url": "https://cc-github.bmwgroup.net/swh/zuul-trusted-ddad/pull/1338",
        "event_id": "15512a00-3872-11eb-8b32-3b6c8a129920",
        "buildset": {"uuid": "55d3dd6d0afb4e319526a4718200cf4a"},
    },
    {
        "uuid": "77c57d0e825f4a039f045dd42ebb6b81",
        "job_name": "bazel-build-and-test-with-cache-upload",
        "result": "FAILURE",
        "held": False,
        "start_time": "2020-12-07T09:57:24",
        "end_time": "2020-12-07T12:15:04",
        "duration": 8259.582845,
        "voting": True,
        "log_url": "https://cc-ci.bmwgroup.net/logs/t/ddad/swh/ddad_platform/42/10442/75859471f949d0444ba7590d7c80bee3872a5f99/post-independent/bazel-build-and-test-with-cache-upload/77c57d0/",
        "node_name": None,
        "error_detail": None,
        "final": True,
        "artifacts": [
            {
                "name": "Zuul Manifest",
                "url": "https://cc-ci.bmwgroup.net/logs/t/ddad/swh/ddad_platform/42/10442/75859471f949d0444ba7590d7c80bee3872a5f99/post-independent/bazel-build-and-test-with-cache-upload/77c57d0/zuul-manifest.json",
                "metadata": {"type": "zuul_manifest"},
            }
        ],
        "provides": [],
        "project": "swh/ddad_platform",
        "branch": "master",
        "pipeline": "post-independent",
        "change": 10442,
        "patchset": "75859471f949d0444ba7590d7c80bee3872a5f99",
        "ref": "refs/pull/10442/head",
        "newrev": None,
        "ref_url": "https://cc-github.bmwgroup.net/swh/ddad_platform/pull/10442",
        "event_id": "4f223080-3872-11eb-94bb-0c85912dced0",
        "buildset": {"uuid": "802a46d4021e490ba8f7a36af659d80b"},
    },
]
